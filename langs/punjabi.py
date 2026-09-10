from .baselang import BaseLang

# the consonants of the script, in the order the block lays them out, with
# the six that gurmukhi writes with a nukta at the end. A subjoined
# consonant, a cluster and a dead consonant are built out of these in
# Conjuncts below
CONSONANT_TOKENS = [ \
    'KA',  'KHA', 'GA',  'GHA', 'NGA',        \
    'CA',  'CHA', 'JA',  'JHA', 'NYA',        \
    'TTA', 'TTHA','DDA', 'DDHA','NNA',        \
    'TA',  'THA', 'DA',  'DHA', 'NA',         \
    'PA',  'PHA', 'BA',  'BHA', 'MA',         \
    'YA',  'RA',  'LA',  'VA',  'SA',  'HA',  \
    'RRA',                                    \
    'LLA', 'SHA', 'KHHA','GHHA','ZA',  'FA',  \
]

# the consonants that gurmukhi writes under the letter they are bound to,
# the pairin. ੍ਹ, ੍ਰ and ੍ਵ are the three that modern punjabi writes; ੍ਯ and
# the other four are the subjoined letters of the older orthography that
# the scriptures are printed in and that a font for them draws as well.
# Unicode writes each of them as the virama and the letter, behind the
# consonant it hangs under
PAIRI_TOKENS = ['HA', 'RA', 'VA', 'YA', 'CA', 'TTA', 'TA', 'NA']

# the three pairin of modern punjabi, which a font that draws a cluster in
# one shape has a glyph of the pair for - see Conjuncts below
CLUSTER_PAIRI_TOKENS = ['HA', 'RA', 'VA']

# the vowel signs that the bindi is drawn over rather than the tippi. Unicode
# writes the bindi behind the vowel sign, and a font draws some of the pairs
# in one glyph - ਾਂ, ੀਂ
BINDI_SIGN_TOKENS = ['MATRA_AA', 'MATRA_II', 'MATRA_EE', 'MATRA_AI', \
                     'MATRA_OO', 'MATRA_AU']

# the vowels of gurmukhi are not letters of their own shape. Each of them is
# one of the three carriers - ੳ, ਅ and ੲ - with a vowel sign drawn on it, and
# a legacy font types it that way: ਆ as ਅ and ਾ, ਇ as ੲ and ਿ. Unicode has a
# character of its own for each of these vowels and asks that it be used
# rather than the carrier and the sign, which is what these pairs are for.
# ਅ carries no sign of its own and is the vowel A as well as the carrier.
# ਓ is ੳ with a stroke of its own over it rather than a vowel sign, so it is
# not built out of a pair
VOWEL_COMPOSITIONS = { \
    ('URA', 'MATRA_U')  : 'U',  \
    ('URA', 'MATRA_UU') : 'UU', \
    ('A',   'MATRA_AA') : 'AA', \
    ('A',   'MATRA_AI') : 'AI', \
    ('A',   'MATRA_AU') : 'AU', \
    ('IRI', 'MATRA_I')  : 'I',  \
    ('IRI', 'MATRA_II') : 'II', \
    ('IRI', 'MATRA_EE') : 'EE', \
}

