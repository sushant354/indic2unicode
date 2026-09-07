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

class Gautami(BaseLang):
    '''the tokens that the text of a Gautami document carries beyond the
       telugu of TeluguUnicode and Vattus above, and the glyphs of that font
       that draw more than one character.

       Gautami is a real opentype font - unlike Priyaanka above, which is an
       8 bit display font - so nothing here stands for less than a
       character. What it needs are the names of the syllables and the
       clusters that the font draws in a single glyph, each of them spelled
       out of the tokens it is made of:

       1. The dead consonant, a letter written with the pollu of its
          cluster. The font has a glyph per letter for it - కోర్ట్ is drawn
          కో ర్ ్ట - and it is the letter and the virama, in that order,
          which is the order the glyph draws them in and the order unicode
          writes them in once the vattus of the cluster have moved in front
          of that virama. See fonts/telugu/gautami.py.
       2. The letters that a vowel sign is drawn into rather than written
          beside. The signs i and ii replace the talakattu of a letter and
          reshape it, so a syllable that carries either of them is one
          glyph, and so are ఙు, జు, శు, క్షు and their long forms, the four
          letters that end in the stroke the sign u is drawn with, and the
          syllables that the signs o and oo are drawn into - ఘొ, ఝొ, మొ, యొ
          and హో. హా is one glyph as well, the ా of a హ being drawn into
          the stem of the letter.
       3. క్ష and జ్ఞ, the two clusters telugu writes as a letter of their
          own. The font draws each of them as one glyph, gives each a vattu
          of its own and a dead form of its own, and spells them here the
          way unicode does - the letter, the virama and the letter under it.
       4. The vattu of pa with the vowel sign u drawn into it, which is one
          glyph of the font and two characters, exactly as it is in
          Priyaanka above.

       The two archaic letters ౘ and ౙ are here as well: TeluguUnicode
       above names neither of them, and Gautami draws both, with a vattu, a
       dead form and the vowel signs of any other letter.
    '''
    # the letters that the font draws each vowel sign into, so that the
    # syllable is one glyph of the font and two characters here
    DRAWN_IN = {\
        'MATRA_I'  : ['KHA', 'CA', 'CHA', 'JA', 'TA', 'NA', 'BA', 'BHA', \
                      'MA', 'LA', 'LLA', 'VA', 'SHA', 'TSA', 'DZA'],     \
        'MATRA_II' : ['KHA', 'CA', 'CHA', 'JA', 'TA', 'NA', 'BA', 'BHA', \
                      'MA', 'LA', 'LLA', 'VA', 'SHA', 'TSA', 'DZA'],     \
        'MATRA_U'  : ['NGA', 'JA', 'SHA', 'KSSA', 'DZA'],                \
        'MATRA_UU' : ['NGA', 'JA', 'SHA', 'KSSA', 'DZA'],                \
        'MATRA_O'  : ['GHA', 'JHA', 'MA', 'YA'],                         \
        'MATRA_OO' : ['GHA', 'JHA', 'MA', 'YA', 'HA'],                   \
        'MATRA_AA' : ['HA'],                                             \
    }

    # what a token of DRAWN_IN is called after the letter it belongs to
    SIGN_SUFFIX = {'MATRA_AA': 'AA', 'MATRA_I' : 'I',  'MATRA_II': 'II', \
                   'MATRA_U' : 'U',  'MATRA_UU': 'UU', 'MATRA_O' : 'O',  \
                   'MATRA_OO': 'OO'}

    def __init__(self):
        BaseLang.__init__(self)
        telUnicode = TeluguUnicode()
        uMap       = telUnicode.tokendict
        virama     = uMap['VIRAMA']

        self.tokendict = {\
            # the two archaic letters, which TeluguUnicode does not name,   \
            # and the vattu of each of them                                 \
            'TSA'              : 'ౘ',                                 \
            'DZA'              : 'ౙ',                                 \
            'VATTU_TSA'        : virama + 'ౘ',                        \
            'VATTU_DZA'        : virama + 'ౙ',                        \
                                                                            \
            # the two vowel signs of the vocalic l, which TeluguUnicode      \
            # does not name either                                          \
            'MATRA_VOCALIC_L'  : 'ౢ',                                 \
            'MATRA_VOCALIC_LL' : 'ౣ',                                 \
        }

        # the letters that a cluster of this font can be built out of: the
        # telugu of TeluguUnicode, the two archaic letters above, and క్ష
        # and జ్ఞ, which the font draws and treats as letters of their own
        letters = [tokenName for tokenName, ustr in uMap.items() \
                   if is_consonant(ustr)] + ['TSA', 'DZA']

        self.conjunct_tokens = {\
            # క్ష and జ్ఞ, and the vattu of each of them                    \
            'KSSA'       : ['KA', 'VATTU_SSA'],                            \
            'JNYA'       : ['JA', 'VATTU_NYA'],                            \
            'VATTU_KSSA' : ['VATTU_KA', 'VATTU_SSA'],                      \
            'VATTU_JNYA' : ['VATTU_JA', 'VATTU_NYA'],                      \
                                                                           \
            # the vattu of pa with the vowel sign u drawn into it           \
            'VATTU_PA_U' : ['VATTU_PA', 'MATRA_U'],                        \
        }

        # the dead consonants, a letter and the pollu of its cluster. A
        # conjunct token is expanded once and not again, so the two clusters
        # are spelled out of their letters here rather than out of their own
        # token
        for tokenName in letters:
            self.conjunct_tokens[tokenName + '_VIRAMA'] = [tokenName, 'VIRAMA']
        self.conjunct_tokens['KSSA_VIRAMA'] = ['KA', 'VATTU_SSA', 'VIRAMA']
        self.conjunct_tokens['JNYA_VIRAMA'] = ['JA', 'VATTU_NYA', 'VIRAMA']

        # the syllables that the font draws in one glyph
        for sign, consonants in self.DRAWN_IN.items():
            for tokenName in consonants:
                name = tokenName + '_' + self.SIGN_SUFFIX[sign]
                if tokenName == 'KSSA':
                    self.conjunct_tokens[name] = ['KA', 'VATTU_SSA', sign]
                else:
                    self.conjunct_tokens[name] = [tokenName, sign]
