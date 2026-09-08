import re

from indic2unicode.langs import odiya
from ..basefont import BaseFont
import ply.lex as lex

class Akruti(BaseFont):
    '''AkrutiOri is the legacy 8 bit odiya font of the Akruti typing package
       that the Odisha Gazette sets a part of its land acquisition
       notifications in. It is an 8 bit font of the same kind as
       fonts/odiya/shree.py and fonts/marathi/yogesh.py: the pdf embeds it
       as a simple TrueType font with WinAnsiEncoding and no ToUnicode map
       at all, so its text extracts as the cp1252 characters of the bytes
       that were typed - ଓଡିଶା comes out as "IWògû" - and every one of those
       characters is a glyph of the font rather than a character of the
       script.

       The three faces the gazette carries, AkrutiOriAshok-99Normal,
       AkrutiOriAshok-99Bold and AkrutiOriKoshal-99Normal, share this
       layout. Ashok Normal is the text face and draws all but 30 of the
       6250 akruti glyphs of this document, Ashok Bold the one the headings
       are set in and Koshal a display face that draws a single letter.
       Every byte the two smaller faces draw was read off its own outlines
       and is the character Ashok Normal draws on that byte, so one
       converter reads all three. What they agree on beyond those bytes is
       not in this document to be checked.

       NO SPACER

       Unlike Shree, this font pays back no width: it steps every letter
       over the width its outline really takes, so there is no empty glyph
       between the letters and every character of the text stands for
       something on the page.

       WHAT IS TYPED IN A DIFFERENT ORDER FROM UNICODE

       Two things, and both of them are what the letterpress order of the
       script asks for rather than anything wrong with the font:

       1. େ, ୋ, ୈ and ୌ are drawn in front of the letter they belong to, and
          the front half of all four is the same 'ù' glyph. ୋ is that glyph
          and the ା behind the letter and ୈ is that glyph and the hook
          '÷'. ୌ is either that glyph and 'ø', which this document writes
          once, or the ୋ of the letter with the same hook added to it,
          which it writes four times and doubles the hook of every time -
          the two are one shape drawn in two pieces and in three. The
          pieces are joined back into one character once the front half has
          jumped over its letter.
       2. The reph, the ର୍ that odiya draws as a stroke over its syllable,
          is typed behind the letter it is drawn on and unicode writes it
          in front of that letter - ସାର୍ବ is typed as ସ, ା, ବ, reph.

       Everything else is typed in the order unicode wants it, ି included:
       odiya draws ି over the letter and to the left of it, but it is typed
       behind that letter and the font gives it a negative side bearing to
       carry it back.

       THE GLYPHS THAT DRAW ONE CHARACTER IN TWO SHAPES

       ି is drawn as a hook over the letter and as a stroke under it, and
       the two are separate glyphs - 'ò' and 'ô'. The letter decides which
       of the two the typist strikes, ଧ carrying the stroke because its own
       shape leaves no room above it. ୁ likewise has a glyph that hangs off
       the letter, 'ê', and one that hangs off a cluster that is already
       carrying a consonant under it, 'ë'. Each pair is one token here.

       THE GLYPH THAT DRAWS TWO CHARACTERS

       'ó' is ି and ଁ in one shape, drawn where the two would be drawn side
       by side, and ନାହିଁ is typed with it. Neither of the two moves, so it
       is handed on as the two tokens rather than as a token of its own -
       see MATRA_I_CANDRABINDU in langs/odiya.py.

       WHAT THE FONT SPELLS OUT AND WHAT IT DRAWS WHOLE

       The clusters of consonants this document writes fall in two halves.
       Twenty of them have a ligature of their own in the font, from ନ୍ତ and
       ମ୍ବ to ଷ୍ଟ and ଳ୍ପ, and a cluster like that is one glyph and one
       token. The rest are spelled out, the second consonant of them being
       one of the nine that this font draws as a mark of its own under the
       letter - ୍ର and ୍ୟ, the phalas, among them - so ଜିଲ୍ଲା is ଜ, ି, ଲ, ୍ଲ.
       ଆ is likewise typed as ଅ and ା and is one character in unicode.

       THE DANDA THE ା KEY DRAWS

       The full stop of all 39 sentences of this document is a ା, whose
       glyph is the same upright stroke as the danda and whose key sits
       under the typist's finger. A vowel sign never starts a word, so a ା
       that begins one is read as the danda here, as it is in
       fonts/odiya/shree.py.

       WHAT THE READINGS WERE CHECKED AGAINST

       The pdf embeds the font, so what every byte draws is in the document
       itself: each of the 102 bytes this one draws was set in the font and
       read off its own outlines, and each was read again in the words it
       stands in, so the glyph that is ି under ଧ and the one that is ମ୍ମ
       rather than ମ are what the page draws and not what an OCR of it
       guesses. Where the two disagree it is the page that is followed:
       ସକରାମିକ and ନକରାମିକ are what this document draws for ସକରାତ୍ମକ and
       ନକରାତ୍ମକ, the typist having reached for ମ and ି instead of ତ and ୍ମ,
       and they are converted as drawn.
    '''
    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(odiya.OdiyaUnicode())
        self.langobjs.append(odiya.Conjuncts())

        self.lexer = self.get_lexer()

        # େ, ୋ, ୈ and ୌ are drawn in front of the letter they belong to, the
        # front half of all four being େ MATRA_E
        self.waitdict   = {'MATRA_E': 1}

        # the reph is drawn as a stroke over the letter it belongs to and
        # is typed behind that letter
        self.jumpbefore = {'REPH': 1}

        # the consonants that this font draws as a mark under the letter
        # they are bound to, which stand between that letter and the vowel
        # sign of it and are transparent to both of the reordering passes
        self.subjointokens = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName.startswith('SUBJOINED_'):
                    self.subjointokens.add(tokenName)

        # while the reph jumps back to the head of its syllable it has to
        # jump over the vowel signs and the marks of that syllable and over
        # the consonants that are bound under its letter
        self.jumpover = set([ \
            'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',   \
            'MATRA_VOCALIC_R', 'MATRA_E', 'AI_LENGTH_MARK',             \
            'AU_LENGTH_MARK', 'ANUSVARA', 'CANDRABINDU', 'VISARGA',     \
        ])
        self.jumpover.update(self.subjointokens)

        # a consonant that is bound under a letter belongs to the letter
        # MATRA_E has already passed, so MATRA_E stays behind it
        self.waitover = set(self.subjointokens)

        # a reph that has jumped to the head of the syllable is not the
        # letter MATRA_E is waiting for, it is the head of that same
        # syllable, so MATRA_E is emitted behind it
        self.halftokens = set(['REPH'])

        # what a word can begin behind, which is what tells the ା of a
        # syllable from the one that stands for the danda - see split_danda
        self.wordbreaks = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                ustr = obj.get_unicode_string(tokenName)
                if ustr and ustr.isspace():
                    self.wordbreaks.add(tokenName)

        self.composeTokens = { \
            # ଆ is typed as ଅ and the ା of it, and unicode has a character
            # of its own for the pair
            ('A', 'MATRA_AA')      : 'AA', \
        }

        # the pieces of a two part vowel sign, put back together once the
        # front half has jumped over the letter that stood between them.
        # The order matters: ୌ is drawn more often as the ୋ of the letter
        # with a hook added to it than with its own back half, so ୋ has to
        # be built before the hook is read, and the second of the two hooks
        # the typist strikes adds nothing to what the first one already
        # made
        self.joinTokens = { \
            ('MATRA_E', 'MATRA_AA')        : 'MATRA_O',  \
            ('MATRA_O', 'AI_LENGTH_MARK')  : 'MATRA_AU', \
            ('MATRA_AU', 'AI_LENGTH_MARK') : 'MATRA_AU', \
            ('MATRA_E', 'AI_LENGTH_MARK')  : 'MATRA_AI', \
            ('MATRA_E', 'AU_LENGTH_MARK')  : 'MATRA_AU', \
        }

    def split_danda(self, tokentypes):
        '''the ା that stands for the danda. A vowel sign never starts a
           word, so a ା that begins one is the upright stroke that ends a
           sentence - see the class comment. It is read off the word it
           begins rather than off the letter behind it because this
           document once writes a ଁ in front of the ା it belongs behind,
           ନିଜଗାଁ being typed as ନ, ି, ଜ, ଗ, ଁ, ା, and that ା is carried by
           the ଗ of its own syllable all the same'''
        out = []
        for i, tokenName in enumerate(tokentypes):
            prev = tokentypes[i - 1] if i > 0 else None

            if tokenName == 'MATRA_AA' and \
                    (prev == None or prev in self.wordbreaks):
                tokenName = 'DANDA'

            out.append(tokenName)
        return out

    def to_unicode(self, data):
        '''the passes in the order this font needs them: the ା that stands
           for the danda is read out of the word it starts before anything
           moves, and the pieces of ୋ, ୈ and ୌ are joined after the front
           half has jumped over its letter, the letter having stood between
           them until then'''
        tokentypes = self.tokenize(data)

        tokentypes = self.split_danda(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)
        tokentypes = self.jump_before_tokens(tokentypes)
        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes, self.joinTokens)

        return self.tokens_to_unicode(tokentypes)

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        def pat(*glyphs):
            # token strings are regular expressions for ply, so the glyphs
            # have to be escaped. Alternate glyphs of the same token are
            # joined into one pattern
            return '|'.join([re.escape(glyph) for glyph in glyphs])

        # VOWELS. ଆ is typed as ଅ and a ା, see self.composeTokens
        t_A              = pat('@')
        t_I              = pat('A')
        t_U              = pat('C')
        t_E              = pat('G')
        t_O              = pat('I')
        t_AU             = pat('J')

        # CONSONANTS
        t_KA             = pat('K')
        t_KHA            = pat('L')
        t_GA             = pat('M')
        t_GHA            = pat('N')

        t_CA             = pat('P')
        t_CHA            = pat('Q')
        t_JA             = pat('R')
        t_JHA            = pat('S')

        t_TTA            = pat('U')
        t_TTHA           = pat('V')
        t_DDA            = pat('W')
        t_DDHA           = pat('X')
        t_NNA            = pat('Y')

        t_TA             = pat('Z')
        t_THA            = pat('[')
        t_DA             = pat('\\')
        t_DHA            = pat(']')
        t_NA             = pat('^')

        t_PA             = pat('_')
        t_PHA            = pat('`')
        t_BA             = pat('a')
        t_BHA            = pat('b')
        t_MA             = pat('c')

        t_YA             = pat('~')
        t_RA             = pat('e')
        t_LA             = pat('f')
        t_LLA            = pat('k')
        t_SHA            = pat('g')
        t_SSA            = pat('h')
        t_SA             = pat('i')
        t_HA             = pat('j')

        t_YYA            = pat('d')

        # CONJUNCTS, each of them a ligature of its own in the font
        t_KA_TA          = pat('q')
        t_KA_SSA         = pat('l')

        t_NGA_KA         = pat('u')
        t_NGA_GA         = pat('w')

        t_NNA_DDA        = pat('Š')

        t_DA_DA          = pat('Ÿ')
        t_DHA_YYA        = pat('¤')

        t_NA_TA          = pat('«')
        t_NA_DA          = pat('¦')
        t_NA_DHA         = pat('§')

        t_PA_TA          = pat('¯')

        t_MA_PA          = pat('µ')
        t_MA_BA          = pat('´')
        t_MA_BHA         = pat('¸')
        t_MA_MA          = pat('¹')

        t_LLA_PA         = pat('Ì')

        t_SSA_TTA        = pat('Á')
        t_SSA_NNA        = pat('¾')
        t_SA_TA          = pat('É')
        t_SA_WA          = pat('Ê')

        # SUBJOINED CONSONANTS, the ones odiya draws as a mark of their own
        # under the letter they are bound to
        t_SUBJOINED_TTHA = pat('×')
        t_SUBJOINED_THA  = pat('Ú')
        t_SUBJOINED_NA   = pat('Ü')
        t_SUBJOINED_MA   = pat('à')
        t_SUBJOINED_YYA  = pat('ý')
        t_SUBJOINED_RA   = pat('â')
        t_SUBJOINED_LA   = pat('ä')
        t_SUBJOINED_WA   = pat('ß')
        t_SUBJOINED_SA   = pat('è')

        # MATRAS. ି is drawn over the letter for most of the alphabet and
        # under it for ଧ, and ୁ hangs off the letter or off the consonant
        # that is bound under it. Each pair is one token here
        t_MATRA_AA       = pat('û')
        t_MATRA_I        = pat('ò', 'ô')
        t_MATRA_II       = pat('ú')
        t_MATRA_U        = pat('ê', 'ë')
        t_MATRA_UU       = pat('ì')
        t_MATRA_VOCALIC_R = pat('é')
        # the front half of ୋ, ୈ and ୌ, which the font draws in front of
        # the letter, and the back halves of ୈ and ୌ. The back half of ୋ is
        # the ା above, and the hook of ୈ is what this document more often
        # adds to a ୋ to make a ୌ - see self.joinTokens
        t_MATRA_E        = pat('ù')
        t_AI_LENGTH_MARK = pat('÷')
        t_AU_LENGTH_MARK = pat('ø')

        # SIGNS. ି and ଁ are drawn in one glyph as well as in two
        t_REPH           = pat('ð')
        t_ANUSVARA       = pat('õ')
        t_CANDRABINDU    = pat('ñ')
        t_VISARGA        = pat('ü')
        t_VIRAMA         = pat('þ')
        t_MATRA_I_CANDRABINDU = pat('ó')

        # DIGITS. the digit keys of this font draw the odiya digits
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
        t_DOT            = pat('.')
        t_DASH           = pat('-')
        t_ENDASH         = pat('–')
        t_SLASH          = pat('/')
        t_SPACE          = pat(' ')
        t_NEWLINE        = pat('\n')
        t_CARRIAGERET    = pat('\r')
        t_TAB            = pat('\t')

        def t_error(t):
            self.report_error(t)
            t.lexer.skip(1)

        # only the tokens that the font has a glyph for
        rules  = locals()
        tokens = [tokenName for tokenName in tokens if 't_' + tokenName in rules]

        return lex.lex()