class PunjabiUnicode(BaseLang):
    '''the unicode values of the gurmukhi script that punjabi is written in.

       Gurmukhi writes every vowel sign of a letter behind that letter and
       draws all but one of them there as well. The one that is drawn
       elsewhere is ਿ MATRA_I, which is drawn in front of the letter it
       belongs to.

       Six consonants are written as another consonant with a nukta under
       it - ਲ਼, ਸ਼, ਖ਼, ਗ਼, ਜ਼ and ਫ਼. Unicode has a character of its own for
       each of the six, but every one of those characters decomposes into
       the letter and the nukta and is kept out of composition, so the
       normalized form of the text - NFC as much as NFD - is always the
       letter and the nukta. That is the form they are given here, so that
       a word comes out of every font the same way and the same way a
       search for it is typed.

       The nasal signs are the tippi ੰ and the bindi ਂ, the one drawn over
       a letter that carries no vowel sign or a ਿ, ੁ or ੂ and the other over
       one that carries any other. ੱ ADDAK doubles the consonant that
       follows it and is written in front of that consonant.
    '''
    def __init__(self):
        BaseLang.__init__(self)
        nukta = '਼'
        self.tokendict = { \
          # SIGNS                     \
          'ADAK_BINDI'          : 'ਁ', \
          'BINDI'               : 'ਂ', \
          'VISARGA'             : 'ਃ', \
                                     \
          # VOWELS                   \
          'A'           : 'ਅ', \
          'AA'          : 'ਆ', \
          'I'           : 'ਇ', \
          'II'          : 'ਈ', \
          'U'           : 'ਉ', \
          'UU'          : 'ਊ', \
          'EE'          : 'ਏ', \
          'AI'          : 'ਐ', \
          'OO'          : 'ਓ', \
          'AU'          : 'ਔ', \
                                     \
          # CONSONANTS               \
          'KA'          : 'ਕ', \
          'KHA'         : 'ਖ', \
          'GA'          : 'ਗ', \
          'GHA'         : 'ਘ', \
          'NGA'         : 'ਙ', \
                                     \
          'CA'          : 'ਚ', \
          'CHA'         : 'ਛ', \
          'JA'          : 'ਜ', \
          'JHA'         : 'ਝ', \
          'NYA'         : 'ਞ', \
                                     \
          'TTA'         : 'ਟ', \
          'TTHA'        : 'ਠ', \
          'DDA'         : 'ਡ', \
          'DDHA'        : 'ਢ', \
          'NNA'         : 'ਣ', \
                                     \
          'TA'          : 'ਤ', \
          'THA'         : 'ਥ', \
          'DA'          : 'ਦ', \
          'DHA'         : 'ਧ', \
          'NA'          : 'ਨ', \
                                     \
          'PA'          : 'ਪ', \
          'PHA'         : 'ਫ', \
          'BA'          : 'ਬ', \
          'BHA'         : 'ਭ', \
          'MA'          : 'ਮ', \
                                     \
          'YA'          : 'ਯ', \
          'RA'          : 'ਰ', \
          'LA'          : 'ਲ', \
          'VA'          : 'ਵ', \
          'SA'          : 'ਸ', \
          'HA'          : 'ਹ', \
          'RRA'         : 'ੜ', \
                                     \
          # the consonants written with a nukta, as the letter and the    \
          # nukta - see the class comment                                 \
          'LLA'         : 'ਲ' + nukta, \
          'SHA'         : 'ਸ' + nukta, \
          'KHHA'        : 'ਖ' + nukta, \
          'GHHA'        : 'ਗ' + nukta, \
          'ZA'          : 'ਜ' + nukta, \
          'FA'          : 'ਫ' + nukta, \
                                     \
          # MATRAS                    \
          'MATRA_AA'         : 'ਾ', \
          'MATRA_I'          : 'ਿ', \
          'MATRA_II'         : 'ੀ', \
          'MATRA_U'          : 'ੁ', \
          'MATRA_UU'         : 'ੂ', \
          'MATRA_EE'         : 'ੇ', \
          'MATRA_AI'         : 'ੈ', \
          'MATRA_OO'         : 'ੋ', \
          'MATRA_AU'         : 'ੌ', \
                                          \
          # SIGNS                          \
          'NUKTA'            : nukta,      \
          'VIRAMA'           : '੍', \
          'UDAAT'            : 'ੑ', \
          'TIPPI'            : 'ੰ', \
          'ADDAK'            : 'ੱ', \
          'YAKASH'           : 'ੵ', \
          'ABBREVIATION'     : '੶', \
          'EK_ONKAR'         : 'ੴ', \
                                          \
          # the carriers the vowels are drawn on, see VOWEL_COMPOSITIONS   \
          # above. ਅ, the third of them, is the vowel A                    \
          'IRI'              : 'ੲ', \
          'URA'              : 'ੳ', \
                                          \
          # DIGITS                         \
          'ZERO'        : '੦', \
          'ONE'         : '੧', \
          'TWO'         : '੨', \
          'THREE'       : '੩', \
          'FOUR'        : '੪', \
          'FIVE'        : '੫', \
          'SIX'         : '੬', \
          'SEVEN'       : '੭', \
          'EIGHT'       : '੮', \
          'NINE'        : '੯', \
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
    '''the pieces of a syllable that a gurmukhi font draws as one glyph and
       that are more than one character.

       1. A subjoined consonant, the pairi, which gurmukhi draws as a mark
          under the letter it is bound to - PAIRI_RA is the ੍ਰ of ਪ੍ਰਧਾਨ and
          PAIRI_HA the ੍ਹ of ਪੜ੍ਹ. It is the virama and the letter in the
          order unicode writes them, behind the consonant it hangs under,
          and a font that draws the mark on its own types it there as well.
       2. A cluster of a consonant and the pairi under it that a font draws
          in one shape, PA_RA being ਪ੍ਰ. The token of it is the tokens of
          its consonants joined by an underscore, the way the clusters of
          langs/gujarati.py are named.
       3. A dead consonant, DEAD_YA being ਯ੍, which is the letter and the
          virama that ends it - the half form a font draws for the ਯ of
          ਕ੍ਯ, or what the text of a sanskrit word asks for.

       The pieces that a font draws in one glyph and that neither of the
       reordering passes moves apart are handed on as the tokens they are
       made of rather than given a string of their own, see conjunct_tokens
       below: MATRA_AA_BINDI is the ਾਂ of ਹਾਂ, which is a vowel sign and the
       bindi over it.

       Not every one of these is drawn as a glyph by every font - a font that
       spells one of them out carries no code for that token, and the lexer
       of a font is built over the tokens it does carry
    '''
    def __init__(self):
        BaseLang.__init__(self)
        punjabiUnicode = PunjabiUnicode()
        uMap   = punjabiUnicode.tokendict
        virama = uMap['VIRAMA']

        self.tokendict = {}

        for tokenName in PAIRI_TOKENS:
            self.tokendict['PAIRI_' + tokenName] = virama + uMap[tokenName]

        # a consonant with ੍ਹ, ੍ਰ or ੍ਵ under it. Only the letters are
        # bound this way, not the consonants a nukta is written under - ਸ਼੍ਰ
        # is no cluster of punjabi
        for tokenName in CONSONANT_TOKENS:
            if len(uMap[tokenName]) != 1:
                continue
            for pairiName in CLUSTER_PAIRI_TOKENS:
                self.tokendict[tokenName + '_' + pairiName] = \
                        uMap[tokenName] + virama + uMap[pairiName]

        for tokenName in CONSONANT_TOKENS:
            self.tokendict['DEAD_' + tokenName] = uMap[tokenName] + virama

        # the vowel signs that a font draws in one glyph with the bindi over
        # them. Neither of the reordering passes moves the two apart, so the
        # tokenizer hands the two tokens on in place of the glyph
        for signName in BINDI_SIGN_TOKENS:
            self.conjunct_tokens[signName + '_BINDI'] = [signName, 'BINDI']

class Asees(BaseLang):
    '''the tokens that the text of an Asees document carries beyond the
       gurmukhi of it. The digit keys of that font draw the western digits
       rather than the gurmukhi ones, and the Punjab Government Gazette
       numbers its notifications and its tables with them
    '''
    def __init__(self):
        BaseLang.__init__(self)

        digitnames = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', \
                      'SEVEN', 'EIGHT', 'NINE']
        for digit, name in enumerate(digitnames):
            self.tokendict['ASCII_' + name] = '%d' % digit
