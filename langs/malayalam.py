from .baselang import BaseLang

# the consonants of malayalam, in the order the script lists them - the five
# vargas and then the ya-varga, with the two letters malayalam has of its
# own, റ and ഴ, among them where the alphabet puts them
CONSONANT_TOKENS = [ \
    'KA',  'KHA',  'GA',  'GHA',  'NGA',  \
    'CA',  'CHA',  'JA',  'JHA',  'NYA',  \
    'TTA', 'TTHA', 'DDA', 'DDHA', 'NNA',  \
    'TA',  'THA',  'DA',  'DHA',  'NA',   \
    'PA',  'PHA',  'BA',  'BHA',  'MA',   \
    'YA',  'RA',   'RRA', 'LA',   'LLA',  \
    'LLLA','VA',   'SHA', 'SSA',  'SA', 'HA', \
]

# the clusters that a malayalam font draws as a single glyph. Each of them is
# the consonants it is written out of, and the token of it is their tokens
# joined by an underscore - ('NA', 'RRA') is ന്റ and its token is NA_RRA.
#
# A cluster is a token of its own and not a sequence of them because a font
# draws it as one glyph and because the vowel signs that are written in front
# of a syllable have to jump over the whole of it - see the class comment of
# Conjuncts below. Only the clusters that the fonts of this package have a
# glyph for are listed: the 33 that fonts/malayalam/revathi.py carries a code
# for, and the 89 that fonts/malayalam/meera.py reads, which are a superset of
# them. A font that draws one this leaves out simply has no glyph whose token
# is missing here
CONJUNCT_TOKENS = [ \
    ('KA', 'KA'),      ('KA', 'TTA'),     ('KA', 'TTA', 'RA'), \
    ('KA', 'TA'),      ('KA', 'NA'),      ('KA', 'RA'),        \
    ('KA', 'RRA', 'RRA'), ('KA', 'LA'),   ('KA', 'SSA'),       \
    ('KA', 'SSA', 'MA'), ('KA', 'SA'),                         \
    ('GA', 'GA'),      ('GA', 'DA'),      ('GA', 'RA'),        \
    ('GA', 'LA'),                                              \
    ('NGA', 'KA'),     ('NGA', 'NGA'),                         \
    ('CA', 'CA'),                                              \
    ('JA', 'JA'),      ('JA', 'NYA'),     ('JA', 'MA'),        \
    ('NYA', 'CA'),     ('NYA', 'NYA'),                         \
    ('TTA', 'TTA'),    ('TTA', 'RA'),                          \
    ('NNA', 'TTA'),    ('NNA', 'TTA', 'RA'), ('NNA', 'DDA'),   \
    ('NNA', 'NNA'),    ('NNA', 'MA'),                          \
    ('TA', 'TA'),      ('TA', 'THA'),     ('TA', 'MA'),        \
    ('TA', 'RA'),      ('TA', 'SA'),                           \
    ('DA', 'DA'),      ('DA', 'DHA'),     ('DA', 'RA'),        \
    ('NA', 'TA'),      ('NA', 'TA', 'RA'), ('NA', 'DA'),       \
    ('NA', 'DA', 'RA'), ('NA', 'DHA'),    ('NA', 'NA'),        \
    ('NA', 'MA'),      ('NA', 'RRA'),                          \
    ('PA', 'TTA'),     ('PA', 'TA'),      ('PA', 'PA'),        \
    ('PA', 'RA'),      ('PA', 'LA'),                           \
    ('PHA', 'RA'),     ('PHA', 'RRA', 'RRA'),                  \
    ('BA', 'RA'),      ('BA', 'LA'),                           \
    ('MA', 'PA'),      ('MA', 'PA', 'RA'), ('MA', 'MA'),       \
    ('YA', 'KA', 'KA'), ('YA', 'TA'),     ('YA', 'PA'),        \
    ('YA', 'YA'),                                              \
    ('RRA', 'RRA'),                                            \
    ('LA', 'KA'),      ('LA', 'PA'),      ('LA', 'LA'),        \
    ('LLA', 'LLA'),                                            \
    ('LLLA', 'CA'),    ('LLLA', 'TA', 'TA'), ('LLLA', 'NA', 'NA'), \
    ('LLLA', 'SA'),                                            \
    ('VA', 'VA'),                                              \
    ('SHA', 'CA'),     ('SHA', 'NA'),     ('SHA', 'RA'),       \
    ('SHA', 'SHA'),                                            \
    ('SSA', 'KA'),     ('SSA', 'TTA'),    ('SSA', 'TTHA'),     \
    ('SA', 'KA'),      ('SA', 'TTA', 'RA'), ('SA', 'TA'),      \
    ('SA', 'TA', 'RA'), ('SA', 'THA'),    ('SA', 'PA'),        \
    ('SA', 'MA'),      ('SA', 'RRA', 'RRA'), ('SA', 'SA'),     \
    ('HA', 'RA'),                                              \
]

