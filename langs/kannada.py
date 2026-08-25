import string

from .baselang import BaseLang

# The arkavattu - the ra of a cluster, written as a mark on top of the
# consonant that follows it - is spelled 'ರ್' like a dead ra, and a font
# draws the two with different glyphs. A pdf whose ToUnicode map has been
# repaired by tools/fix_tounicode.py keeps them apart by writing this after
# the arkavattu: unicode writes a virama and a zero width joiner for the
# half form of a consonant, which is what that glyph draws, so the mark says
# what the glyph is rather than standing for anything of its own and is
# dropped again once the syllable has been put in order. Without it a
# converter has to guess, as fonts/kannada/tunga.py does
ARKAVATTU_MARK = '\u200d'

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

class Nudi(BaseLang):
    '''the tokens that the text of a Nudi document carries beyond the
       kannada of it, and the glyphs of the font that draw more than one
       character or less than a whole one.

       Nudi is an ascii font: every glyph of it sits on a key of the
       keyboard and the text of a pdf that is set in it is the sequence of
       keys the typist pressed, so what the glyphs draw is a syllable of
       kannada and what they say is latin. The font has a glyph for the
       consonant, one for every vowel sign of it and one for every vattu,
       and a syllable is spelled out of those in the order they are drawn.

       Three kinds of glyph are neither a character of their own nor a
       whole one:

       1. INHERENT_A, the glyph a consonant that carries the vowel a is
          written with. It draws the head stroke of the consonant it
          follows, which is already part of the letter in unicode, so it
          stands for no character at all - 'PÀ' is ಕ and 'Pï' is ಕ್.
       2. SPACER, a glyph of no width that the typist puts between two
          vattus that would otherwise be drawn into each other. It stands
          for no character either, ನಿರ್ಲಕ್ಷ್ಯತೆ being typed '¤®ðPÀëöåvÉ'.
       3. ASPIRATION and ASPIRATION_I, the stroke that turns ಪ into ಫ, ಬ
          into ಭ and ದ into ಧ. The font draws it as a glyph of its own on
          top of the letter, so ಫ is typed '¥s' and ಫಿ is '¦ü', and the
          two are put back together in fonts/kannada/nudi.py

       The conjunct tokens below are the other way round: one glyph of the
       font draws a whole syllable. Every consonant that changes shape when
       the vowel sign i replaces its head stroke has a glyph of its own for
       that syllable, so ಕಿ is one glyph and not two, and ಮ and ಯ are drawn
       out of pieces that are shared with other letters - ಮ is the ವ glyph
       and the tail that also draws the vowel sign u, ಯ is the anusvara
       glyph, a stem and that same tail
    '''
    def __init__(self):
        BaseLang.__init__(self)

        self.tokendict = {\
            # the two glyphs that draw a part of a letter rather than a  \
            # letter, see 1. and 2. above                                \
            'INHERENT_A'       : '',         \
            'SPACER'           : '',         \
                                             \
            # no key of the font draws this one. It is put in behind a     \
            # virama that a consonant follows, see fonts/kannada/nudi.py   \
            'ZWNJ'             : '\u200c',   \
                                             \
            # the aspiration stroke, see 3. above. It is put back together \
            # with the letter it sits on in fonts/kannada/nudi.py and is   \
            # no character of its own if it ever stands alone              \
            'ASPIRATION'       : '',         \
            'ASPIRATION_I'     : '',         \
                                             \
            # punctuation of the document that has no kannada token \
            'AMPERSAND'        : '&',        \
            'APOSTROPHE'       : "'",        \
            'UNDERSCORE'       : '_',        \
            'LSQUOTE'          : '‘',   \
            'RSQUOTE'          : '’',   \
            'LDQUOTE'          : '“',   \
            'RDQUOTE'          : '”',   \
            # pdftotext ends a page with a form feed, which is text of the \
            # document rather than a glyph of the font                     \
            'FORMFEED'         : '\f',       \
        }

        # the latin digits, which the roman weight of Nudi keeps on the
        # digit keys. The kannada weight draws the kannada digits there
        # instead, see fonts/kannada/nudi.py
        digitnames = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', \
                      'SEVEN', 'EIGHT', 'NINE']
        for digit, name in enumerate(digitnames):
            self.tokendict['ASCII_' + name] = '%d' % digit

        # the glyphs that draw a consonant and the vowel sign i of it in
        # one, i.e. every consonant whose head stroke that sign replaces.
        # ಣ is not one of them: it keeps its head stroke and the sign is a
        # glyph of its own there, ಣಿ being 'tÂ'
        ivowels = ['KA', 'KHA', 'GA', 'GHA', 'CA', 'CHA', 'JA', 'TTA',    \
                   'DDA', 'TA', 'THA', 'DA', 'NA', 'PA', 'BA', 'MA', 'YA', \
                   'RA', 'LA', 'VA', 'SHA', 'SSA', 'SA', 'HA', 'LLA']

        self.conjunct_tokens = {}
        for consonant in ivowels:
            self.conjunct_tokens[consonant + '_I'] = [consonant, 'MATRA_I']

        # ma and ya are drawn out of pieces, and the piece that ends them
        # is the same glyph that draws the vowel sign u. A vowel sign that
        # is drawn in front of that piece therefore sits inside the letter
        # rather than behind it, so ಮೆ is one token here and not two. The
        # second half of a two part vowel sign follows as it always does,
        # ಮೇ being 'ªÉÄ' and the length mark
        for consonant in ['MA', 'YA']:
            self.conjunct_tokens[consonant + '_E'] = [consonant, 'MATRA_E']
            self.conjunct_tokens[consonant + '_O'] = [consonant, 'MATRA_E', \
                                                      'MATRA_UU']

class Aklite(BaseLang):
    '''the tokens that the text of an Aklite document carries beyond the
       kannada of it.

       Aklite is an 8-bit display font like Nudi, so the head stroke of a
       consonant that carries the vowel a is a glyph of its own there too -
       it draws a part of a letter and stands for no character, ಕ being the
       ka glyph and that stroke while ಟ, which kannada writes no head
       stroke on, is the letter alone. See fonts/kannada/aklite.py
    '''
    def __init__(self):
        BaseLang.__init__(self)

        self.tokendict = {\
            'INHERENT_A'       : '',         \
        }
