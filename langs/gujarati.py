import string

from .baselang import BaseLang

# the consonants of the script, in the order the block lays them out. A
# cluster, a dead consonant and a letter that carries a sign are built out of
# these in Conjuncts below
CONSONANT_TOKENS = [ \
    'KA',  'KHA', 'GA',  'GHA', 'NGA',        \
    'CA',  'CHA', 'JA',  'JHA', 'NYA',        \
    'TTA', 'TTHA','DDA', 'DDHA','NNA',        \
    'TA',  'THA', 'DA',  'DHA', 'NA',         \
    'PA',  'PHA', 'BA',  'BHA', 'MA',         \
    'YA',  'RA',  'LA',  'LLA', 'VA',         \
    'SHA', 'SSA', 'SA',  'HA',                \
]

# the vowels, which are letters in their own right and which a font draws
# together with the sign that follows them as readily as it does a consonant
VOWEL_TOKENS = [ \
    'A',   'AA',  'I',   'II',  'U',   'UU',  \
    'VOCALIC_R',  'VOCALIC_L',  'CANDRA_E',   \
    'E',   'AI',  'CANDRA_O',   'O',   'AU',  \
]

# the clusters of consonants that a gujarati font draws as a ligature of its
# own. The list is KrishnaUni's, read off the akhn, the pres and the vatu
# lookups of that font, with the clusters Krishna has a key of its own for
# added to it - ક્ષ and જ્ઞ, which KrishnaUni spells out. Gujarati binds a
# consonant to the one before it with a virama and a font that has a glyph
# for the pair draws the whole cluster in one shape, so the cluster is a
# token rather than a run of tokens - see the class comment of Conjuncts.
# A cluster the font has no ligature for is drawn as a half form and the
# letter that follows it instead, e.g. લ્પ, and is two tokens
CONJUNCT_TOKENS = [ \
    ('KA', 'KA'),   ('KA', 'CA'),   ('KA', 'TA'),   ('KA', 'NA'),   \
    ('KA', 'RA'),   ('KA', 'LA'),   ('KA', 'VA'),   ('KA', 'SSA'),  \
    ('KHA', 'NA'),  ('KHA', 'RA'),                                  \
    ('GA', 'NA'),   ('GA', 'RA'),                                   \
    ('GHA', 'NA'),  ('GHA', 'RA'),                                  \
    ('CA', 'CA'),   ('CA', 'NA'),   ('CA', 'RA'),   ('CA', 'VA'),   \
    ('CHA', 'RA'),  ('CHA', 'VA'),                                  \
    ('JA', 'JA'),   ('JA', 'NA'),   ('JA', 'NYA'),  ('JA', 'RA'),   \
    ('JA', 'VA'),                                                   \
    ('TTA', 'TTA'), ('TTA', 'YA'),  ('TTA', 'RA'),  ('TTA', 'VA'),  \
    ('DDA', 'TTA'), ('DDA', 'DDA'), ('DDA', 'DDHA'),                \
    ('DDA', 'YA'),  ('DDA', 'RA'),                                  \
    ('DDHA', 'DDHA'), ('DDHA', 'YA'), ('DDHA', 'RA'),               \
    ('TA', 'TA'),   ('TA', 'NA'),   ('TA', 'RA'),                   \
    ('THA', 'NA'),  ('THA', 'RA'),                                  \
    ('DA', 'GA'),   ('DA', 'GHA'),  ('DA', 'DA'),   ('DA', 'DHA'),  \
    ('DA', 'NA'),   ('DA', 'BA'),   ('DA', 'BHA'),  ('DA', 'MA'),   \
    ('DA', 'YA'),   ('DA', 'RA'),   ('DA', 'VA'),                   \
    ('DHA', 'NA'),  ('DHA', 'RA'),                                  \
    ('NA', 'NA'),   ('NA', 'RA'),                                   \
    ('PA', 'TA'),   ('PA', 'NA'),   ('PA', 'RA'),                   \
    ('PHA', 'NA'),  ('PHA', 'RA'),                                  \
    ('BA', 'NA'),   ('BA', 'RA'),                                   \
    ('BHA', 'NA'),  ('BHA', 'RA'),                                  \
    ('MA', 'NA'),   ('MA', 'RA'),                                   \
    ('YA', 'RA'),                                                   \
    ('LA', 'LA'),   ('LA', 'RA'),                                   \
    ('LLA', 'RA'),                                                  \
    ('VA', 'NA'),   ('VA', 'RA'),                                   \
    ('SHA', 'CA'),  ('SHA', 'NA'),  ('SHA', 'RA'),  ('SHA', 'LA'),  \
    ('SHA', 'VA'),                                                  \
    ('SA', 'NA'),   ('SA', 'RA'),   ('SA', 'TA', 'RA'),             \
    ('HA', 'NNA'),  ('HA', 'NA'),   ('HA', 'MA'),   ('HA', 'YA'),   \
    ('HA', 'RA'),   ('HA', 'LA'),   ('HA', 'VA'),                   \
]

