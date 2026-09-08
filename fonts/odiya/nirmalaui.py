import re
import types

from indic2unicode.langs import odiya
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class NirmalaUIOdiyaGlyphs(BaseFont):
    '''The odiya of a pdf set in Nirmala UI whose ToUnicode map has been
       repaired by tools/fix_tounicode.py, the Odisha Gazette being set in
       Nirmala UI as well as in Kalinga. Every glyph now carries the
       characters it really stands for - ଜ and ବ, which the broken map hands
       the 'ର୍' of the reph to both of, the reph itself, the ୋ that is drawn
       in front of its letter and the ୟ that is handed a space are all back -
       so nothing of the text is lost any more, unlike fonts/odiya/kalinga.py,
       which works on the text of a pdf whose map is still broken.

       What is left is the order, because the glyphs are stored in the order
       in which they are drawn and odiya draws two things elsewhere than
       unicode writes them:

       1. ୋ, ୈ and ୌ are drawn in front of the letter they belong to, and the
          front half of all three is the same େ MATRA_E glyph. ୋ is that
          glyph and the ା behind the letter, ୈ is that glyph and ୖ, ୌ is that
          glyph and ୗ, so the two halves are joined back into one character
          once the front half has jumped over its letter. ଘୋଷଣା comes out of
          the repaired pdf as େଘାଷଣା, ଦୈନିକ as େଦୖନିକ and ମୌଜାରେ as େମୗଜାେର.
       2. The reph, the ର୍ that odiya draws as a stroke over its syllable, is
          stored behind the letter it sits on and unicode writes it in front
          of that letter - ସର୍ବ comes out as ସବର୍, ଆଦର୍ଶ as ଆଦଶର୍ and ଖର୍ଚ୍ଚ
          as ଖଚ୍ଚର୍.

       Everything else is stored in the order unicode wants it, ି included:
       odiya draws ି over the letter and to the left of it and the font gives
       the glyph a negative side bearing to carry it there, so it is stored
       behind its letter like any other sign.

       WHAT THE FONT DRAWS WHOLE AND WHAT IT SPELLS OUT

       Nirmala UI has a ligature for most of the clusters this gazette
       writes, from ନ୍ତ and ଙ୍କ to ସ୍ତ୍ର and କ୍ଷ୍ମ, and each of those is one
       glyph and one token. A cluster it has no ligature for is drawn as a
       half form and a form of the letter that follows - ପଦ୍ମ is ଦ୍ and ମ,
       ନିମ୍ନ is ମ୍ and ନ - and the two spell the cluster out, so the lexer
       reads it as one token all the same and a sign that jumps over the
       cluster jumps over the whole of it.

       The vowel sign of such a cluster is drawn over its half form rather
       than behind the whole of it, ରଶ୍ମିତା coming out as ରଶ୍ + ି + ମତା, and
       join_halves() puts it back behind the letter it belongs to.

       THE REPH AND THE DEAD RA

       The reph is spelled with the same two characters as a dead ra, so the
       repair writes langs/odiya.REPH_MARK behind it and the lexer holds the
       token to that mark. Without it the two could not be told apart in the
       text - a reph that ends a run of the pdf looks exactly like the dead
       ra that ends a word - and a dead ra would be carried off to the head
       of the syllable in front of it.

       WHAT THE EXTRACTOR PUTS IN THE MIDDLE OF A WORD

       pdftotext writes a space wherever a glyph is drawn back over the one
       before it, which is every mark of this font that has no width of its
       own: ଅଧିକାର comes out as "ଅଧ ିକାର" and ପୂର୍ବରୁ as "ପୂବ ର୍ ୁ". That
       space is no glyph of the font and a converter cannot tell it from a
       real one, so it is left where it is - but the reph steps over it on
       its way back to the head of its syllable, a reph never being the first
       thing in a word.
    '''
    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(odiya.OdiyaUnicode())
        self.langobjs.append(odiya.Conjuncts())

        self.lexer = self.get_lexer()

        # ୋ, ୈ and ୌ are drawn in front of the letter they belong to, the
        # front half of all three being େ MATRA_E
        self.waitdict   = {'MATRA_E': 1}

        # the reph is drawn as a stroke over the letter it belongs to and is
        # stored behind that letter
        self.jumpbefore = {'REPH': 1}

        # the half forms, which are the head of the cluster that follows
        # them, the consonants that odiya binds under a letter as a mark of
        # its own, the letters and clusters that a vowel sign can sit on,
        # and the signs themselves
        self.deadtokens    = set()
        self.subjointokens = set()
        self.lettertokens  = set()
        self.signtokens    = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                ustr = obj.get_unicode_string(tokenName)
                if tokenName.startswith('DEAD_'):
                    self.deadtokens.add(tokenName)
                elif tokenName.startswith('SUBJOINED_'):
                    self.subjointokens.add(tokenName)
                elif tokenName == 'REPH':
                    continue
                elif self.is_letter(ustr):
                    self.lettertokens.add(tokenName)
                elif self.is_sign(ustr):
                    self.signtokens.add(tokenName)

        # while the reph jumps back to the head of its syllable it has to
        # jump over the vowel signs and the marks of that syllable, over the
        # consonants that are bound under its letter, and over the space
        # that the extractor writes in the middle of a word - a reph is
        # never the first thing in a word, see the class comment
        self.jumpover = set(['SPACE'])
        self.jumpover.update(self.signtokens)
        self.jumpover.update(self.subjointokens)

        # a consonant that is bound under a letter belongs to the letter
        # MATRA_E has already passed, so MATRA_E stays behind it
        self.waitover = set(self.subjointokens)

        # a half form is not the letter MATRA_E is waiting for, it is the
        # head of the cluster that MATRA_E belongs to, and so is a reph that
        # has jumped to the head of the syllable
        self.halftokens = set(self.deadtokens)
        self.halftokens.add('REPH')

        # the two halves of a two part vowel sign, put back together once
        # the front half has jumped over the letter that stood between them
        self.joinTokens = { \
            ('MATRA_E', 'MATRA_AA')       : 'MATRA_O',  \
            ('MATRA_E', 'AI_LENGTH_MARK') : 'MATRA_AI', \
            ('MATRA_E', 'AU_LENGTH_MARK') : 'MATRA_AU', \
        }

    def to_unicode(self, data):
        '''the passes in the order this font needs them: the vowel sign that
           is drawn over a half form is put back behind the cluster before
           anything moves, and the two halves of ୋ, ୈ and ୌ are joined after
           the front half has jumped over its letter, the letter having
           stood between them until then'''
        tokentypes = self.tokenize(data)

        tokentypes = self.join_halves(tokentypes)
        tokentypes = self.jump_before_tokens(tokentypes)
        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes, self.joinTokens)

        return self.tokens_to_unicode(tokentypes)

    def is_letter(self, ustr):
        '''whether the string of a token is a letter or a cluster of them,
           which is what a vowel sign can sit on'''
        if not ustr:
            return False

        char = ustr[0]
        # the vowels and the consonants of the block, and the letters that
        # unicode puts behind the signs - ଡ଼ ଢ଼ ୟ ୠ ୡ - and ୱ. The second
        # range is written as escapes because two of its bounds are a letter
        # and a nukta rather than one character in the decomposed form, and
        # a comparison against a pair of characters would let every vowel
        # sign through
        return '\u0b05' <= char <= '\u0b39' or \
               '\u0b5c' <= char <= '\u0b61' or char == '\u0b71'

    def is_sign(self, ustr):
        '''whether the string of a token is a vowel sign or a mark that is
           drawn on the letter of its syllable'''
        if ustr == None or len(ustr) != 1:
            return False

        # the vowel signs, the length marks, the virama and the marks that
        # are drawn on a letter
        return '\u0b3e' <= ustr <= '\u0b57' or \
               '\u0b01' <= ustr <= '\u0b03' or ustr == '\u0b3c' or \
               '\u0b62' <= ustr <= '\u0b63'

    def join_halves(self, tokentypes):
        '''the vowel sign that stands between a half form and the letter it
           is bound to. A cluster the font has no ligature for is drawn as a
           half form and a form of its letter, and the vowel sign of that
           syllable is drawn over the half form rather than behind the whole
           cluster, so ରଶ୍ମିତା reaches this as ର + ଶ୍ + ି + ମ + ତା. A sign
           cannot sit on a half form, so one that does belongs behind the
           letter that follows it'''
        out = list(tokentypes)
        i   = 1
        while i < len(out):
            if out[i] in self.signtokens and out[i - 1] in self.deadtokens:
                # the letter of the cluster, over the space that the
                # extractor writes between the two every now and then -
                # "ରଶ୍ି ମତା" is one of them, see the class comment
                j = i + 1
                while j < len(out) and out[j] == 'SPACE':
                    j += 1

                if j < len(out) and out[j] in self.lettertokens:
                    # once the sign is out of the way the letter stands one
                    # place earlier, so this puts the sign behind it
                    out.insert(j, out.pop(i))
            i += 1
        return out

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        def pat(*strings):
            # token strings are regular expressions for ply, so what a glyph
            # says has to be escaped. The text of a repaired pdf is unicode
            # already, so the pattern of a token is the characters of that
            # token and not a byte the typist pressed
            return '|'.join([re.escape(string) for string in strings])

        # VOWELS
        t_A              = pat('ଅ')
        t_AA             = pat('ଆ')
        t_I              = pat('ଇ')
        t_II             = pat('ଈ')
        t_U              = pat('ଉ')
        t_UU             = pat('ଊ')
        t_VOCALIC_R      = pat('ଋ')
        t_VOCALIC_L      = pat('ଌ')
        t_E              = pat('ଏ')
        t_AI             = pat('ଐ')
        t_O              = pat('ଓ')
        t_AU             = pat('ଔ')

        # CONSONANTS
        t_KA             = pat('କ')
        t_KHA            = pat('ଖ')
        t_GA             = pat('ଗ')
        t_GHA            = pat('ଘ')
        t_NGA            = pat('ଙ')

        t_CA             = pat('ଚ')
        t_CHA            = pat('ଛ')
        t_JA             = pat('ଜ')
        t_JHA            = pat('ଝ')
        t_NYA            = pat('ଞ')

        t_TTA            = pat('ଟ')
        t_TTHA           = pat('ଠ')
        t_DDA            = pat('ଡ')
        t_DDHA           = pat('ଢ')
        t_NNA            = pat('ଣ')

        t_TA             = pat('ତ')
        t_THA            = pat('ଥ')
        t_DA             = pat('ଦ')
        t_DHA            = pat('ଧ')
        t_NA             = pat('ନ')

        t_PA             = pat('ପ')
        t_PHA            = pat('ଫ')
        t_BA             = pat('ବ')
        t_BHA            = pat('ଭ')
        t_MA             = pat('ମ')

        t_YA             = pat('ଯ')
        t_RA             = pat('ର')
        t_LA             = pat('ଲ')
        t_LLA            = pat('ଳ')
        t_VA             = pat('ଵ')
        t_SHA            = pat('ଶ')
        t_SSA            = pat('ଷ')
        t_SA             = pat('ସ')
        t_HA             = pat('ହ')
        t_YYA            = pat('ୟ')

        # CONJUNCTS. The font draws each of these as a ligature of its own
        # but for the five that follow them, which it spells out as a half
        # form and a form of the letter behind it - and either way the
        # cluster is one token here
        t_KA_TA          = pat('କ୍ତ')
        t_KA_RA          = pat('କ୍ର')
        t_KA_SSA         = pat('କ୍ଷ')
        t_KA_SSA_MA      = pat('କ୍ଷ୍ମ')

        t_GA_NA          = pat('ଗ୍ନ')
        t_GA_RA          = pat('ଗ୍ର')

        t_NGA_KA         = pat('ଙ୍କ')
        t_NGA_GA         = pat('ଙ୍ଗ')

        t_CA_CA          = pat('ଚ୍ଚ')
        t_CA_CHA         = pat('ଚ୍ଛ')

        t_JA_NYA         = pat('ଜ୍ଞ')
        t_NYA_CHA        = pat('ଞ୍ଛ')
        t_NYA_JA         = pat('ଞ୍ଜ')
        t_NYA_JHA        = pat('ଞ୍ଝ')

        t_TTA_TTA        = pat('ଟ୍ଟ')
        t_NNA_TTA        = pat('ଣ୍ଟ')
        t_NNA_DDA        = pat('ଣ୍ଡ')
        t_NNA_NNA        = pat('ଣ୍ଣ')

        t_TA_TA          = pat('ତ୍ତ')
        t_TA_RA          = pat('ତ୍ର')
        t_DA_DA          = pat('ଦ୍ଦ')
        t_DA_WA          = pat('ଦ୍ୱ')
        t_DHA_YYA        = pat('ଧ୍ୟ')

        t_NA_TA          = pat('ନ୍ତ')
        t_NA_TA_RA       = pat('ନ୍ତ୍ର')
        t_NA_THA         = pat('ନ୍ଥ')
        t_NA_DA          = pat('ନ୍ଦ')
        t_NA_DA_RA       = pat('ନ୍ଦ୍ର')
        t_NA_DHA         = pat('ନ୍ଧ')

        t_PA_RA          = pat('ପ୍ର')
        t_PA_LA          = pat('ପ୍ଲ')
        t_BA_RA          = pat('ବ୍ର')
        t_MA_BHA         = pat('ମ୍ଭ')
        t_LA_LA          = pat('ଲ୍ଲ')
        t_LLA_PA         = pat('ଳ୍ପ')

        t_SHA_RA         = pat('ଶ୍ର')
        t_SHA_WA         = pat('ଶ୍ୱ')
        t_SSA_TTA        = pat('ଷ୍ଟ')
        t_SSA_NNA        = pat('ଷ୍ଣ')
        t_SSA_PA         = pat('ଷ୍ପ')

        t_SA_KA          = pat('ସ୍କ')
        t_SA_TA          = pat('ସ୍ତ')
        t_SA_TA_RA       = pat('ସ୍ତ୍ର')
        t_SA_THA         = pat('ସ୍ଥ')
        t_SA_WA          = pat('ସ୍ୱ')

        t_HA_NA          = pat('ହ୍ନ')
        t_HA_MA          = pat('ହ୍ମ')

        # the clusters that the font has no ligature for and spells out as a
        # half form and a form of the letter behind it, ପଦ୍ମ and ନିମ୍ନ among
        # them
        t_DA_MA          = pat('ଦ୍ମ')
        t_MA_NA          = pat('ମ୍ନ')
        t_MA_BA          = pat('ମ୍ବ')
        t_SHA_MA         = pat('ଶ୍ମ')
        t_SSA_TTHA       = pat('ଷ୍ଠ')

        # SUBJOINED CONSONANTS, the ones odiya draws as a mark of their own
        # under the letter they are bound to
        t_SUBJOINED_NA   = pat('୍ନ')
        t_SUBJOINED_YYA  = pat('୍ୟ')

        # MATRAS. The front half of ୋ, ୈ and ୌ is େ MATRA_E, which the font
        # draws in front of the letter, and the back halves of the last two
        # are ୖ and ୗ - the back half of ୋ is the ା above
        t_MATRA_AA       = pat('ା')
        t_MATRA_I        = pat('ି')
        t_MATRA_II       = pat('ୀ')
        t_MATRA_U        = pat('ୁ')
        t_MATRA_UU       = pat('ୂ')
        t_MATRA_VOCALIC_R  = pat('ୃ')
        t_MATRA_VOCALIC_RR = pat('ୄ')
        t_MATRA_E        = pat('େ')
        t_AI_LENGTH_MARK = pat('ୖ')
        t_AU_LENGTH_MARK = pat('ୗ')

        # SIGNS. the reph carries the mark that tells it from a dead ra, see
        # the class comment
        t_REPH           = pat('ର୍' + odiya.REPH_MARK)
        t_CANDRABINDU    = pat('ଁ')
        t_ANUSVARA       = pat('ଂ')
        t_VISARGA        = pat('ଃ')
        t_VIRAMA         = pat('୍')
        t_DANDA          = pat('।')

        # DIGITS
        t_ZERO           = pat('୦')
        t_ONE            = pat('୧')
        t_TWO            = pat('୨')
        t_THREE          = pat('୩')
        t_FOUR           = pat('୪')
        t_FIVE           = pat('୫')
        t_SIX            = pat('୬')
        t_SEVEN          = pat('୭')
        t_EIGHT          = pat('୮')
        t_NINE           = pat('୯')

        # the space, which the reph steps over on its way back, and the
        # whitespace that the lines of the pdf are broken on
        t_SPACE          = pat(' ')
        t_NEWLINE        = pat('\n')
        t_CARRIAGERET    = pat('\r')
        t_TAB            = pat('\t')

        def t_error(t):
            # the text of a repaired pdf is unicode already and only its
            # order is wrong, so a character with no token of its own is not
            # a glyph waiting to be reordered, it is text - the latin of the
            # document, its punctuation, a bullet - and has to come out the
            # way it went in rather than be dropped. Only a glyph code that
            # no map could turn into a character is dropped, and that is
            # reported
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

        # a dead consonant, the letter and the virama that ends it. The font
        # draws the virama with a glyph of its own, so every letter of it can
        # carry one and all of them are here rather than the five half forms
        # this gazette draws
        for tokenName in odiya.CONSONANT_TOKENS:
            ustr = self.token_to_unicode(tokenName)
            if ustr != None:
                rules['t_DEAD_' + tokenName] = pat(ustr + '୍')

        # only the tokens that the font has a glyph for
        rules['tokens'] = [tokenName for tokenName in tokens \
                                     if 't_' + tokenName in rules]

        # the rules of the dead consonants are made in a loop, so they are
        # handed to ply in an object of their own rather than in the locals
        # of this function. ply looks up the module of that object
        rules['__module__'] = self.__class__.__module__
        return lex.lex(object = types.SimpleNamespace(**rules))
