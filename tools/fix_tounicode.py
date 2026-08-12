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
# font, so the string of every one of them is repaired by hand. The string
# that the broken map hands such a glyph is the character it happened to be
# paired with in that document, and that differs from document to document:
# the matra_i of दि is handed a द in one gazette and the matra_i of कि a क
# in another, both by the same glyph. So a glyph is repaired to what it
# really is whatever its map says, and the comment only records the string
# that was seen first. A map that is already right says the same thing that
# the table does, so repairing it changes nothing
ARIAL_UNICODE_MS = { \
    # the half forms, which the font lays out in the order of the consonants
    # they belong to, क् at 6989 through ह् at 7022. A pdf whose map hands
    # them the halant and a zwj instead of the consonant loses the consonant
    # of every one of them, उक्त comes out as उ त and उपलब्ध as उपल् ध \
    6989: 'क्',  # seen as ‍ \
    6990: 'ख्',  # seen as ्‍ \
    6991: 'ग्',  # seen as ‍ \
    7005: 'थ्',  # seen as ्‍ \
    7007: 'ध्',  # seen as ‍ \
    7009: 'प्',  # seen as ‍ \
    7011: 'ब्',  # seen as ्‍ \
    7021: 'स्',  # seen as स्ट् \
    # the glyphs the shaper made out of a whole cluster \
    6979: 'क्ष', # seen as ि \
    6981: 'र्',  # seen as व, ा \
    7069: 'ट्र',  # seen as र \
    7081: 'ब्र',  # seen as ि \
    7278: 'र्',  # seen as ी \
    7399: 'ष्ठ',  # seen as ि \
    # the width variants of matra_i \
    7407: 'ि',   # seen as र \
    7408: 'ि',   # seen as क, द \
    7409: 'ी',   \
    7410: 'ि',   # seen as ल, स \
    # the rest of the half forms, in the order of their consonants \
    6996: 'ज्',  \
    7004: 'त्',  \
    7008: 'न्',  # seen as a space \
    7013: 'म्',  \
    7016: 'ल्',  \
    7019: 'श्',  \
    7020: 'ष्',  \
    # the ligatures that the shaper made out of a whole cluster \
    7074: 'त्र',  # seen as ि \
    7079: 'प्र',  \
    7272: 'रू',  \
    7275: 'त्त',  \
    7286: 'ें',   \
    7289: 'ैं',   \
    7298: 'ों',  # seen as स \
    7312: 'ओं',  \
    7334: 'क्त',  # seen as ि \
    7367: 'द्व',  \
    7374: 'द्द',  \
    7378: 'द्य',  \
    7382: 'न्न',  \
    7385: 'प्त',  \
    7388: 'म्न',  \
    7397: 'ष्ट',  \
    7398: 'ष्ट्र', \
}

BROKEN_FONTS = {'Arial Unicode MS': ARIAL_UNICODE_MS}

# the font whose glyph ids a type3 font of a distilled gazette names its
# glyphs after, see fix_type3_fonts below
TYPE3_GLYPH_FONT = 'Arial Unicode MS'

# the text of a repaired font carries the characters that are really there,
# but still in the order in which the glyphs are drawn, so it has to go
# through this converter of indic2unicode and not through the one that is
# named after the font, which is for the text of a pdf that was not repaired
FONT_CONVERTERS = {'Arial Unicode MS': 'arialuni_glyphs'}

def font_lookup_key(fontname):
    '''one font is embedded under more than one spelling of its name, Arial
       Unicode MS is carried both as "Arial Unicode MS" and as
       "ArialUnicodeMS", so a font is looked up by a spelling of its name
       that the separators and the case do not change'''
    return re.sub(r'[\s\-_,]+', '', fontname).lower()

BROKEN_FONTS_BY_KEY    = {font_lookup_key(name): fixes \
                          for name, fixes in BROKEN_FONTS.items()}
FONT_CONVERTERS_BY_KEY = {font_lookup_key(name): conv  \
                          for name, conv  in FONT_CONVERTERS.items()}

def get_glyph_fixes(fontname):
    '''the glyphs to repair by hand for a font known to carry a broken map,
       None for every other font'''
    return BROKEN_FONTS_BY_KEY.get(font_lookup_key(fontname))

