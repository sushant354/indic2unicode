import re

from indic2unicode.langs import devanagari
from .basefont import BaseFont
import ply.lex as lex

class Chanakya(BaseFont):
    '''Chanakya is an ascii font i.e. all the glyphs of the font sit in the
       printable ascii range (plus a few characters in the cp1252 upper
       range). A full consonant is mostly drawn as the glyph of the half
       consonant followed by the vertical bar 'k', which is the same glyph
       that is used for MATRA_AA.
    '''
    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs  = []
        self.langobjs.append(devanagari.DevanagariUnicode())
        self.langobjs.append(devanagari.Conjuncts())
        self.langobjs.append(devanagari.Chanakya())

        self.lexer = self.get_lexer()

        # matra_i is drawn to the left of the consonant it belongs to
        self.waitdict   = {'MATRA_I': 1, 'MATRAIBINDU': 1}

        # reph is typed after the whole syllable it sits on
        self.jumpbefore = {'ADHA_RA': 1}

        self.composeTokens = { \
            # matra_chandra_o is drawn as the vertical bar plus chandra \
            ('MATRA_AA', 'CHANDRA')  : 'MATRA_CHANDRA_O', \
            ('A', 'MATRA_AA')        : 'AA',        \
            ('A', 'MATRA_O')         : 'OO',        \
            ('A', 'MATRA_AU')        : 'AU',        \
            ('A', 'MATRA_CHANDRA_O') : 'CHANDRA_O', \
            ('E', 'MATRA_E')         : 'AI',        \
            ('ADHA_RA', 'ADHA_RA')   : 'ADHA_RA',   \
            # visarga never starts a word, there it is a colon \
            ('SPACE', 'VISARGA')     : ['SPACE', 'COLON'], \
        }

        # bindu does not touch the matra of its syllable, so the two get
        # typed in either order. Unicode always wants the matra first
        for sign in ['BINDU', 'CHANDRABINDU']:
            for matra in ['MATRA_AA', 'MATRA_II', 'MATRA_U', 'MATRA_UU', \
                          'MATRA_RI', 'MATRA_E', 'MATRA_AI', 'MATRA_O',  \
                          'MATRA_AU']:
                self.composeTokens[(sign, matra)] = [matra, sign]

        # while the reph jumps back to the head of its syllable, it has to
        # jump over the matras and the signs of that syllable
        self.jumpover = set([ \
            'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',      \
            'MATRA_RI', 'MATRA_RR', 'MATRA_E', 'MATRA_AI', 'MATRA_O',      \
            'MATRA_AU', 'MATRA_CHANDRA_O', 'CHANDRA', 'MATRAIBINDU',       \
            'MATRAIIBINDU', 'BINDU', 'CHANDRABINDU', 'VISARGA', 'NUKTA',   \
        ])

        # nukta and the glyphs that hang below a consonant belong to the
        # syllable matra_i has already passed, so it has to stay behind them
        self.waitover = set(['RAKAR', 'YAKAR', 'NUKTA'])

        # a half consonant is not the consonant matra_i is waiting for, but
        # it is the head of the syllable that matra_i belongs to
        self.halftokens = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName.startswith('ADHA_'):
                    self.halftokens.add(tokenName)

        # a nuktaed consonant is typed as the half consonant, the nukta and
        # then the vertical bar that makes the consonant full
        for tokenName in sorted(self.halftokens):
            fullName = tokenName[len('ADHA_'):]
            if self.token_to_unicode(fullName) != None:
                self.composeTokens[(tokenName, 'NUKTA', 'MATRA_AA')] = \
                    [fullName, 'NUKTA']

    def to_unicode(self, data):
        # A zero width non joiner/joiner is not a glyph of the font. The pdf
        # extraction puts them in and if one lands in the middle of a
        # multiple character glyph like '[k' it splits the glyph in two, so
        # they are dropped before the text is tokenized
        for zerowidth in ['‌', '‍']:
            data = data.replace(zerowidth, '')

        return BaseFont.to_unicode(self, data)

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        def pat(*glyphs):
            # token strings are regular expressions for ply, so the glyphs
            # have to be escaped. Alternate glyphs of the same token are
            # joined into one pattern
            return '|'.join([re.escape(glyph) for glyph in glyphs])

        bar = 'k'  # the vertical bar that makes a half consonant full

        def full(*glyphs):
            # a full consonant is its half consonant plus the vertical bar
            return pat(*[glyph + bar for glyph in glyphs])

        # VOWELS. aa, o, au and ai are composed out of a/e and a matra
        t_A              = pat('v')
        t_CHANDRA_O      = pat('v‚')
        t_I              = pat('b')
        t_II             = pat('bZ', 'Ã')
        t_IIBINDU        = pat('b±')
        t_U              = pat('m')
        t_UU             = pat('Å')
        t_RE             = pat('_')
        t_E              = pat(',')

        # CONSONANTS
        t_ADHA_KA        = pat('D')
        t_KA             = full('D') + '|' + pat('d')
        t_ADHA_KHA       = pat('[')
        t_KHA            = full('[')
        t_ADHA_GA        = pat('X')
        t_GA             = full('X') + '|' + pat('x')
        t_ADHA_GHA       = pat('?')
        t_GHA            = full('?') + '|' + pat('Ä')
        t_NGA            = pat('³')

        t_ADHA_CA        = pat('P')
        t_CA             = full('P') + '|' + pat('p')
        t_CHA            = pat('N')
        t_ADHA_JA        = pat('T')
        t_JA             = full('T') + '|' + pat('t')
        t_ADHA_JHA       = pat('÷', 'Ö')
        t_JHA            = pat('>')
        t_NYA            = pat('¥')

        t_TTA            = pat('V')
        t_TTHA           = pat('B')
        t_DDA            = pat('M')
        t_DDHA           = pat('<')
        t_ADHA_NNA       = pat('.')
        t_NNA            = full('.')

        t_ADHA_TA        = pat('R')
        t_TA             = full('R') + '|' + pat('r')
        t_ADHA_THA       = pat('F')
        t_THA            = full('F')
        t_DA             = pat('n')
        t_ADHA_DHA       = pat('/', 'è', 'Ë')
        t_DHA            = full('/', 'è', 'Ë')
        t_ADHA_NA        = pat('U')
        t_NA             = full('U') + '|' + pat('u')

        t_ADHA_PA        = pat('I')
        t_PA             = full('I') + '|' + pat('i')
        t_ADHA_PHA       = pat('¶')
        t_PHA            = pat('Q')
        t_ADHA_BA        = pat('C')
        t_BA             = full('C') + '|' + pat('c')
        t_ADHA_BHA       = pat('H')
        t_BHA            = full('H') + '|' + pat('Ò')
        t_ADHA_MA        = pat('E')
        t_MA             = full('E') + '|' + pat('e')

        t_ADHA_YA        = pat('¸')
        t_YA             = pat(';')
        t_RA             = pat('j')
        t_ADHA_LA        = pat('Y')
        t_LA             = full('Y') + '|' + pat('y')
        t_LLA            = pat('G')
        t_ADHA_VA        = pat('O')
        t_VA             = full('O') + '|' + pat('o')

        # the pdf extraction of the font turns the quotes of sha and ssa
        # into their curly variants
        t_ADHA_SHA       = pat("'", 'Ü', '“', '”', '‘')
        t_SHA            = full("'", 'Ü', '“', '”', '‘')
        t_ADHA_SSA       = pat('"', '’')
        t_SSA            = full('"', '’')
        t_ADHA_SA        = pat('L')
        t_SA             = full('L') + '|' + pat('l')
        t_HA             = pat('g')

        # CONJUNCTS that have a glyph of their own
        t_ADHA_CHHHA     = pat('{')
        t_CHHHA          = full('{')
        t_ADHA_TRA       = pat('«')
        t_TRA            = pat('=')
        t_GYAN           = pat('K')
        t_SHRA           = pat('J')
        t_DAYA           = pat('|')
        t_DAWA           = pat('}')
        t_DRA            = pat('æ')
        t_DADA           = pat('í', 'Ì')
        t_DADHA          = pat(')')
        t_PRA            = pat('ç', 'Á')
        t_KRA            = pat('Ø')
        t_PHRA           = pat('Ý')
        t_KTA            = pat('ä')
        t_KAKA           = pat('ô')
        t_ADHA_TATA      = pat('Ù')
        t_TATA           = full('Ù')
        t_ADHA_NANA      = pat('™')
        t_NANA           = pat('é')
        t_KRI            = pat('Ñ')
        t_TTATTA         = pat('ê', 'Í')
        t_TTATTHA        = pat('ë', 'Î')
        t_DDADDA         = pat('ì', 'Ï')
        t_DDADDHA        = pat('ï', 'Ô')
        t_HANA           = pat('à')
        t_HAYA           = pat('á')
        t_HARI           = pat('â')
        t_HAMA           = pat('ã')
        t_RAU            = pat('#')
        t_RAUU           = pat(':')

        # MATRAS. matra_o and matra_au are the vertical bar plus matra_e
        # and matra_ai, so they have to be matched before the vertical bar
        t_MATRA_O        = pat('ks')
        t_MATRA_AU       = pat('kS')
        t_MATRA_AA       = pat(bar)
        t_MATRA_I        = pat('f')
        t_MATRAIBINDU    = pat('Ç')
        t_MATRAIRI2      = pat('Æ')
        t_MATRAIRIBINDU2 = pat('É')
        t_MATRAIIRI      = pat('Ê')
        t_MATRA_II       = pat('h')
        t_MATRAIIBINDU   = pat('È')
        t_MATRA_U        = pat('q')
        t_MATRA_UU       = pat('w')
        t_MATRA_RI       = pat('`')
        t_MATRA_E        = pat('s')
        t_MATRA_AI       = pat('S')
        t_CHANDRA        = pat('W')
        t_MATRA_CHANDRA_O = pat('‚')

        # SIGNS
        t_BINDU          = pat('a')
        t_ADHA_RA_BINDU  = pat('±')
        t_CHANDRABINDU   = pat('¡')
        t_VISARGA        = pat('%')
        t_NUKTA          = pat('+')
        t_ADHA_RA        = pat('Z')
        t_RAKAR          = pat('z', 'ª', '~j')
        t_YAKAR          = pat('î', 'Ó')
        t_EXPLICIT_HALANT = pat('~')
        t_AVAGRAHA       = pat('•', '·', '∙')
        t_ABBREV         = pat('ö', 'Œ', 'ñ')
        t_VIRAM          = pat('A')

        # DIGITS. the font keeps the latin digits on the digit keys
        t_ASCII_ZERO     = pat('0')
        t_ASCII_ONE      = pat('1')
        t_ASCII_TWO      = pat('2')
        t_ASCII_THREE    = pat('3')
        t_ASCII_FOUR     = pat('4')
        t_ASCII_FIVE     = pat('5')
        t_ASCII_SIX      = pat('6')
        t_ASCII_SEVEN    = pat('7')
        t_ASCII_EIGHT    = pat('8')
        t_ASCII_NINE     = pat('9')

        t_ZERO           = pat('å')
        t_ONE            = pat('ƒ')
        t_TWO            = pat('„')
        t_THREE          = pat('…')
        t_FOUR           = pat('†')
        t_FIVE           = pat('‡')
        t_SIX            = pat('ˆ')
        t_SEVEN          = pat('‰')
        t_EIGHT          = pat('Š')
        t_NINE           = pat('‹')

        # PUNCTUATIONS
        t_LEFTPARAN      = pat('¼')
        t_RIGHTPARAN     = pat('½')
        t_COMMA          = pat(']')
        t_DOT            = pat('-')
        t_DASH           = pat('&')
        t_SLASH          = pat('@')
        t_SEMICOLON      = pat('(')
        t_QUESTION       = pat('\\')
        t_EQ             = pat('¾')
        t_LEFTBRACE      = pat('¿')
        t_RIGHTBRACE     = pat('À')
        t_LSQUOTE        = pat('^')
        t_RSQUOTE        = pat('*')
        t_LDQUOTE        = pat('Þ')
        t_RDQUOTE        = pat('ß')

        # These glyphs are shared with the latin font that the headers and
        # the english text of the document are set in, so they come out of
        # the pdf as plain punctuation. In a document that is only in
        # chanakya they are the conjuncts kri('—'), dri('–') and adha_ha
        # ('º') instead
        t_LEFTSQBRACE    = pat('¹')
        t_RIGHTSQBRACE   = pat('º')
        t_ENDASH         = pat('–')
        t_EMDASH         = pat('—', 'µ')
        t_SPACE          = pat(' ')
        t_NEWLINE        = pat('\n')
        t_CARRIAGERET    = pat('\r')
        t_FORMFEED       = pat('')

        def t_error(t):
            self.report_error(t)
            t.lexer.skip(1)

        # only the tokens that the font has a glyph for
        rules  = locals()
        tokens = [tokenName for tokenName in tokens if 't_' + tokenName in rules]

        return lex.lex()
