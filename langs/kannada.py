import string

from .baselang import BaseLang

def is_consonant(ustr):
    '''whether the string of a token is a single kannada consonant, which is
       what a vattu can be made of'''
    return len(ustr) == 1 and ('ಕ' <= ustr <= 'ಹ' or \
                               ustr in ('ೝ', 'ೞ'))

class KannadaUnicode(BaseLang):
    '''the unicode values of the kannada script. The short and the long
       vowels are named the way unicode names them, so E is the short one
       and EE the long one, and the same for O and OO
    '''
    def __init__(self):
        BaseLang.__init__(self)
        self.tokendict = { \
          # SIGNS                     \
          'SPACING_CANDRABINDU' : 'ಀ', \
          'CANDRABINDU'         : 'ಁ', \
          'ANUSVARA'            : 'ಂ', \
          'VISARGA'             : 'ಃ', \
                                     \
          # VOWELS                   \
          'A'           : 'ಅ', \
          'AA'          : 'ಆ', \
          'I'           : 'ಇ', \
          'II'          : 'ಈ', \
          'U'           : 'ಉ', \
          'UU'          : 'ಊ', \
          'VOCALIC_R'   : 'ಋ', \
          'VOCALIC_L'   : 'ಌ', \
          'E'           : 'ಎ', \
          'EE'          : 'ಏ', \
          'AI'          : 'ಐ', \
          'O'           : 'ಒ', \
          'OO'          : 'ಓ', \
          'AU'          : 'ಔ', \
          'VOCALIC_RR'  : 'ೠ', \
          'VOCALIC_LL'  : 'ೡ', \
                                     \
          # CONSONANTS               \
          'KA'          : 'ಕ', \
          'KHA'         : 'ಖ', \
          'GA'          : 'ಗ', \
          'GHA'         : 'ಘ', \
          'NGA'         : 'ಙ', \
                                     \
          'CA'          : 'ಚ', \
          'CHA'         : 'ಛ', \
          'JA'          : 'ಜ', \
          'JHA'         : 'ಝ', \
          'NYA'         : 'ಞ', \
                                     \
          'TTA'         : 'ಟ', \
          'TTHA'        : 'ಠ', \
          'DDA'         : 'ಡ', \
          'DDHA'        : 'ಢ', \
          'NNA'         : 'ಣ', \
                                     \
          'TA'          : 'ತ', \
          'THA'         : 'ಥ', \
          'DA'          : 'ದ', \
          'DHA'         : 'ಧ', \
          'NA'          : 'ನ', \
                                     \
          'PA'          : 'ಪ', \
          'PHA'         : 'ಫ', \
          'BA'          : 'ಬ', \
          'BHA'         : 'ಭ', \
          'MA'          : 'ಮ', \
                                     \
          'YA'          : 'ಯ', \
          'RA'          : 'ರ', \
          'RRA'         : 'ಱ', \
          'LA'          : 'ಲ', \
          'LLA'         : 'ಳ', \
          'VA'          : 'ವ', \
          'SHA'         : 'ಶ', \
          'SSA'         : 'ಷ', \
          'SA'          : 'ಸ', \
          'HA'          : 'ಹ', \
          'NAKAARA_POLLU': 'ೝ', \
          'FA'          : 'ೞ', \
                                     \
          # MATRAS. a two part matra is one character here, the font decides \
          # how many glyphs it is drawn in                                   \
          'MATRA_AA'         : 'ಾ', \
          'MATRA_I'          : 'ಿ', \
          'MATRA_II'         : 'ೀ', \
          'MATRA_U'          : 'ು', \
          'MATRA_UU'         : 'ೂ', \
          'MATRA_VOCALIC_R'  : 'ೃ', \
          'MATRA_VOCALIC_RR' : 'ೄ', \
          'MATRA_E'          : 'ೆ', \
          'MATRA_EE'         : 'ೇ', \
          'MATRA_AI'         : 'ೈ', \
          'MATRA_O'          : 'ೊ', \
          'MATRA_OO'         : 'ೋ', \
          'MATRA_AU'         : 'ೌ', \
          'MATRA_VOCALIC_L'  : 'ೢ', \
          'MATRA_VOCALIC_LL' : 'ೣ', \
                                          \
          # the second half of a two part matra, which the fonts draw as a  \
          # glyph of its own                                                \
          'LENGTH_MARK'      : 'ೕ', \
          'AI_LENGTH_MARK'   : 'ೖ', \
                                          \
          # SIGNS                          \
          'NUKTA'            : '಼', \
          'AVAGRAHA'         : 'ಽ', \
          'VIRAMA'           : '್', \
          'JIHVAMULIYA'      : 'ೱ', \
          'UPADHMANIYA'      : 'ೲ', \
          'COMBINING_ANUSVARA' : 'ೳ', \
                                          \
          # DIGITS                         \
          'ZERO'        : '೦', \
          'ONE'         : '೧', \
          'TWO'         : '೨', \
          'THREE'       : '೩', \
          'FOUR'        : '೪', \
          'FIVE'        : '೫', \
          'SIX'         : '೬', \
          'SEVEN'       : '೭', \
          'EIGHT'       : '೮', \
          'NINE'        : '೯', \
                                     \
          # PUNCTUATIONS             \
          'STAR'             : '*',        \
          'QUOT'             : '"',        \
          'PLUS'             : '+',        \
          'EQ'               : '=',        \
          'SPACE'            : ' ',        \
          'NEWLINE'          : '\n',       \
          'CARRIAGERET'      : '\r',       \
          'TAB'              : '\t',       \
          'PERCENT'          : '%',        \
          'LEFTPARAN'        : '(',        \
          'RIGHTPARAN'       : ')',        \
          'COMMA'            : ',',        \
          'DASH'             : '-',        \
          'DOT'              : '.',        \
          'SLASH'            : '/',        \
          'COLON'            : ':',        \
          'SEMICOLON'        : ';',        \
          'QUESTION'         : '?',        \
          'EXCLAMATION'      : '!',        \
          'DANDA'            : '।',   \
          'DOUBLE_DANDA'     : '॥',   \
        }

