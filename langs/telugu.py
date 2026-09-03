import string

from .baselang import BaseLang

def is_consonant(ustr):
    '''whether the string of a token is a single telugu consonant, which is
       what a vattu can be made of'''
    return len(ustr) == 1 and ('క' <= ustr <= 'హ' or \
                               ustr in ('ౘ', 'ౙ', 'ౚ'))

class TeluguUnicode(BaseLang):
    '''the unicode values of the telugu script. The short and the long
       vowels are named the way unicode names them, so E is the short one
       and EE the long one, and the same for O and OO
    '''
    def __init__(self):
        BaseLang.__init__(self)
        self.tokendict = { \
          # SIGNS                     \
          'CANDRABINDU'         : 'ఁ', \
          'ANUSVARA'            : 'ం', \
          'VISARGA'             : 'ః', \
                                     \
          # VOWELS                   \
          'A'           : 'అ', \
          'AA'          : 'ఆ', \
          'I'           : 'ఇ', \
          'II'          : 'ఈ', \
          'U'           : 'ఉ', \
          'UU'          : 'ఊ', \
          'VOCALIC_R'   : 'ఋ', \
          'VOCALIC_L'   : 'ఌ', \
          'E'           : 'ఎ', \
          'EE'          : 'ఏ', \
          'AI'          : 'ఐ', \
          'O'           : 'ఒ', \
          'OO'          : 'ఓ', \
          'AU'          : 'ఔ', \
          'VOCALIC_RR'  : 'ౠ', \
          'VOCALIC_LL'  : 'ౡ', \
                                     \
          # CONSONANTS               \
          'KA'          : 'క', \
          'KHA'         : 'ఖ', \
          'GA'          : 'గ', \
          'GHA'         : 'ఘ', \
          'NGA'         : 'ఙ', \
                                     \
          'CA'          : 'చ', \
          'CHA'         : 'ఛ', \
          'JA'          : 'జ', \
          'JHA'         : 'ఝ', \
          'NYA'         : 'ఞ', \
                                     \
          'TTA'         : 'ట', \
          'TTHA'        : 'ఠ', \
          'DDA'         : 'డ', \
          'DDHA'        : 'ఢ', \
          'NNA'         : 'ణ', \
                                     \
          'TA'          : 'త', \
          'THA'         : 'థ', \
          'DA'          : 'ద', \
          'DHA'         : 'ధ', \
          'NA'          : 'న', \
                                     \
          'PA'          : 'ప', \
          'PHA'         : 'ఫ', \
          'BA'          : 'బ', \
          'BHA'         : 'భ', \
          'MA'          : 'మ', \
                                     \
          'YA'          : 'య', \
          'RA'          : 'ర', \
          'RRA'         : 'ఱ', \
          'LA'          : 'ల', \
          'LLA'         : 'ళ', \
          'LLLA'        : 'ఴ', \
          'VA'          : 'వ', \
          'SHA'         : 'శ', \
          'SSA'         : 'ష', \
          'SA'          : 'స', \
          'HA'          : 'హ', \
                                     \
          # MATRAS. a two part matra is one character here, the font decides \
          # how many glyphs it is drawn in                                   \
          'MATRA_AA'         : 'ా', \
          'MATRA_I'          : 'ి', \
          'MATRA_II'         : 'ీ', \
          'MATRA_U'          : 'ు', \
          'MATRA_UU'         : 'ూ', \
          'MATRA_VOCALIC_R'  : 'ృ', \
          'MATRA_VOCALIC_RR' : 'ౄ', \
          'MATRA_E'          : 'ె', \
          'MATRA_EE'         : 'ే', \
          'MATRA_AI'         : 'ై', \
          'MATRA_O'          : 'ొ', \
          'MATRA_OO'         : 'ో', \
          'MATRA_AU'         : 'ౌ', \
                                          \
          # the second half of a two part matra, which the fonts draw as a  \
          # glyph of its own                                                \
          'LENGTH_MARK'      : 'ౕ', \
          'AI_LENGTH_MARK'   : 'ౖ', \
                                          \
          # SIGNS                          \
          'AVAGRAHA'         : 'ఽ', \
          'VIRAMA'           : '్', \
                                          \
          # DIGITS                         \
          'ZERO'        : '౦', \
          'ONE'         : '౧', \
          'TWO'         : '౨', \
          'THREE'       : '౩', \
          'FOUR'        : '౪', \
          'FIVE'        : '౫', \
          'SIX'         : '౬', \
          'SEVEN'       : '౭', \
          'EIGHT'       : '౮', \
          'NINE'        : '౯', \
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
    '''the subjoined consonants. Telugu writes a consonant that a virama
       binds to the one before it under that consonant rather than beside
       it, and a display font has a glyph of its own for every one of them,
       so they are tokens of their own here - the vattu of ka is the virama
       and ka, in that order, however the font spells it
    '''
    def __init__(self):
        BaseLang.__init__(self)
        telUnicode = TeluguUnicode()
        uMap   = telUnicode.tokendict
        virama = uMap['VIRAMA']

        self.tokendict = {}
        for tokenName, ustr in uMap.items():
            if is_consonant(ustr):
                self.tokendict['VATTU_' + tokenName] = virama + ustr

class Priyaanka(BaseLang):
    '''the tokens that the text of a Priyaanka document carries beyond the
       telugu of it, and the glyphs of the font that draw more than one
       character or less than a whole one.

       Priyaanka is an 8-bit display font of the Anu family: every glyph of
       it sits on a byte and a syllable is spelled out of the pieces it is
       drawn with, in the order they stand on the page. Telugu draws a
       consonant as a body with a mark on top of it - the talakattu, which
       says that the letter carries the inherent vowel a - and a vowel sign
       replaces that mark, so the font has a glyph for the body of the
       letter and one for each mark that can sit on it. Five kinds of glyph
       here are therefore neither a character of their own nor a whole one:

       1. INHERENT_A, the talakattu. It is the mark of the vowel a, which
          is already part of the letter in unicode, so it stands for no
          character at all - '‘·' is త and '‘˚' is తే.
       2. AI_MARK and OO_MARK, the back halves of ై and ో. Both signs are
          drawn in two pieces with the letter between them, the front piece
          being the ె the font draws anyway, and composeTokens reads the
          pair back as the one sign.
       3. The aspiration strokes. ధ is ద with a stroke through it, థ is ద
          with another, ఫ is ప with one and భ is బ with the same stroke ధ
          takes, and the font draws each of them as a glyph of its own on
          top of the letter rather than as a letter - so ధ is two glyphs
          and not one, and fonts/telugu/priyaanka.py puts them back
          together.
       4. YA_BASE, the body of య, which is not the whole letter: the tail
          of య is the same glyph that draws the vowel sign u, and the two
          are put back together in fonts/telugu/priyaanka.py the way మ is
          put together out of the body of వ and that same tail.
       5. The stem of హ, which is the stroke the vowel sign ా is drawn
          with. 'Vü≤' is హ - a body, a talakattu and a ా that is no
          character - and the ా of a హ is a glyph of its own that draws
          the stem and a second stroke beside it, STEM_MATRA_AA below.

       The conjunct tokens below are the other way round: one glyph of the
       font draws a whole syllable. The vowel signs i and ii replace the
       talakattu and change the shape of the letter they sit on, so a
       letter that takes either of them is drawn as one glyph and not two,
       and so is ష్ట్ర, the one cluster of this document that the font
       draws in a single piece
    '''
    def __init__(self):
        BaseLang.__init__(self)

        self.tokendict = {\
            # the talakattu, see 1. above                                   \
            'INHERENT_A'       : '',         \
                                             \
            # the back halves of ై and ో, see 2. above. Neither is a        \
            # character on its own; each is joined to the ె in front of it  \
            # once that ె has jumped over the letter between them, and      \
            # what is left over if one ever stands alone is the mark it     \
            # draws - the stroke of ా for the second, nothing at all for    \
            # the first                                                     \
            'AI_MARK'          : '',         \
            'OO_MARK'          : 'ా',   \
                                             \
            # the stem of హ written with a second stroke beside it, see 5. \
            # above. It is the ా of a హ, the stem itself being a ా that     \
            # draws no character and that fonts/telugu/priyaanka.py drops   \
            'STEM_MATRA_AA'    : 'ా',   \
                                             \
            # the aspiration strokes, see 3. above. STROKE_H is the one     \
            # that turns ద into ధ and బ into భ, STROKE_TH the one that      \
            # turns ద into థ, STROKE_PH the one that turns ప into ఫ, and    \
            # SUB_STROKE_H the one that turns the vattu ్బ into ్భ. None    \
            # of them is a character if it ever stands alone                \
            'STROKE_H'         : '',         \
            'STROKE_TH'        : '',         \
            'STROKE_PH'        : '',         \
            'SUB_STROKE_H'     : '',         \
                                             \
            # the body of య, see 4. above. It is the letter without its     \
            # tail, and the letter if the tail is ever missing              \
            'YA_BASE'          : 'య',   \
                                             \
            # the tail of మ and of య, which is the glyph that draws the    \
            # vowel sign u as well - see 4. above. It is that sign          \
            # wherever it is not the tail of one of those two letters       \
            'TAIL'             : 'ు',  \
                                             \
            # ె and ే as they are drawn on the letters that carry the sign  \
            # in front of them rather than behind, which is a glyph of its  \
            # own for each of the two signs. They are the sign they draw    \
            # and travel, see fonts/telugu/priyaanka.py                     \
            'PRE_MATRA_E'      : 'ె',  \
            'PRE_MATRA_EE'     : 'ే',  \
                                             \
            # punctuation of the document that has no telugu token          \
            'HYPHEN'           : '-',        \
        }

        # the syllables that the font draws in one glyph. The vowel signs i
        # and ii replace the talakattu of the letter and reshape it, so
        # every letter that takes either of them has a glyph of its own for
        # that syllable
        ivowels = ['GA', 'CA', 'JA', 'TA', 'DA', 'NA', 'BA', 'RA', 'LA', \
                   'LLA', 'VA']

        self.conjunct_tokens = {}
        for consonant in ivowels:
            self.conjunct_tokens[consonant + '_I']  = [consonant, 'MATRA_I']
            self.conjunct_tokens[consonant + '_II'] = [consonant, 'MATRA_II']

        # జ is the one letter this document draws with the vowel sign u or
        # uu written into it as well
        self.conjunct_tokens['JA_U']  = ['JA', 'MATRA_U']
        self.conjunct_tokens['JA_UU'] = ['JA', 'MATRA_UU']

        # ష్ట్ర, the one cluster the font draws in a single piece. Its ra
        # is spelled out of the virama and the letter rather than as the
        # vattu the two make: the vattu of ra is a token that travels, this
        # glyph having already drawn it where it belongs
        self.conjunct_tokens['SSA_TTA_RA'] = ['SSA', 'VATTU_TTA', 'VIRAMA', \
                                              'RA']

        # the vattu of pa with the vowel sign u drawn into it, which is one
        # glyph of the font and two characters
        self.conjunct_tokens['VATTU_PA_U'] = ['VATTU_PA', 'MATRA_U']
