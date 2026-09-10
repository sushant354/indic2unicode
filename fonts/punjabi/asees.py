import re
import types

from indic2unicode.langs import punjabi
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class Asees(BaseFont):
    '''Asees is the legacy 8 bit gurmukhi font that the Punjab Government
       Gazette sets the notifications of its district offices in - the test
       document is the one that lays out the wards of the gram panchayats of
       the Batala block of Gurdaspur. It is a font of the same kind as
       fonts/gujarati/krishna.py: the pdf embeds it as a simple TrueType
       font with WinAnsiEncoding and no ToUnicode map at all, so its text
       extracts as the characters of the bytes that were typed -
       ਦਫ਼ਤਰ, ਡਿਪਟੀ ਕਮਿਸ਼ਨਰ, ਗੁਰਦਾਸਪੁਰ comes out as
       "d|so, fvgNh efwPBo, r[odk;g[o" - and every one of those characters is
       a glyph of the font rather than a character of the script. Every byte
       this document draws is plain ascii.

       The pdf carries the font as two subsets. OMPIJG draws every page and
       VUGYDS the heading of the first one, and every byte both of them carry
       has the same outline in the two - but for M ਝ, which the second never
       draws and so carries an empty outline for.

       WHAT IS TYPED IN A DIFFERENT ORDER FROM UNICODE

       1. ਿ MATRA_I is drawn in front of the letter it belongs to and is
          typed there as well, so ਮਿਤੀ is typed as ਿ, ਮ, ਤ, ੀ. The marks that
          are drawn under the letter belong to it and ਿ stays behind them -
          the nukta, ੍ਰ, ੍ਹ and ੵ - so ਪੜ੍ਹਿਆ, which is typed as ਪ, ਿ, ੜ,
          ੍ਹ, ਅ, ਾ, comes out with the ਿ behind the ੍ਹ.
       2. ੰ TIPPI and ੱ ADDAK are drawn over a letter and ੁ and ੂ under it,
          so the order the two are typed in does not show on the page. The
          test document types a tippi in front of the vowel sign 17 times -
          ਕੁੰਨਣ as ਕ, ੰ, ੁ, ਨ, ਣ - and an addak 3 times, ਪੁੱਤਰ as ਪ, ੱ, ੁ,
          ਤ, ਰ where it is otherwise typed ਪ, ੁ, ੱ, ਤ, ਰ. Unicode writes the
          vowel sign of a letter in front of the tippi and the addak, and
          neither of them ever comes in front of a vowel sign in unicode
          gurmukhi, so the two are swapped back.

       Everything else is typed in the order unicode wants it. The bindi is
       typed behind the vowel sign it sits on - ਤੋਂ as ਤ, ੋ, ਂ - and the
       addak in front of the letter it doubles - ਵਿੱਚ as ਿ, ਵ, ੱ, ਚ.

       THE VOWELS

       Gurmukhi draws a vowel as one of three carriers with a vowel sign on
       it, and this font types it that way: ਆ as ਅ and ਾ, ਐ as ਅ and ੈ, ਇ as
       ਿ and ੲ, ਈ as ੲ and ੀ, ਏ as ੲ and ੇ, ਉ as ੳ and ੁ. Unicode has a
       character of its own for each of these, see the VOWEL_COMPOSITIONS of
       langs/punjabi.py, which this converter puts together before the
       reordering - ਿ comes in front of the ੲ it is drawn on, and read out of
       the text as ਇ it has nothing left to wait for. ਾਂ is one glyph of this
       font, K, and ਆਂ is typed as ਅ and that glyph.

       THE NUKTA

       ਸ਼ has a key of its own, P, and is typed as ਸ and the nukta dot as
       often - ਸ਼ਾਮਲ is typed as ਸ, ਼, ਾ, ਮ, ਲ. ਜ਼ is the same, with a key of
       its own in I and typed as ਜ and the dot in ਹਜ਼ਾਰਾ. Both ways come out
       as the letter and the nukta, which is how langs/punjabi.py writes the
       six letters that carry one.

       THE KEYS THAT DRAW PUNCTUATION

       This font draws the danda on the key of the full stop, and the full
       stop on H: ਐਸ.ਸੀ is typed as n?;H;h and ਕਰਦਾ ਹਾਂ। as "eodk jK.". Its
       keys of the quote marks draw ੋ and ੌ and the key of the colon draws
       ਯ, so the colon is typed on L, the semicolon on l, the hyphen on ^ and
       the slash on $. The digit keys draw the western digits.

       WHAT THE READINGS WERE CHECKED AGAINST

       The pdf embeds the font, so what every byte draws is in the document
       itself: each of the 72 bytes it draws was set in the font and read off
       its own outlines, and = was read against the ੵ of a unicode gurmukhi
       font. Of the 19509 words of gurmukhi this converter writes for the
       test document, 17197 are read back word for word by an OCR of the
       same pages.

       The 2312 that are not are the OCR's. 1729 of them have no word like
       them on the OCR's page at all - the OCR loses whole cells of the wide
       tables of the document, reads ਐਸ.ਸੀ as ਐਸਸੀ and cuts ਸਿੰਘ short to
       ਸਿ. 151 are the nukta, which the OCR drops, ਦਰਸਨ for ਦਰਸ਼ਨ, or reads
       as a ੁ, ਕਸੁਮੀਰ for ਕਸ਼ਮੀਰ. Most of the rest are ੁ and ੂ, which it
       confuses both ways - ਅਧਿਸੁਚਨਾ for ਅਧਿਸੂਚਨਾ and ਜਾਹਦਪੂਰ for ਜਾਹਦਪੁਰ.
       A few words are what the typist typed rather than what the word is -
       a nukta for the bindi of ਤੋਂ, a ੰ for the ੱ of ਉੱਤਰੀ, a stray ੋ in
       ਪੁੱਤਰ and a stray ੵ in another - and those come out here as the pdf
       says they were drawn.
    '''
    # the marks that are drawn under a letter, which ਿ stays behind while it
    # waits for the letter they belong to - see the class comment
    UNDER_MARKS = ['NUKTA', 'PAIRI_RA', 'PAIRI_HA', 'YAKASH']

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(punjabi.PunjabiUnicode())
        self.langobjs.append(punjabi.Conjuncts())
        self.langobjs.append(punjabi.Asees())

        self.lexer = self.get_lexer()

        # ਿ is drawn in front of the letter it belongs to and is typed there
        # as well
        self.waitdict = {'MATRA_I': 1}

        # a mark under the letter belongs to the letter ਿ has already
        # passed, so ਿ stays behind it and is emitted once the whole of the
        # letter has been drawn
        self.waitover = set(self.UNDER_MARKS)

        self.composeTokens = self.get_compose_tokens()

    def get_compose_tokens(self):
        '''the tippi and the addak that are typed in front of a ੁ or a ੂ, and
           the vowels that are typed as a carrier and a vowel sign, in that
           order so that ਉੰ, typed as ੳ, ੰ, ੁ, is the ੳ and the ੁ side by side
           by the time the vowels are read - see the class comment'''
        composeTokens = {}

        for markName in ['TIPPI', 'ADDAK']:
            for signName in ['MATRA_U', 'MATRA_UU']:
                composeTokens[(markName, signName)] = [signName, markName]

        # ਿ is typed in front of the ੲ it is drawn on, the other vowel signs
        # behind their carrier
        for pair, vowel in punjabi.VOWEL_COMPOSITIONS.items():
            if pair[1] == 'MATRA_I':
                pair = (pair[1], pair[0])
            composeTokens[pair] = [vowel]

        return composeTokens

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        def pat(*glyphs):
            # token strings are regular expressions for ply, so the glyphs
            # have to be escaped. Alternate glyphs of the same token are
            # joined into one pattern
            return '|'.join([re.escape(glyph) for glyph in glyphs])

        # VOWELS. The three carriers, which every vowel is typed as with a
        # vowel sign drawn on it - see self.composeTokens
        t_A              = pat('n')
        t_IRI            = pat('J')
        t_URA            = pat('T')

        # CONSONANTS
        t_KA             = pat('e')
        t_KHA            = pat('y')
        t_GA             = pat('r')
        t_GHA            = pat('x')

        t_CA             = pat('u')
        t_CHA            = pat('S')
        t_JA             = pat('i')
        t_JHA            = pat('M')

        t_TTA            = pat('N')
        t_TTHA           = pat('m')
        t_DDA            = pat('v')
        t_DDHA           = pat('Y')
        t_NNA            = pat('D')

        t_TA             = pat('s')
        t_THA            = pat('E')
        t_DA             = pat('d')
        t_DHA            = pat('X')
        t_NA             = pat('B')

        t_PA             = pat('g')
        t_PHA            = pat('c')
        t_BA             = pat('p')
        t_BHA            = pat('G')
        t_MA             = pat('w')

        t_YA             = pat(':')
        t_RA             = pat('o')
        t_LA             = pat('b')
        t_VA             = pat('t')
        t_SA             = pat(';')
        t_HA             = pat('j')
        t_RRA            = pat('V')

        # the letters that carry a nukta and have a key of their own. ਸ਼ and
        # ਜ਼ are typed as the letter and the nukta as well
        t_SHA            = pat('P')
        t_ZA             = pat('I')
        t_FA             = pat('|')

        # the pairin, drawn under the letter they are bound to and typed
        # behind it
        t_PAIRI_RA       = pat('q')
        t_PAIRI_HA       = pat('Q')

        # MATRAS. ਾਂ is one glyph and hands on the ਾ and the ਂ of it, see
        # the conjunct_tokens of langs/punjabi.py
        t_MATRA_AA       = pat('k')
        t_MATRA_I        = pat('f')
        t_MATRA_II       = pat('h')
        t_MATRA_U        = pat('[')
        t_MATRA_UU       = pat('{')
        t_MATRA_EE       = pat('/')
        t_MATRA_AI       = pat('?')
        t_MATRA_OO       = pat("'")
        t_MATRA_AU       = pat('"')
        t_MATRA_AA_BINDI = pat('K')

        # SIGNS
        t_NUKTA          = pat('a')
        t_BINDI          = pat('A')
        t_TIPPI          = pat('z')
        t_ADDAK          = pat('Z')
        t_YAKASH         = pat('=')

        # DIGITS. the digit keys of this font draw the western digits
        t_ASCII_ZERO     = pat('0')
        t_ASCII_ONE      = pat('1')
        t_ASCII_TWO      = pat('2')
        t_ASCII_THREE    = pat('3')
        t_ASCII_FOUR     = pat('4')
        t_ASCII_FIVE     = pat('5')
        t_ASCII_SIX      = pat('6')
        t_ASCII_SEVEN    = pat('7')
        t_ASCII_EIGHT    = pat('8')
        t_ASCII_NINE     = pat('9')

        # PUNCTUATIONS. The full stop draws the danda, and the punctuation
        # whose keys draw a letter or a sign has a key of its own - see the
        # class comment
        t_DANDA          = pat('.')
        t_DOT            = pat('H')
        t_COLON          = pat('L')
        t_SEMICOLON      = pat('l')
        t_DASH           = pat('^')
        t_SLASH          = pat('$')
        t_COMMA          = pat(',')
        t_LEFTPARAN      = pat('(')
        t_RIGHTPARAN     = pat(')')
        t_SPACE          = pat(' ')
        t_NEWLINE        = pat('\n')
        t_CARRIAGERET    = pat('\r')
        t_TAB            = pat('\t')
        t_FORMFEED       = pat('\f')

        def t_error(t):
            # a character with no token that can stand on a page is handed
            # on as itself rather than dropped, the way fonts/gujarati/
            # krishna.py hands on the english set in a latin font in the
            # middle of a line. Only a character that this converter has no
            # reading for at all is dropped, and that is reported
            char = t.value[0]

            if not self.is_text_char(char):
                self.report_error(t)
                t.lexer.skip(1)
                return None

            t.lexer.skip(1)
            t.type  = LITERAL
            t.value = char
            return t

        rules = dict(locals())

        # only the tokens that the font has a glyph for
        rules['tokens'] = [tokenName for tokenName in tokens \
                                     if 't_' + tokenName in rules]

        # the rules are handed to ply in an object of their own, as
        # fonts/gujarati/krishna.py does. ply looks up the module of that
        # object
        rules['__module__'] = self.__class__.__module__
        return lex.lex(object = types.SimpleNamespace(**rules))
