import re
import string
import types

from indic2unicode.langs import devanagari
from ..basefont import BaseFont
import ply.lex as lex

class NirmalaUI(BaseFont):
    '''Nirmala UI is a unicode font, and the pdfs of the Gazette that are set
       in it carry the same kind of broken ToUnicode map as the ones that are
       set in Arial Unicode MS: the map was built by pairing the glyphs of a
       run with the characters of that run one by one, so every glyph that
       devanagari shaping moved was handed the string of its neighbour. The
       text that comes out of such a pdf is therefore devanagari that is

       1. in the visual order of the glyphs and not in the order of unicode,
          so matra_i sits in front of the consonant it belongs to and the
          reph sits behind the whole syllable it sits on, and

       2. spelled with the wrong characters for a part of the alphabet, e.g.
          'ि' for ka and 'क' for matra_i, which are the two that were paired
          with each other in the first 'कि' of the document.

       So the text is treated like any other font of this package: every
       glyph of the font is a token, the token is given the unicode string
       it really stands for and the tokens are put back in the order that
       unicode wants.

       The map cannot be inverted completely. What is lost is

       * sha. Both ka and sha, and the conjunct shcha as well, are handed the
         'ि' of the cluster they were first drawn in, so all of them come out
         as 'ि' and cannot be told apart any more. 'ि' is read as ka, which
         is by far the more common of the two, and sha is lost.

       * matra_o. Its glyph is handed no string at all and comes out of the
         pdf as the space of its own advance, so को is left as 'क'. Only a
         matra_o that carries an anusvara can be brought back, because the
         anusvara of the pair is handed 'ों' and the two together are the
         'ों' of every plural that the document has.

       * the reph. The font draws it together with the matra of the syllable
         it sits on, so it is handed 'ा', 'ी', 'ो' or nothing at all,
         depending on that matra. Only the reph over a matra_aa can be found
         again, by the 'ाा' that it leaves behind.
    '''
    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs  = []
        self.langobjs.append(devanagari.DevanagariUnicode())
        self.langobjs.append(devanagari.Conjuncts())
        self.langobjs.append(devanagari.NirmalaUI())

        self.lexer = self.get_lexer()

        # matra_i is drawn to the left of the consonant it belongs to
        self.waitdict   = {'MATRA_I': 1}

        # the reph is drawn on top of the last consonant of its syllable and
        # is stored after that whole syllable
        self.jumpbefore = {'ADHA_RA': 1}

        self.composeTokens = { \
            # the font has one glyph of matra_i per width of the syllable
            # that follows it, and those glyphs are handed the strings of
            # ka, of ra and of the conjunct kta. So a ra in front of the
            # syllable ra, and a kta in front of a syllable that the font
            # draws with the wide matra_i, is a matra and not a consonant
            # (a real रर, as in थरराना, is lost to this)
            ('RA', 'RA')       : ['MATRA_I', 'RA'],       \
            ('KTA', 'KTA')     : ['MATRA_I', 'KTA'],      \
            ('KTA', 'ADHA_SA') : ['MATRA_I', 'ADHA_SA'],  \
                                                          \
            # the reph is handed the matra_aa of the syllable it sits on, so
            # a matra_aa that a second matra_aa follows is a matra_aa with a
            # reph on top of it, as in कार्यालय
            ('MATRA_AA', 'MATRA_AA') : ['MATRA_AA', 'ADHA_RA'], \
        }

        # the sta ligature of the font is handed the string of the half sa,
        # so a 'स्' that a matra or the end of a word follows is that
        # ligature and the ta of it has to be put back. A 'स्' that a
        # consonant follows is the half sa that is really there, as in स्थान
        for tokenName in ['MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U',   \
                          'MATRA_UU', 'MATRA_RI', 'MATRA_E', 'MATRA_AI',  \
                          'MATRA_AU', 'MATRA_CHANDRA_O', 'BINDU',         \
                          'MATRAOBINDU', 'VISARGA', 'SPACE', 'NEWLINE',   \
                          'COMMA', 'DOT', 'SEMICOLON', 'COLON',           \
                          'RIGHTPARAN', 'VIRAM']:
            self.composeTokens[('ADHA_SA', tokenName)] = \
                                            ['ADHA_SA', 'TA', tokenName]

        # while the reph jumps back to the head of its syllable, it has to
        # jump over the matras and the signs of that syllable
        self.jumpover = set([ \
            'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',      \
            'MATRA_RI', 'MATRA_RR', 'MATRA_E', 'MATRA_AI', 'MATRA_O',      \
            'MATRA_AU', 'MATRA_CHANDRA_O', 'CHANDRA', 'BINDU',             \
            'CHANDRABINDU', 'VISARGA', 'NUKTA', 'MATRAOBINDU',             \
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
        t_A              = pat('अ')
        t_AA             = pat('आ')
        t_I              = pat('इ')
        t_II             = pat('ई')
        t_U              = pat('उ')
        t_UU             = pat('ऊ')
        t_RE             = pat('ऋ')
        t_E              = pat('ए')
        t_AI             = pat('ऐ')
        t_OO             = pat('ओ')
        t_AU             = pat('औ')
        t_CHANDRA_O      = pat('ऑ')

        # CONSONANTS. ka and sha are both handed the string of the matra_i
        # of the cluster they were first drawn in, so both of them come out
        # as 'ि' and are read as ka, the more common of the two
        t_ADHA_KA        = pat('क्')
        t_KA             = pat('ि')
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

        t_ADHA_PA        = pat('प्')
        t_PA             = pat('प')
        t_ADHA_PHA       = pat('फ्')
        t_PHA            = pat('फ')
        t_FA             = pat('\u095e', '\u092b\u093c')
        t_ADHA_BA        = pat('ब्')
        t_BA             = pat('ब')
        t_ADHA_BHA       = pat('भ्')
        t_BHA            = pat('भ')
        t_ADHA_MA        = pat('म्')
        t_MA             = pat('म')

        t_ADHA_YA        = pat('य्')
        t_YA             = pat('य')
        # ra is also the string of the matra_i that the font draws in front
        # of the syllable ra, which is sorted out in composeTokens
        t_RA             = pat('र')
        t_ADHA_LA        = pat('ल्')
        t_LA             = pat('ल')
        t_LLA            = pat('ळ')
        t_ADHA_VA        = pat('व्')
        t_VA             = pat('व')

        t_ADHA_SSA       = pat('ष्')
        t_SSA            = pat('ष')
        # the sta ligature of the font is handed the string of the half sa
        t_ADHA_SA        = pat('स्')
        t_SA             = pat('स')
        t_ADHA_HA        = pat('ह्')
        t_HA             = pat('ह')

        # CONJUNCTS whose glyph is handed a string that ends in a consonant
        # that is a glyph of its own, so they have to be matched as a whole.
        # The shta ligature is handed a halant too many, and kta is also the
        # string of the matra_i that the font draws in front of a wide
        # syllable, which is sorted out in composeTokens
        t_ADHA_CHHHA     = pat('क्ष्')
        t_CHHHA          = pat('क्ष')
        t_KTA            = pat('क्त')
        t_SSATTARA       = pat('ष्ट्र')
        t_SSATTA         = pat('ष्ट्')

        # MATRAS. the glyphs of matra_i are handed the strings of ka, of ra
        # and of kta, so ra and kta are only a matra in front of the
        # syllables that the font draws with those two glyphs, which is done
        # in composeTokens. matra_o is handed no string at all and is only
        # there when the anusvara that follows it puts it back
        t_MATRA_AA       = pat('ा')
        t_MATRA_I        = pat('क')
        t_MATRA_II       = pat('ी')
        t_MATRA_U        = pat('ु')
        t_MATRA_UU       = pat('ू')
        t_MATRA_RI       = pat('ृ')
        t_MATRA_E        = pat('े')
        t_MATRA_AI       = pat('ै')
        t_MATRA_AU       = pat('ौ')
        t_CHANDRA        = pat('ॅ')
        t_MATRA_CHANDRA_O = pat('ॉ')
        # the reph that the font draws together with a matra_o
        t_MATRAORI       = pat('ो')
        # the anusvara of a matra_o, with the space of the matra_o in front
        # of it
        t_MATRAOBINDU    = pat(' ों')

        # SIGNS. the anusvara has one glyph for the head of a letter and one
        # for the head of a matra_e, and the first of them is handed a
        # matra_o as well. The reph has no glyph whose string is its own,
        # see MATRA_AA and MATRAORI
        t_BINDU          = pat('ों', 'ं')
        t_CHANDRABINDU   = pat('ाँ', 'ँ')
        t_VISARGA        = pat('ः')
        t_NUKTA          = pat('़')
        t_HALANT         = pat('्')
        t_AVAGRAHA       = pat('ऽ')
        t_VIRAM          = pat('।')
        t_DEERGH_VIRAM   = pat('॥')

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
            self.report_error(t)
            t.lexer.skip(1)

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