# the signs that a font draws together with the letter or the cluster they
# belong to rather than beside it, so that the two are one glyph and one
# token. ુ and ૂ hang under the letter and a shape they cannot hang under
# gets a glyph of the pair - રુ, હૂ, ટ્ટુ, હ્મૂ - ં sits over the letter and
# over the vowel sign of it - ઇં, જ્જં - and the જ family merges with the
# vowel sign behind it, જા, જી and જો
COMPOSED_SIGN_TOKENS = ['MATRA_AA', 'MATRA_II', 'MATRA_U', 'MATRA_UU', \
                        'MATRA_O', 'ANUSVARA']

class GujaratiUnicode(BaseLang):
    '''the unicode values of the gujarati script.

       Gujarati writes every vowel sign of a letter behind that letter and
       draws all but one of them there as well. The one that is drawn
       elsewhere is િ MATRA_I, which is drawn in front of the cluster it
       belongs to, and the other thing a font draws elsewhere than unicode
       writes it is the reph - see Conjuncts below, which is where the reph
       is, both of them being more than one character.
    '''
    def __init__(self):
        BaseLang.__init__(self)
        self.tokendict = { \
          # SIGNS                     \
          'CANDRABINDU'         : 'ઁ', \
          'ANUSVARA'            : 'ં', \
          'VISARGA'             : 'ઃ', \
                                     \
          # VOWELS                   \
          'A'           : 'અ', \
          'AA'          : 'આ', \
          'I'           : 'ઇ', \
          'II'          : 'ઈ', \
          'U'           : 'ઉ', \
          'UU'          : 'ઊ', \
          'VOCALIC_R'   : 'ઋ', \
          'VOCALIC_L'   : 'ઌ', \
          'CANDRA_E'    : 'ઍ', \
          'E'           : 'એ', \
          'AI'          : 'ઐ', \
          'CANDRA_O'    : 'ઑ', \
          'O'           : 'ઓ', \
          'AU'          : 'ઔ', \
          'VOCALIC_RR'  : 'ૠ', \
          'VOCALIC_LL'  : 'ૡ', \
                                     \
          # CONSONANTS               \
          'KA'          : 'ક', \
          'KHA'         : 'ખ', \
          'GA'          : 'ગ', \
          'GHA'         : 'ઘ', \
          'NGA'         : 'ઙ', \
                                     \
          'CA'          : 'ચ', \
          'CHA'         : 'છ', \
          'JA'          : 'જ', \
          'JHA'         : 'ઝ', \
          'NYA'         : 'ઞ', \
                                     \
          'TTA'         : 'ટ', \
          'TTHA'        : 'ઠ', \
          'DDA'         : 'ડ', \
          'DDHA'        : 'ઢ', \
          'NNA'         : 'ણ', \
                                     \
          'TA'          : 'ત', \
          'THA'         : 'થ', \
          'DA'          : 'દ', \
          'DHA'         : 'ધ', \
          'NA'          : 'ન', \
                                     \
          'PA'          : 'પ', \
          'PHA'         : 'ફ', \
          'BA'          : 'બ', \
          'BHA'         : 'ભ', \
          'MA'          : 'મ', \
                                     \
          'YA'          : 'ય', \
          'RA'          : 'ર', \
          'LA'          : 'લ', \
          'LLA'         : 'ળ', \
          'VA'          : 'વ', \
          'SHA'         : 'શ', \
          'SSA'         : 'ષ', \
          'SA'          : 'સ', \
          'HA'          : 'હ', \
                                     \
          # MATRAS                    \
          'MATRA_AA'         : 'ા', \
          'MATRA_I'          : 'િ', \
          'MATRA_II'         : 'ી', \
          'MATRA_U'          : 'ુ', \
          'MATRA_UU'         : 'ૂ', \
          'MATRA_VOCALIC_R'  : 'ૃ', \
          'MATRA_VOCALIC_RR' : 'ૄ', \
          'MATRA_CANDRA_E'   : 'ૅ', \
          'MATRA_E'          : 'ે', \
          'MATRA_AI'         : 'ૈ', \
          'MATRA_CANDRA_O'   : 'ૉ', \
          'MATRA_O'          : 'ો', \
          'MATRA_AU'         : 'ૌ', \
          'MATRA_VOCALIC_L'  : 'ૢ', \
          'MATRA_VOCALIC_LL' : 'ૣ', \
                                          \
          # SIGNS                          \
          'NUKTA'            : '઼', \
          'AVAGRAHA'         : 'ઽ', \
          'VIRAMA'           : '્', \
          'OM'               : 'ૐ', \
          'ABBREVIATION'     : '૰', \
          'RUPEE'            : '૱', \
                                          \
          # DIGITS                         \
          'ZERO'        : '૦', \
          'ONE'         : '૧', \
          'TWO'         : '૨', \
          'THREE'       : '૩', \
          'FOUR'        : '૪', \
          'FIVE'        : '૫', \
          'SIX'         : '૬', \
          'SEVEN'       : '૭', \
          'EIGHT'       : '૮', \
          'NINE'        : '૯', \
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
          'FORMFEED'         : '\f',       \
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
          'LSQUOTE'          : '‘',   \
          'RSQUOTE'          : '’',   \
          'LDQUOTE'          : '“',   \
          'RDQUOTE'          : '”',   \
          'DANDA'            : '।',   \
          'DOUBLE_DANDA'     : '॥',   \
        }

