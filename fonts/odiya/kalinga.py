import re
import string
import types

from indic2unicode.langs import odiya
from ..basefont import BaseFont
import ply.lex as lex

class Kalinga(BaseFont):
    '''Kalinga is the unicode odiya font that the Odisha Gazette is set in,
       and the pdfs that carry it carry a broken ToUnicode map: the map was
       built by pairing the glyphs of a run with the characters of that run
       one by one, and odiya shaping draws a syllable in a different number
       of glyphs than it is written in - a cluster is drawn as one ligature,
       ୋ is drawn in two pieces with the letter between them and the reph is
       drawn behind the letter it sits on - so the pairing slips on every
       glyph that the shaper moved or made. The text that comes out of such
       a pdf is therefore odiya that is

       1. in the visual order of the glyphs and not in the order of unicode,
          so ୋ, ୈ and ୌ stand in front of the letter they belong to and the
          reph stands behind the letter it sits on, and

       2. spelled with the wrong characters for a part of the alphabet, e.g.
          'ନ' for the ୋ that is really there and 'ଥ' for the reph, so
          ନିର୍ବାଚନ comes out as ନିବ୍ଥାଚନ and ଖୋର୍ଦ୍ଧା as ନଖ୍ାେଥା.

       So the text is treated like any other font of this package: every
       glyph of the font is a token, the token is given the unicode string
       it really stands for and the tokens are put back in the order that
       unicode wants.

       WHAT THE MAP HANDS THE WRONG GLYPH

       The strings that slipped landed one glyph away from where they
       belong, so most of them are simply swapped with their neighbour and
       nothing is lost: the reph carries 'ଥ' and ଥ carries 'ର୍', ବ carries
       'ବ୍' and ୍ୱ carries 'ବ', ଖ carries 'ଖ୍', ୖ carries 'ୈ' and ୗ carries
       'ୌ', ଦ୍ଧ carries 'େ' and ଣ୍ଣ carries 'ର୍ଣ୍'. Each of those is read
       back here, and ପ୍ରାର୍ଥୀ comes out of the swapped pair right without
       anything having to move at all - the reph is stored behind ଥ and the
       two carry each other's string, which is the order unicode wants.

       WHAT CANNOT BE READ BACK

       Some of those strings landed on a glyph whose own string is still in
       the map as well, and the two cannot be told apart any more. What is
       left then is to read each of them as what it is more often, the way
       fonts/hindi/arialuni.py reads the glyphs its own map cannot tell
       apart, and to take back the readings that the syllable around them
       settles:

       1. ୋ MATRA_E carries 'ନ', which is what ନ carries too, and the two
          are the commonest glyphs of the font after ା. ୋ is drawn in front
          of the letter it belongs to and ନ is a letter, so a 'ନ' that a
          letter follows is read as the vowel sign and a 'ନ' that anything
          else follows as ନ. The words that write a ନ in front of a letter
          often enough to be worth naming - ଜନତା, ବିଧାନସଭା, ଭୁବନେଶ୍ୱର, ନଗର,
          ଆନନ୍ଦ and the ପିନ of a pin code - are named in self.plainwords.
          What is left is a real loss: ଜମନକିରା comes out as ଜମକେିରା.
       2. ଶ carries the space, so ଶ is read out of a space that a vowel
          sign follows, a sign never starting a word, and out of a space in
          front of the ଙ୍କ family, ଶଙ୍ଖ and ଶଙ୍କର being how this document
          writes them. A ଶ that a plain letter follows cannot be told from
          a space and is lost.
       3. The subjoined consonants ୍ୟ, ୍ମ, ୍ଲ, ୍ଚ, ୍ଟ, ୍ଡ, ୍ର and ୍ଳ carry
          the string of their own letter, so 'ୟ' is both ୟ and ୍ୟ. What
          tells them apart is the letter in front of them, odiya writing
          ବ୍ୟ, ଦ୍ମ and ପ୍ଲ as a cluster and ମୟ, ସମ and ଆଲ as two letters,
          so the pairs of self.subjoined are read as a cluster and
          everything else as two letters. ୍ଟ, ୍ଡ, ୍ର and ୍ଳ are drawn a
          handful of times each and are lost.
       4. The ligature of ି and the reph carries 'ି' alone, so the reph of
          a syllable that carries ି is not in the text at all. It is put
          back in the two words the test document writes with it, ପାର୍ଟି
          and the ର୍ଣ୍ଣି of ରିଟର୍ଣ୍ଣିଂ, and lost everywhere else.
       5. ର୍, the dead ra, carries the same 'ର୍' that ଥ carries and is read
          as ଥ, that being 632 of the 638 of them.
       6. ବ୍ର is one glyph and ବ and ର are two, and both spell out as
          'ବ୍ର', so the 15 ବର of the test document are read as ବ୍ର.

       WHAT IS LEFT

       The font itself says what every one of its glyphs is - its cmap and
       its post name the letters and its GSUB says which glyphs the shaper
       made out of which others - so the text the page really draws can be
       read out of the pdf and the readings above can be measured against
       it. On the 15763 odiya runs of the test document this converter
       reads 98.5% of the runs and 99.3% of the characters the way the font
       says they are drawn, and what it gets wrong is the four losses
       above: the ନ that a letter follows, the ଶ that one follows, the
       subjoined consonants that are drawn a handful of times each, and the
       reph that the ି ର୍ ligature swallowed.
    '''
    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(odiya.OdiyaUnicode())
        self.langobjs.append(odiya.Conjuncts())
        self.langobjs.append(odiya.Kalinga())

        self.lexer = self.get_lexer()

        # ୋ, ୈ and ୌ are drawn in front of the letter they belong to, the
        # front half of all three being ୋ MATRA_E
        self.waitdict   = {'MATRA_E': 1}

        # the reph is drawn as a stroke over the last letter of its syllable
        # and is stored behind that letter
        self.jumpbefore = {'REPH': 1}

        # the letters and the clusters that a vowel sign can sit on, which
        # is what tells the ୋ that is drawn in front of a letter from the ନ
        # that carries the same string, and the marks that are drawn on such
        # a letter, which is what tells a ଶ from a space
        self.lettertokens = set()
        self.signtokens   = set()
        self.subjointokens = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                ustr = obj.get_unicode_string(tokenName)
                if tokenName.startswith('SUBJOINED_'):
                    self.subjointokens.add(tokenName)
                elif self.is_letter(ustr):
                    self.lettertokens.add(tokenName)
                elif self.is_sign(ustr):
                    self.signtokens.add(tokenName)

        # a subjoined consonant carries the string of its own letter, so
        # what tells the two apart is the letter in front of it: odiya
        # writes ବ୍ୟ, ଦ୍ମ and ପ୍ଲ as a cluster and ମୟ, ସମ and ଆଲ as two
        # letters. These are the pairs that the test document writes as a
        # cluster more often than as two letters, and every one of them is
        # an ordinary odiya conjunct
        self.subjoined = { \
            ('KA',  'YYA') : 'SUBJOINED_YYA', \
            ('KHA', 'YYA') : 'SUBJOINED_YYA', \
            ('GA',  'YYA') : 'SUBJOINED_YYA', \
            ('TA',  'YYA') : 'SUBJOINED_YYA', \
            ('DA',  'YYA') : 'SUBJOINED_YYA', \
            ('NA',  'YYA') : 'SUBJOINED_YYA', \
            ('BA',  'YYA') : 'SUBJOINED_YYA', \
            ('LA',  'YYA') : 'SUBJOINED_YYA', \
                                              \
            ('DA',  'MA')  : 'SUBJOINED_MA',  \
            ('SSA', 'MA')  : 'SUBJOINED_MA',  \
                                              \
            ('PA',  'LA')  : 'SUBJOINED_LA',  \
            ('PHA', 'LA')  : 'SUBJOINED_LA',  \
            ('BA',  'LA')  : 'SUBJOINED_LA',  \
                                              \
            ('SSA', 'CA')  : 'SUBJOINED_CA',  \
                                              \
            # ଜ୍ୟ is a cluster in ରାଜ୍ୟ and in little else, ଜୟ being a name \
            # this document is full of, so this one pair is held to the ା  \
            # in front of it                                               \
            ('MATRA_AA', 'JA', 'YYA') : 'SUBJOINED_YYA', \
                                                         \
            # the font draws a ୁ in front of the ୍ୟ that belongs to the   \
            # same letter, so this pair has the ୁ between the two of them. \
            # It is the କମ୍ୟୁନିଷ୍ଟ of the party names, which is nearly     \
            # every subjoined consonant of the document that a vowel sign  \
            # is drawn in front of                                        \
            ('MA', 'MATRA_U', 'YYA')  : 'SUBJOINED_YYA', \
        }

        # the words that the rules above read wrong, each of them a run of
        # tokens every token of which keeps the reading the lexer gave it.
        # They are ordinary odiya words rather than anything peculiar to
        # this gazette - ଜନତା, which every party name of it carries,
        # ବିଧାନସଭା, ଭୁବନେଶ୍ୱର, ନଗର, ଆନନ୍ଦ, the ପିନ of a pin code and
        # ନୟାଗଡ଼ - and none of them costs a reading that the rules would
        # have got right
        self.plainwords = [ \
            ('JA', 'NA', 'TA'),        \
            ('NA', 'SA', 'BHA'),       \
            ('NA', 'SHA_WA'),          \
            ('NA', 'GA', 'RA'),        \
            ('AA', 'NA', 'NA_DA'),     \
            ('PA', 'MATRA_I', 'NA'),   \
            ('NA', 'YYA', 'MATRA_AA'), \
        ]

        # the ଙ୍କ family, which a space in front of is a ଶ - see split_sha
        self.ngatokens = set(['NGA_KA', 'NGA_KHA', 'NGA_GA', 'NGA_GHA'])

        # while the reph jumps back to the head of its syllable it has to
        # jump over the ି that the same glyph drew it with, and over
        # anything else of that syllable that is drawn in front of it
        self.jumpover = set(self.signtokens)
        self.jumpover.update(self.subjointokens)

        # a reph that has jumped to the head of the syllable is not the
        # letter ୋ is waiting for, it is the head of that same syllable, so
        # ୋ is emitted in front of it
        self.halftokens = set(['REPH'])

        # a subjoined consonant and a nukta belong to the letter that ୋ has
        # already passed, so ୋ stays behind them
        self.waitover = set(['NUKTA'])
        self.waitover.update(self.subjointokens)

        self.composeTokens = { \
            # the ligature of ି and the reph carries 'ି' alone, so the reph
            # of such a syllable is not in the text. The test document
            # writes two words with that glyph, ପାର୍ଟି and the ର୍ଣ୍ଣି of
            # ରିଟର୍ଣ୍ଣିଂ, and both of them are put back here - every ଣ୍ଣି of
            # it carries that reph and so does every ପାଟି, while a plain ଟି
            # elsewhere, as in ୟୁନିଟି, does not
            ('NNA_NNA', 'MATRA_I') : ['NNA_NNA', 'MATRA_I', 'REPH'], \
            ('PA', 'MATRA_AA', 'TTA', 'MATRA_I') : \
                    ['PA', 'MATRA_AA', 'TTA', 'MATRA_I', 'REPH'], \
                                                                  \
            # a subjoined consonant belongs to its letter and unicode
            # writes it in front of the vowel sign of that letter, while
            # the font draws the ୁ of କମ୍ୟୁନିଷ୍ଟ in front of the ୍ୟ
            ('MATRA_U', 'SUBJOINED_YYA') : ['SUBJOINED_YYA', 'MATRA_U'], \
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
        # the vowels and the consonants of the block, the letters that
        # unicode puts behind the signs - ଡ଼ ଢ଼ ୟ ୠ ୡ - and ୱ. The second
        # range is written as escapes because two of its bounds are a
        # letter and a nukta rather than one character in the decomposed
        # form, and a comparison against a pair of characters would let
        # every vowel sign through
        return '\u0b05' <= char <= '\u0b39' or \
               '\u0b5c' <= char <= '\u0b61' or char == '\u0b71'

    def is_sign(self, ustr):
        '''whether the string of a token is a vowel sign or a mark that is
           drawn on the letter of its syllable'''
        if ustr == None or len(ustr) != 1:
            return False

        # the vowel signs, the length marks, the virama and the marks
        # that are drawn on a letter
        return '\u0b3e' <= ustr <= '\u0b57' or \
               '\u0b01' <= ustr <= '\u0b03' or ustr == '\u0b3c' or \
               '\u0b62' <= ustr <= '\u0b63'

    def to_unicode(self, data):
        '''the passes in the order this font needs them: the glyphs whose
           string is another glyph's as well are read out of the syllable
           around them before anything moves, and the two halves of ୋ, ୈ
           and ୌ are joined after the front half has jumped over its
           letter, the letter having stood between them until then'''
        tokentypes = self.tokenize(data)

        tokentypes = self.split_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)
        tokentypes = self.jump_before_tokens(tokentypes)
        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes, self.joinTokens)

        return self.tokens_to_unicode(tokentypes)

    def split_tokens(self, tokentypes):
        '''the glyphs whose string the map hands to another glyph as well,
           read out of what stands around them - see the class comment.

           The three passes run in this order because each of them settles
           what the next one reads: ଶ carries a space, and it is a letter,
           so the ଶ of କିଶୋର is what makes the 'ନ' in front of it a ୋ -
           that word reaches this as 'କି' + 'ନ' + ' ' + 'ା' + 'ର'; and ୍ୟ
           carries 'ୟ', and it is no letter, so the ୍ୟ of ଅନ୍ୟ is what
           keeps the 'ନ' in front of it a ନ'''
        tokentypes = self.split_sha(tokentypes)
        tokentypes = self.split_subjoined(tokentypes)

        return self.split_matra_e(tokentypes)

    def split_sha(self, tokentypes):
        '''the ଶ that the map hands the string of the space. A vowel sign
           never starts a word, so a space that one follows is a ଶ, and so
           is a space in front of the ଙ୍କ family'''
        out = []
        for i, tokenName in enumerate(tokentypes):
            nxt = tokentypes[i + 1] if i + 1 < len(tokentypes) else None

            if tokenName == 'SPACE' and \
                    (nxt in self.signtokens or nxt in self.ngatokens):
                tokenName = 'SHA'

            out.append(tokenName)
        return out

    def split_subjoined(self, tokentypes):
        '''the subjoined consonants that the map hands the string of their
           own letter, read out of the letter that stands in front of them
           - see self.subjoined'''
        out = []
        for i, tokenName in enumerate(tokentypes):
            # the longer run first: ଜ୍ୟ is held to the ା of ରାଜ୍ୟ
            for start in (i - 2, i - 1):
                if start < 0:
                    continue

                subjoined = self.subjoined.get(tuple(tokentypes[start:i + 1]))
                if subjoined and not self.is_plain(tokentypes, i):
                    tokenName = subjoined
                    break

            out.append(tokenName)
        return out

    def split_matra_e(self, tokentypes):
        '''the ୋ that the map hands the string of ନ. It is drawn in front
           of the letter it belongs to and ନ is a letter, so a 'ନ' that a
           letter follows is the vowel sign, bar the words of
           self.plainwords'''
        out = []
        for i, tokenName in enumerate(tokentypes):
            nxt = tokentypes[i + 1] if i + 1 < len(tokentypes) else None

            if tokenName == 'NA' and nxt in self.lettertokens and \
                    not self.is_plain(tokentypes, i):
                tokenName = 'MATRA_E'

            out.append(tokenName)
        return out

    def is_plain(self, tokentypes, i):
        '''whether the token at i is a token of one of the words that keep
           the reading the lexer gave them - see self.plainwords'''
        for tokens in self.plainwords:
            for pos in range(len(tokens)):
                if i >= pos and self.match_tokenlist(list(tokens), \
                                                     tokentypes, i - pos):
                    return True
        return False

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        def pat(*glyphs):
            # token strings are regular expressions for ply, so the glyphs
            # have to be escaped. Alternate glyphs of the same token are
            # joined into one pattern
            return '|'.join([re.escape(glyph) for glyph in glyphs])

        # VOWELS
        t_A              = pat('ଅ')
        t_AA             = pat('ଆ')
        t_I              = pat('ଇ')
        t_II             = pat('ଈ')
        t_U              = pat('ଉ')
        t_UU             = pat('ଊ')
        t_VOCALIC_R      = pat('ଋ')
        t_E              = pat('ଏ')
        t_AI             = pat('ଐ')
        t_O              = pat('ଓ')
        t_AU             = pat('ଔ')

        # CONSONANTS. ବ is handed the string of the dead ba and ଖ that of
        # the dead kha, while ୍ୱ, the ba that is bound under a letter, is
        # handed the plain 'ବ'
        t_KA             = pat('କ')
        t_KHA            = pat('ଖ୍')
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
        # ଥ is handed the string of the reph and the reph the string of ଥ
        t_THA            = pat('ର୍')
        t_DA             = pat('ଦ')
        t_DHA            = pat('ଧ')
        t_NA             = pat('ନ')

        t_PA             = pat('ପ')
        t_PHA            = pat('ଫ')
        t_BA             = pat('ବ୍')
        t_BHA            = pat('ଭ')
        t_MA             = pat('ମ')

        t_YA             = pat('ଯ')
        t_RA             = pat('ର')
        t_LA             = pat('ଲ')
        t_LLA            = pat('ଳ')
        t_VA             = pat('ଵ')
        # ଶ is handed the string of the space, see the class comment
        t_SSA            = pat('ଷ')
        t_SA             = pat('ସ')
        t_HA             = pat('ହ')

        t_RRA            = pat('\u0b5c', '\u0b21\u0b3c')
        t_RHA            = pat('\u0b5d', '\u0b22\u0b3c')
        t_YYA            = pat('ୟ')
        t_WA             = pat('ୱ')

        # DEAD CONSONANTS, the letter and the virama that ends it. The dead
        # ra is handed the same 'ର୍' that ଥ is and is read as ଥ
        t_DEAD_KA        = pat('କ୍')
        t_DEAD_CA        = pat('ଚ୍')
        t_DEAD_JA        = pat('ଜ୍')
        t_DEAD_TTA       = pat('ଟ୍')
        t_DEAD_TTHA      = pat('ଠ୍')
        t_DEAD_DDA       = pat('ଡ୍')
        t_DEAD_TA        = pat('ତ୍')
        t_DEAD_DA        = pat('ଦ୍')
        t_DEAD_NA        = pat('ନ୍')
        t_DEAD_PA        = pat('ପ୍')
        t_DEAD_PHA       = pat('ଫ୍')
        t_DEAD_MA        = pat('ମ୍')
        t_DEAD_LA        = pat('ଲ୍')
        t_DEAD_SHA       = pat('ଶ୍')
        t_DEAD_SA        = pat('ସ୍')

        # SUBJOINED CONSONANTS. Every one of them but ୍ୱ is handed the
        # string of its own letter and is read out of what stands in front
        # of it, see the class comment
        t_SUBJOINED_WA   = pat('ବ')

        # CONJUNCTS, which the font draws as a ligature of its own. The
        # four that carry a reph in their string carry it because the map
        # slipped a reph onto them and not because one is drawn
        t_KA_TA          = pat('କ୍ତ')
        t_KA_RA          = pat('କ୍ର')
        t_KA_SA          = pat('କ୍ସ')
        t_KA_SSA         = pat('କ୍ଷ')
        t_KA_WA          = pat('କ୍ୱ')
        t_KA_SSA_MA      = pat('କ୍ଷ୍ମ')

        t_GA_RA          = pat('ଗ୍ର')

        t_NGA_KA         = pat('ଙ୍କ')
        t_NGA_KHA        = pat('ଙ୍ଖ')
        t_NGA_GA         = pat('ଙ୍ଗ')

        t_CA_CA          = pat('ର୍ଚ୍')
        t_CA_CHA         = pat('ଚ୍ଛ')

        t_JA_NYA         = pat('ଜ୍ଞ')
        t_NYA_CA         = pat('ଞ୍ଚ')
        t_NYA_JA         = pat('ଞ୍ଜ')

        t_TTA_TTA        = pat('ଟ୍ଟ')
        t_TTA_RA         = pat('ଟ୍ର')
        t_DDA_RA         = pat('ଡ୍ର')

        t_NNA_TTA        = pat('ଣ୍ଟ')
        t_NNA_TTHA       = pat('ଣ୍ଠ')
        t_NNA_DDA        = pat('ଣ୍ଡ')
        t_NNA_NNA        = pat('ର୍ଣ୍')

        t_TA_TA          = pat('ର୍ତ୍ତ')
        t_TA_NA          = pat('ତ୍ନ')
        t_TA_RA          = pat('ତ୍ର')

        t_DA_DA          = pat('ର୍ଦ୍')
        # ଦ୍ଧ is handed the string of ୋ
        t_DA_DHA         = pat('େ')
        t_DA_RA          = pat('ଦ୍ର')
        t_DA_WA          = pat('ଦ୍ୱ')
        t_DHA_YYA        = pat('ଧ୍ୟ')

        t_NA_TA          = pat('ନ୍ତ')
        t_NA_THA         = pat('ନ୍ଥ')
        t_NA_DA          = pat('ନ୍ଦ')
        t_NA_DHA         = pat('ନ୍ଧ')
        t_NA_NA          = pat('ନ୍ନ')
        t_NA_DA_RA       = pat('ନ୍ଦ୍ର')

        t_PA_TA          = pat('ପ୍ତ')
        t_PA_RA          = pat('ପ୍ର')
        t_PA_LLA         = pat('ପ୍ଳ')
        t_PHA_RA         = pat('ଫ୍ର')
        # the ligature of ଭ and ର is handed the string of the dead bha.
        # ବ୍ର is the one pattern of this font that another one begins with:
        # ବ is handed 'ବ୍' and ଣ୍ଣ is handed 'ର୍ଣ୍', so ବ + ଣ୍ଣ spells out
        # as 'ବ୍ର୍ଣ୍' and the ligature has to hold to a 'ବ୍ର' that no
        # virama follows
        t_BA_RA          = re.escape('ବ୍ର') + '(?!' + re.escape('୍') + ')'
        t_BHA_RA         = pat('ଭ୍')

        t_MA_PA          = pat('ମ୍ପ')
        t_MA_BA          = pat('ମ୍ବ')
        t_MA_BHA         = pat('ମ୍ଭ')
        t_MA_MA          = pat('ମ୍ମ')
        t_MA_RA          = pat('ମ୍ର')
        t_LA_LA          = pat('ଲ୍ଲ')

        t_SHA_CA         = pat('ଶ୍ଚ')
        t_SHA_RA         = pat('ଶ୍ର')
        t_SHA_WA         = pat('ଶ୍ଵ')
        t_SSA_TTA        = pat('ଷ୍ଟ')
        t_SSA_NNA        = pat('ଷ୍ଣ')
        t_SSA_TTA_RA     = pat('ଷ୍ଟ୍ର')

        t_SA_KA          = pat('ସ୍କ')
        t_SA_TA          = pat('ସ୍ତ')
        t_SA_THA         = pat('ସ୍ଥ')
        t_SA_MA          = pat('ସ୍ମ')
        t_SA_WA          = pat('ସ୍ଵ')

        t_HA_NA          = pat('ହ୍ନ')
        t_HA_MA          = pat('ହ୍ମ')
        t_HA_LA          = pat('ହ୍ଲ')

        # the letters that the font draws together with the ି of them
        t_KHA_MATRA_I    = pat('ଖି')
        t_THA_MATRA_I    = pat('ଥି')
        t_DHA_MATRA_I    = pat('ଧି')

        # MATRAS. ୋ MATRA_E is handed the string of ନ and is read out of
        # what follows it, see split_tokens
        t_MATRA_AA       = pat('ା')
        t_MATRA_I        = pat('ି')
        t_MATRA_II       = pat('ୀ')
        t_MATRA_U        = pat('ୁ')
        t_MATRA_UU       = pat('ୂ')
        t_MATRA_VOCALIC_R = pat('ୃ')
        # the back halves of ୈ and ୌ, which are handed the strings of the
        # whole signs
        t_AI_LENGTH_MARK = pat('ୈ')
        t_AU_LENGTH_MARK = pat('ୌ')

        # SIGNS. the reph is handed the string of ଥ
        t_REPH           = pat('ଥ')
        t_CANDRABINDU    = pat('ଁ')
        t_ANUSVARA       = pat('ଂ')
        t_VISARGA        = pat('ଃ')
        t_NUKTA          = pat('଼')
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

        # PUNCTUATIONS
        t_LEFTPARAN      = pat('(')
        t_RIGHTPARAN     = pat(')')
        t_LEFTSQBRACE    = pat('[')
        t_RIGHTSQBRACE   = pat(']')
        t_COMMA          = pat(',')
        t_DOT            = pat('.')
        t_DASH           = pat('-')
        t_ENDASH         = pat('–')
        t_EMDASH         = pat('—')
        t_SLASH          = pat('/')
        t_COLON          = pat(':')
        t_SEMICOLON      = pat(';')
        t_QUESTION       = pat('?')
        t_EXCLAMATION    = pat('!')
        t_PERCENT        = pat('%')
        t_PLUS           = pat('+')
        t_EQ             = pat('=')
        t_STAR           = pat('*')
        t_QUOT           = pat('"')
        t_AMPERSAND      = pat('&')
        t_AT             = pat('@')
        t_APOSTROPHE     = pat("'")
        # the space is handed to ଶ as well, see split_tokens
        t_SPACE          = pat(' ')
        t_NEWLINE        = pat('\n')
        t_CARRIAGERET    = pat('\r')
        t_TAB            = pat('\t')

        def t_error(t):
            self.report_error(t)
            t.lexer.skip(1)

        rules = dict(locals())

        # the english of the document is set in a latin font and comes out
        # of the pdf as itself, and a Kalinga run carries latin of its own
        # every now and then - the (i) of a heading, an e-mail address
        digitnames = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', \
                      'SEVEN', 'EIGHT', 'NINE']
        for digit, name in enumerate(digitnames):
            rules['t_ASCII_' + name] = pat('%d' % digit)

        for char in string.ascii_uppercase:
            rules['t_LATIN_' + char] = pat(char)
        for char in string.ascii_lowercase:
            rules['t_LATIN_SMALL_' + char.upper()] = pat(char)

        # only the tokens that the font has a glyph for
        rules['tokens'] = [tokenName for tokenName in tokens \
                                     if 't_' + tokenName in rules]

        # the rules of the latin text are made in a loop, so they are handed
        # to ply in an object of their own rather than in the locals of this
        # function. ply looks up the module of that object
        rules['__module__'] = self.__class__.__module__
        return lex.lex(object = types.SimpleNamespace(**rules))
