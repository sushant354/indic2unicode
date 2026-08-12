'''Repair the ToUnicode map of the fonts of a pdf that are known to carry a
broken one.

The Gazette pdfs that are set in Arial Unicode MS carry a ToUnicode map that
was built by pairing the glyphs of a run with the characters of that run one
by one. Devanagari shaping moves matra_i to the left of its cluster and the
reph to the right of its syllable, so the pairing slips exactly on the glyphs
that were moved: every consonant that occurs in a matra_i cluster is handed
the 'ि' of that cluster, matra_i is handed a consonant back, va and tha are
handed the reph of र्व and र्थ, and the reph is handed a va. A nukta pair and
a ligature lose a character in the same way.

The glyphs themselves are drawn correctly, so the text on the page is right
and only its extraction is wrong. The subset of the font that the pdf carries
keeps the original name of every glyph of the devanagari block, so the map of
those glyphs can be built again from the font itself. The glyphs that the
shaper made have no name of their own and are repaired from a table.

The text that comes out of the repaired pdf is in the visual order of the
glyphs, so it still has to go through fonts/arialuni_glyphs.py to be put in
the order that unicode wants.

USAGE:
    python fix_tounicode.py input.pdf output.pdf
'''

import getopt
import io
import logging
import re
import sys
import unicodedata

import pymupdf
from fontTools.ttLib import TTFont

# the glyphs that the shaper made. They have no name of their own in the
# font, so the string of every one of them is repaired by hand. The first
# string is what the broken map says, and a glyph is only repaired if it
# still says exactly that
ARIAL_UNICODE_MS = { \
    6979: ('ि',   'क्ष'), \
    6981: ('व',   'र्'),  \
    7021: ('स्ट्', 'स्'),  \
    7069: ('र',   'ट्र'),  \
    7081: ('ि',   'ब्र'),  \
    7278: ('ी',   'र्'),  \
    7399: ('ि',   'ष्ठ'),  \
    # the width variants of matra_i \
    7407: ('र',   'ि'),   \
    7408: ('क',   'ि'),   \
    7410: ('ल',   'ि'),   \
}

BROKEN_FONTS = {'Arial Unicode MS': ARIAL_UNICODE_MS}

# the text of a repaired font carries the characters that are really there,
# but still in the order in which the glyphs are drawn, so it has to go
# through this converter of indic2unicode and not through the one that is
# named after the font, which is for the text of a pdf that was not repaired
FONT_CONVERTERS = {'Arial Unicode MS': 'arialuni_glyphs'}