def get_font_converter(fontname):
    '''the converter that puts the text of a repaired font in the order that
       unicode wants, None if there is none for it'''
    return FONT_CONVERTERS_BY_KEY.get(font_lookup_key(fontname))

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
                # a glyph that the shaper made, repaired to what it really
                # is whatever the character it was paired with in this
                # document happens to be
                correct = glyphfixes[code]

            if correct != None and correct != ustr:
                num += 1
                self.logger.debug('Font %d glyph %d: %r -> %r', \
                                  xref, code, ustr, correct)
            fixed[code] = correct if correct != None else ustr

        if num:
            doc.update_stream(cmapxref, self.build_cmap(fixed), compress = True)
        return num

    # ------------------------------------------------------------------
    # the type3 fonts of a distilled gazette
    #
    # A gazette that was distilled rather than written out carries its
    # devanagari as type3 fonts whose glyphs are one bit images, one font
    # per handful of glyphs. There is no font program left to read the
    # names of the glyphs from, but the /Encoding /Differences of the font
    # names every code it draws, and those names are the ones the original
    # font gave its glyphs: uni0928 for a glyph of the devanagari block and
    # g7079 for one that the shaper made, the same glyph ids that
    # ARIAL_UNICODE_MS repairs by hand. So the map of such a font can be
    # built from its /Differences alone, which is what recovers the fonts
    # that carry no ToUnicode at all and whose text comes out as (cid:9).
    # ------------------------------------------------------------------

    def type3_differences(self, doc, xref):
        '''the name that the /Encoding of a type3 font gives to every code
           it draws, as a code -> glyph name dict'''
        key, val = doc.xref_get_key(xref, 'Encoding')
        if key != 'xref':
            return {}

        try:
            encoding = doc.xref_object(int(val.split()[0]), compressed = False)
        except Exception as e:
            self.logger.warning('Could not read the encoding of %d: %s', xref, e)
            return {}

        if 'Differences' not in encoding:
            return {}

        # [ 1 /uni092E /uni0902 /g7074 ... ], a number starts a new run of
        # codes and every name after it takes the next code
        body  = encoding.split('Differences', 1)[1].split(']', 1)[0]
        names = {}
        code  = None
        for token in re.findall(r'(\d+|/[^\s/\[\]<>()]+)', body):
            if token.isdigit():
                code = int(token)
            elif code != None:
                names[code] = token[1:]
                code += 1

        return names

    def glyph_id_name(self, gname):
        '''the glyph id that a name like g7079 stands for, None otherwise'''
        match = re.fullmatch(r'g(\d+)', gname or '')
        return int(match.group(1)) if match else None

    def unicode_glyph_name(self, gname):
        '''the character that a name like uni0928 stands for, None otherwise'''
        match = re.fullmatch(r'uni([0-9A-Fa-f]{4})', gname or '')
        if not match:
            return None
        return unicodedata.normalize('NFC', chr(int(match.group(1), 16)))

    def is_devanagari(self, strings):
        '''whether any of the strings is written in devanagari'''
        for ustr in strings:
            for char in ustr:
                if 'ऀ' <= char <= 'ॿ':
                    return True
        return False

    def learn_type3_gids(self, doc, xrefs):
        '''what the type3 fonts of this document that do carry a ToUnicode
           say about the glyph ids they draw, as a glyph id -> string dict.

           The fonts of one document are subsets of a single original font,
           so a glyph id that one of them maps is the same glyph in all of
           them: the fonts that carry a map are what fills in the fonts
           that carry none, without a table of the whole font being needed'''
        learnt = {}

        for xref in xrefs:
            cmapxref = self.get_cmap_xref(doc, xref)
            if cmapxref == None:
                continue

            try:
                table = self.parse_cmap(doc, cmapxref)
            except Exception as e:
                self.logger.warning('Could not read the map of %d: %s', xref, e)
                continue

            for code, gname in self.type3_differences(doc, xref).items():
                gid = self.glyph_id_name(gname)
                if gid == None or gid in learnt:
                    continue
                ustr = table.get(code)
                if ustr:
                    learnt[gid] = ustr

        return learnt

    def set_tounicode(self, doc, xref, table):
        '''write a map for a font, making one if the font carries none'''
        cmap     = self.build_cmap(table)
        cmapxref = self.get_cmap_xref(doc, xref)

        if cmapxref == None:
            cmapxref = doc.get_new_xref()
            doc.update_object(cmapxref, '<<>>')
            doc.xref_set_key(xref, 'ToUnicode', '%d 0 R' % cmapxref)

        doc.update_stream(cmapxref, cmap, compress = True)

    def name_type3_font(self, doc, xref, fontname):
        '''give a repaired type3 font the name of the font its glyphs come
           from, so that what reads the pdf next can tell which converter
           puts its text in the order unicode wants. A type3 font carries no
           basefont of its own and pdfminer calls it "unknown" without a
           font descriptor to read a name out of'''
        key, val = doc.xref_get_key(xref, 'FontDescriptor')
        if key != 'null':
            return

        key, bbox = doc.xref_get_key(xref, 'FontBBox')
        if key != 'array':
            bbox = '[ 0 0 1000 1000 ]'

        # a space is not allowed in a pdf name, #20 is how it is written
        pdfname = fontname.replace(' ', '#20')
        fdxref  = doc.get_new_xref()
        doc.update_object(fdxref, '<< /Type /FontDescriptor /FontName /%s '  \
                                  '/Flags 4 /ItalicAngle 0 /Ascent 0 '       \
                                  '/Descent 0 /MissingWidth 0 /StemV 0 '     \
                                  '/FontBBox %s >>' % (pdfname, bbox))
        doc.xref_set_key(xref, 'FontDescriptor', '%d 0 R' % fdxref)

    def fix_type3_font(self, doc, xref, glyphfixes, learnt):
        '''build the map of a type3 font from the names its encoding gives
           its glyphs. Returns the number of codes that the map gained or
           that it had wrong'''
        names = self.type3_differences(doc, xref)
        if not names:
            return 0

        cmapxref = self.get_cmap_xref(doc, xref)
        table    = self.parse_cmap(doc, cmapxref) if cmapxref != None else {}

        fixed = dict(table)
        num   = 0
        for code, gname in names.items():
            # the name of a glyph of the devanagari block says which
            # character it is, one the shaper made is repaired by hand and,
            # failing that, from what the other fonts of this document say
            correct = self.unicode_glyph_name(gname)

            if correct == None:
                gid = self.glyph_id_name(gname)
                if gid != None:
                    correct = glyphfixes.get(gid) or learnt.get(gid)

            if correct == None or correct == table.get(code):
                continue

            self.logger.debug('Type3 font %d code %d (%s): %r -> %r', \
                              xref, code, gname, table.get(code), correct)
            fixed[code] = correct
            num += 1

        if not num:
            return 0

        # a type3 font that draws no devanagari is not one of the fonts this
        # is about, whatever its glyphs are named, and is left alone: naming
        # it after a devanagari font would send its text through a converter
        # that has no business reordering it
        if not self.is_devanagari(fixed.values()):
            self.logger.info('Type3 font %d draws no devanagari, leaving it ' \
                             'alone', xref)
            return 0

        self.set_tounicode(doc, xref, fixed)

        return num

    def fix_type3_fonts(self, doc, xrefs):
        '''repair every type3 font of the document. Returns the number of
           codes repaired, and the name of the font the glyphs come from if
           any of them was'''
        glyphfixes = BROKEN_FONTS[TYPE3_GLYPH_FONT]
        learnt     = self.learn_type3_gids(doc, xrefs)
        num        = 0

        for xref in xrefs:
            numfixed = self.fix_type3_font(doc, xref, glyphfixes, learnt)
            if numfixed:
                self.name_type3_font(doc, xref, TYPE3_GLYPH_FONT)
            num += numfixed

        if num:
            self.logger.info(\
                'Repaired %d codes of the %d type3 font(s), %d glyph id(s) ' \
                'read out of the fonts of the document itself', num,         \
                len(xrefs), len(learnt))
            self.fixed_fonts.add(TYPE3_GLYPH_FONT)

        return num

    def fix_document(self, doc):
        '''repair every font of the document that is known to carry a broken
           map. Returns the number of glyphs that were repaired, and leaves
           the names of the fonts they belong to in self.fixed_fonts'''
        fonts  = {}
        type3s = []
        for pagenum in range(doc.page_count):
            for font in doc[pagenum].get_fonts(full = True):
                xref, ext, ftype, fontname, refname, encoding = font[:6]
                fonts[xref] = (fontname, encoding)
                if ftype == 'Type3' and xref not in type3s:
                    type3s.append(xref)

        num = 0
        self.fixed_fonts = set()
        for xref in sorted(fonts):
            fontname, encoding = fonts[xref]
            basefont   = self.base_font(fontname)
            glyphfixes = get_glyph_fixes(basefont)
            if glyphfixes == None:
                continue

            numfixed = self.fix_font(doc, xref, fontname, encoding, glyphfixes)
            if numfixed:
                self.fixed_fonts.add(basefont)
            num += numfixed

        if type3s:
            num += self.fix_type3_fonts(doc, sorted(type3s))

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
