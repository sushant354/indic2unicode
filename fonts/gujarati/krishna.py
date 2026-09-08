import re

from indic2unicode.langs import gujarati
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class Krishna(BaseFont):
    '''Krishna is the legacy 8 bit gujarati font that the Gujarat Government
       Gazette sets the orders of its district magistrates in. It is a font
       of the same kind as fonts/odiya/shree.py and fonts/marathi/yogesh.py:
       the pdf embeds it as a simple TrueType font with WinAnsiEncoding and
       no ToUnicode map at all, so its text extracts as the cp1252
       characters of the bytes that were typed - જિલ્લા મેજીસ્ટ્રેટ દ્વારા
       comes out as "ìÉSáë Üõ°VËÿõË ¦ëßë" - and every one of those
       characters is a glyph of the font rather than a character of the
       script.

       Four faces of the typing package share this layout and this document
       carries all four: Krishna, which draws 40995 of the 42624 glyphs of
       it, KrishnaBold, which sets the signature blocks, and Mani and
       Suchitra, which set the headings and the table headers. Every byte
       the last three draw was read in the words it stands in and is the
       character Krishna draws on that byte, so one converter reads all four.

       The pdf carries the regular face twice over, as this simple font on
       the bytes that were typed and as a Type0 subset whose ToUnicode map
       hands its glyphs those same bytes back, so both come out of the pdf
       as one encoding. શ્ચ 0x8D is drawn by the second of the two alone.

       WHAT IS TYPED IN A DIFFERENT ORDER FROM UNICODE

       Two things, and both of them are what the letterpress order of the
       script asks for rather than anything wrong with the font:

       1. િ MATRA_I is drawn in front of the cluster it belongs to and is
          typed there as well, so જિલ્લા is typed as િ, જ, લ્, લ, ા.
       2. the reph, the ર્ that gujarati draws as a stroke over its
          syllable, is typed behind the letter it is drawn on and unicode
          writes it in front of that letter - સંદર્ભ is typed as સ, ં, દ, ભ,
          reph and પૂર્ણ as પ, ૂ, ણ, reph.

       Everything else is typed in the order unicode wants it, the rakar
       ્ર included: it is drawn as a mark under the letter it is bound to
       and is typed behind that letter, which is where unicode writes it -
       પ્રચાર is typed as પ, rakar, ચ, ા, ર.

       THE UPRIGHT THAT COMPLETES A HALF FORM

       Most of the gujarati alphabet is drawn as a shape and an upright
       stroke beside it, and the half form of such a letter is that shape
       without the upright - ક્ against ક. This font keeps the two apart on
       two keys and builds the letter out of them: the upright is the same
       glyph as ા MATRA_AA, and ઘ is typed as ઘ્ and a ા, ણ as ણ્ and a ા,
       ક્ષ as ક્ષ્ and a ા. So ચૂંટણી is typed as ચ, ૂ, ં, ટ, ણ્, ા, ી and
       સત્તાની as સ, ત્ત્, ા, ા, ન, ી - the first ા of it the upright of the
       ત્ત and the second the vowel sign. A half consonant is never followed
       by a ા in gujarati, so a ા behind one is read as its upright here.

       ી, ો and ૌ carry an upright of their own and complete a half form the
       same way, ણી being typed as either ણ્, ા, ી or ણ્, ી.

       ો is that upright with a ે over it, so a ા that a ે follows is the
       one character ો - જો is typed as જા, the glyph this font draws જ and
       its upright with, and a ે. ૌ is the same with a ૈ.

       આ, એ, ઓ, ઐ and ઔ are each typed as અ and the vowel sign that is drawn
       beside it, and unicode has a character of its own for each of the
       five.

       THE TWO SPACERS

       Two of the bytes this document draws stand for nothing at all. The
       first is 0xAD, which the font gives an empty outline and the pdf a
       width of zero, and which stands between a letter and the one that
       follows it 15 times - પ્રચાર is typed as પ, rakar, 0xAD, ચ, ા, ર. The
       second is 0xEF, 4 units wide and with an outline of two units, which
       stands between થ and વ. Neither is a character, so both are dropped
       before the text is tokenized rather than carried through the passes
       as a token that converts to nothing.

       THE ENGLISH IN THE MIDDLE OF A GUJARATI LINE

       The gazette sets the odd english word inside a gujarati line - a
       (GAS) behind an officer's name, the number of a circular - in a latin
       font, and an extractor that hands a converter the whole line hands it
       those letters too. An 8 bit font has a glyph on every byte and
       nothing in the text says which font drew it, so a latin letter that
       this font draws something on is read as that something: (GAS) comes
       out as (Gખ્લ્), the G alone surviving because this font draws nothing
       on it. A caller that converts a run of text at a time, which is what
       the font name of a run is for, never sees this.

       WHAT THE READINGS WERE CHECKED AGAINST

       The pdf embeds the font, so what every byte draws is in the document
       itself: each of the 117 bytes the four faces draw was set in the font
       and read off its own outlines, and each was read again in the words
       it stands in, so that the glyph that is ક્ષ્ rather than શ્ and the
       one that is દ્ય rather than ઘ are what the page draws and not what an
       OCR of it guesses. Of the 6564 words of gujarati this converter
       writes for the test document, 6354 are read back word for word by an
       OCR of the same pages.

       The 210 that are not are mostly the OCR's own: it reads a word of a
       table twice or not at all, joins two of them, or splits a word this
       document runs together. 11 of them are the english above. 68 are what
       the typist typed rather than what the word is - ૫, the digit five,
       for the પ of ઉપર, ર, the letter ra, for the ૨ that numbers a
       paragraph, and ઃ, the visarga, for the colon that ends a heading,
       each pair being one shape in this script - and those come out here as
       the pdf says they were drawn.
    '''
    # the two bytes that draw nothing and stand for nothing, see the class
    # comment. Neither is a character, so they never reach the tokenizer
    SPACERS = '\xad\xef'

    # the vowel signs that carry the upright of the letter they sit on and
    # so complete a half form, ા being the upright by itself
    UPRIGHT_SIGNS = ['MATRA_II', 'MATRA_O', 'MATRA_AU']

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(gujarati.GujaratiUnicode())
        self.langobjs.append(gujarati.Conjuncts())

        self.lexer = self.get_lexer()

        # િ is drawn in front of the cluster it belongs to and is typed
        # there as well
        self.waitdict   = {'MATRA_I': 1}

        # the reph is drawn as a stroke over the syllable it belongs to and
        # is typed behind the letter of it
        self.jumpbefore = {'REPH': 1}

        # the half forms, which are the head of the cluster that follows
        # them, and the vowel signs and the marks that are drawn on a letter
        self.deadtokens = set()
        self.signtokens = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                ustr = obj.get_unicode_string(tokenName)
                if tokenName.startswith('DEAD_'):
                    self.deadtokens.add(tokenName)
                elif tokenName == 'REPH':
                    continue
                elif self.is_sign(ustr):
                    self.signtokens.add(tokenName)

        # while the reph jumps back to the head of its syllable it has to
        # jump over the vowel signs and the marks of that syllable and over
        # the rakar, which is bound under the letter it belongs to
        self.jumpover = set(self.signtokens)
        self.jumpover.add('RAKAR')

        # a rakar belongs to the letter િ has already passed, so િ stays
        # behind it and is emitted once the whole cluster has been drawn
        self.waitover = set(['RAKAR'])

        # a half form is not the letter િ is waiting for, it is the head of
        # the cluster િ belongs to, and so is a reph that has already jumped
        # to the head of the syllable
        self.halftokens = set(self.deadtokens)
        self.halftokens.add('REPH')

        self.composeTokens = self.get_compose_tokens()

    def get_compose_tokens(self):
        '''the pieces this font types a letter in, in the order they have to
           be put back together: the upright of a half form is read out of
           the cluster before ો is read out of the ા of it, so that the ે of
           ણે is not taken for the ે of a ો - see the class comment'''
        composeTokens = {}

        # a half form and the upright behind it are the whole letter, and
        # the vowel signs that carry an upright of their own complete it as
        # readily as the bare upright does. Only the half forms this font
        # has a glyph for are worth a rule, the tokens of the script that it
        # draws nothing on never reaching the passes
        for tokenName in sorted(self.deadtokens & self.lexer.lextokens):
            letter = tokenName[len('DEAD_'):]
            composeTokens[(tokenName, 'MATRA_AA')] = [letter]
            for signName in self.UPRIGHT_SIGNS:
                composeTokens[(tokenName, signName)] = [letter, signName]

        # જા is one glyph of this font and the ો of જો is the ે over the
        # upright of it
        composeTokens[('JA_MATRA_AA', 'MATRA_E')]  = ['JA', 'MATRA_O']
        composeTokens[('JA_MATRA_AA', 'MATRA_AI')] = ['JA', 'MATRA_AU']

        # ો is the upright of ા with a ે over it and ૌ the same with a ૈ.
        # Whatever upright a half form asked for has been read out of the
        # text by now, so a ા that is still here is a vowel sign
        composeTokens[('MATRA_AA', 'MATRA_E')]  = ['MATRA_O']
        composeTokens[('MATRA_AA', 'MATRA_AI')] = ['MATRA_AU']

        # the vowels that are typed as અ and the vowel sign drawn beside it
        composeTokens[('A', 'MATRA_AA')] = ['AA']
        composeTokens[('A', 'MATRA_E')]  = ['E']
        composeTokens[('A', 'MATRA_AI')] = ['AI']
        composeTokens[('A', 'MATRA_O')]  = ['O']
        composeTokens[('A', 'MATRA_AU')] = ['AU']

        return composeTokens

    def is_sign(self, ustr):
        '''whether the string of a token is a vowel sign or a mark that is
           drawn on the letter of its syllable'''
        if ustr == None or len(ustr) != 1:
            return False

        # the vowel signs and the virama, the marks that are drawn over a
        # letter - ઁ ં ઃ - the nukta and the two vowel signs that unicode
        # puts behind the letters, ૢ and ૣ
        return '\u0abe' <= ustr <= '\u0acd' or \
               '\u0a81' <= ustr <= '\u0a83' or ustr == '\u0abc' or \
               '\u0ae2' <= ustr <= '\u0ae3'

    def to_unicode(self, data):
        return BaseFont.to_unicode(self, self.drop_spacers(data))

    def drop_spacers(self, data):
        '''the two bytes that draw nothing and stand for nothing, see the
           class comment'''
        for spacer in self.SPACERS:
            data = data.replace(spacer, '')
        return data

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        def pat(*glyphs):
            # token strings are regular expressions for ply, so the glyphs
            # have to be escaped. Alternate glyphs of the same token are
            # joined into one pattern
            return '|'.join([re.escape(glyph) for glyph in glyphs])

        # VOWELS. આ, એ, ઐ, ઓ and ઔ are each typed as અ and a vowel sign,
        # see self.composeTokens
        t_A              = pat('±')
        t_II             = pat('´')
        t_U              = pat('µ')

        # CONSONANTS. ઘ and ણ have no key of their own, being typed as a
        # half form and the upright behind it, and ફ has two glyphs
        t_KA             = pat('À')
        t_KHA            = pat('Â')
        t_GA             = pat('Ã')

        t_CA             = pat('Ç')
        t_CHA            = pat('È')
        t_JA             = pat('É')
        t_JHA            = pat('{')

        t_TTA            = pat('Ë')
        t_TTHA           = pat('Ì')
        t_DDA            = pat('Í')
        t_DDHA           = pat('Ï')

        t_TA             = pat('Ö')
        t_THA            = pat('×')
        t_DA             = pat('Ø')
        t_DHA            = pat('Ô')
        t_NA             = pat('Þ')

        t_PA             = pat('Õ')
        t_PHA            = pat('Î', 'N')
        t_BA             = pat('Ú')
        t_BHA            = pat('Û')
        t_MA             = pat('Ü')

        t_YA             = pat('Ý')
        t_RA             = pat('ß')
        t_LA             = pat('á')
        t_LLA            = pat('â')
        t_VA             = pat('ä')
        t_SHA            = pat('å')
        t_SSA            = pat('æ')
        t_SA             = pat('ç')
        t_HA             = pat('è')

        # HALF FORMS, which is what this font draws a letter without its
        # upright with. A cluster the font has no ligature of its own for is
        # drawn as one of these and the letter that follows it, ન્ય being ન્
        # and ય, and a letter whose own key it is not - ઘ, ણ, ક્ષ, ત્ર, જ્ઞ,
        # ત્ત, ન્ન - is drawn as one of these and the upright behind it
        t_DEAD_KA        = pat('@')
        t_DEAD_KHA       = pat('A')
        t_DEAD_GA        = pat('B')
        t_DEAD_GHA       = pat('C')
        t_DEAD_CA        = pat('E')
        t_DEAD_JA        = pat('F')
        t_DEAD_NNA       = pat('H')
        t_DEAD_TA        = pat('I')
        t_DEAD_THA       = pat('J')
        t_DEAD_DHA       = pat('K')
        t_DEAD_NA        = pat('L')
        t_DEAD_PA        = pat('M')
        t_DEAD_BA        = pat('O')
        t_DEAD_MA        = pat('Q')
        t_DEAD_LA        = pat('S')
        t_DEAD_VA        = pat('T')
        t_DEAD_SHA       = pat('U')
        t_DEAD_SA        = pat('V')
        t_DEAD_SSA       = pat('W')
        t_DEAD_KA_SSA    = pat('Z')
        t_DEAD_TA_RA     = pat('h')
        t_DEAD_JA_NYA    = pat('i')
        t_DEAD_TA_TA     = pat('k')
        t_DEAD_NA_NA     = pat('ø')

        # CONJUNCTS, each of them a ligature of its own in the font and each
        # of them drawn with the upright it needs
        t_KA_KA          = pat('y')
        t_KA_RA          = pat('¿')
        t_DA_DA          = pat('¡')
        t_DA_DHA         = pat('¢')
        t_DA_RA          = pat('Ä')
        t_DA_VA          = pat('¦')
        t_DA_YA          = pat('z')
        t_SHA_CA         = pat('\x8d')
        t_SHA_RA         = pat('l')

        # the letters that the font draws together with the sign behind them
        t_JA_MATRA_AA    = pat('½')
        t_JA_MATRA_II    = pat('°')
        t_RA_MATRA_U     = pat('v')
        t_RA_MATRA_UU    = pat('w')
        t_PHA_MATRA_UU   = pat('d')

        # MATRAS. ા is the upright of a half form as well as the vowel sign,
        # and ો is that upright with a ે over it, so neither has a key of
        # its own - see self.composeTokens. િ has a narrow glyph and a wide
        # one, ુ and ૂ a glyph for every shape they hang under
        t_MATRA_AA       = pat('ë')
        t_MATRA_I        = pat('ì', 'ã')
        t_MATRA_II       = pat('í')
        t_MATRA_U        = pat('ð', '<', '\\')
        t_MATRA_UU       = pat('ñ', '^')
        t_MATRA_VOCALIC_R = pat('ò')
        t_MATRA_E        = pat('õ')
        t_MATRA_AI       = pat('ö')
        t_MATRA_O        = pat('ù')
        t_MATRA_AU       = pat('ú')

        # the marks a letter carries that the font draws together with the
        # vowel sign of it, and which neither of the reordering passes moves
        # apart - see the conjunct_tokens of langs/gujarati.py. ૃ is drawn
        # on the upright of its letter and so carries that upright with it
        t_MATRA_AA_MATRA_VOCALIC_R = pat('²')
        t_MATRA_II_ANUSVARA = pat('Ù')
        t_MATRA_II_REPH     = pat('`', 'a')

        # SIGNS. ં has a glyph for every height it is drawn at, and the reph
        # and the rakar one for every shape they sit on
        t_ANUSVARA       = pat('_', 'o', 'î')
        t_VISARGA        = pat('Ñ')
        t_REPH           = pat('ý', 'ó')
        t_RAKAR          = pat('þ', 'ÿ')

        # DIGITS. the digit keys of this font draw the gujarati digits
        t_ZERO           = pat('0')
        t_ONE            = pat('1')
        t_TWO            = pat('2')
        t_THREE          = pat('3')
        t_FOUR           = pat('4')
        t_FIVE           = pat('5')
        t_SIX            = pat('6')
        t_SEVEN          = pat('7')
        t_EIGHT          = pat('8')
        t_NINE           = pat('9')

        # PUNCTUATIONS, which this font keeps on the keys they are typed on
        t_LEFTPARAN      = pat('(')
        t_RIGHTPARAN     = pat(')')
        t_COMMA          = pat(',')
        t_DASH           = pat('-')
        t_DOT            = pat('.')
        t_SLASH          = pat('/')
        t_QUESTION       = pat('?')
        t_SPACE          = pat(' ')
        t_NEWLINE        = pat('\n')
        t_CARRIAGERET    = pat('\r')
        t_TAB            = pat('\t')
        t_FORMFEED       = pat('\f')

        def t_error(t):
            # the gazette sets the odd word of english in the middle of a
            # gujarati line - a (GAS) behind an officer's name, the number
            # of a circular - and that word is set in a latin font and comes
            # out of the pdf as itself. This font draws no glyph on those
            # bytes, so a character with no token that can stand on a page
            # is handed on as itself rather than dropped. Only a byte that
            # this converter has no reading for at all is dropped, and that
            # is reported
            char = t.value[0]

            if not self.is_text_char(char):
                self.report_error(t)
                t.lexer.skip(1)
                return None

            t.lexer.skip(1)
            t.type  = LITERAL
            t.value = char
            return t

        # only the tokens that the font has a glyph for
        rules  = locals()
        tokens = [tokenName for tokenName in tokens if 't_' + tokenName in rules]

        return lex.lex()