class Vattus(BaseLang):
    '''the subjoined consonants. Kannada writes a consonant that a virama
       binds to the one before it under that consonant rather than beside
       it, and a font has a glyph of its own for every one of them, so they
       are tokens of their own here - the vattu of ka is the virama and ka,
       in that order, however the font spells it.

       The arkavattu is the other way round: a ra that a virama binds to the
       consonant after it is written as a mark on top of that consonant, and
       is the ra and the virama of the syllable that follows it
    '''
    def __init__(self):
        BaseLang.__init__(self)
        kanUnicode = KannadaUnicode()
        uMap   = kanUnicode.tokendict
        virama = uMap['VIRAMA']

        self.tokendict = {}
        for tokenName, ustr in uMap.items():
            if is_consonant(ustr):
                self.tokendict['VATTU_' + tokenName] = virama + ustr

        self.tokendict['ARKAVATTU'] = uMap['RA'] + virama

class Tunga(BaseLang):
    '''the tokens that the text of a Tunga pdf carries beyond the kannada of
       it: the glyphs of the font that its ToUnicode map has no entry for at
       all and the latin text of the document

       Tunga draws a consonant and the matra i or the matra o of it in one
       glyph, and the maps of these pdfs hand a number of those ligatures no
       string. An extractor that falls back on the cid of such a glyph, e.g.
       pymupdf, hands them out as the character of that cid, which is a
       latin letter here because the cids are the glyph ids of Tunga itself.
       That is what the LIG_ tokens below are, e.g. the ligature of va and
       the matra i is cid 0x13b and comes out as U+013B. An extractor that
       drops a glyph it has no string for, e.g. pdftotext, loses them
       outright and nothing can bring them back
    '''
    def __init__(self):
        BaseLang.__init__(self)

        self.tokendict = {\
            # punctuation of the document that has no kannada token \
            'BAR'              : '|',        \
            'AMPERSAND'        : '&',        \
            'APOSTROPHE'       : "'",        \
            'LEFTSQBRACE'      : '[',        \
            'RIGHTSQBRACE'     : ']',        \
            'AT'               : '@',        \
            'HASH'             : '#',        \
            'UNDERSCORE'       : '_',        \
            'LSQUOTE'          : '‘',   \
            'RSQUOTE'          : '’',   \
            'LDQUOTE'          : '“',   \
            'RDQUOTE'          : '”',   \
            'ENDASH'           : '–',   \
            'EMDASH'           : '—',   \
            'HYPHEN'           : '‐',   \
            # pdftotext ends a page with a form feed, which is text of the \
            # document rather than a glyph of the font                     \
            'FORMFEED'         : '',   \
        }

        # the english text of the document is set in a latin font, so its
        # letters and digits come out of the pdf as themselves
        digitnames = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', \
                      'SEVEN', 'EIGHT', 'NINE']
        for digit, name in enumerate(digitnames):
            self.tokendict['ASCII_' + name] = '%d' % digit

        for char in string.ascii_uppercase:
            self.tokendict['LATIN_' + char] = char
        for char in string.ascii_lowercase:
            self.tokendict['LATIN_SMALL_' + char.upper()] = char

        # the ligature glyphs of the font that the map has no entry for. Each
        # of them is a consonant and a matra, so it is more than one token
        self.conjunct_tokens = { \
            'LIG_LA_I'    : ['LA',  'MATRA_I'], \
            'LIG_LLA_I'   : ['LLA', 'MATRA_I'], \
            'LIG_VA_I'    : ['VA',  'MATRA_I'], \
            'LIG_SHA_I'   : ['SHA', 'MATRA_I'], \
            'LIG_SSA_I'   : ['SSA', 'MATRA_I'], \
            'LIG_SA_I'    : ['SA',  'MATRA_I'], \
            'LIG_HA_I'    : ['HA',  'MATRA_I'], \
            'LIG_PA_O'    : ['PA',  'MATRA_O'], \
            'LIG_YA_O'    : ['YA',  'MATRA_O'], \
        }