class MalayalamUnicode(BaseLang):
    '''the unicode values of the malayalam script. The short and the long
       vowels are named the way unicode names them, so E is the short one
       and EE the long one, and the same for O and OO.

       THE CHILLUS

       A malayalam consonant that ends a syllable with no vowel of its own
       is written as a chillu, a letter of its own shape rather than the
       letter and a chandrakkala: നന്‍ is not ന and a virama but ൻ. Unicode
       spelled those as the consonant, the virama and a zero width joiner
       until 5.1 and has had a character for each of the five since, and
       the five characters are what this hands out - അവർ and not അവര്‍.
       The two spellings are different strings that no normalisation brings
       together, so a reader of this text has to be told which it is: this
       is the one the script's own block defines and the one malayalam
       text on the web is written in today.

       THE SIGNS THAT ARE A CONSONANT

       Three consonants are written as a mark on the letter they are bound
       to rather than beside it - ്യ, ്വ and ്ര - and a font draws each of
       those marks as a glyph of its own. They are the virama and that
       consonant however the font spells them, so ്യ is YA_SIGN here the
       way the vattus of langs/kannada.py are tokens of their own, and the
       ്ര of a cluster is written in front of the letter it belongs to,
       which is what the reordering of fonts/malayalam/revathi.py is for
    '''
    def __init__(self):
        BaseLang.__init__(self)
        self.tokendict = { \
          # SIGNS                     \
          'ANUSVARA'    : 'ം', \
          'VISARGA'     : 'ഃ', \
                                     \
          # VOWELS                   \
          'A'           : 'അ', \
          'AA'          : 'ആ', \
          'I'           : 'ഇ', \
          'II'          : 'ഈ', \
          'U'           : 'ഉ', \
          'UU'          : 'ഊ', \
          'VOCALIC_R'   : 'ഋ', \
          'VOCALIC_L'   : 'ഌ', \
          'E'           : 'എ', \
          'EE'          : 'ഏ', \
          'AI'          : 'ഐ', \
          'O'           : 'ഒ', \
          'OO'          : 'ഓ', \
          'AU'          : 'ഔ', \
          'VOCALIC_RR'  : 'ൠ', \
          'VOCALIC_LL'  : 'ൡ', \
                                     \
          # CONSONANTS               \
          'KA'          : 'ക', \
          'KHA'         : 'ഖ', \
          'GA'          : 'ഗ', \
          'GHA'         : 'ഘ', \
          'NGA'         : 'ങ', \
                                     \
          'CA'          : 'ച', \
          'CHA'         : 'ഛ', \
          'JA'          : 'ജ', \
          'JHA'         : 'ഝ', \
          'NYA'         : 'ഞ', \
                                     \
          'TTA'         : 'ട', \
          'TTHA'        : 'ഠ', \
          'DDA'         : 'ഡ', \
          'DDHA'        : 'ഢ', \
          'NNA'         : 'ണ', \
                                     \
          'TA'          : 'ത', \
          'THA'         : 'ഥ', \
          'DA'          : 'ദ', \
          'DHA'         : 'ധ', \
          'NA'          : 'ന', \
                                     \
          'PA'          : 'പ', \
          'PHA'         : 'ഫ', \
          'BA'          : 'ബ', \
          'BHA'         : 'ഭ', \
          'MA'          : 'മ', \
                                     \
          'YA'          : 'യ', \
          'RA'          : 'ര', \
          'RRA'         : 'റ', \
          'LA'          : 'ല', \
          'LLA'         : 'ള', \
          'LLLA'        : 'ഴ', \
          'VA'          : 'വ', \
          'SHA'         : 'ശ', \
          'SSA'         : 'ഷ', \
          'SA'          : 'സ', \
          'HA'          : 'ഹ', \
                                     \
          # THE CHILLUS. a consonant that carries no vowel and that ends  \
          # the syllable, each of them a character of its own - see the   \
          # class comment                                                 \
          'CHILLU_NN'   : 'ൺ', \
          'CHILLU_N'    : 'ൻ', \
          'CHILLU_RR'   : 'ർ', \
          'CHILLU_L'    : 'ൽ', \
          'CHILLU_LL'   : 'ൾ', \
          'CHILLU_K'    : 'ൿ', \
                                     \
          # MATRAS. a two part matra is one character here, the font      \
          # decides how many glyphs it is drawn in                        \
          'MATRA_AA'         : 'ാ', \
          'MATRA_I'          : 'ി', \
          'MATRA_II'         : 'ീ', \
          'MATRA_U'          : 'ു', \
          'MATRA_UU'         : 'ൂ', \
          'MATRA_VOCALIC_R'  : 'ൃ', \
          'MATRA_VOCALIC_RR' : 'ൄ', \
          'MATRA_E'          : 'െ', \
          'MATRA_EE'         : 'േ', \
          'MATRA_AI'         : 'ൈ', \
          'MATRA_O'          : 'ൊ', \
          'MATRA_OO'         : 'ോ', \
          'MATRA_AU'         : 'ൌ', \
                                          \
          # the second half of a two part matra, which the fonts draw as  \
          # a glyph of its own. AU_LENGTH_MARK is the sign of ഔ, and it   \
          # is also the stroke that ഈ and ഊ are drawn with                \
          'AU_LENGTH_MARK'   : 'ൗ', \
                                          \
          # SIGNS. the chandrakkala is malayalam's virama                 \
          'VIRAMA'           : '്', \
          'AVAGRAHA'         : 'ഽ', \
                                          \
          # DIGITS                         \
          'ZERO'        : '൦', \
          'ONE'         : '൧', \
          'TWO'         : '൨', \
          'THREE'       : '൩', \
          'FOUR'        : '൪', \
          'FIVE'        : '൫', \
          'SIX'         : '൬', \
          'SEVEN'       : '൭', \
          'EIGHT'       : '൮', \
          'NINE'        : '൯', \
          'TEN'         : '൰', \
          'HUNDRED'     : '൱', \
          'THOUSAND'    : '൲', \
                                     \
          # PUNCTUATIONS             \
          'SPACE'            : ' ',        \
          'NEWLINE'          : '\n',       \
          'CARRIAGERET'      : '\r',       \
          'TAB'              : '\t',       \
          'STAR'             : '*',        \
          'QUOT'             : '"',        \
          'PLUS'             : '+',        \
          'EQ'               : '=',        \
          'PERCENT'          : '%',        \
          'AMPERSAND'        : '&',        \
          'APOSTROPHE'       : "'",        \
          'LEFTPARAN'        : '(',        \
          'RIGHTPARAN'       : ')',        \
          'LEFTSQBRACE'      : '[',        \
          'RIGHTSQBRACE'     : ']',        \
          'COMMA'            : ',',        \
          'DASH'             : '-',        \
          'DOT'              : '.',        \
          'SLASH'            : '/',        \
          'COLON'            : ':',        \
          'SEMICOLON'        : ';',        \
          'QUESTION'         : '?',        \
          'EXCLAMATION'      : '!',        \
          'AT'               : '@',        \
          'UNDERSCORE'       : '_',        \
          'BULLET'           : '•',   \
          'MIDDLEDOT'        : '·',   \
          'LSQUOTE'          : '‘',   \
          'RSQUOTE'          : '’',   \
          'LDQUOTE'          : '“',   \
          'RDQUOTE'          : '”',   \
          'ENDASH'           : '–',   \
          'EMDASH'           : '—',   \
                                          \
          # the hyphen a dtp package writes into a word to say where it   \
          # may be broken across a line. The fonts draw it as a glyph of  \
          # no width, so it is on the page in the sense that a glyph of   \
          # it is drawn and in no other - see fonts/malayalam/revathi.py  \
          'SOFT_HYPHEN'      : '',    \
        }

        # the three consonants that are written as a mark on the letter
        # they are bound to. They are the virama and that consonant, in
        # that order, however the font spells them - see the class comment
        virama = self.tokendict['VIRAMA']
        for tokenName in ('YA', 'VA', 'RA'):
            self.tokendict[tokenName + '_SIGN'] = \
                    virama + self.tokendict[tokenName]

class Conjuncts(BaseLang):
    '''the clusters that a malayalam font draws as a single glyph.

       A cluster is the consonants of it bound by viramas, and the token of
       it is their tokens joined by an underscore, so NA_RRA is ന്റ and
       SA_RRA_RRA is സ്റ്റ. They are tokens rather than sequences of tokens
       because a font draws each of them as one glyph and because the vowel
       signs that are written in front of a syllable have to jump over the
       whole of it: a േ in front of the one glyph of ട്ട belongs behind
       both letters and the virama between them, not inside the cluster
    '''
    def __init__(self):
        BaseLang.__init__(self)
        malUnicode = MalayalamUnicode()
        uMap   = malUnicode.tokendict
        virama = uMap['VIRAMA']

        self.tokendict = {}
        for tokens in CONJUNCT_TOKENS:
            self.tokendict['_'.join(tokens)] = \
                    virama.join([uMap[tokenName] for tokenName in tokens])