class Conjuncts(BaseLang):
    '''the pieces of a syllable that a gujarati font draws as one glyph and
       that are more than one character.

       1. A cluster of consonants, which gujarati binds with a virama and a
          font draws in one shape - TA_TA is ત્ત and SA_TA_RA is સ્ત્ર. The
          token of it is the tokens of its consonants joined by an
          underscore.
       2. A dead consonant, DEAD_KA being ક્, which is the letter and the
          virama that ends it. It is the half form a font draws for a
          cluster it has no ligature of its own for, ક્લ being drawn whole
          and ક્પ as ક્ and પ.
       3. REPH, the ર્ that gujarati draws as a stroke over the syllable it
          belongs to rather than beside it. It is the same two characters as
          DEAD_RA and a token of its own because a font draws it with a glyph
          of its own and because it has to travel back to the head of its
          syllable, a dead ra staying where it is.
       4. A letter or a cluster that a font draws together with the sign
          behind it, JA_MATRA_AA being જા and TTA_TTA_MATRA_U ટ્ટુ. It is one
          token rather than two because the font has one glyph for the pair,
          and a sign that jumps over the letter has to jump over the whole of
          it - see COMPOSED_SIGN_TOKENS above.

       The pieces that a font draws in one glyph and that neither of the
       reordering passes moves apart are handed on as the tokens they are
       made of rather than given a token of their own, see conjunct_tokens
       below: MATRA_II_ANUSVARA is the ીં of બિલ્ડીંગ, which is a vowel sign
       and the ં over it, and MATRA_E_REPH is the ેર્ of સર્વે, which is a
       vowel sign and a reph that still has to travel over its letter.

       Not every one of these is drawn as a glyph by every font - a font that
       spells one of them out carries no code for that token, and the lexer
       of a font is built over the tokens it does carry
    '''
    def __init__(self):
        BaseLang.__init__(self)
        gujaratiUnicode = GujaratiUnicode()
        uMap   = gujaratiUnicode.tokendict
        virama = uMap['VIRAMA']

        self.tokendict = {}

        clusters = {}
        for tokens in CONJUNCT_TOKENS:
            clusters['_'.join(tokens)] = \
                    virama.join([uMap[tokenName] for tokenName in tokens])
        self.tokendict.update(clusters)

        for tokenName in CONSONANT_TOKENS:
            self.tokendict['DEAD_' + tokenName] = uMap[tokenName] + virama
        for tokenName, cluster in list(clusters.items()):
            self.tokendict['DEAD_' + tokenName] = cluster + virama

        self.tokendict['REPH'] = uMap['RA'] + virama

        # the rakar, the ્ર that gujarati draws as a mark under the letter
        # it is bound to rather than beside it. It is the virama and the ra
        # of that binding in the order unicode writes them, unlike REPH
        # above, and it is a token of its own because a font draws it with a
        # glyph of its own
        self.tokendict['RAKAR'] = virama + uMap['RA']

        # the letters and the clusters that a font draws together with the
        # sign behind them
        letters = {tokenName: uMap[tokenName] \
                   for tokenName in VOWEL_TOKENS + CONSONANT_TOKENS}
        letters.update(clusters)
        for tokenName, letter in letters.items():
            for signName in COMPOSED_SIGN_TOKENS:
                self.tokendict[tokenName + '_' + signName] = \
                        letter + uMap[signName]

        # the glyphs that stand for more than one token and whose tokens are
        # not moved apart by the two reordering passes, so that nothing is
        # gained by giving the glyph a string of its own: the tokenizer hands
        # the tokens on in place of the glyph and the passes see them. The
        # reph of the last three still travels back to the head of its
        # syllable, the vowel sign of the pair staying where it is
        self.conjunct_tokens = { \
            'MATRA_AA_MATRA_VOCALIC_R' : ['MATRA_AA', 'MATRA_VOCALIC_R'], \
            'MATRA_II_ANUSVARA'    : ['MATRA_II', 'ANUSVARA'],       \
            'MATRA_E_ANUSVARA'     : ['MATRA_E',  'ANUSVARA'],       \
            'MATRA_O_ANUSVARA'     : ['MATRA_O',  'ANUSVARA'],       \
            'REPH_ANUSVARA'        : ['REPH',     'ANUSVARA'],       \
            'MATRA_II_REPH'        : ['MATRA_II', 'REPH'],           \
            'MATRA_E_REPH'         : ['MATRA_E',  'REPH'],           \
            'MATRA_O_REPH'         : ['MATRA_O',  'REPH'],           \
            'MATRA_II_REPH_ANUSVARA' : ['MATRA_II', 'REPH', 'ANUSVARA'], \
            'MATRA_E_REPH_ANUSVARA'  : ['MATRA_E',  'REPH', 'ANUSVARA'], \
            'MATRA_O_REPH_ANUSVARA'  : ['MATRA_O',  'REPH', 'ANUSVARA'], \
        }

class KrishnaUni(BaseLang):
    '''the tokens that the text of a KrishnaUni document carries beyond the
       gujarati of it. The Gujarat Government Gazette is headed and numbered
       in english and its notifications carry a file number every now and
       then, and that text is set in a latin font and comes out of the pdf as
       itself
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
