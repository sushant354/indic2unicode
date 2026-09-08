import string

from .baselang import BaseLang

# the consonants of the script, in the order the block lays them out. A
# cluster, a dead consonant and a subjoined consonant are built out of these
# in Conjuncts below
CONSONANT_TOKENS = [ \
    'KA',  'KHA', 'GA',  'GHA', 'NGA',        \
    'CA',  'CHA', 'JA',  'JHA', 'NYA',        \
    'TTA', 'TTHA','DDA', 'DDHA','NNA',        \
    'TA',  'THA', 'DA',  'DHA', 'NA',         \
    'PA',  'PHA', 'BA',  'BHA', 'MA',         \
    'YA',  'RA',  'LA',  'LLA', 'VA',         \
    'SHA', 'SSA', 'SA',  'HA',                \
    'RRA', 'RHA', 'YYA', 'WA',                \
]

# the clusters of two and three consonants that an odiya display font draws
# as a ligature of its own. Odiya writes a consonant that a virama binds to
# the one before it under that consonant, and a font that has a glyph for
# the pair draws the whole cluster in one shape, so the cluster is a token
# rather than a run of tokens - see the class comment of Conjuncts
CONJUNCT_TOKENS = [ \
    ('KA', 'TA'),   ('KA', 'RA'),   ('KA', 'LA'),   ('KA', 'SA'),   \
    ('KA', 'SSA'),  ('KA', 'WA'),   ('KA', 'SSA', 'MA'),            \
    ('KHA', 'RA'),                                                  \
    ('GA', 'GA'),   ('GA', 'NA'),   ('GA', 'MA'),   ('GA', 'RA'),   \
    ('GA', 'LA'),   ('GHA', 'RA'),                                  \
    ('NGA', 'KA'),  ('NGA', 'KHA'), ('NGA', 'GA'),  ('NGA', 'GHA'), \
    ('CA', 'CA'),   ('CA', 'CHA'),                                  \
    ('JA', 'JA'),   ('JA', 'NYA'),  ('JA', 'WA'),                   \
    ('NYA', 'CA'),  ('NYA', 'CHA'), ('NYA', 'JA'),  ('NYA', 'JHA'), \
    ('TTA', 'TTA'), ('TTA', 'TTHA'),('TTA', 'RA'),                  \
    ('DDA', 'DDA'), ('DDA', 'RA'),                                  \
    ('NNA', 'TTA'), ('NNA', 'TTHA'),('NNA', 'DDA'), ('NNA', 'DDHA'),\
    ('NNA', 'NNA'), ('NNA', 'MA'),                                  \
    ('TA', 'TA'),   ('TA', 'THA'),  ('TA', 'NA'),   ('TA', 'MA'),   \
    ('TA', 'RA'),   ('TA', 'WA'),                                   \
    ('DA', 'DA'),   ('DA', 'DHA'),  ('DA', 'NA'),   ('DA', 'MA'),   \
    ('DA', 'RA'),   ('DA', 'WA'),                                   \
    ('DHA', 'NA'),  ('DHA', 'MA'),  ('DHA', 'YYA'),                 \
    ('NA', 'TA'),   ('NA', 'THA'),  ('NA', 'DA'),   ('NA', 'DHA'),  \
    ('NA', 'NA'),   ('NA', 'MA'),   ('NA', 'DA', 'RA'),             \
    ('NA', 'TA', 'RA'),                                             \
    ('PA', 'TA'),   ('PA', 'NA'),   ('PA', 'PA'),   ('PA', 'RA'),   \
    ('PA', 'LA'),   ('PA', 'LLA'),                                  \
    ('PHA', 'RA'),                                                  \
    ('BA', 'DA'),   ('BA', 'JA'),   ('BA', 'RA'),                   \
    ('BHA', 'RA'),                                                  \
    ('MA', 'NA'),   ('MA', 'PA'),   ('MA', 'BA'),   ('MA', 'BHA'),  \
    ('MA', 'MA'),   ('MA', 'RA'),                                   \
    ('LA', 'KA'),   ('LA', 'PA'),   ('LA', 'LA'),   ('LA', 'MA'),   \
    ('LLA', 'PA'),                                                  \
    ('SHA', 'CA'),  ('SHA', 'MA'),  ('SHA', 'NA'),  ('SHA', 'RA'),  \
    ('SHA', 'WA'),                                                  \
    ('SSA', 'KA'),  ('SSA', 'TTA'), ('SSA', 'TTHA'),('SSA', 'NNA'), \
    ('SSA', 'MA'),  ('SSA', 'PA'),  ('SSA', 'TTA', 'RA'),           \
    ('SA', 'KA'),   ('SA', 'KHA'),  ('SA', 'TA'),   ('SA', 'THA'),  \
    ('SA', 'NA'),   ('SA', 'PA'),   ('SA', 'PHA'),  ('SA', 'MA'),   \
    ('SA', 'RA'),   ('SA', 'LA'),   ('SA', 'WA'),   ('SA', 'TA', 'RA'), \
    ('HA', 'NA'),   ('HA', 'NNA'),  ('HA', 'MA'),   ('HA', 'LA'),   \
]

