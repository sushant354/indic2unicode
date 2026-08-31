import re
import types

from indic2unicode.langs import kannada
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

# the block of the script, which is what the lexer builds a rule for and
# what tells a kannada character from the latin and the punctuation around it
KANNADA_RE = re.compile('[\u0c80-\u0cff]')

class ArialUniKannadaGlyphs(BaseFont):
    '''The kannada of a pdf whose ToUnicode map has been repaired by
       tools/fix_tounicode.py, the Karnataka gazette being set in Arial
       Unicode MS as the Union gazette is. Every glyph now carries the
       characters it really stands for, and what is left to do is the order:
       kannada draws a syllable as

           [base] [head of the matra] [vattus] [tail of the matra] [signs]

       and writes the arkavattu of it behind the whole syllable it sits on,
       while unicode wants the arkavattu, the base, the vattus and then the
       whole matra. So ಸ್ಟೇಟ್ is drawn ಸೆ + ್ಟ + ೕ + ಟ್, ಪ್ರಾ is ಪ + ಾ + ್ರ and
       ಕರ್ನಾಟಕ is ಕ + ನ + ಾ + ರ್ + ಟ + ಕ, and each of them is read as a whole
       syllable here and written out again in the order unicode wants.

       WHAT THE REPAIR SETTLES AND THIS PASS THEREFORE NEED NOT GUESS

       fonts/kannada/tunga.py reads the same script out of a map that spells
       a vattu, a dead consonant and the arkavattu all three as 'ಟ್', and it
       has to guess from the syllable around them which of the three it is
       looking at. This pass has to guess nothing. The repair spells a vattu
       as the virama and its consonant, '್ಟ', which is the order unicode
       writes a subjoined consonant in, and a dead consonant the other way
       round, so those two are already different tokens. The arkavattu is
       spelled 'ರ್' like a dead ra and nothing in the text tells them apart
       - both of them stand at the end of a word in the drawn order, ಅರ್ಥ
       being drawn ಅಥರ್ and ಡೈರೆಕ್ಟರ್ being drawn ಡೈರೆಕ್ಟರ್ - so the repair
       marks the arkavattu, the pdf drawing the two with glyphs of their
       own, see langs/kannada.ARKAVATTU_MARK.

       The virama that a dead consonant carries is the virama of the whole
       cluster, and unicode writes it behind the vattus of that cluster
       rather than behind its base. That is a move of the order and not of
       the reading, so ಕ್ + ್ಟ comes out as ಕ್ಟ್ and not as ಕ್್ಟ.

       A two part matra is drawn in two glyphs with the vattus of its
       syllable in between - ೇ as ೆ + ೕ, ೊ as ೆ + ೂ, ೋ as ೆ + ೂ + ೕ - and
       unicode has one character for the whole of it, so the halves are put
       back together once the syllable is in order.
    '''
    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(kannada.KannadaUnicode())
        self.langobjs.append(kannada.Vattus())

        self.lexer = self.get_lexer()

        # the matras, the two halves of a two part matra among them
        self.matratokens = set([ \
            'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',      \
            'MATRA_VOCALIC_R', 'MATRA_VOCALIC_RR', 'MATRA_E', 'MATRA_EE',  \
            'MATRA_AI', 'MATRA_O', 'MATRA_OO', 'MATRA_AU',                 \
            'MATRA_VOCALIC_L', 'MATRA_VOCALIC_LL',                         \
            'LENGTH_MARK', 'AI_LENGTH_MARK',                               \
        ])

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

        # every vattu of the script, and the two tokens it is spelled out in
        # when it turns out to have no syllable to sit under
        self.vattutokens = set()
        self.deadtokens  = {}
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName.startswith('VATTU_'):
                    consonant = tokenName[len('VATTU_'):]
                    self.vattutokens.add(tokenName)
                    self.deadtokens[tokenName] = [consonant, 'VIRAMA']

    def to_unicode(self, data):
        tokentypes = self.tokenize(data)

        tokentypes = self.reorder_clusters(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def reorder_clusters(self, tokentypes):
        '''every syllable of the text read as a whole and written out again
           in the order unicode wants: the arkavattu of it, the base, the
           vattus, the virama of the cluster, the whole matra and the signs
        '''
        out = []
        i   = 0
        while i < len(tokentypes):
            head = tokentypes[i]
            i   += 1

            if head in self.vattutokens:
                # no consonant in front of it to sit under
                out.extend(self.deadtokens[head])
                continue

            matras = []
            vattus = []
            signs  = []
            arka   = []
            virama = []
            while i < len(tokentypes):
                token = tokentypes[i]
                if token in self.vattutokens:
                    vattus.append(token)
                elif token in self.matratokens:
                    matras.append(token)
                elif token in self.signtokens:
                    signs.append(token)
                elif token == 'VIRAMA' and not \
                        (virama or vattus or matras or signs):
                    # the virama that the base glyph of a dead cluster
                    # carries, which belongs behind the vattus of it
                    virama.append(token)
                elif token == 'ARKAVATTU':
                    arka.append(token)
                else:
                    break
                i += 1

            out.extend(arka)
            out.append(head)
            out.extend(vattus)
            out.extend(virama)
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

    def get_arkavattu(self):
        '''how the repaired text of this font spells the arkavattu. Arial
           Unicode MS and Nirmala UI draw it with a glyph of its own but
           spell it 'ರ್' like a dead ra, so the repair marks it, see
           langs/kannada.ARKAVATTU_MARK. A font whose own cmap gives the
           arkavattu a character of its own needs no mark and says so by
           overriding this, see fonts/kannada/nudiuni.py'''
        return kannada.Vattus().tokendict['ARKAVATTU'] + kannada.ARKAVATTU_MARK

    def get_lexer(self):
        '''a rule per token of the script. The text of a repaired pdf spells
           every one of them exactly as unicode does - that is what the
           repair is - so the pattern of a token is its own unicode string
           and the rules are read straight off langs/kannada.py rather than
           written out again. Only the tokens that are kannada get a rule:
           the latin of the document, its digits and its punctuation are
           text that comes out the way it went in, which is what t_error
           does with a character that no rule matched'''
        vattus    = kannada.Vattus().tokendict
        arkavattu = self.get_arkavattu()

        # the tokens the text does not spell the way unicode does, as ready
        # made patterns rather than as strings to be escaped.
        #
        # The arkavattu is whatever the repair of this font writes for it -
        # 'ರ್' and the mark that keeps it apart from a dead ra, or a
        # character of the font's own. Either way the token is still written
        # out as the plain 'ರ್' of langs/kannada.py, since the mark says what
        # the glyph is rather than standing for anything of its own
        patterns = {'ARKAVATTU': re.escape(arkavattu)}

        # The vattu of ra only has to stand out of the arkavattu's way when
        # the two are spelled alike: a dead consonant that an arkavattu sits
        # behind - ಅಪಾರ್ಟ್ಮೆಂಟ್ is drawn ಅಪಾಟ್ + ರ್ - then spells a virama, a ra
        # and a virama in a row, and the vattu is the first thing a lexer
        # matching left to right sees there. It is not one: an arkavattu
        # follows, and what stands in front of it is the virama of the dead
        # consonant. A font that spells its arkavattu with a character of
        # its own can never read as a vattu in the first place
        if arkavattu.startswith(vattus['ARKAVATTU'][0]):
            patterns['VATTU_RA'] = re.escape(vattus['VATTU_RA']) + \
                                   '(?!' + re.escape(arkavattu[1:]) + ')'

        rules  = {}
        tokens = []
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                ustr = obj.get_unicode_string(tokenName)
                if not ustr or not all(KANNADA_RE.match(c) for c in ustr):
                    continue
                rules['t_' + tokenName] = patterns.get(tokenName) or \
                                              re.escape(ustr)
                tokens.append(tokenName)

        def t_error(t):
            # the text of a repaired pdf is unicode already and only its
            # order is wrong, so a character with no token of its own is not
            # a glyph waiting to be reordered, it is text - the latin of the
            # document, a digit, a bracket, a dash - and has to come out the
            # way it went in rather than be dropped. Only a character that
            # no map could have made is dropped, and that is reported
            char = t.value[0]

            if not self.is_text_char(char):
                self.report_error(t)
                t.lexer.skip(1)
                return None

            t.lexer.skip(1)
            t.type  = LITERAL
            t.value = char
            return t

        rules['t_error']    = t_error
        rules['tokens']     = tokens
        # the rules are made in a loop, so they are handed to ply in an
        # object of their own rather than in the locals of this function.
        # ply looks up the module of that object
        rules['__module__'] = self.__class__.__module__
        return lex.lex(object = types.SimpleNamespace(**rules))