class ToUnicodeFixer:
    def __init__(self):
        self.logger = logging.getLogger('fix_tounicode')
        # the fonts of the last document that were actually repaired
        self.fixed_fonts = set()

    def base_font(self, fontname):
        # a subsetted font is named like ABCDEE+Arial Unicode MS
        if len(fontname) > 7 and fontname[6] == '+':
            fontname = fontname[7:]
        return fontname

    def get_cmap_xref(self, doc, xref):
        key, val = doc.xref_get_key(xref, 'ToUnicode')
        if key != 'xref':
            return None
        return int(val.split()[0])

    def parse_cmap(self, doc, cmapxref):
        '''the code -> string map that the pdf carries'''
        cmap = doc.xref_stream(cmapxref).decode('latin-1')

        def to_str(hexstr):
            return bytes.fromhex(hexstr).decode('utf-16-be')

        table = {}
        for match in re.finditer(r'beginbfchar(.*?)endbfchar', cmap, re.S):
            for src, dst in re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', \
                                       match.group(1)):
                table[int(src, 16)] = to_str(dst)

        for match in re.finditer(r'beginbfrange(.*?)endbfrange', cmap, re.S):
            body = match.group(1)
            # <lo> <hi> [<dst> <dst> ...]
            for lo, hi, array in re.findall(\
                    r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>\s*\[(.*?)\]', body, re.S):
                for i, dst in enumerate(re.findall(r'<([0-9a-fA-F]+)>', array)):
                    table[int(lo, 16) + i] = to_str(dst)
            # <lo> <hi> <dst>, the last code unit of dst counts up
            body = re.sub(r'<[0-9a-fA-F]+>\s*<[0-9a-fA-F]+>\s*\[.*?\]', ' ', \
                          body, flags = re.S)
            for lo, hi, dst in re.findall(\
                    r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', body):
                lo, hi = int(lo, 16), int(hi, 16)
                units  = [dst[i:i+4] for i in range(0, len(dst), 4)]
                base   = int(units[-1], 16)
                for code in range(lo, hi + 1):
                    last = '%04X' % (base + code - lo)
                    table[code] = to_str(''.join(units[:-1] + [last]))
        return table

    def build_cmap(self, table):
        lines = ['/CIDInit /ProcSet findresource begin', '12 dict begin',   \
                 'begincmap', '/CMapName /Adobe-Identity-UCS def',          \
                 '/CMapType 2 def', '1 begincodespacerange',                \
                 '<0000> <FFFF>', 'endcodespacerange']

        items = sorted(table.items())
        # a cmap may hold at most 100 entries in one bfchar section
        for i in range(0, len(items), 100):
            chunk = items[i:i+100]
            lines.append('%d beginbfchar' % len(chunk))
            for code, ustr in chunk:
                lines.append('<%04X> <%s>' % \
                             (code, ustr.encode('utf-16-be').hex().upper()))
            lines.append('endbfchar')

        lines.extend(['endcmap',                                       \
                      'CMapName currentdict /CMap defineresource pop', \
                      'end', 'end'])
        return ('\n'.join(lines) + '\n').encode('latin-1')

    def glyph_names(self, doc, xref):
        '''the name that the font gives to every one of its glyphs'''
        try:
            name, ext, ftype, buf = doc.extract_font(xref, named = False)
        except Exception as e:
            self.logger.warning('Could not extract the font %d: %s', xref, e)
            return []

        if not buf:
            return []

        try:
            font = TTFont(io.BytesIO(buf), fontNumber = 0, lazy = True)
            return font.getGlyphOrder()
        except Exception as e:
            self.logger.warning('Could not read the font %d: %s', xref, e)
            return []

    def is_identity(self, doc, xref, encoding):
        '''the code of a glyph is its glyph id only if the font is encoded
           with identity-h and maps the cids to the glyphs one to one'''
        if encoding != 'Identity-H':
            return False

        key, val = doc.xref_get_key(xref, 'DescendantFonts')
        if key == 'array':
            match = re.search(r'(\d+) 0 R', val)
            if match:
                key, val = doc.xref_get_key(int(match.group(1)), 'CIDToGIDMap')
                if key not in ('null', 'name') or \
                   (key == 'name' and val not in ('/Identity', 'Identity')):
                    return False
        return True

    def fix_font(self, doc, xref, fontname, encoding, glyphfixes):
        cmapxref = self.get_cmap_xref(doc, xref)
        if cmapxref == None:
            return 0

        if not self.is_identity(doc, xref, encoding):
            self.logger.info('Font %d (%s) is not identity encoded', \
                             xref, fontname)
            return 0

        names = self.glyph_names(doc, xref)
        if not names:
            return 0

        table = self.parse_cmap(doc, cmapxref)
        fixed = {}
        num   = 0
        for code, ustr in table.items():
            correct = None

            gname = names[code] if code < len(names) else ''
            match = re.fullmatch(r'uni([0-9A-Fa-f]{4})', gname)
            if match:
                # the font itself says which character this glyph is. A
                # nukta consonant is handed out in its canonical form, i.e.
                # ड़ as ड and a nukta
                correct = unicodedata.normalize('NFC', \
                                                chr(int(match.group(1), 16)))
            elif code in glyphfixes:
                broken, repl = glyphfixes[code]
                if ustr == broken:
                    correct = repl
                else:
                    self.logger.info(\
                        'Glyph %d of %s says %r and not the expected %r, ' \
                        'leaving it alone', code, fontname, ustr, broken)

            if correct != None and correct != ustr:
                num += 1
                self.logger.debug('Font %d glyph %d: %r -> %r', \
                                  xref, code, ustr, correct)
            fixed[code] = correct if correct != None else ustr

        if num:
            doc.update_stream(cmapxref, self.build_cmap(fixed), compress = True)
        return num

    def fix_document(self, doc):
        '''repair every font of the document that is known to carry a broken
           map. Returns the number of glyphs that were repaired, and leaves
           the names of the fonts they belong to in self.fixed_fonts'''
        fonts = {}
        for pagenum in range(doc.page_count):
            for font in doc[pagenum].get_fonts(full = True):
                xref, ext, ftype, fontname, refname, encoding = font[:6]
                fonts[xref] = (fontname, encoding)

        num = 0
        self.fixed_fonts = set()
        for xref in sorted(fonts):
            fontname, encoding = fonts[xref]
            basefont   = self.base_font(fontname)
            glyphfixes = BROKEN_FONTS.get(basefont)
            if glyphfixes == None:
                continue

            numfixed = self.fix_font(doc, xref, fontname, encoding, glyphfixes)
            if numfixed:
                self.fixed_fonts.add(basefont)
            num += numfixed

        self.logger.info('Repaired %d glyphs in the fonts: %s', num, \
                         ', '.join(sorted(self.fixed_fonts)))
        return num

def print_usage(progname):
    print('Usage: %s input.pdf output.pdf' % progname)

if __name__ == '__main__':
    optlist = getopt.getopt(sys.argv[1:], 'h')

    for o, v in optlist[0]:
        if o == '-h':
            print_usage(sys.argv[0])
            sys.exit(0)

    if len(optlist[1]) != 2:
        print_usage(sys.argv[0])
        sys.exit(0)

    logging.basicConfig(\
        level   = logging.INFO, \
        format  = '%(asctime)s: %(name)s: %(levelname)s %(message)s', \
        datefmt = '%Y-%m-%d %H:%M:%S', \
    )

    infile, outfile = optlist[1]

    doc = pymupdf.open(infile)
    num = ToUnicodeFixer().fix_document(doc)
    doc.save(outfile)
    print('Repaired %d glyphs. Wrote %s' % (num, outfile))