# the reph, the ର୍ that odiya draws as a stroke over the syllable it belongs
# to, is spelled with the same two characters as a dead ra, and a font draws
# the two with glyphs of their own. The text of a pdf that has been repaired
# by tools/fix_tounicode.py keeps them apart by writing this after the reph:
# a zero width joiner is what unicode writes behind a virama to ask for a
# form of the letter rather than for a plain dead consonant, so the mark says
# which of the two glyphs was drawn rather than standing for anything of its
# own, and is dropped again once the syllable has been put in order. Without
# it a converter has to guess - a reph that ends a run of the pdf and a dead
# ra that ends a word look exactly alike
REPH_MARK = '\u200d'

class OdiyaUnicode(BaseLang):
    '''the unicode values of the odiya script.

       The two part vowel signs are one character each here - ୋ, ୈ and ୌ -
       and the second half that a font draws them with is a token of its
       own, AI_LENGTH_MARK and AU_LENGTH_MARK, the way the two part matras
       of kannada and malayalam are handled. The front half of all three is
       ୋ MATRA_E itself, which odiya writes in front of the letter it
       belongs to, so a font hands the halves over with the letter between
       them and the converter puts them back together - see
       fonts/odiya/kalinga.py
    '''
    def __init__(self):
        BaseLang.__init__(self)
        self.tokendict = { \
          # SIGNS                     \
          'CANDRABINDU'         : 'ଁ', \
          'ANUSVARA'            : 'ଂ', \
          'VISARGA'             : 'ଃ', \
                                     \
          # VOWELS                   \
          'A'           : 'ଅ', \
          'AA'          : 'ଆ', \
          'I'           : 'ଇ', \
          'II'          : 'ଈ', \
          'U'           : 'ଉ', \
          'UU'          : 'ଊ', \
          'VOCALIC_R'   : 'ଋ', \
          'VOCALIC_L'   : 'ଌ', \
          'E'           : 'ଏ', \
          'AI'          : 'ଐ', \
          'O'           : 'ଓ', \
          'AU'          : 'ଔ', \
          'VOCALIC_RR'  : 'ୠ', \
          'VOCALIC_LL'  : 'ୡ', \
                                     \
          # CONSONANTS               \
          'KA'          : 'କ', \
          'KHA'         : 'ଖ', \
          'GA'          : 'ଗ', \
          'GHA'         : 'ଘ', \
          'NGA'         : 'ଙ', \
                                     \
          'CA'          : 'ଚ', \
          'CHA'         : 'ଛ', \
          'JA'          : 'ଜ', \
          'JHA'         : 'ଝ', \
          'NYA'         : 'ଞ', \
                                     \
          'TTA'         : 'ଟ', \
          'TTHA'        : 'ଠ', \
          'DDA'         : 'ଡ', \
          'DDHA'        : 'ଢ', \
          'NNA'         : 'ଣ', \
                                     \
          'TA'          : 'ତ', \
          'THA'         : 'ଥ', \
          'DA'          : 'ଦ', \
          'DHA'         : 'ଧ', \
          'NA'          : 'ନ', \
                                     \
          'PA'          : 'ପ', \
          'PHA'         : 'ଫ', \
          'BA'          : 'ବ', \
          'BHA'         : 'ଭ', \
          'MA'          : 'ମ', \
                                     \
          'YA'          : 'ଯ', \
          'RA'          : 'ର', \
          'LA'          : 'ଲ', \
          'LLA'         : 'ଳ', \
          'VA'          : 'ଵ', \
          'SHA'         : 'ଶ', \
          'SSA'         : 'ଷ', \
          'SA'          : 'ସ', \
          'HA'          : 'ହ', \
                                     \
          # the three letters that unicode has a character of its own for  \
          # beside the nukta pair, and the wa that odiya writes a ba as     \
          # when it is bound under another consonant                       \
          'RRA'         : '\u0b5c', \
          'RHA'         : '\u0b5d', \
          'YYA'         : 'ୟ', \
          'WA'          : 'ୱ', \
                                     \
          # MATRAS. a two part matra is one character here, the font        \
          # decides how many glyphs it is drawn in                          \
          'MATRA_AA'         : 'ା', \
          'MATRA_I'          : 'ି', \
          'MATRA_II'         : 'ୀ', \
          'MATRA_U'          : 'ୁ', \
          'MATRA_UU'         : 'ୂ', \
          'MATRA_VOCALIC_R'  : 'ୃ', \
          'MATRA_VOCALIC_RR' : 'ୄ', \
          'MATRA_E'          : 'େ', \
          'MATRA_AI'         : 'ୈ', \
          'MATRA_O'          : 'ୋ', \
          'MATRA_AU'         : 'ୌ', \
          'MATRA_VOCALIC_L'  : 'ୢ', \
          'MATRA_VOCALIC_LL' : 'ୣ', \
                                          \
          # the second half of a two part matra, which the fonts draw as a  \
          # glyph of its own                                                \
          'AI_LENGTH_MARK'   : 'ୖ', \
          'AU_LENGTH_MARK'   : 'ୗ', \
                                          \
          # SIGNS                          \
          'NUKTA'            : '଼', \
          'AVAGRAHA'         : 'ଽ', \
          'VIRAMA'           : '୍', \
          'ISSHAR'           : '୰', \
                                          \
          # DIGITS                         \
          'ZERO'        : '୦', \
          'ONE'         : '୧', \
          'TWO'         : '୨', \
          'THREE'       : '୩', \
          'FOUR'        : '୪', \
          'FIVE'        : '୫', \
          'SIX'         : '୬', \
          'SEVEN'       : '୭', \
          'EIGHT'       : '୮', \
          'NINE'        : '୯', \
                                          \
          # PUNCTUATIONS                   \
          'STAR'             : '*',        \
          'QUOT'             : '"',        \
          'PLUS'             : '+',        \
          'EQ'               : '=',        \
          'SPACE'            : ' ',        \
          'NEWLINE'          : '\n',       \
          'CARRIAGERET'      : '\r',       \
          'TAB'              : '\t',       \
          'PERCENT'          : '%',        \
          'AMPERSAND'        : '&',        \
          'AT'               : '@',        \
          'APOSTROPHE'       : "'",        \
          'LEFTPARAN'        : '(',        \
          'RIGHTPARAN'       : ')',        \
          'LEFTSQBRACE'      : '[',        \
          'RIGHTSQBRACE'     : ']',        \
          'COMMA'            : ',',        \
          'DASH'             : '-',        \
          'ENDASH'           : '–',   \
          'EMDASH'           : '—',   \
          'DOT'              : '.',        \
          'SLASH'            : '/',        \
          'COLON'            : ':',        \
          'SEMICOLON'        : ';',        \
          'QUESTION'         : '?',        \
          'EXCLAMATION'      : '!',        \
          'DANDA'            : '।',   \
          'DOUBLE_DANDA'     : '॥',   \
        }

