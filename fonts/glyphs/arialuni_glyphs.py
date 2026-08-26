import re
import string
import types

from indic2unicode.langs import devanagari
from ..basefont import BaseFont, LITERAL
from ..kannada.arialuni import ArialUniKannadaGlyphs
import ply.lex as lex

# the two scripts that a pdf set in Arial Unicode MS draws its indic text
# in. The font is one font and the repaired pdf hands both of them to this
# converter, but a syllable of each is put together in an order of its own,
# so a run of text is split on these and each half is read by the pass that
# knows it, see ArialUniGlyphs.split_scripts()
DEVANAGARI_RE = re.compile('[\u0900-\u097f]')
KANNADA_RE    = re.compile('[\u0c80-\u0cff]')

class ArialUniGlyphs(BaseFont):
    '''The text of a pdf whose ToUnicode map has been repaired by
       tools/fix_tounicode.py. Every glyph now carries the characters it
       really stands for, but the glyphs are still stored in the order in
       which they are drawn, so matra_i sits in front of the consonant it
       belongs to and the reph sits behind the whole syllable it sits on,
       e.g. निर्माण comes out as िनमार्ण and अर्थात् as अथार्त्.

       Nothing more than the two reordering passes is needed here. Unlike
       fonts/hindi/arialuni.py, which works on the text of a pdf whose map is
       still broken, this one loses nothing: ja, na, pha, sha and ksha are
       all still there, and so are va, tha and the nuktas.

       THE OTHER SCRIPT OF THE SAME FONT

       Arial Unicode MS sets the Karnataka gazette as well, and the repair
       hands the kannada of it to this same converter - the font is one
       font and get_font_converter() names one converter for it. A kannada
       syllable is drawn in an order of its own and is put back together by
       fonts/kannada/arialuni.py, so a run of text is split on its script
       and each half is read by the pass that knows it. A pdf that draws
       only devanagari is one segment and goes through exactly the two
       passes it always did.
    '''
    # the pass that reads the kannada of this font, which the fonts that
    # inherit this one name their own of
    kannadaclass = ArialUniKannadaGlyphs

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs  = []
        self.langobjs.append(devanagari.DevanagariUnicode())
        self.langobjs.append(devanagari.Conjuncts())
        self.langobjs.append(devanagari.ArialUni())

        # the kannada of the same font, which is read by a pass of its own
        self.kannadaobj = self.kannadaclass()

        self.lexer = self.get_lexer()

        # matra_i is drawn to the left of the consonant it belongs to
        self.waitdict   = {'MATRA_I': 1}

        # the reph is drawn on top of the last consonant of its syllable and
        # is stored after that whole syllable
        self.jumpbefore = {'ADHA_RA': 1}

        # while the reph jumps back to the head of its syllable, it has to
        # jump over the matras and the signs of that syllable
        self.jumpover = set([ \
            'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',      \
            'MATRA_RI', 'MATRA_RR', 'MATRA_E', 'MATRA_AI', 'MATRA_O',      \
            'MATRA_AU', 'MATRA_CHANDRA_O', 'CHANDRA', 'BINDU',             \
            'CHANDRABINDU', 'VISARGA', 'NUKTA',                            \
            'MATRA_SHORT_E', 'MATRA_SHORT_O', 'MATRA_L', 'MATRA_LL',       \
            'UDATTA', 'ANUDATTA', 'GRAVE_ACCENT', 'ACUTE_ACCENT',          \
        ])

        # nukta belongs to the syllable matra_i has already passed, so it
        # has to stay behind it
        self.waitover = set(['NUKTA'])

        # a half consonant is not the consonant matra_i is waiting for, but
        # it is the head of the syllable that matra_i belongs to
        self.halftokens = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName.startswith('ADHA_'):
                    self.halftokens.add(tokenName)

    def to_unicode(self, data):
        '''the two scripts of the font are read by passes of their own, so
           the text is split on its script first. A run of a pdf that draws
           only devanagari - every pdf this converter was written for before
           the kannada gazettes - is one segment and comes out of the same
           two passes it always did'''
        out = []
        for iskannada, segment in self.split_scripts(data):
            if iskannada:
                out.append(self.kannadaobj.to_unicode(segment))
            else:
                out.append(BaseFont.to_unicode(self, segment))
        return ''.join(out)

    def split_scripts(self, data):
        '''the text broken into runs of one script, as (is it kannada, text)
           pairs. A character that belongs to neither script - a space, a
           digit, the latin of the document, the punctuation - says nothing
           about which pass should read it and stays with the run it was
           found in, so a segment only ever ends where the script really
           changes'''
        segments  = []
        iskannada = False
        start     = 0

        for pos, char in enumerate(data):
            if KANNADA_RE.match(char):
                ischanged = not iskannada
            elif DEVANAGARI_RE.match(char):
                ischanged = iskannada
            else:
                continue

            if ischanged:
                if pos > start:
                    segments.append((iskannada, data[start:pos]))
                start     = pos
                iskannada = not iskannada

        segments.append((iskannada, data[start:]))
        return segments

    def log_error_summary(self):
        '''the characters of both scripts that could not be read, the
           kannada pass keeping a count of its own'''
        BaseFont.log_error_summary(self)
        self.kannadaobj.log_error_summary()

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        def pat(*glyphs):
            # token strings are regular expressions for ply, so the glyphs
            # have to be escaped. Alternate glyphs of the same token are
            # joined into one pattern
            return '|'.join([re.escape(glyph) for glyph in glyphs])

        # VOWELS
        t_SHORT_A        = pat('ऄ')
        t_A              = pat('अ')
        t_AA             = pat('आ')
        t_I              = pat('इ')
        t_II             = pat('ई')
        t_U              = pat('उ')
        t_UU             = pat('ऊ')
        t_RE             = pat('ऋ')
        t_LI             = pat('ऌ')
        t_RRE            = pat('ॠ')
        t_LLE            = pat('ॡ')
        t_CHANDRA_E      = pat('ऍ')
        t_SHORT_E        = pat('ऎ')
        t_E              = pat('ए')
        t_AI             = pat('ऐ')
        t_SHORT_O        = pat('ऒ')
        t_OO             = pat('ओ')
        t_AU             = pat('औ')
        t_CHANDRA_O      = pat('ऑ')

        # CONSONANTS. a conjunct of the font needs no glyph of its own here,
        # क्ष is the half ka and ssa, ब्र is the half ba and ra, and so on
        t_ADHA_KA        = pat('क्')
        t_KA             = pat('क')
        t_ADHA_KHA       = pat('ख्')
        t_KHA            = pat('ख')
        t_ADHA_GA        = pat('ग्')
        t_GA             = pat('ग')
        t_ADHA_GHA       = pat('घ्')
        t_GHA            = pat('घ')
        t_NGA            = pat('ङ')

        t_ADHA_CA        = pat('च्')
        t_CA             = pat('च')
        t_ADHA_CHA       = pat('छ्')
        t_CHA            = pat('छ')
        t_ADHA_JA        = pat('ज्')
        t_JA             = pat('ज')
        t_ADHA_JHA       = pat('झ्')
        t_JHA            = pat('झ')
        t_ADHA_NYA       = pat('ञ्')
        t_NYA            = pat('ञ')

        t_ADHA_TTA       = pat('ट्')
        t_TTA            = pat('ट')
        t_ADHA_TTHA      = pat('ठ्')
        t_TTHA           = pat('ठ')
        t_ADHA_DDA       = pat('ड्')
        t_DDA            = pat('ड')
        t_ADHA_DDHA      = pat('ढ्')
        t_DDHA           = pat('ढ')
        t_ADHA_NNA       = pat('ण्')
        t_NNA            = pat('ण')

        t_ADHA_TA        = pat('त्')
        t_TA             = pat('त')
        t_ADHA_THA       = pat('थ्')
        t_THA            = pat('थ')
        t_ADHA_DA        = pat('द्')
        t_DA             = pat('द')
        t_ADHA_DHA       = pat('ध्')
        t_DHA            = pat('ध')
        t_ADHA_NA        = pat('न्')
        t_NA             = pat('न')
        t_NNNA           = pat('ऩ')

        t_ADHA_PA        = pat('प्')
        t_PA             = pat('प')
        t_ADHA_PHA       = pat('फ्')
        t_PHA            = pat('फ')
        t_ADHA_BA        = pat('ब्')
        t_BA             = pat('ब')
        t_ADHA_BHA       = pat('भ्')
        t_BHA            = pat('भ')
        t_ADHA_MA        = pat('म्')
        t_MA             = pat('म')

        t_ADHA_YA        = pat('य्')
        t_YA             = pat('य')
        # the font draws the reph together with ma, and there it is already
        # in front of the consonant it sits on
        t_RA_MA          = pat('र्म')
        t_ADHA_RA        = pat('र्')
        t_RA             = pat('र')
        t_RRA            = pat('ऱ')
        t_ADHA_LA        = pat('ल्')
        t_LA             = pat('ल')
        t_LLA            = pat('ळ')
        t_LLLA           = pat('ऴ')
        t_ADHA_VA        = pat('व्')
        t_VA             = pat('व')

        t_ADHA_SHA       = pat('श्')
        t_SHA            = pat('श')
        t_ADHA_SSA       = pat('ष्')
        t_SSA            = pat('ष')
        t_ADHA_SA        = pat('स्')
        t_SA             = pat('स')
        t_ADHA_HA        = pat('ह्')
        t_HA             = pat('ह')

        # CONSONANTS WITH A NUKTA. the decomposed form of these is
        # tokenized as the consonant and the nukta
        t_QA             = pat('\u0958')
        t_KHHA           = pat('\u0959')
        t_GHHA           = pat('\u095a')
        t_ZA             = pat('\u095b')
        t_DDDHA          = pat('\u095c')
        t_RHA            = pat('\u095d')
        t_FA             = pat('\u095e')
        t_YYA            = pat('\u095f')

        # MATRAS
        t_MATRA_AA       = pat('ा')
        t_MATRA_I        = pat('ि')
        t_MATRA_II       = pat('ी')
        t_MATRA_U        = pat('ु')
        t_MATRA_UU       = pat('ू')
        t_MATRA_RI       = pat('ृ')
        t_MATRA_RR       = pat('ॄ')
        t_MATRA_L        = pat('ॢ')
        t_MATRA_LL       = pat('ॣ')
        t_MATRA_SHORT_E  = pat('ॆ')
        t_MATRA_E        = pat('े')
        t_MATRA_AI       = pat('ै')
        t_MATRA_SHORT_O  = pat('ॊ')
        t_MATRA_O        = pat('ो')
        t_MATRA_AU       = pat('ौ')
        t_CHANDRA        = pat('ॅ')
        t_MATRA_CHANDRA_O = pat('ॉ')

        # SIGNS
        t_BINDU          = pat('ं')
        t_CHANDRABINDU   = pat('ँ')
        t_VISARGA        = pat('ः')
        t_NUKTA          = pat('़')
        t_HALANT         = pat('्')
        t_AVAGRAHA       = pat('ऽ')
        t_OM             = pat('ॐ')
        t_VIRAM          = pat('।')
        t_DEERGH_VIRAM   = pat('॥')
        t_ABBREV         = pat('॰')
        # the vedic accents, which sit on a syllable like the signs do
        t_UDATTA         = pat('॑')
        t_ANUDATTA       = pat('॒')
        t_GRAVE_ACCENT   = pat('॓')
        t_ACUTE_ACCENT   = pat('॔')

        # DIGITS
        t_ZERO           = pat('०')
        t_ONE            = pat('१')
        t_TWO            = pat('२')
        t_THREE          = pat('३')
        t_FOUR           = pat('४')
        t_FIVE           = pat('५')
        t_SIX            = pat('६')
        t_SEVEN          = pat('७')
        t_EIGHT          = pat('८')
        t_NINE           = pat('९')

        # PUNCTUATIONS
        t_LEFTPARAN      = pat('(')
        t_RIGHTPARAN     = pat(')')
        t_LEFTSQBRACE    = pat('[')
        t_RIGHTSQBRACE   = pat(']')
        t_COMMA          = pat(',')
        t_DOT            = pat('.')
        t_DASH           = pat('-')
        t_SLASH          = pat('/')
        t_COLON          = pat(':')
        t_SEMICOLON      = pat(';')
        t_QUESTION       = pat('?')
        t_EXCLAMATION    = pat('!')
        t_PERCENT        = pat('%')
        t_PLUS           = pat('+')
        t_EQ             = pat('=')
        t_STAR           = pat('*')
        t_QUOT           = pat('"')
        t_BAR            = pat('|')
        t_AMPERSAND      = pat('&')
        t_APOSTROPHE     = pat("'")
        t_LSQUOTE        = pat('‘')
        t_RSQUOTE        = pat('’')
        t_LDQUOTE        = pat('“')
        t_RDQUOTE        = pat('”')
        t_ENDASH         = pat('–')
        t_EMDASH         = pat('—')
        t_SPACE          = pat(' ')
        t_NEWLINE        = pat('\n')
        t_CARRIAGERET    = pat('\r')

        def t_error(t):
            # the text of a repaired pdf is unicode already and only its
            # order is wrong, so a character with no token of its own is not
            # a glyph waiting to be reordered, it is text - an ellipsis, an
            # underscore of a form, a bullet, a zero width joiner - and has
            # to come out the way it went in rather than be dropped. Only a
            # glyph code that no map could turn into a character is dropped,
            # and that is reported
            char = t.value[0]

            if not self.is_text_char(char):
                self.report_error(t)
                t.lexer.skip(1)
                return None

            t.lexer.skip(1)
            t.type  = LITERAL
            t.value = char
            return t

        rules = dict(locals())

        # the english text of the document is set in a latin font and comes
        # out of the pdf as itself
        digitnames = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', \
                      'SEVEN', 'EIGHT', 'NINE']
        for digit, name in enumerate(digitnames):
            rules['t_ASCII_' + name] = pat('%d' % digit)

        for char in string.ascii_uppercase:
            rules['t_LATIN_' + char] = pat(char)
        for char in string.ascii_lowercase:
            rules['t_LATIN_SMALL_' + char.upper()] = pat(char)

        # only the tokens that the font has a glyph for
        rules['tokens'] = [tokenName for tokenName in tokens \
                                     if 't_' + tokenName in rules]

        # the rules of the latin text are made in a loop, so they are handed
        # to ply in an object of their own rather than in the locals of this
        # function. ply looks up the module of that object
        rules['__module__'] = self.__class__.__module__
        return lex.lex(object = types.SimpleNamespace(**rules))
