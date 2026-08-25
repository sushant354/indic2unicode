import re
import types

from indic2unicode.langs import kannada
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class Nudi(BaseFont):
    '''The text of a pdf that is set in Nudi, the ascii kannada font family
       that the Karnataka gazette is published in. Every glyph of the font
       sits on a key of the keyboard, so the text of such a pdf is not
       kannada at all - it is the sequence of keys the typist pressed, and
       what comes out of the pdf is latin1: ಸಂಪುಟ is '¸ÀA¥ÀÄl' and ಕರ್ನಾಟಕ is
       'PÀ£ÁðlPÀ'.

       The font has a glyph for every piece a syllable of kannada is drawn
       out of, and the keys spell those pieces in the order they are drawn,
       which is the order kannada writes them in:

           [arkavattu of the syllable before] base [first half of the
           matra] vattu(s) [length mark] [signs] [arkavattu]

       while unicode wants the arkavattu of a syllable in front of its base
       and the whole matra behind the vattus. Every syllable of the text is
       read as a whole here and written out again in that order.

       WHAT THE PIECES ARE

       1. A consonant that carries the vowel a is written with the glyph of
          the letter and INHERENT_A, a mark that draws its head stroke and
          stands for no character of its own, so 'PÀ' is ಕ while 'Pï' - the
          same letter and the virama - is ಕ್.
       2. A consonant that the vowel sign i replaces the head stroke of is
          one glyph and not two, so ಕಿ is 'Q' and not 'P' and a sign. Those
          are the _I tokens of langs/kannada.py, each of them a consonant
          and the matra i.
       3. ಫ, ಭ and ಧ are ಪ, ಬ and ದ and a stroke on top, which the font
          draws as a glyph of its own - ASPIRATION on a letter that carries
          the vowel a and ASPIRATION_I on one that carries the vowel i, the
          two letters being different glyphs. They are put back together in
          composeTokens below.
       4. ಮ is the ವ glyph and a tail, and ಯ is the anusvara glyph, a stem
          and that same tail. The tail is the glyph that draws the vowel
          sign u as well, so a vowel sign of ಮ or ಯ that is drawn in front
          of the tail sits inside the letter: ಮ is 'ªÀÄ' and ಮೆ is 'ªÉÄ',
          both of them one token here. ವ takes a second glyph for its own
          vowel sign u so that ವು and ಮ stay apart, 'ªÀÅ' against 'ªÀÄ'.
       5. A few consonants are drawn with a second glyph when a matra
          follows that changes their shape, ಖ ಜ ಟ ಣ ಬ ಲ - ಖ is 'R' at the
          end of a word and 'S' in ಖೆ. Both glyphs are the same letter and
          are alternates of one token here.
       6. Every vattu is a glyph of its own, and so is the arkavattu. They
          are all different glyphs, and different again from ರ and from the
          virama, so nothing here has to guess what a virama between two
          consonants was - the text of a Nudi pdf says which of ಕ್ರ, ರ್ಕ
          and ಕ್ ರ was typed, where the text of a unicode font like Tunga
          does not.

       WHAT IS NOT KNOWN

       The pdfs this was built from draw 132 of the glyphs of the font and
       nothing says what the rest of them are. The vattus are laid out in
       the order of the alphabet over an unbroken run of keys, 0xCC to
       0xEE, so the twelve of them that these documents never use are read
       off that run. The letters are laid out in no order that holds, so a
       key that no document here presses has a token only where its
       neighbours leave one reading open - the thirteen vowels fill
       thirteen keys in the order of the alphabet, and ಙ and ಛಿ each fall
       in a single gap between the letters around them. What is left over
       is reported and dropped: ಝ, ಞ, ಢ, ಱ and ೞ have no token here, nor
       does the vowel sign i of ಙ, ಠ and ಢ.
    '''
    # the roman weights of Nudi (Nudi01e, Nudi05e) keep the latin digits on
    # the digit keys, the kannada weights (Nudi01k) draw the kannada digits
    # there instead, see NudiKannadaDigits below
    digittokens = ['ASCII_ZERO', 'ASCII_ONE', 'ASCII_TWO', 'ASCII_THREE',   \
                   'ASCII_FOUR', 'ASCII_FIVE', 'ASCII_SIX', 'ASCII_SEVEN',  \
                   'ASCII_EIGHT', 'ASCII_NINE']

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(kannada.KannadaUnicode())
        self.langobjs.append(kannada.Vattus())
        self.langobjs.append(kannada.Nudi())

        self.lexer = self.get_lexer()

        # the stroke that turns a letter into the aspirated one is a glyph
        # of its own, and the letter it sits on is a different glyph when
        # it carries the vowel sign i
        self.composeTokens = { \
            ('PA', 'ASPIRATION') : 'PHA', \
            ('BA', 'ASPIRATION') : 'BHA', \
            ('DA', 'ASPIRATION') : 'DHA', \
            ('PA', 'MATRA_I', 'ASPIRATION_I') : ['PHA', 'MATRA_I'], \
            ('BA', 'MATRA_I', 'ASPIRATION_I') : ['BHA', 'MATRA_I'], \
            ('DA', 'MATRA_I', 'ASPIRATION_I') : ['DHA', 'MATRA_I'], \
        }

        # the matras, the two halves of a two part matra among them
        self.matratokens = set([ \
            'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',      \
            'MATRA_VOCALIC_R', 'MATRA_VOCALIC_RR', 'MATRA_E', 'MATRA_EE',  \
            'MATRA_AI', 'MATRA_O', 'MATRA_OO', 'MATRA_AU',                 \
            'MATRA_VOCALIC_L', 'MATRA_VOCALIC_LL',                         \
            'LENGTH_MARK', 'AI_LENGTH_MARK',                               \
        ])

        # the signs that sit on a syllable and are written behind the whole
        # of it. The virama is one of them here: it ends the syllable the
        # same way, 'mïð' being ರ್ಟ್
        self.signtokens = set([ \
            'ANUSVARA', 'VISARGA', 'CANDRABINDU', 'SPACING_CANDRABINDU',   \
            'NUKTA', 'COMBINING_ANUSVARA', 'VIRAMA',                       \
        ])

        # the two halves of a two part matra and the character that unicode
        # has for the whole of it
        self.jointokens = { \
            ('MATRA_I', 'LENGTH_MARK')    : 'MATRA_II', \
            ('MATRA_E', 'LENGTH_MARK')    : 'MATRA_EE', \
            ('MATRA_E', 'AI_LENGTH_MARK') : 'MATRA_AI', \
            ('MATRA_E', 'MATRA_UU')       : 'MATRA_O',  \
            ('MATRA_O', 'LENGTH_MARK')    : 'MATRA_OO', \
        }

        # the glyphs that draw no character of their own, see 1. and 2. of
        # the class comment. They are dropped before the syllables are read
        # so that they are not taken for the head of one
        self.emptytokens = set(['INHERENT_A', 'SPACER'])

        self.vattutokens = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName.startswith('VATTU_'):
                    self.vattutokens.add(tokenName)

    def to_unicode(self, data):
        tokentypes = self.tokenize(data)

        tokentypes = self.compose_tokens(tokentypes)
        tokentypes = [t for t in tokentypes if t not in self.emptytokens]
        tokentypes = self.reorder_clusters(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def reorder_clusters(self, tokentypes):
        '''kannada draws a syllable as the base, the head of its matra, the
           vattus, the tail of the matra and then the signs, and unicode
           wants the base, the vattus, the whole matra and then the signs.
           Every syllable of the text is read as a whole here and written
           out again in that order, the arkavattu of it in front of the
           base it sits on
        '''
        out = []
        i   = 0
        while i < len(tokentypes):
            head = tokentypes[i]
            i   += 1

            matras = []
            vattus = []
            signs  = []
            arka   = []
            while i < len(tokentypes):
                token = tokentypes[i]
                if token in self.matratokens:
                    matras.append(token)
                elif token in self.signtokens:
                    signs.append(token)
                elif token in self.vattutokens:
                    vattus.append(token)
                elif token == 'ARKAVATTU':
                    arka.append(token)
                else:
                    break
                i += 1

            out.extend(arka)
            out.append(head)
            out.extend(vattus)
            out.extend(self.join_matras(matras))
            out.extend(signs)
        return out

    def join_matras(self, matras):
        '''a two part matra is drawn in two glyphs with the vattus of its
           syllable in between, so its halves are only next to each other
           once the syllable has been put in order'''
        out = []
        for token in matras:
            if out and (out[-1], token) in self.jointokens:
                out[-1] = self.jointokens[(out[-1], token)]
            else:
                out.append(token)
        return out

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        def pat(*glyphs):
            # token strings are regular expressions for ply, so the glyphs
            # have to be escaped. Alternate glyphs of the same token are
            # joined into one pattern
            return '|'.join([re.escape(glyph) for glyph in glyphs])

        # VOWELS. the thirteen of them sit on thirteen keys in the order of
        # the alphabet, so ಊ, ಋ and ಔ are read off that run - this document
        # writes none of them
        t_A                = pat('C')
        t_AA               = pat('D')
        t_I                = pat('E')
        t_II               = pat('F')
        t_U                = pat('G')
        t_UU               = pat('H')
        t_VOCALIC_R        = pat('I')
        t_E                = pat('J')
        t_EE               = pat('K')
        t_AI               = pat('L')
        t_O                = pat('M')
        t_OO               = pat('N')
        t_AU               = pat('O')

        # CONSONANTS. a letter that has a second glyph for the shape it
        # takes in front of a matra carries both of them here, and the
        # glyph that draws a letter and the matra i of it is a token of its
        # own, see 2. and 5. of the class comment
        t_KA               = pat('P')
        t_KA_I             = pat('Q')
        t_KHA              = pat('R', 'S')
        t_KHA_I            = pat('T')
        t_GA               = pat('U')
        t_GA_I             = pat('V')
        t_GHA              = pat('W')
        t_GHA_I            = pat('X')
        t_NGA              = pat('Y')

        t_CA               = pat('Z')
        t_CA_I             = pat('a')
        t_CHA              = pat('b')
        t_CHA_I            = pat('c')
        t_JA               = pat('d', 'e')
        t_JA_I             = pat('f')

        t_TTA              = pat('l', 'm')
        t_TTA_I            = pat('n')
        t_TTHA             = pat('o')
        t_DDA              = pat('q')
        t_DDA_I            = pat('r')
        t_NNA              = pat('t', 'u')

        t_TA               = pat('v')
        t_TA_I             = pat('w')
        t_THA              = pat('x')
        t_THA_I            = pat('y')
        t_DA               = pat('z')
        t_DA_I             = pat('¢')
        t_NA               = pat('£')
        t_NA_I             = pat('¤')

        t_PA               = pat('¥')
        t_PA_I             = pat('¦')
        t_BA               = pat('§', '¨')
        t_BA_I             = pat('©')

        # ma and ya out of the pieces they are drawn in, see 4. of the
        # class comment. The stem alone ends the letter in front of a matra
        # that draws its own tail, ಮಾ being 'ªÀiÁ' against the ಮ of 'ªÀÄ'
        t_MA               = pat('ªÀÄ', 'ªÀi')
        t_MA_I             = pat('«Ä')
        t_MA_E             = pat('ªÉÄ')
        t_MA_O             = pat('ªÉÆ')
        t_YA               = pat('AiÀÄ', 'AiÀi')
        t_YA_I             = pat('¬Ä')
        t_YA_E             = pat('AiÉÄ')
        t_YA_O             = pat('AiÉÆ')

        t_RA               = pat('g')
        t_RA_I             = pat('j')
        t_LA               = pat('®', '¯')
        t_LA_I             = pat('°')
        t_VA               = pat('ª')
        t_VA_I             = pat('«')
        t_SHA              = pat('±')
        t_SHA_I            = pat('²')
        t_SSA              = pat('µ')
        t_SSA_I            = pat('¶')
        t_SA               = pat('¸')
        t_SA_I             = pat('¹')
        t_HA               = pat('º')
        t_HA_I             = pat('»')
        t_LLA              = pat('¼')
        t_LLA_I            = pat('½')

        # the stroke that aspirates a letter, on its own key
        t_ASPIRATION       = pat('s')
        t_ASPIRATION_I     = pat('ü')

        # MATRAS. a two part matra is typed in its two parts and put
        # together in join_matras(). va takes a second glyph for its vowel
        # sign u and its vowel sign uu, the first ones being the tail that
        # ma and ya are drawn with
        t_INHERENT_A       = pat('À')
        t_MATRA_AA         = pat('Á')
        t_MATRA_I          = pat('Â')
        t_LENGTH_MARK      = pat('Ã')
        t_MATRA_U          = pat('Ä', 'Å')
        t_MATRA_UU         = pat('Æ', 'Ç')
        t_MATRA_VOCALIC_R  = pat('È')
        t_MATRA_E          = pat('É')
        t_AI_LENGTH_MARK   = pat('Ê')
        t_MATRA_AU         = pat('Ë')

        # VATTUS. the subjoined consonants sit on an unbroken run of keys
        # in the order of the alphabet, 0xCC to 0xEE, and the virama
        # follows them. The key of ಱ, which kannada no longer writes, draws
        # a second ra vattu instead, the one that is used when the vattu is
        # subjoined to another vattu - ಸ್ಟ್ರೇ is '¸ÉÖçÃ'
        t_VATTU_KA         = pat('Ì')
        t_VATTU_KHA        = pat('Í')
        t_VATTU_GA         = pat('Î')
        t_VATTU_GHA        = pat('Ï')
        t_VATTU_NGA        = pat('Ð')
        t_VATTU_CA         = pat('Ñ')
        t_VATTU_CHA        = pat('Ò')
        t_VATTU_JA         = pat('Ó')
        t_VATTU_JHA        = pat('Ô')
        t_VATTU_NYA        = pat('Õ')
        t_VATTU_TTA        = pat('Ö')
        t_VATTU_TTHA       = pat('×')
        t_VATTU_DDA        = pat('Ø')
        t_VATTU_DDHA       = pat('Ù')
        t_VATTU_NNA        = pat('Ú')
        t_VATTU_TA         = pat('Û')
        t_VATTU_THA        = pat('Ü')
        t_VATTU_DA         = pat('Ý')
        t_VATTU_DHA        = pat('Þ')
        t_VATTU_NA         = pat('ß')
        t_VATTU_PA         = pat('à')
        t_VATTU_PHA        = pat('á')
        t_VATTU_BA         = pat('â')
        t_VATTU_BHA        = pat('ã')
        t_VATTU_MA         = pat('ä')
        t_VATTU_YA         = pat('å')
        t_VATTU_RA         = pat('æ', 'ç')
        t_VATTU_LA         = pat('è')
        t_VATTU_VA         = pat('é')
        t_VATTU_SHA        = pat('ê')
        t_VATTU_SSA        = pat('ë')
        t_VATTU_SA         = pat('ì')
        t_VATTU_HA         = pat('í')
        t_VATTU_LLA        = pat('î')
        t_VIRAMA           = pat('ï')

        # SIGNS
        t_ANUSVARA         = pat('A')
        t_VISARGA          = pat('B')
        t_ARKAVATTU        = pat('ð')
        # the glyph of no width that keeps two vattus apart
        t_SPACER           = pat('ö')

        # DIGITS. the rules of these are made in set_digit_rules() below,
        # the roman and the kannada weights of the font drawing different
        # characters on the same keys

        # PUNCTUATIONS
        t_LEFTPARAN        = pat('(')
        t_RIGHTPARAN       = pat(')')
        t_COMMA            = pat(',')
        t_DOT              = pat('.')
        t_DASH             = pat('-')
        t_SLASH            = pat('/')
        t_COLON            = pat(':')
        t_QUOT             = pat('"')
        t_AMPERSAND        = pat('&')
        t_APOSTROPHE       = pat("'")
        t_UNDERSCORE       = pat('_')
        t_LSQUOTE          = pat('‘')
        t_RSQUOTE          = pat('’')
        t_LDQUOTE          = pat('“')
        t_RDQUOTE          = pat('”')
        t_SPACE            = pat(' ')
        t_NEWLINE          = pat('\n')
        t_CARRIAGERET      = pat('\r')
        t_TAB              = pat('\t')
        t_FORMFEED         = pat('\f')

        def t_error(t):
            # a key that this font has no token for is either a glyph of
            # the font that no document here presses, which nothing can
            # turn into a character, or a character that the extraction put
            # in of its own - a zero width joiner, an ellipsis - and that
            # has to come out the way it went in
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
        self.set_digit_rules(rules, pat)

        # only the tokens that the font has a glyph for
        rules['tokens'] = [tokenName for tokenName in tokens \
                                     if 't_' + tokenName in rules]

        # the rules of the digits are made in a loop, so they are handed to
        # ply in an object of their own rather than in the locals of this
        # function. ply looks up the module of that object
        rules['__module__'] = self.__class__.__module__
        return lex.lex(object = types.SimpleNamespace(**rules))

    def set_digit_rules(self, rules, pat):
        for digit, tokenName in enumerate(self.digittokens):
            rules['t_' + tokenName] = pat('%d' % digit)

class NudiKannadaDigits(Nudi):
    '''Nudi01k, the weight of the font that draws the kannada digits on the
       digit keys rather than the latin ones. Everything else about it is
       the same font, so the gazette sets the volume and the issue number
       of a page in it - '15' there is ೧೫ and not 15
    '''
    digittokens = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', \
                   'SEVEN', 'EIGHT', 'NINE']
