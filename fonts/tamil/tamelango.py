import re
import types

from indic2unicode.langs import tamil
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class TamElango(BaseFont):
    '''The text of a pdf that is set in TAM_ELANGO_Panchali, the tamil font
       the Tamil Nadu gazette is set in - 3,166 of the 8,248 documents of
       that corpus draw text in it - and in the rest of the TAM_ELANGO
       family, which share its encoding.

       It is an 8-bit font: every glyph of it sits on a byte, the pdf calls
       it a TrueType font with WinAnsiEncoding and names its glyphs after
       the latin characters that live on those bytes, so what an extractor
       hands out is cp1252 and not tamil at all - «ðÏó£†Cèœ is
       பேரூராட்சிகள். The bytes are the TAM (tamil monolingual) layout,
       which keeps the digits and the punctuation of ascii where they are
       and puts tamil on the letter positions and on the whole upper half.

       WHAT THE GLYPHS ARE

       Tamil writes no conjunct consonants, so an 8-bit font needs a glyph
       for each of

         - the vowels and the aytham
         - the eighteen consonants and the five grantha letters
         - each of those letters with a pulli on it
         - each of them with the vowel sign i, ii, u or uu written into it,
           which is one glyph because the sign changes the letter's shape
         - the vowel signs aa, e, ee and ai, which are drawn beside the
           letter rather than into it and so are glyphs of their own

       and it lays them out one block per row of that list, each block in
       the order langs/tamil.CONSONANT_TOKENS gives. The blocks are broken
       wherever a byte was wanted for punctuation - the -ii block runs
       57..5A and picks up again at 61, leaving [ \\ ] ^ _ ` where ascii has
       them - which is why the table below is written out byte by byte
       rather than generated from the blocks.

       Every reading in it was established from the font itself: the glyphs
       were rendered out of the embedded subsets of the corpus (no one
       document carries them all - the readings here are the union over
       ~2,800 of them) and read against a tesseract -l tam OCR of the pages
       that draw them.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       The vowel signs e, ee and ai are drawn in front of the consonant
       they belong to and unicode writes them behind it, so each of them
       waits for one token and is emitted after it - ªê¡¬ù is ெ ச ன் ை ன
       and சென்னை. The signs o and oo are drawn in two halves with
       the letter between them, so they arrive as a ெ or a ே in front and
       a ா behind, and are put back together by composeTokens once the
       front half has jumped - ªî£Nô£÷˜ is ெ த ா ழி ல ா ள ர் and
       தொழிலாளர்.

       WHAT IS NOT KNOWN

       The font's cmap names 223 bytes and only 162 of them are ever drawn
       in the ~2,800 documents this was read from, so 61 carry a glyph that
       nothing in the corpus says anything about. Two of them matter: ஔ and
       the vowel sign ௌ, which a font of this family draws out of a ெ and a
       length mark of its own the way it draws ொ out of a ெ and a ா. No
       document draws that mark, so which byte carries it is unknown and
       neither ஔ nor ௌ is in the table - when the byte turns up, it is that
       one code and the two composition rules that go with it. A byte
       outside the table that is a character in its own right (a digit, the
       ascii punctuation) comes through as it is and the rest is reported
       and dropped: over 336,073 characters of 400 documents that is 24
       characters, all of them control codes an extractor put in itself.

       ர AND ா ARE THE SAME STROKE

       Some of these documents write the letter ர with the vowel sign ா,
       the two being drawn very nearly alike, and then put the sign that
       belongs on the ர behind it: ªðò£¢ is ெ ப ய ா ் for பெயர் and
       H£¤¬õ„ is பி ா ி ை வ ச் for பிரிவைச். A vowel sign can carry
       neither a pulli nor a second vowel sign, so a ா followed by one of
       them is not a ா at all, and composeTokens reads that pair back as
       the ர it was typed for. Nothing else in the text can be spelled that
       way, so this costs the documents that write ர properly nothing
    '''
    # the byte each glyph of the font sits on. The tokens are the ones
    # langs/tamil.py defines: a name of its own for a whole glyph, and
    # <CONSONANT>_PULLI / _I / _II / _U / _UU for the syllables that are one
    # glyph here. Only what needs decoding is listed - a byte the font
    # draws as itself (the digits, the ascii punctuation, the quotes at
    # 91..94) reaches the output through the literal path of t_error, see
    # BaseFont.is_text_char
    glyphcodes = { \
        # VOWELS and the aytham. No byte of these documents draws ஔ,     \
        # which is why there is none here - see the class comment         \
        'A'            : 0xDC, 'AA'          : 0xDD, \
        'I'            : 0xDE, 'II'          : 0xDF, \
        'U'            : 0xE0, 'UU'          : 0xE1, \
        'E'            : 0xE2, 'EE'          : 0xE3, \
        'AI'           : 0xE4,                       \
        'O'            : 0xE5, 'OO'          : 0xE6, \
        'AYTHAM'       : 0xE7,                       \
                                                     \
        # CONSONANTS, each of them the letter with its inherent vowel a.  \
        # The block runs unbroken from க to ஸ்ரீ, the grantha letters     \
        # after the tamil ones                                            \
        'KA'           : 0xE8, 'NGA'         : 0xE9, \
        'CA'           : 0xEA, 'NYA'         : 0xEB, \
        'TTA'          : 0xEC, 'NNA'         : 0xED, \
        'TA'           : 0xEE, 'NA'          : 0xEF, \
        'PA'           : 0xF0, 'MA'          : 0xF1, \
        'YA'           : 0xF2, 'RA'          : 0xF3, \
        'LA'           : 0xF4, 'VA'          : 0xF5, \
        'LLLA'         : 0xF6, 'LLA'         : 0xF7, \
        'RRA'          : 0xF8, 'NNNA'        : 0xF9, \
        'SA'           : 0xFA, 'SSA'         : 0xFB, \
        'JA'           : 0xFC, 'HA'          : 0xFD, \
        'KSSA'         : 0xFE, 'SHRI'        : 0xFF, \
                                                     \
        # THE PULLI FORMS. the letter with a pulli on it, i.e. carrying   \
        # no vowel. The block starts at 82, breaks at ய for the four      \
        # bytes cp1252 leaves undefined and the quotes and dashes that    \
        # follow them, and picks up again at ர. The grantha five sit in   \
        # front of it, at the end of the lower half                       \
        'SA_PULLI'     : 0x76, 'SSA_PULLI'   : 0x77, \
        'JA_PULLI'     : 0x78, 'HA_PULLI'    : 0x79, \
        'KSSA_PULLI'   : 0x7A,                       \
        'KA_PULLI'     : 0x82, 'NGA_PULLI'   : 0x83, \
        'CA_PULLI'     : 0x84, 'NYA_PULLI'   : 0x85, \
        'TTA_PULLI'    : 0x86, 'NNA_PULLI'   : 0x87, \
        'TA_PULLI'     : 0x88, 'NA_PULLI'    : 0x89, \
        'PA_PULLI'     : 0x8A, 'MA_PULLI'    : 0x8B, \
        'YA_PULLI'     : 0x8C,                       \
        'RA_PULLI'     : 0x98, 'LA_PULLI'    : 0x99, \
        'VA_PULLI'     : 0x9A, 'LLLA_PULLI'  : 0x9B, \
        'LLA_PULLI'    : 0x9C, 'RRA_PULLI'   : 0x9F, \
        'NNNA_PULLI'   : 0xA1,                       \
                                                     \
        # THE VOWEL SIGN I WRITTEN INTO THE LETTER. the block runs from   \
        # 41, where ascii has its capitals, and leaves ட out: ட is the    \
        # one letter whose i and ii forms are drawn somewhere else        \
        # entirely, at AE and AF                                          \
        'KA_I'         : 0x41, 'NGA_I'       : 0x42, \
        'CA_I'         : 0x43, 'NYA_I'       : 0x44, \
        'NNA_I'        : 0x45, 'TA_I'        : 0x46, \
        'NA_I'         : 0x47, 'PA_I'        : 0x48, \
        'MA_I'         : 0x49, 'YA_I'        : 0x4A, \
        'RA_I'         : 0x4B, 'LA_I'        : 0x4C, \
        'VA_I'         : 0x4D, 'LLLA_I'      : 0x4E, \
        'LLA_I'        : 0x4F, 'RRA_I'       : 0x50, \
        'NNNA_I'       : 0x51, 'SA_I'        : 0x52, \
        'SSA_I'        : 0x53, 'JA_I'        : 0x54, \
        'HA_I'         : 0x55, 'KSSA_I'      : 0x56, \
        'TTA_I'        : 0xAE,                       \
                                                     \
        # THE VOWEL SIGN II. the block carries straight on from the i     \
        # one at 57 and breaks for [ \\ ] ^ _ ` before finishing at 61     \
        'KA_II'        : 0x57, 'NGA_II'      : 0x58, \
        'CA_II'        : 0x59, 'NYA_II'      : 0x5A, \
        'NNA_II'       : 0x61, 'TA_II'       : 0x62, \
        'NA_II'        : 0x63, 'PA_II'       : 0x64, \
        'MA_II'        : 0x65, 'YA_II'       : 0x66, \
        'RA_II'        : 0x67, 'LA_II'       : 0x68, \
        'VA_II'        : 0x69, 'LLLA_II'     : 0x6A, \
        'LLA_II'       : 0x6B, 'RRA_II'      : 0x6C, \
        'NNNA_II'      : 0x6D, 'SA_II'       : 0x6E, \
        'SSA_II'       : 0x6F, 'JA_II'       : 0x70, \
        'HA_II'        : 0x71, 'KSSA_II'     : 0x72, \
        'TTA_II'       : 0xAF,                       \
                                                     \
        # THE VOWEL SIGN U. the eighteen tamil letters only - a grantha   \
        # letter takes the sign as a glyph of its own, at A7. The block   \
        # steps over B7, where the font keeps the middle dot              \
        'KA_U'         : 0xB0, 'NGA_U'       : 0xB1, \
        'CA_U'         : 0xB2, 'NYA_U'       : 0xB3, \
        'TTA_U'        : 0xB4, 'NNA_U'       : 0xB5, \
        'TA_U'         : 0xB6, 'NA_U'        : 0xB8, \
        'PA_U'         : 0xB9, 'MA_U'        : 0xBA, \
        'YA_U'         : 0xBB, 'RA_U'        : 0xBC, \
        'LA_U'         : 0xBD, 'VA_U'        : 0xBE, \
        'LLLA_U'       : 0xBF, 'LLA_U'       : 0xC0, \
        'RRA_U'        : 0xC1, 'NNNA_U'      : 0xC2, \
                                                     \
        # THE VOWEL SIGN UU. the same eighteen, stepping over CA and over \
        # D0..D5, where the font keeps a second set of quotes             \
        'KA_UU'        : 0xC3, 'NGA_UU'      : 0xC4, \
        'CA_UU'        : 0xC5, 'NYA_UU'      : 0xC6, \
        'TTA_UU'       : 0xC7, 'NNA_UU'      : 0xC8, \
        'TA_UU'        : 0xC9, 'NA_UU'       : 0xCB, \
        'PA_UU'        : 0xCC, 'MA_UU'       : 0xCD, \
        'YA_UU'        : 0xCE, 'RA_UU'       : 0xCF, \
        'LA_UU'        : 0xD6, 'VA_UU'       : 0xD7, \
        'LLLA_UU'      : 0xD8, 'LLA_UU'      : 0xD9, \
        'RRA_UU'       : 0xDA, 'NNNA_UU'     : 0xDB, \
                                                     \
        # THE SIGNS THAT ARE GLYPHS OF THEIR OWN. the pulli and the       \
        # signs i, ii, u and uu are here for the letters the font draws   \
        # no single glyph for - the grantha five, and the letters of a    \
        # document that writes ர as ா, see the class comment. aa, e, ee   \
        # and ai are drawn beside the letter by every font and are always \
        # these                                                           \
        'PULLI'        : 0xA2, \
        'MATRA_AA'     : 0xA3, 'MATRA_I'     : 0xA4, \
        'MATRA_II'     : 0xA6, 'MATRA_U'     : 0xA7, \
        'MATRA_UU'     : 0xA8,                       \
        'MATRA_E'      : 0xAA, 'MATRA_EE'    : 0xAB, \
        'MATRA_AI'     : 0xAC,                       \
                                                     \
        # the second set of quotes, which is the only punctuation of the  \
        # font that does not come out of the pdf as itself                \
        'LDQUOTE'      : 0xD2, 'RDQUOTE'     : 0xD3, \
        'LSQUOTE'      : 0xD4, 'RSQUOTE'     : 0xD5, \
    }

    # the pdf names the glyphs of this font after the characters of this
    # table, so this is what an extractor hands its text out as
    encoding = 'cp1252'

    # a second character a glyph reaches this converter as. A pdf that
    # carries the font a second time as a CID font names its glyphs in a
    # ToUnicode map of its own rather than by WinAnsiEncoding, and one
    # producer of these documents writes the byte B5 - the micro sign
    # U+00B5, which is where the font draws ணு - as U+03BC, the greek
    # small letter mu that unicode normalises the micro sign to. The
    # glyph is the same glyph, so the character is read as the byte's own
    glyph_aliases = { \
        'NNA_U' : '\u03bc', \
    }

    # the vowel signs that are drawn in front of the letter they belong to.
    # Each of them waits for one token - a letter is one token here however
    # many glyphs the font draws it in, which is what makes this a one
    # rather than a count of glyphs
    prefix_matras = ('MATRA_E', 'MATRA_EE', 'MATRA_AI')

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(tamil.TamilUnicode())
        self.langobjs.append(tamil.Conjuncts())

        self.glyphchars = self.get_glyph_chars()
        self.lexer      = self.get_lexer()

        self.waitdict = {}
        for tokenName in self.prefix_matras:
            self.waitdict[tokenName] = 1

        # the rules run in this order, and the ர ones come first: a ர that
        # was typed as a ா can stand behind the letter of a vowel sign
        # whose front half is waiting right in front of it, and reading
        # that ா as the back half of the sign would swallow it -
        # «ê£¢‰î is சேர்ந்த and not சோ்ந்த
        self.composeTokens = { \
            # a ா that carries a pulli or a second vowel sign is a ர      \
            # that was typed with the sign it is drawn alike, see the      \
            # class comment. Nothing else can be spelled this way: a vowel \
            # sign takes neither                                          \
            ('MATRA_AA', 'PULLI')          : ['RA', 'PULLI'],    \
            ('MATRA_AA', 'MATRA_I')        : ['RA', 'MATRA_I'],  \
            ('MATRA_AA', 'MATRA_II')       : ['RA', 'MATRA_II'], \
            ('MATRA_AA', 'MATRA_U')        : ['RA', 'MATRA_U'],  \
            ('MATRA_AA', 'MATRA_UU')       : ['RA', 'MATRA_UU'], \
                                                         \
            # the two halves of a vowel sign that is drawn with the letter \
            # between them, put back together once the front half has      \
            # jumped over that letter. ௌ is drawn the same way, out of a  \
            # ெ and the length mark, and has no rule here because no byte  \
            # of this font is known to draw that mark - see the class      \
            # comment                                                      \
            ('MATRA_E',  'MATRA_AA')       : 'MATRA_O',  \
            ('MATRA_EE', 'MATRA_AA')       : 'MATRA_OO', \
        }

    def get_glyph_chars(self):
        '''the characters each glyph of the font reaches this converter
           as: the byte it sits on read the way the pdf names that byte's
           glyph, and whatever else glyph_aliases says it also arrives as'''
        glyphchars = {}

        for tokenName, code in self.glyphcodes.items():
            try:
                char = bytes([code]).decode(self.encoding)
            except UnicodeDecodeError:
                self.logger.debug('%s leaves the byte 0x%02X of %s undefined',
                                  self.encoding, code, tokenName)
                continue

            glyphchars[tokenName] = char + self.glyph_aliases.get(tokenName, '')

        return glyphchars

    def to_unicode(self, data):
        '''the vowel signs have to be put where unicode wants them before
           the two halves of a two part sign can be joined, so the passes
           run the other way round here from BaseFont.to_unicode: a ெ and
           the ா of the same sign have the letter between them until the ெ
           has jumped over it'''
        tokentypes = self.tokenize(data)

        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        rules = {}
        for tokenName, chars in self.glyphchars.items():
            # token strings are regular expressions for ply, so the
            # characters have to be escaped. A glyph that reaches this
            # converter under more than one character - see glyph_aliases -
            # is one rule matching any of them
            rules['t_' + tokenName] = \
                    '|'.join([re.escape(char) for char in chars])

        def t_error(t):
            # a byte that is not in the table above is either one the font
            # draws as itself - a digit, the ascii punctuation, the quotes
            # at 91..94 - which is text and comes through as it is, or a
            # glyph of the font that these documents never draw and that
            # nothing can turn into a character
            char = t.value[0]

            if not self.is_text_char(char):
                self.report_error(t)
                t.lexer.skip(1)
                return None

            t.lexer.skip(1)
            t.type  = LITERAL
            t.value = char
            return t

        rules['t_error'] = t_error

        # only the tokens that the font has a glyph for
        rules['tokens'] = [tokenName for tokenName in tokens \
                                     if 't_' + tokenName in rules]

        # the rules are made in a loop, so they are handed to ply in an
        # object of their own rather than in the locals of this function.
        # ply looks up the module of that object
        rules['__module__'] = self.__class__.__module__
        return lex.lex(object = types.SimpleNamespace(**rules))