class Conjuncts(BaseLang):
    '''the pieces of a syllable that an odiya font draws as one glyph and
       that are more than one character.

       1. A cluster of consonants, which odiya binds with a virama and
          writes as one shape - NNA_DDA is ଣ୍ଡ and SSA_TTA_RA is ଷ୍ଟ୍ର. The
          token of it is the tokens of its consonants joined by an
          underscore.
       2. A dead consonant, DEAD_KA being କ୍, which is the letter and the
          virama that ends it.
       3. A subjoined consonant, SUBJOINED_MA being ୍ମ, which is the virama
          and the letter, in that order - that being how unicode writes a
          consonant that is bound under the one before it. A font draws
          each of them as a mark of its own under the letter, ୟ, ୱ and ର
          among them, which odiya calls the phalas.
       4. REPH, the ର୍ that odiya draws as a stroke over the syllable it
          belongs to rather than beside it. It is the same two characters
          as DEAD_RA and a token of its own because a font draws it with a
          glyph of its own and because it has to travel back to the head of
          its syllable, a dead ra staying where it is.
       5. A letter that a font draws together with the vowel sign i of it,
          THA_MATRA_I being ଥି. It is a token rather than two because the
          font has one glyph for the pair, and a sign that jumps over the
          letter has to jump over the whole of it.
       6. MATRA_I_CANDRABINDU, the ିଁ that a font draws in one glyph. It is
          two characters and neither of them moves, so it is handed on as
          the two rather than given a string of its own - see
          conjunct_tokens below and fonts/odiya/akruti.py.

       Not every one of these is drawn as a glyph by every font - a font
       that spells one of them out carries no code for that token, and the
       lexer of a font is built over the tokens it does carry
    '''
    def __init__(self):
        BaseLang.__init__(self)
        odiyaUnicode = OdiyaUnicode()
        uMap    = odiyaUnicode.tokendict
        virama  = uMap['VIRAMA']
        matra_i = uMap['MATRA_I']

        self.tokendict = {}
        for tokens in CONJUNCT_TOKENS:
            self.tokendict['_'.join(tokens)] = \
                    virama.join([uMap[tokenName] for tokenName in tokens])

        for tokenName in CONSONANT_TOKENS:
            consonant = uMap[tokenName]
            self.tokendict['DEAD_'      + tokenName] = consonant + virama
            self.tokendict['SUBJOINED_' + tokenName] = virama + consonant
            self.tokendict[tokenName + '_MATRA_I']   = consonant + matra_i

        self.tokendict['REPH'] = uMap['RA'] + virama

        # the glyphs that stand for more than one token and whose tokens
        # each stay where they are, so that nothing is gained by giving the
        # pair a string of its own: the tokenizer hands the tokens on in
        # place of the glyph and the passes see the two
        self.conjunct_tokens = { \
            'MATRA_I_CANDRABINDU' : ['MATRA_I', 'CANDRABINDU'], \
        }

class Kalinga(BaseLang):
    '''the tokens that the text of a Kalinga document carries beyond the
       odiya of it. A Kalinga run of such a pdf carries latin every now and
       then - the (i) of a heading, an e-mail address - and it comes out of
       the pdf as itself
    '''
    def __init__(self):
        BaseLang.__init__(self)

        digitnames = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', \
                      'SEVEN', 'EIGHT', 'NINE']
        for digit, name in enumerate(digitnames):
            self.tokendict['ASCII_' + name] = '%d' % digit

        for char in string.ascii_uppercase:
            self.tokendict['LATIN_' + char] = char
        for char in string.ascii_lowercase:
            self.tokendict['LATIN_SMALL_' + char.upper()] = char
