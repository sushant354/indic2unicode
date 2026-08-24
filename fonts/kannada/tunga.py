import re
import string
import types

from indic2unicode.langs import kannada
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class Tunga(BaseFont):
    '''The text of a pdf that is set in Tunga, the unicode kannada font that
       the Karnataka gazette is published in. Its ToUnicode map is nearly
       sound - every glyph carries the characters it stands for - but the
       glyphs are stored in the order in which they are drawn, and kannada
       draws a syllable in an order of its own:

           base [first half of the matra] vattu(s) [length mark] [anusvara]

       while unicode wants the base, the vattus and then the whole matra. So
       a vattu comes out behind the matra of the syllable it belongs to and
       spelled the wrong way round, ಪ್ರಸ್ತಾವನೆ as ಪರ್ಸಾತ್ವನೆ and ಸಲ್ಲಿಸಿದ as ಸಲಿಲ್ಸಿದ,
       and an arkavattu comes out behind the whole syllable it sits on,
       ಕರ್ನಾಟಕ as ಕನಾರ್ಟಕ and ಸರ್ಕಾರದ as ಸಕಾರ್ರದ.

       A two part matra comes out in its two parts, ೀ as ಿ + ೕ and ೋ as
       ೆ + ೂ + ೕ, and a vattu of that syllable stands between them, so ಶ್ರೀ
       comes out as ಶಿ + ರ್ + ೕ. Unicode has one character for each of these
       matras and the two halves are put back together here.

       WHAT THE TEXT CANNOT SAY

       The map spells a vattu as its consonant and a virama, in that order,
       which is what a dead consonant at the end of a word looks like as
       well, and it hands the arkavattu, the vattu of ra and a dead ra the
       same 'ರ್'. The pdf itself keeps all three apart - they are different
       glyphs - so a repaired map would lose nothing, but in the text they
       are one string and this font has to guess:

       1. A vattu that a length mark follows belongs to the syllable that
          mark is the tail of, so it is a vattu and not anything else, which
          is what makes ಶಿ + ರ್ + ೕ come out as ಶ್ರೀ.
       2. A 'C ್' behind a length mark is not a vattu of that syllable - a
          vattu is drawn before the mark - so it is a dead consonant, which
          is what ends ಎಂಪ್ಲಾಯೀಸ್ and ವೆಲ್ಫೇರ್. A 'ರ್' there can still be the
          arkavattu of the syllable that follows, as in ನಿರ್ದೇಶನ.
       3. A vattu needs a consonant to sit under, so a 'C ್' that a vowel or
          a digit or a latin letter carries is a dead consonant, as in ಆರ್.
       4. Everything else that stands in the middle of a word is a vattu:
          kannada writes every virama between two consonants that way. An
          english loan that is written with a dead consonant in the middle
          is lost here, ವೆಲ್ಫೇರ್ comes out as ವ್ಲೆಫೇರ್ wherever the pdf leaves no
          space between the two halves of it.
       5. At the end of a word a 'C ್' is a vattu unless its consonant is one
          of the few that a kannada word is written to end with, ಸ ಶ ಥ ನ ಲ -
          ಎಸ್, ಲೋಕೇಶ್, ಮಂಜುನಾಥ್, ಅಸೋಸಿಯೇಷನ್, ವೆಲ್. A doubled consonant is a vattu
          all the same, so ಗಳನ್ನು and ರಲ್ಲಿ come out whole.
       6. A 'ರ್' is read as the vattu of ra when it sits on one of the
          consonants that ra is most often written under, ಪ ಫ ಬ ಭ ತ ದ ಗ, and
          as the arkavattu everywhere else. ಕ takes either about as often
          and the matra of the syllable decides there, see below. Both
          readings are ordinary kannada and the text does not say which one
          it is, so ಪ್ರ and ಪತ್ರ and ಕೇಂದ್ರ and ಸರ್ಕಾರ and ಕರ್ನಾಟಕ come out right
          while ಆಶ್ರಯ comes out as ಆರ್ಶಯ and ತರ್ಕ as ತಕ್ರ.

       WHAT THE EXTRACTOR LOSES BEFORE THIS

       Tunga draws a consonant and the matra i or o of it in one glyph and
       the map of these pdfs has no entry at all for a number of those
       ligatures. An extractor that falls back on the cid of a glyph hands
       them out as a latin letter, e.g. ವಿ as U+013B, and those are tokens
       here, so ವಿಷಯ comes back whole. An extractor that drops a glyph it
       has no string for - pdftotext does - loses them before this font ever
       sees the text and ವಿಷಯ is ಷಯ there for good.
    '''
    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(kannada.KannadaUnicode())
        self.langobjs.append(kannada.Vattus())
        self.langobjs.append(kannada.Tunga())

        self.lexer = self.get_lexer()

        # the matras, the two halves of a two part matra among them
        self.matratokens = set([ \
            'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',      \
            'MATRA_VOCALIC_R', 'MATRA_VOCALIC_RR', 'MATRA_E', 'MATRA_EE',  \
            'MATRA_AI', 'MATRA_O', 'MATRA_OO', 'MATRA_AU',                 \
            'MATRA_VOCALIC_L', 'MATRA_VOCALIC_LL',                         \
            'LENGTH_MARK', 'AI_LENGTH_MARK',                               \
        ])

        # the tail of a two part matra, which is drawn behind the vattus of
        # its syllable while the head of it is drawn in front of them
        self.lengthtokens = set(['LENGTH_MARK', 'AI_LENGTH_MARK'])

        # the signs that sit on a syllable and are written behind the whole
        # of it
        self.signtokens = set([ \
            'ANUSVARA', 'VISARGA', 'CANDRABINDU', 'SPACING_CANDRABINDU',   \
            'NUKTA', 'COMBINING_ANUSVARA',                                 \
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

        # the consonants that ra is written under more often than it is
        # written on top of, see 6. above
        self.ravattubases = set([ \
            'PA', 'PHA', 'BA', 'BHA', 'TA', 'DA', 'GA', \
        ])

        # ka is written under ra about as often as it carries an arkavattu,
        # and the matra of the syllable is what tells the two apart most of
        # the time: the ರ್ಕ of ಸರ್ಕಾರ and of ಮಾರ್ಕೆಟ್ carries one and the ಕ್ರ of
        # ಕ್ರಮ and of ಚಕ್ರ does not
        self.ravattubases_nomatra = set(['KA'])

        # the consonants that a kannada word is written to end with, see 5.
        self.deadfinals = set(['SA', 'SHA', 'THA', 'NA', 'LA'])

        # every vattu of the script, and the two tokens it is spelled out in
        # when it turns out to be a dead consonant rather than a vattu
        self.vattutokens = set()
        self.deadtokens  = {}
        # the tokens that are kannada, i.e. that carry a word on
        self.kannadatokens   = set()
        self.consonanttokens = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName.startswith('VATTU_'):
                    consonant = tokenName[len('VATTU_'):]
                    self.vattutokens.add(tokenName)
                    self.deadtokens[tokenName] = [consonant, 'VIRAMA']

                ustr = self.token_to_unicode(tokenName)
                if not ustr:
                    continue
                if kannada.is_consonant(ustr):
                    self.consonanttokens.add(tokenName)
                if 'ಀ' <= ustr[0] <= '೿':
                    self.kannadatokens.add(tokenName)

    def to_unicode(self, data):
        tokentypes = self.tokenize(data)

        tokentypes = self.compose_tokens(tokentypes)
        tokentypes = self.reorder_clusters(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def reorder_clusters(self, tokentypes):
        '''kannada draws a syllable as the base, the head of its matra, the
           vattus, the tail of the matra and then the signs, and unicode
           wants the base, the vattus, the whole matra and then the signs.
           Every syllable of the text is read as a whole here and written
           out again in that order, the arkavattu of it in front of the base
           it sits on
        '''
        out = []
        i   = 0
        while i < len(tokentypes):
            head = tokentypes[i]
            i   += 1

            if head in self.vattutokens:
                # a consonant and a virama with no syllable to sit under
                out.extend(self.deadtokens[head])
                continue

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
                    role = self.vattu_role(head, token, matras, tokentypes, i)
                    if role == 'dead':
                        # it opens a syllable of its own
                        break
                    elif role == 'arka':
                        arka.append('ARKAVATTU')
                    else:
                        vattus.append(token)
                else:
                    break
                i += 1

            out.extend(arka)
            out.append(head)
            out.extend(vattus)
            out.extend(self.join_matras(matras))
            out.extend(signs)
        return out

    def vattu_role(self, head, token, matras, tokentypes, i):
        '''what a consonant and a virama behind a syllable are: a vattu of
           that syllable, the arkavattu of the syllable that follows or a
           dead consonant that is a syllable of its own'''
        consonant = token[len('VATTU_'):]
        if i + 1 < len(tokentypes):
            nextToken = tokentypes[i + 1]
        else:
            nextToken = None

        if head not in self.consonanttokens:
            # a vattu is drawn under a consonant and there is none
            return 'dead'

        if matras and matras[-1] in self.lengthtokens:
            # a vattu of this syllable would have been drawn in front of
            # that mark rather than behind it
            if consonant == 'RA' and nextToken in self.consonanttokens:
                return 'arka'
            return 'dead'

        if consonant == 'RA':
            if nextToken in self.lengthtokens:
                # the mark is the tail of the matra of this syllable, so
                # the ra is drawn inside the syllable and is a vattu
                return 'vattu'
            if head in self.ravattubases:
                return 'vattu'
            if not matras and head in self.ravattubases_nomatra:
                return 'vattu'
            return 'arka'

        if nextToken not in self.kannadatokens and consonant != head and \
                consonant in self.deadfinals:
            # the end of a word, where kannada does write a dead consonant
            return 'dead'

        return 'vattu'

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

        # VOWELS
        t_A                = pat('ಅ')
        t_AA               = pat('ಆ')
        t_I                = pat('ಇ')
        t_II               = pat('ಈ')
        t_U                = pat('ಉ')
        t_UU               = pat('ಊ')
        t_VOCALIC_R        = pat('ಋ')
        t_VOCALIC_L        = pat('ಌ')
        t_E                = pat('ಎ')
        t_EE               = pat('ಏ')
        t_AI               = pat('ಐ')
        t_O                = pat('ಒ')
        t_OO               = pat('ಓ')
        t_AU               = pat('ಔ')
        t_VOCALIC_RR       = pat('ೠ')
        t_VOCALIC_LL       = pat('ೡ')

        # CONSONANTS. a vattu is the consonant of it and a virama, and is a
        # token of its own so that the syllable it belongs to can be put in
        # order. Whether it really is a vattu is decided in vattu_role()
        t_VATTU_KA         = pat('ಕ್')
        t_KA               = pat('ಕ')
        t_VATTU_KHA        = pat('ಖ್')
        t_KHA              = pat('ಖ')
        t_VATTU_GA         = pat('ಗ್')
        t_GA               = pat('ಗ')
        t_VATTU_GHA        = pat('ಘ್')
        t_GHA              = pat('ಘ')
        t_VATTU_NGA        = pat('ಙ್')
        t_NGA              = pat('ಙ')

        t_VATTU_CA         = pat('ಚ್')
        t_CA               = pat('ಚ')
        t_VATTU_CHA        = pat('ಛ್')
        t_CHA              = pat('ಛ')
        t_VATTU_JA         = pat('ಜ್')
        t_JA               = pat('ಜ')
        t_VATTU_JHA        = pat('ಝ್')
        t_JHA              = pat('ಝ')
        t_VATTU_NYA        = pat('ಞ್')
        t_NYA              = pat('ಞ')

        t_VATTU_TTA        = pat('ಟ್')
        t_TTA              = pat('ಟ')
        t_VATTU_TTHA       = pat('ಠ್')
        t_TTHA             = pat('ಠ')
        t_VATTU_DDA        = pat('ಡ್')
        t_DDA              = pat('ಡ')
        t_VATTU_DDHA       = pat('ಢ್')
        t_DDHA             = pat('ಢ')
        t_VATTU_NNA        = pat('ಣ್')
        t_NNA              = pat('ಣ')

        t_VATTU_TA         = pat('ತ್')
        t_TA               = pat('ತ')
        t_VATTU_THA        = pat('ಥ್')
        t_THA              = pat('ಥ')
        t_VATTU_DA         = pat('ದ್')
        t_DA               = pat('ದ')
        t_VATTU_DHA        = pat('ಧ್')
        t_DHA              = pat('ಧ')
        t_VATTU_NA         = pat('ನ್')
        t_NA               = pat('ನ')

        t_VATTU_PA         = pat('ಪ್')
        t_PA               = pat('ಪ')
        t_VATTU_PHA        = pat('ಫ್')
        t_PHA              = pat('ಫ')
        t_VATTU_BA         = pat('ಬ್')
        t_BA               = pat('ಬ')
        t_VATTU_BHA        = pat('ಭ್')
        t_BHA              = pat('ಭ')
        t_VATTU_MA         = pat('ಮ್')
        t_MA               = pat('ಮ')

        t_VATTU_YA         = pat('ಯ್')
        t_YA               = pat('ಯ')
        t_VATTU_RA         = pat('ರ್')
        t_RA               = pat('ರ')
        t_VATTU_RRA        = pat('ಱ್')
        t_RRA              = pat('ಱ')
        t_VATTU_LA         = pat('ಲ್')
        t_LA               = pat('ಲ')
        t_VATTU_LLA        = pat('ಳ್')
        t_LLA              = pat('ಳ')
        t_VATTU_VA         = pat('ವ್')
        t_VA               = pat('ವ')
        t_VATTU_SHA        = pat('ಶ್')
        t_SHA              = pat('ಶ')
        t_VATTU_SSA        = pat('ಷ್')
        t_SSA              = pat('ಷ')
        t_VATTU_SA         = pat('ಸ್')
        t_SA               = pat('ಸ')
        t_VATTU_HA         = pat('ಹ್')
        t_HA               = pat('ಹ')
        t_VATTU_FA         = pat('ೞ್')
        t_FA               = pat('ೞ')
        t_NAKAARA_POLLU    = pat('ೝ')

        # MATRAS. a two part matra of the text is read in its two parts and
        # put together in join_matras(), but a document that carries it as
        # one character is read as it is
        t_MATRA_AA         = pat('ಾ')
        t_MATRA_I          = pat('ಿ')
        t_MATRA_II         = pat('ೀ')
        t_MATRA_U          = pat('ು')
        t_MATRA_UU         = pat('ೂ')
        t_MATRA_VOCALIC_R  = pat('ೃ')
        t_MATRA_VOCALIC_RR = pat('ೄ')
        t_MATRA_E          = pat('ೆ')
        t_MATRA_EE         = pat('ೇ')
        t_MATRA_AI         = pat('ೈ')
        t_MATRA_O          = pat('ೊ')
        t_MATRA_OO         = pat('ೋ')
        t_MATRA_AU         = pat('ೌ')
        t_MATRA_VOCALIC_L  = pat('ೢ')
        t_MATRA_VOCALIC_LL = pat('ೣ')
        t_LENGTH_MARK      = pat('ೕ')
        t_AI_LENGTH_MARK   = pat('ೖ')

        # SIGNS
        t_SPACING_CANDRABINDU = pat('ಀ')
        t_CANDRABINDU      = pat('ಁ')
        t_ANUSVARA         = pat('ಂ')
        t_VISARGA          = pat('ಃ')
        t_NUKTA            = pat('಼')
        t_AVAGRAHA         = pat('ಽ')
        t_VIRAMA           = pat('್')
        t_JIHVAMULIYA      = pat('ೱ')
        t_UPADHMANIYA      = pat('ೲ')
        t_COMBINING_ANUSVARA = pat('ೳ')

        # THE LIGATURES THE MAP HAS NO ENTRY FOR. An extractor that falls
        # back on the cid of such a glyph hands out the character of that
        # cid, and the cids of these pdfs are the glyph ids of Tunga itself
        t_LIG_LA_I         = pat('Ĺ')
        t_LIG_LLA_I        = pat('ĺ')
        t_LIG_VA_I         = pat('Ļ')
        t_LIG_SHA_I        = pat('ļ')
        t_LIG_SSA_I        = pat('Ľ')
        t_LIG_SA_I         = pat('ľ')
        t_LIG_HA_I         = pat('Ŀ')
        t_LIG_PA_O         = pat('Ū')
        t_LIG_YA_O         = pat('Ŵ')

        # DIGITS
        t_ZERO             = pat('೦')
        t_ONE              = pat('೧')
        t_TWO              = pat('೨')
        t_THREE            = pat('೩')
        t_FOUR             = pat('೪')
        t_FIVE             = pat('೫')
        t_SIX              = pat('೬')
        t_SEVEN            = pat('೭')
        t_EIGHT            = pat('೮')
        t_NINE             = pat('೯')

        # PUNCTUATIONS
        t_LEFTPARAN        = pat('(')
        t_RIGHTPARAN       = pat(')')
        t_LEFTSQBRACE      = pat('[')
        t_RIGHTSQBRACE     = pat(']')
        t_COMMA            = pat(',')
        t_DOT              = pat('.')
        t_DASH             = pat('-')
        t_SLASH            = pat('/')
        t_COLON            = pat(':')
        t_SEMICOLON        = pat(';')
        t_QUESTION         = pat('?')
        t_EXCLAMATION      = pat('!')
        t_PERCENT          = pat('%')
        t_PLUS             = pat('+')
        t_EQ               = pat('=')
        t_STAR             = pat('*')
        t_QUOT             = pat('"')
        t_BAR              = pat('|')
        t_AMPERSAND        = pat('&')
        t_AT               = pat('@')
        t_HASH             = pat('#')
        t_UNDERSCORE       = pat('_')
        t_APOSTROPHE       = pat("'")
        t_LSQUOTE          = pat('‘')
        t_RSQUOTE          = pat('’')
        t_LDQUOTE          = pat('“')
        t_RDQUOTE          = pat('”')
        t_ENDASH           = pat('–')
        t_EMDASH           = pat('—')
        t_HYPHEN           = pat('‐')
        t_DANDA            = pat('।')
        t_DOUBLE_DANDA     = pat('॥')
        t_SPACE            = pat(' ')
        t_NEWLINE          = pat('\n')
        t_CARRIAGERET      = pat('\r')
        t_TAB              = pat('\t')
        t_FORMFEED         = pat('\f')

        def t_error(t):
            # the text of this font is unicode already and only its order is
            # wrong, so a character with no token of its own is not a glyph
            # waiting to be reordered, it is text - an ellipsis, a bullet, a
            # zero width joiner - and has to come out the way it went in
            # rather than be dropped. Only a glyph code that no map could
            # turn into a character is dropped, and that is reported
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

        # the english text of the document is set in a latin font and comes
        # out of the pdf as itself
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
