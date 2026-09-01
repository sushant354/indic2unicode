from .baselang import BaseLang

# the consonants of tamil, in the order the script itself lists them: the
# eighteen letters of tamil proper (vallinam, mellinam, idaiyinam) and then
# the five grantha letters it borrows to write sanskrit and foreign names.
# The order is the one the 8 bit fonts lay their glyph blocks out in, so
# fonts/tamil/tamelango.py reads a block of theirs straight off this list
CONSONANT_TOKENS = [ \
    'KA', 'NGA', 'CA', 'NYA', 'TTA', 'NNA', 'TA', 'NA', 'PA', 'MA', \
    'YA', 'RA', 'LA', 'VA', 'LLLA', 'LLA', 'RRA', 'NNNA', \
    'SA', 'SSA', 'JA', 'HA', 'KSSA', \
]

# the vowel signs a consonant is drawn together with, and the token each of
# those syllables gets in Conjuncts below. Only these four are ever one
# glyph: the rest of the signs are drawn beside the letter rather than into
# it, so they are glyphs - and tokens - of their own
LIGATURE_MATRAS = [ \
    ('I',  'MATRA_I'),  ('II', 'MATRA_II'), \
    ('U',  'MATRA_U'),  ('UU', 'MATRA_UU'), \
]

class TamilUnicode(BaseLang):
    '''the unicode values of the tamil script. The short and the long
       vowels are named the way unicode names them, so E is the short one
       and EE the long one, and the same for O and OO.

       Tamil writes no half forms and no conjuncts: a consonant that
       carries no vowel is that letter and a pulli (the virama), and a
       cluster is simply one of those followed by the next letter. The one
       exception is grantha KSSA, which is written out of three characters
       and which every font draws as a single glyph, so it is one token here
    '''
    def __init__(self):
        BaseLang.__init__(self)
        self.tokendict = { \
          # VOWELS                   \
          'A'           : 'அ', \
          'AA'          : 'ஆ', \
          'I'           : 'இ', \
          'II'          : 'ஈ', \
          'U'           : 'உ', \
          'UU'          : 'ஊ', \
          'E'           : 'எ', \
          'EE'          : 'ஏ', \
          'AI'          : 'ஐ', \
          'O'           : 'ஒ', \
          'OO'          : 'ஓ', \
          'AU'          : 'ஔ', \
                                     \
          # the aytham, which is a letter of its own in tamil rather than \
          # a sign written on another one                                \
          'AYTHAM'      : 'ஃ', \
                                     \
          # CONSONANTS. vallinam     \
          'KA'          : 'க', \
          'CA'          : 'ச', \
          'TTA'         : 'ட', \
          'TA'          : 'த', \
          'PA'          : 'ப', \
          'RRA'         : 'ற', \
                                     \
          # mellinam                 \
          'NGA'         : 'ங', \
          'NYA'         : 'ஞ', \
          'NNA'         : 'ண', \
          'NA'          : 'ந', \
          'MA'          : 'ம', \
          'NNNA'        : 'ன', \
                                     \
          # idaiyinam                \
          'YA'          : 'ய', \
          'RA'          : 'ர', \
          'LA'          : 'ல', \
          'VA'          : 'வ', \
          'LLLA'        : 'ழ', \
          'LLA'         : 'ள', \
                                     \
          # the grantha letters, which tamil borrows to write sanskrit    \
          # and foreign names. KSSA is three characters and SHRI four,    \
          # and a font draws each of them as one glyph                    \
          'SA'          : 'ஸ', \
          'SSA'         : 'ஷ', \
          'SHA'         : 'ஶ', \
          'JA'          : 'ஜ', \
          'HA'          : 'ஹ', \
          'KSSA'        : 'க்ஷ', \
          'SHRI'        : 'ஸ்ரீ', \
                                     \
          # MATRAS. the vowel signs. ஒ, ஓ and ஔ are written with two of  \
          # them, and a font draws each of those two halves as a glyph of \
          # its own - see the composition rules in the font module        \
          'MATRA_AA'         : 'ா', \
          'MATRA_I'          : 'ி', \
          'MATRA_II'         : 'ீ', \
          'MATRA_U'          : 'ு', \
          'MATRA_UU'         : 'ூ', \
          'MATRA_E'          : 'ெ', \
          'MATRA_EE'         : 'ே', \
          'MATRA_AI'         : 'ை', \
          'MATRA_O'          : 'ொ', \
          'MATRA_OO'         : 'ோ', \
          'MATRA_AU'         : 'ௌ', \
                                          \
          # the tail of ஔ and of the vowel sign of it, which the fonts   \
          # draw as a glyph of its own                                   \
          'AU_LENGTH_MARK'   : 'ௗ', \
                                          \
          # SIGNS. the pulli is tamil's virama - it says that the letter \
          # it sits on carries no vowel                                  \
          'PULLI'            : '்', \
                                          \
          # DIGITS. the tamil digits, which a document sets in the same  \
          # font as the latin ones - see fonts/tamil/tamelango.py, whose \
          # font draws the latin digits on the digit keys                \
          'ZERO'        : '௦', \
          'ONE'         : '௧', \
          'TWO'         : '௨', \
          'THREE'       : '௩', \
          'FOUR'        : '௪', \
          'FIVE'        : '௫', \
          'SIX'         : '௬', \
          'SEVEN'       : '௭', \
          'EIGHT'       : '௮', \
          'NINE'        : '௯', \
          'TEN'         : '௰', \
          'HUNDRED'     : '௱', \
          'THOUSAND'    : '௲', \
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
        }

class Conjuncts(BaseLang):
    '''the syllables that a tamil font draws as a single glyph, which is
       every consonant with a pulli on it and every consonant that one of
       the four vowel signs written into it is drawn with.

       Tamil has no conjunct consonants, so a glyph of this kind is always
       one letter and one sign, and the token of it is the letter's token
       and the sign's - KA_PULLI is க் and KA_I is கி. They are tokens
       rather than pairs of tokens because a font draws them as one glyph
       and because the vowel signs that are written in front of a letter
       have to jump over the whole of it: a ெ in front of the one glyph
       of ன் belongs behind that letter and its pulli, not between them

       Not every one of these is drawn as a glyph by every font - a font
       that spells one of them out of a letter and a sign simply carries no
       code for that token, see fonts/tamil/tamelango.py
    '''
    def __init__(self):
        BaseLang.__init__(self)
        tamUnicode = TamilUnicode()
        uMap   = tamUnicode.tokendict
        pulli  = uMap['PULLI']

        self.tokendict = {}
        for tokenName in CONSONANT_TOKENS:
            consonant = uMap[tokenName]
            self.tokendict[tokenName + '_PULLI'] = consonant + pulli
            for suffix, matraToken in LIGATURE_MATRAS:
                self.tokendict[tokenName + '_' + suffix] = \
                        consonant + uMap[matraToken]
