import re
import types

from indic2unicode.langs import punjabi
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class RaaviFont(BaseFont):
    '''the gurmukhi of a pdf that Microsoft Print To PDF made, which embeds
       every font as a CIDFont+Fn of its own - the test document is the
       Punjab Government Gazette extraordinary of 30 September 2025 that
       carries the punjabi translations of the Punjab Education Development
       Act, 1998 and the Punjab Gau Sewa Commission Act, 2014, and CIDFont+F7
       sets the headings in the margin of its sections. The font behind that
       name is Raavi, the unicode gurmukhi of Windows, embedded as a subset
       that keeps Raavi's own glyph ids, its cmap and its GSUB. The body of
       those acts is set in CIDFont+F4, which is Asees - see
       fonts/punjabi/asees.py.

       The producer writes a ToUnicode map out of the cmap of the font, so
       every glyph that the cmap names is spelled right. What the map has no
       entry for is every glyph the shaper made out of more than one
       character or chose in place of another one, and an extractor that
       falls back on the cid of such a glyph, e.g. pymupdf, hands out the
       character of that cid - the glyph id in Raavi. So ਨਾਂ comes out as
       'ਨ\\x7f', ਮੈਂਬਰ as 'ਮ\\x82ਬਰ' and ਕਮਿਸ਼ਨ as 'ਕਿਮ©ਨ', 127 being ਾਂ, 130
       ੈਂ and 169 the ਸ਼ that is typed as ਸ and the nukta. Those glyphs are
       tokens of this font. An extractor that drops such a glyph, e.g.
       pdftotext, loses them before the converter ever sees the text.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       ਿ MATRA_I is drawn in front of the letter it belongs to and the text
       is in the order the glyphs are drawn, so ਪਰਿਭਾਸ਼ਾਵਾਂ comes out as
       ਪਿਰਭਾਸ਼ਾਵ\\x7f and ਨਿਯਮ as ਿਨਯਮ. It waits for its letter and stays
       behind the marks drawn under that letter - the nukta, a pairi, ੵ -
       and it is drawn in front of a whole cluster, so it waits past a dead
       consonant at the head of one as well: ਸ੍ਥਿਤੀ is drawn ਿ, ਸ, ੍ਥ, ਤ, ੀ.
       Everything else is drawn in the order unicode writes it.

       WHERE THE READINGS COME FROM

       The GSUB of the embedded font says what the shaper makes every glyph
       out of, and cidglyphs below is what it says for the glyphs that draw
       the letters and the signs of punjabi: a vowel sign with the bindi
       over it, a vowel with the bindi or the addak on it, the pairin, a
       dead consonant, and the ੇ, ੈ and ੋ that Raavi draws a little further
       to the left over ਠ and ਨ, so that ਨੇ is 'ਨĂ'. The test document draws
       seven of them - 127 ਾਂ 23 times, 169 ਸ਼ 20, 130 ੈਂ 8, 131 ੋਂ 2, 137
       ੍ਹ 2, 135 ੍ਰ and 258 ੇ once each. The rest were checked by shaping
       113 words with HarfBuzz over the embedded font itself, writing out
       the glyphs it drew the way the pdf would spell them and reading them
       back through this converter, which gives every one of the words back.

       What the GSUB draws and this converter leaves out is the nukta under
       the letters that punjabi does not write with one - ਕ਼, ਨ਼, ਰ਼ - and
       under a vowel, and a virama behind a pairi. Such a glyph comes out as
       the character of its number, or is reported and dropped where that
       is no text character.

       The dead consonants and the glyphs from 252 on come out as latin
       letters and signs - ਰਾਜ੍ is 'ਰਾ²' - and the two below 127, the ੰ and
       the ੱ drawn behind a vowel sign, as 'z' and '{'. Word sets the latin
       of a document in a latin font, so a run of Raavi carries none of
       those as text; one that was typed in Raavi all the same would be
       read as the glyph of that number.

       WHAT THE EXTRACTOR ADDS AND LEAVES OUT

       The producer places a mark that Raavi draws to the left of where the
       pen stands by moving the pen back and forward again around it, and
       pymupdf puts a space where the pen moves forward: ਜਿਨ੍ਹਾਂ comes out
       as 'ਿਜਨ\\x89 \\x7f' and ਨੇਕਨੀਤੀ as 'ਨĂ ਕਨੀਤੀ'. No word begins with a
       mark, so a space in front of one is dropped here and ਜਿਨ੍ਹਾਂ comes
       out whole. A space in front of a letter is what a space between two
       words looks like as well - ਨੇ is a word of its own as often as it is
       the start of one - so ਨੇਕਨੀਤੀ comes out as ਨੇ ਕਨੀਤੀ. pymupdf's
       TEXT_INHIBIT_SPACES leaves that space out, but it leaves out the
       space between ਮੈਂਬਰਾਂ and ਦੀ as well, which the pdf draws as a gap
       and not as a glyph.

       The pdf draws no space at all between some words of the headings,
       and pymupdf puts none there either, so ਦੇ ਅਹੁਦੇ ਦੀ ਅਉਧ comes out as
       ਦੇਅਹੁਦੇਦੀਅਉਧ. Nothing in the text says where those words part.

       WHAT THIS WAS CHECKED AGAINST

       A tesseract OCR of the same pages. Of the 211 words of gurmukhi this
       converter writes for the test document, 184 are read back word for
       word by the OCR. Of the 27 that are not, 10 are the OCR reading ਣ as
       ਈ, ਏ or ਛ - ਹੋਣਾ as ਹੋਈ, ਬਣਾਉਣ as ਬਈਉਇ - and 11 are headings the OCR
       drops or garbles, ਪ੍ਰਯੋਜਨ ਜਿਨ੍ਹਾਂ ਲਈ ਫ਼ੰਡ among them, which were read
       off the rendered page instead and are what the page shows. The
       other 6 are the four places where the pdf draws no space between
       two words and the two halves of ਨੇਕਨੀਤੀ, see above.
    '''
    # the string the pdf hands each glyph of the font that its map has an
    # entry for, against the token that glyph draws. The map spells every
    # one of them right, so this is the gurmukhi block itself. A character
    # that is not here - the latin, the digits and the punctuation of the
    # text - is text and reaches the output through the literal path of
    # t_error, see BaseFont.is_text_char
    charstrings = { \
        # VOWELS, and the carriers ੲ and ੳ that a vowel is drawn on        \
        'A'    : 'ਅ', 'AA'   : 'ਆ', 'I'    : 'ਇ', 'II'   : 'ਈ', \
        'U'    : 'ਉ', 'UU'   : 'ਊ', 'EE'   : 'ਏ', 'AI'   : 'ਐ', \
        'OO'   : 'ਓ', 'AU'   : 'ਔ', 'IRI'  : 'ੲ', 'URA'  : 'ੳ', \
                                                              \
        # CONSONANTS                                                       \
        'KA'   : 'ਕ', 'KHA'  : 'ਖ', 'GA'   : 'ਗ', 'GHA'  : 'ਘ', \
        'NGA'  : 'ਙ', 'CA'   : 'ਚ', 'CHA'  : 'ਛ', 'JA'   : 'ਜ', \
        'JHA'  : 'ਝ', 'NYA'  : 'ਞ', 'TTA'  : 'ਟ', 'TTHA' : 'ਠ', \
        'DDA'  : 'ਡ', 'DDHA' : 'ਢ', 'NNA'  : 'ਣ', 'TA'   : 'ਤ', \
        'THA'  : 'ਥ', 'DA'   : 'ਦ', 'DHA'  : 'ਧ', 'NA'   : 'ਨ', \
        'PA'   : 'ਪ', 'PHA'  : 'ਫ', 'BA'   : 'ਬ', 'BHA'  : 'ਭ', \
        'MA'   : 'ਮ', 'YA'   : 'ਯ', 'RA'   : 'ਰ', 'LA'   : 'ਲ', \
        'VA'   : 'ਵ', 'SA'   : 'ਸ', 'HA'   : 'ਹ', 'RRA'  : 'ੜ', \
                                                              \
        # the letters that carry a nukta, which the map spells as the      \
        # characters of their own that unicode has for them                \
        'LLA'  : 'ਲ਼', 'SHA'  : 'ਸ਼', 'KHHA' : 'ਖ਼', 'GHHA' : 'ਗ਼', \
        'ZA'   : 'ਜ਼', 'FA'   : 'ਫ਼', \
                                  \
        # MATRAS                                                           \
        'MATRA_AA' : 'ਾ', 'MATRA_I'  : 'ਿ', 'MATRA_II' : 'ੀ', \
        'MATRA_U'  : 'ੁ', 'MATRA_UU' : 'ੂ', 'MATRA_EE' : 'ੇ', \
        'MATRA_AI' : 'ੈ', 'MATRA_OO' : 'ੋ', 'MATRA_AU' : 'ੌ', \
                                                            \
        # SIGNS                                                            \
        'ADAK_BINDI' : 'ਁ', 'BINDI'  : 'ਂ', 'VISARGA' : 'ਃ', \
        'NUKTA'      : '਼', 'VIRAMA' : '੍', 'UDAAT'   : 'ੑ', \
        'TIPPI'      : 'ੰ', 'ADDAK'  : 'ੱ', 'YAKASH'  : 'ੵ', \
        'EK_ONKAR'   : 'ੴ', \
                           \
        # DIGITS                                                           \
        'ZERO' : '੦', 'ONE'  : '੧', 'TWO'   : '੨', 'THREE' : '੩', \
        'FOUR' : '੪', 'FIVE' : '੫', 'SIX'   : '੬', 'SEVEN' : '੭', \
        'EIGHT': '੮', 'NINE' : '੯', \
                                    \
        # PUNCTUATIONS                                                     \
        'DANDA'     : '।', 'DOUBLE_DANDA' : '॥', 'SPACE' : ' ', \
        'NEWLINE'   : '\n', 'CARRIAGERET' : '\r', 'TAB'  : '\t', \
        'FORMFEED'  : '\f', \
    }

    # the glyphs that the shaper made out of the characters of the text and
    # that the map has no entry for, by their glyph id in Raavi - which is
    # their cid in the pdf, and the character an extractor that falls back
    # on the cid hands out for them. What each of them draws is what the
    # GSUB of the font makes it out of
    cidglyphs = { \
        # the alternate ੰ and ੱ that are drawn behind ੇ, ੈ, ੋ and ੌ - and ੱ \
        # behind ੀ, ਈ, ਐ and the ਿ of ਨਿ and ਠਿ as well                     \
        122 : 'TIPPI', 123 : 'ADDAK', \
                                      \
        # a vowel sign with the bindi over it, see the conjunct_tokens of  \
        # langs/punjabi.py, and ੌ with the addak over it                   \
        127 : 'MATRA_AA_BINDI', 128 : 'MATRA_II_BINDI', \
        129 : 'MATRA_EE_BINDI', 130 : 'MATRA_AI_BINDI', \
        131 : 'MATRA_OO_BINDI', 132 : 'MATRA_AU_BINDI', \
        133 : 'MATRA_AU_ADDAK', \
                                \
        # the pairin, drawn under the letter they are bound to             \
        135 : 'PAIRI_RA',   136 : 'PAIRI_VA',   137 : 'PAIRI_HA', \
        138 : 'PAIRI_YA',   267 : 'PAIRI_GA',   268 : 'PAIRI_CA', \
        269 : 'PAIRI_TTA',  270 : 'PAIRI_TTHA', 271 : 'PAIRI_TA', \
        272 : 'PAIRI_THA',  273 : 'PAIRI_DA',   274 : 'PAIRI_NA', \
                                                                  \
        # a vowel with the bindi or the addak drawn on it                  \
        139 : 'U_BINDI', 140 : 'UU_BINDI', 141 : 'OO_BINDI', \
        142 : 'U_ADDAK', 143 : 'UU_ADDAK', 144 : 'OO_ADDAK', \
                                                             \
        # ਸ਼ typed as ਸ and the nukta rather than as the character of it    \
        169 : 'SHA', \
                     \
        # a dead consonant, the letter with the virama drawn under it      \
        171 : 'DEAD_KA',   172 : 'DEAD_KHA',  173 : 'DEAD_GA',   \
        174 : 'DEAD_GHA',  175 : 'DEAD_NGA',  176 : 'DEAD_CA',   \
        177 : 'DEAD_CHA',  178 : 'DEAD_JA',   179 : 'DEAD_JHA',  \
        180 : 'DEAD_NYA',  181 : 'DEAD_TTA',  182 : 'DEAD_TTHA', \
        183 : 'DEAD_DDA',  184 : 'DEAD_DDHA', 185 : 'DEAD_NNA',  \
        186 : 'DEAD_TA',   187 : 'DEAD_THA',  188 : 'DEAD_DA',   \
        189 : 'DEAD_DHA',  190 : 'DEAD_NA',   191 : 'DEAD_PA',   \
        192 : 'DEAD_PHA',  193 : 'DEAD_BA',   194 : 'DEAD_BHA',  \
        195 : 'DEAD_MA',   196 : 'DEAD_YA',   197 : 'DEAD_RA',   \
        198 : 'DEAD_LA',   200 : 'DEAD_VA',   201 : 'DEAD_SHA',  \
        202 : 'DEAD_SA',   203 : 'DEAD_HA',   205 : 'DEAD_KHHA', \
        206 : 'DEAD_GHHA', 211 : 'DEAD_ZA',   216 : 'DEAD_RRA',  \
        225 : 'DEAD_FA',   231 : 'DEAD_LLA',  233 : 'DEAD_SHA',  \
                                                                 \
        # a pairi with ੁ or ੂ hung under it                               \
        252 : 'PAIRI_RA_MATRA_U', 255 : 'PAIRI_RA_MATRA_UU', \
        253 : 'PAIRI_VA_MATRA_U', 256 : 'PAIRI_VA_MATRA_UU', \
        254 : 'PAIRI_HA_MATRA_U', 257 : 'PAIRI_HA_MATRA_UU', \
                                                             \
        # the alternate ੇ, ੈ and ੋ that are drawn over ਠ and ਨ, alone and   \
        # with the bindi, and the ੌ and ੱ that are drawn over them          \
        258 : 'MATRA_EE', 259 : 'MATRA_AI', 260 : 'MATRA_OO', \
        261 : 'MATRA_EE_BINDI', 262 : 'MATRA_AI_BINDI', \
        263 : 'MATRA_OO_BINDI', 264 : 'MATRA_AU_ADDAK', \
    }

    # the marks that are drawn under a letter, which ਿ stays behind while it
    # waits for the letter they belong to
    UNDER_MARKS = ['NUKTA', 'YAKASH', 'UDAAT'] + \
                  ['PAIRI_' + name for name in punjabi.PAIRI_TOKENS]

    # the signs that are written on a letter and never begin a word, so a
    # space in front of one is not text - see the class comment. ਿ is not
    # among them, being drawn in front of its letter
    COMBINING_MARKS = ['MATRA_AA', 'MATRA_II', 'MATRA_U', 'MATRA_UU', \
                       'MATRA_EE', 'MATRA_AI', 'MATRA_OO', 'MATRA_AU', \
                       'ADAK_BINDI', 'BINDI', 'TIPPI', 'ADDAK', 'VIRAMA'] + \
                      UNDER_MARKS

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(punjabi.PunjabiUnicode())
        self.langobjs.append(punjabi.Conjuncts())
        self.langobjs.append(punjabi.Raavi())

        self.lexer = self.get_lexer()

        # ਿ is drawn in front of the letter it belongs to
        self.waitdict = {'MATRA_I': 1}

        # a mark under the letter belongs to the letter ਿ has already
        # passed, so ਿ stays behind it
        self.waitover = set(self.UNDER_MARKS)

        # a dead consonant is the head of the cluster that ਿ is drawn in
        # front of, so ਿ is emitted behind the letter that ends it
        self.halftokens = set([tokenName for tokenName in \
                               self.get_all_tokens() \
                               if tokenName.startswith('DEAD_')])

        self.composeTokens = self.get_compose_tokens()

    def get_all_tokens(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())
        return tokens

    def get_compose_tokens(self):
        '''the space an extractor puts in front of a mark, and the vowels that
           the text carries as a carrier and a vowel sign - see the class
           comment'''
        composeTokens = {}

        for markName in self.COMBINING_MARKS:
            composeTokens[('SPACE', markName)] = [markName]

        # ਿ is drawn in front of the ੲ it sits on, the other vowel signs
        # behind their carrier
        for pair, vowel in punjabi.VOWEL_COMPOSITIONS.items():
            if pair[1] == 'MATRA_I':
                pair = (pair[1], pair[0])
            composeTokens[pair] = [vowel]

        return composeTokens

    def get_lexer(self):
        tokens = self.get_all_tokens()

        # token strings are regular expressions for ply, so the strings have
        # to be escaped. The glyphs of one token are joined into one pattern
        glyphs = {}
        for tokenName, charstr in self.charstrings.items():
            glyphs.setdefault(tokenName, []).append(charstr)

        for glyphid, tokenName in self.cidglyphs.items():
            glyphs.setdefault(tokenName, []).append(chr(glyphid))

        rules = {}
        for tokenName, glyphstrs in glyphs.items():
            rules['t_' + tokenName] = '|'.join([re.escape(glyphstr) \
                                                for glyphstr in glyphstrs])

        def t_error(t):
            # a character that is not in the tables above is one the font
            # draws as itself - a digit, the punctuation - which is text and
            # comes through as it is
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
