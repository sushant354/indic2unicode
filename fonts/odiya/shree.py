import re

from indic2unicode.langs import odiya
from ..basefont import BaseFont
import ply.lex as lex

class Shree(BaseFont):
    '''SHREE-ORI7 is the legacy 8 bit odiya font of the Shree-Lipi typing
       package that the Odisha Gazette sets its land acquisition
       notifications in. It is an 8 bit font of the same kind as
       fonts/marathi/yogesh.py and fonts/tamil/tamelango.py: the pdf embeds
       it as a simple TrueType font with WinAnsiEncoding and no ToUnicode
       map at all, so its text extracts as the cp1252 characters of the
       bytes that were typed - ମାଲକାନଗିରି comes out as "þæàÿLÿæ[ÿSçÀÿç" -
       and every one of those characters is a glyph of the font rather than
       a character of the script.

       The two faces the gazette carries, SHREE-ORI7-0601 and
       SHREE-ORI7-0602, share this layout. 0601 is the text face and 0602
       the display one the mastheads are set in, and the 34 bytes 0602
       draws in this document were each read off its own outlines and are
       each the character 0601 draws on that byte, so one converter reads
       both. Neither subset carries the glyphs it does not draw, so what
       the two agree on beyond those 34 bytes is not in this document to
       be checked.

       THE SPACER

       The commonest character of such a text is 'ÿ', one character in six
       of what the font draws in this document, and it stands for nothing
       at all: the glyph is empty and 152 units wide. The letters of this
       font are drawn wider than they are stepped over - କ steps 363 units
       and its outline runs to 488 - and 'ÿ' is what pays the difference
       back, so that the next letter starts clear of the one before it. Of
       the 27 letters and clusters of this document whose outline overruns
       its advance, 26 are followed by a 'ÿ' every time they are drawn and
       the 27th, ର, all but once; and only twice in the document does a
       'ÿ' stand behind a glyph that does not overrun. So it is dropped
       before the text is tokenized rather than carried through the passes
       as a token that converts to nothing.

       WHAT IS TYPED IN A DIFFERENT ORDER FROM UNICODE

       Two things, and both of them are what the letterpress order of the
       script asks for rather than anything wrong with the font:

       1. େ, ୈ and ୌ are drawn in front of the letter they belong to, and
          the front half of all three is the same '{' glyph. ୋ is that
          glyph and the ା behind the letter, ୈ is that glyph and 'ð', ୌ is
          that glyph and 'ò', so the two halves are joined back into one
          character once the front half has jumped over its letter.
       2. The reph, the ର୍ that odiya draws as a stroke over its syllable,
          is typed behind the letter it is drawn on and unicode writes it
          in front of that letter - ସର୍ବ is typed as ସ, ବ, reph.

       Everything else is typed in the order unicode wants it, ି included:
       odiya draws ି over the letter and to the left of it, but it is typed
       behind that letter and the font gives it a negative side bearing to
       carry it back.

       THE GLYPHS THAT DRAW ONE CHARACTER IN TWO SHAPES

       ି is drawn as a hook over the letter for most of the alphabet and as
       a stroke under it for ଖ, ଥ and ଧ, whose own shape leaves no room
       above, and the two are separate glyphs - 'ç' and '#'. ଁ likewise has
       a wide glyph ']' and a narrow one 'ô'. Each pair is one token here.

       WHAT THE FONT SPELLS OUT AND WHAT IT DRAWS WHOLE

       Every cluster of consonants this document writes has a ligature of
       its own in the font, from ନ୍ତ and ମ୍ବ to ଣ୍ଣ and ସ୍ଥ, so a cluster is
       one glyph and one token. The exceptions are the seven consonants
       that odiya binds under a letter as a mark of its own - the phalas ୍ୟ
       and ୍ର among them - which are drawn behind their letter, and ଆ and
       ୱ, which are typed as ଅ + ା and ଓ + ୍ୱ and are one character each in
       unicode.

       THE DANDA THE ା KEY DRAWS

       The font has a danda on '>' and this document draws it once. The
       full stop of its other 39 sentences is a ା, whose glyph is the same
       upright stroke and whose key sits under the typist's finger, and it
       stands alone between two spaces. A vowel sign never starts a word,
       so a ା that no letter carries is read as the danda here.

       WHAT THE READINGS WERE CHECKED AGAINST

       The pdf embeds the font, so what every byte draws is in the document
       itself: each of the 104 bytes this one draws was set in the font and
       read off its own outlines, and each was read again in the words it
       stands in, so the glyph that is ି under ଥ and the one that is ଝ
       rather than ଜ are what the page draws and not what an OCR of it
       guesses. Every one of the 466 lines was then set again from the
       unicode this converter writes for it, and all 466 come back as the
       glyphs the page drew, none added and none dropped.
    '''
    # the empty glyph that pays back the width the letter in front of it
    # overran, see the class comment. It is not a character and never
    # stands on its own, so it is dropped rather than tokenized
    SPACER = 'ÿ'

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(odiya.OdiyaUnicode())
        self.langobjs.append(odiya.Conjuncts())

        self.lexer = self.get_lexer()

        # େ, ୈ and ୌ are drawn in front of the letter they belong to, the
        # front half of all three being େ MATRA_E
        self.waitdict   = {'MATRA_E': 1}

        # the reph is drawn as a stroke over the letter it belongs to and
        # is typed behind that letter
        self.jumpbefore = {'REPH': 1}

        self.subjointokens = set()
        # the letters and the clusters of them that a vowel sign can sit
        # on, which is what tells the ା of a syllable from the one that
        # stands for the danda - see split_danda
        self.lettertokens  = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName.startswith('SUBJOINED_'):
                    self.subjointokens.add(tokenName)
                elif self.is_letter(obj.get_unicode_string(tokenName)):
                    self.lettertokens.add(tokenName)

        # while the reph jumps back to the head of its syllable it has to
        # jump over the vowel signs and the marks of that syllable and over
        # the consonants that are bound under its letter
        self.jumpover = set([ \
            'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',   \
            'MATRA_VOCALIC_R', 'MATRA_E', 'AI_LENGTH_MARK',             \
            'AU_LENGTH_MARK', 'ANUSVARA', 'CANDRABINDU',                \
        ])
        self.jumpover.update(self.subjointokens)

        # a consonant that is bound under a letter belongs to the letter
        # MATRA_E has already passed, so MATRA_E stays behind it
        self.waitover = set(self.subjointokens)

        # a reph that has jumped to the head of the syllable is not the
        # letter MATRA_E is waiting for, it is the head of that same
        # syllable, so MATRA_E is emitted behind it
        self.halftokens = set(['REPH'])

        self.composeTokens = { \
            # ଆ is typed as ଅ and the ା of it and ୱ as ଓ and the ୱ that is
            # bound under a letter, and unicode has a character of its own
            # for each of the two
            ('A', 'MATRA_AA')      : 'AA', \
            ('O', 'SUBJOINED_WA')  : 'WA', \
        }

        # the two halves of a two part vowel sign, put back together once
        # the front half has jumped over the letter that stood between them
        self.joinTokens = { \
            ('MATRA_E', 'MATRA_AA')       : 'MATRA_O',  \
            ('MATRA_E', 'AI_LENGTH_MARK') : 'MATRA_AI', \
            ('MATRA_E', 'AU_LENGTH_MARK') : 'MATRA_AU', \
        }

    def is_letter(self, ustr):
        '''whether the string of a token is a letter or a cluster of them,
           which is what a vowel sign can sit on. A dead consonant is one
           too - it is the head of the syllable that follows it'''
        if not ustr:
            return False

        char = ustr[0]
        # the vowels and the consonants of the block, and the letters that
        # unicode puts behind the signs - ଡ଼ ଢ଼ ୟ ୠ ୡ - and ୱ. The second
        # range is written as escapes because two of its bounds are a
        # letter and a nukta rather than one character in the decomposed
        # form, and a comparison against a pair of characters would let
        # every vowel sign through
        return '\u0b05' <= char <= '\u0b39' or \
               '\u0b5c' <= char <= '\u0b61' or char == '\u0b71'

    def split_danda(self, tokentypes):
        '''the ା that stands for the danda. A vowel sign never starts a
           word, so a ା that no letter carries is the upright stroke that
           ends a sentence - see the class comment'''
        out = []
        for i, tokenName in enumerate(tokentypes):
            prev = tokentypes[i - 1] if i > 0 else None

            # a consonant that is bound under a letter stands between that
            # letter and the vowel sign of it, ଗ୍ରା being ଗ, ୍ର and ା, so a
            # ା behind one of those is carried by a letter too
            if tokenName == 'MATRA_AA' and prev not in self.lettertokens \
                    and prev not in self.subjointokens:
                tokenName = 'DANDA'

            out.append(tokenName)
        return out

    def to_unicode(self, data):
        '''the passes in the order this font needs them: the ା that stands
           for the danda is read out of the word it starts before anything
           moves, and the two halves of େ, ୈ and ୌ are joined after the
           front half has jumped over its letter, the letter having stood
           between them until then'''
        tokentypes = self.tokenize(data.replace(self.SPACER, ''))

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
        t_A              = pat('A')
        t_I              = pat('B')
        t_U              = pat('D')
        t_E              = pat('F')
        t_O              = pat('H')

        # CONSONANTS
        t_KA             = pat('L')
        t_KHA            = pat('Q')
        t_GA             = pat('S')
        t_GHA            = pat('W')

        t_CA             = pat('`')
        t_CHA            = pat('d')
        t_JA             = pat('f')
        t_JHA            = pat('l')

        t_TTA            = pat('s')
        t_TTHA           = pat('v')
        t_DDA            = pat('x')
        t_NNA            = pat('~')

        t_TA             = pat('†')
        t_THA            = pat('$')
        t_DA             = pat('’')
        t_DHA            = pat('™')
        t_NA             = pat('[')

        t_PA             = pat('¨')
        t_PHA            = pat('ü')
        t_BA             = pat('¯')
        t_BHA            = pat('µ')
        t_MA             = pat('þ')

        t_YA             = pat('¾')
        t_RA             = pat('À')
        t_LA             = pat('à')
        t_LLA            = pat('Á')
        t_SHA            = pat('É')
        t_SSA            = pat('Ì')
        t_SA             = pat('Ó')
        t_HA             = pat('Ü')

        t_RRA            = pat('Ý')
        t_YYA            = pat('ß')

        # CONJUNCTS, each of them a ligature of its own in the font
        t_KA_TA          = pat('N')
        t_KA_SA          = pat('O')
        t_KA_SSA         = pat('ä')

        t_NGA_KA         = pat('Z')
        t_NGA_GA         = pat('è')

        t_CA_CHA         = pat('b')
        t_JA_NYA         = pat('j')
        t_NYA_CA         = pat('o')
        t_NYA_JA         = pat('ƒ')

        t_NNA_TTHA       = pat('=')
        t_NNA_NNA        = pat('‚')

        t_TA_TA          = pat('ˆ')
        t_DA_DA          = pat('”')
        t_DHA_YYA        = pat('š')

        t_NA_TA          = pat(';')
        t_NA_DA          = pat('¢')
        t_NA_DHA         = pat('¤')
        t_NA_TA_RA       = pat('¦')

        t_PA_TA          = pat('©')
        t_MA_PA          = pat('¸')
        t_MA_BA          = pat('º')
        t_MA_BHA         = pat('»')
        t_LLA_PA         = pat('Å')

        t_SHA_CA         = pat('Ê')
        t_SSA_NNA        = pat('Ð')
        t_SA_TA          = pat('Ö')
        t_SA_THA         = pat('×')

        # SUBJOINED CONSONANTS, the ones odiya draws as a mark of their own
        # under the letter they are bound to
        t_SUBJOINED_GA   = pat('V')
        t_SUBJOINED_NA   = pat('§')
        t_SUBJOINED_MA   = pat('½')
        t_SUBJOINED_YYA  = pat('¿')
        t_SUBJOINED_RA   = pat('÷')
        t_SUBJOINED_LA   = pat('â')
        t_SUBJOINED_WA   = pat('´')

        # MATRAS. ି is drawn over the letter for most of the alphabet and
        # under it for ଖ, ଥ and ଧ, and the two shapes are one token here
        t_MATRA_AA       = pat('æ')
        t_MATRA_I        = pat('ç', '#')
        t_MATRA_II       = pat('ê')
        t_MATRA_U        = pat('ë')
        t_MATRA_UU       = pat('í')
        t_MATRA_VOCALIC_R = pat('õ')
        # the front half of ୋ, ୈ and ୌ, which the font draws in front of
        # the letter, and the back halves of ୈ and ୌ. The back half of ୋ is
        # the ା above
        t_MATRA_E        = pat('{')
        t_AI_LENGTH_MARK = pat('ð')
        t_AU_LENGTH_MARK = pat('ò')

        # SIGNS. ଁ has a wide glyph and a narrow one, as ି has two shapes
        t_REPH           = pat('ö')
        t_ANUSVARA       = pat('ó')
        t_CANDRABINDU    = pat('ô', ']')
        t_DANDA          = pat('>')

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
        t_SLASH          = pat('/')
        t_COLON          = pat(':')
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
