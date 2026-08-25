import re
import types

from indic2unicode.langs import kannada
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class Aklite(BaseFont):
    '''The text of a pdf that is set in AkliteKndIpsita, the kannada display
       font that the masthead of the Karnataka gazette - ಕರ್ನಾಟಕ ರಾಜ್ಯಪತ್ರ,
       drawn as an outlined title - is set in.

       It is an 8-bit font like Nudi: every glyph of it sits on a byte and
       the text of such a pdf is the sequence of keys the typist pressed,
       so what comes out of the pdf is latin1 or macroman and not kannada
       at all. The glyphs spell a syllable in the order it is drawn,

           base [head stroke] [matra] vattu(s) [arkavattu]

       while unicode wants the arkavattu of a syllable in front of its base
       and the matra behind the vattus, so every syllable is read as a whole
       here and written out again in that order - the same reordering
       fonts/kannada/nudi.py does, this font drawing the pieces of a
       syllable the same way.

       TWO NAMES FOR ONE BYTE

       The glyphs of the font are drawn on the bytes of the upper half of a
       latin table and carry the glyph names of the characters that live
       there, which is what an 8-bit font does - the names say nothing about
       what the glyphs draw. The two producers behind these documents chose
       the two conventions for those names: one names the byte 0xC2 the
       macroman way (/logicalnot) and the other the windows way
       (/Acircumflex), and an extractor reads the map back out as those
       characters, so the same glyph comes out of one pdf as '¬' and out of
       the other as 'Â'. Both are the byte 0xC2.

       The glyph table below is therefore keyed by the byte, and a lexer is
       built for each of the two conventions over the characters that byte
       extracts as under it. pick_lexer() picks between them per run of
       text, by how many of the run's characters each convention has a
       glyph for. Only one character means anything under both of them:
       U+00C2, which is the byte 0xE5 read the macroman way (the ya vattu)
       and the byte 0xC2 read the windows way (ನ). A run that is nothing but
       that character and spaces therefore ties, and is read the windows
       way, where it is a letter that can stand on its own rather than a
       vattu with no consonant in front of it.

       WHAT IS NOT KNOWN

       The pdfs this was built from draw thirteen glyphs of the font, the
       ones the masthead is written with, and nothing in them says what the
       rest of it draws: the subsets carry no other glyph, the encoding
       names no other byte and the ToUnicode map of the one pdf that has a
       map is the same list of latin names. The thirteen were read off the
       outlines of the subset, rendered one glyph at a time and lined up
       against an OCR of the same region of the page (tesseract -l eng+kan).
       A byte outside them is reported and dropped.
    '''
    # the byte each glyph of the font sits on and what it draws. Every one
    # of them was read off the rendered outlines of the subset, see the
    # class comment
    glyphcodes = { \
        # CONSONANTS. the ka glyph draws the letter without its head       \
        # stroke, which is a glyph of its own - see INHERENT_A below       \
        'KA'         : 0xB0, \
        'JA'         : 0xB8, \
        'TTA'        : 0xBB, \
        'TA'         : 0xC0, \
        'NA'         : 0xC2, \
        'PA'         : 0xC3, \
        'RA'         : 0xC7, \
                             \
        # MATRAS                                                          \
        'MATRA_AA'   : 0xF1, \
                             \
        # VATTUS. the subjoined consonants, drawn under the letter, and    \
        # the arkavattu, the ra of a cluster drawn as a mark on top of the \
        # consonant that follows it                                       \
        'VATTU_YA'   : 0xE5, \
        'VATTU_RA'   : 0xE6, \
        'ARKAVATTU'  : 0x9E, \
                             \
        # the head stroke of a consonant that carries the vowel a. It      \
        # draws a part of the letter and stands for no character of its    \
        # own, so ಕ is the ka glyph and this one                           \
        'INHERENT_A' : 0xF0, \
                             \
        'SPACE'      : 0x20, \
    }

    # the two conventions a pdf names the glyphs of an 8-bit font by, and
    # so the two ways its text comes back out. See the class comment
    encodings = ('mac_roman', 'cp1252')

    # the convention a run that both of them read equally well is taken to
    # be in, see pick_lexer()
    default_encoding = 'cp1252'

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(kannada.KannadaUnicode())
        self.langobjs.append(kannada.Vattus())
        self.langobjs.append(kannada.Aklite())

        # what each glyph of the font extracts as under each of the two
        # conventions, and a lexer over each of those alphabets
        self.glyphchars = {}
        self.lexers     = {}
        for encoding in self.encodings:
            self.glyphchars[encoding] = self.get_glyph_chars(encoding)
            self.lexers[encoding]     = self.get_lexer(encoding)

        self.lexer = self.lexers[self.default_encoding]

        # the matras. None of the thirteen glyphs draws half of a two part
        # matra, so unlike Nudi nothing here has to be put back together
        self.matratokens = set([ \
            'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',      \
            'MATRA_VOCALIC_R', 'MATRA_VOCALIC_RR', 'MATRA_E', 'MATRA_EE',  \
            'MATRA_AI', 'MATRA_O', 'MATRA_OO', 'MATRA_AU',                 \
            'MATRA_VOCALIC_L', 'MATRA_VOCALIC_LL',                         \
        ])

        # the signs that sit on a syllable and are written behind the whole
        # of it
        self.signtokens = set([ \
            'ANUSVARA', 'VISARGA', 'CANDRABINDU', 'SPACING_CANDRABINDU',   \
            'NUKTA', 'COMBINING_ANUSVARA', 'VIRAMA',                       \
        ])

        # the glyph that draws the head stroke of a letter rather than a
        # letter. It is dropped before the syllables are read so that it is
        # not taken for the head of one
        self.emptytokens = set(['INHERENT_A'])

        self.vattutokens = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName.startswith('VATTU_'):
                    self.vattutokens.add(tokenName)

    def get_glyph_chars(self, encoding):
        '''the character each glyph of the font extracts as when the pdf
           names its glyphs by this convention, i.e. the byte it sits on
           decoded that way. A byte that the convention leaves undefined -
           cp1252 has five of them - has no character and so no rule'''
        glyphchars = {}

        for tokenName, code in self.glyphcodes.items():
            try:
                glyphchars[tokenName] = bytes([code]).decode(encoding)
            except UnicodeDecodeError:
                self.logger.debug('%s leaves the byte 0x%02X of %s undefined',
                                  encoding, code, tokenName)

        return glyphchars

    def pick_lexer(self, data):
        '''which of the two glyph name conventions a run of text is in.

           Every byte of the font extracts as a different character under
           the two of them but one, so the convention that has a glyph for
           more of the run's characters is the one the pdf named its glyphs
           by. A run that both of them read equally well is either empty or
           made of nothing but the one character they share, and is taken
           to be in default_encoding - see the class comment'''
        def matched(encoding):
            glyphs = set(self.glyphchars[encoding].values())
            return len([char for char in data if char in glyphs])

        # default_encoding is the one to beat rather than just another
        # candidate, so that a run the two of them read equally well goes
        # to it whichever order self.encodings happens to list them in
        best  = self.default_encoding
        score = matched(best)

        for encoding in self.encodings:
            if matched(encoding) > score:
                best  = encoding
                score = matched(encoding)

        return self.lexers[best]

    def to_unicode(self, data):
        # a run of text is read under one of the two glyph name conventions
        # as a whole - a document is written by one producer and never
        # mixes them, see pick_lexer()
        self.lexer = self.pick_lexer(data)

        tokentypes = self.tokenize(data)

        tokentypes = [t for t in tokentypes if t not in self.emptytokens]
        tokentypes = self.reorder_clusters(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def reorder_clusters(self, tokentypes):
        '''kannada draws a syllable as the base, the head of its matra, the
           vattus and then the signs, and unicode wants the base, the
           vattus, the matra and then the signs. Every syllable of the text
           is read as a whole here and written out again in that order, the
           arkavattu of it in front of the base it sits on.

           The masthead is drawn in overlapping pieces and a pdf hands them
           out as runs of their own, so a run can begin in the middle of a
           syllable - a matra or a vattu that starts one is the head of it
           here and is written out where it stands rather than dropped.

           A character that is not a glyph of this font at all - a newline
           between two of those pieces, the latin text of the document -
           heads no syllable and is written out on its own: a matra behind
           it belongs to no base, and letting one head a syllable would
           carry the arkavattu of the piece that follows across it
        '''
        out = []
        i   = 0
        while i < len(tokentypes):
            head = tokentypes[i]
            i   += 1

            if type(head) == tuple and head[0] == LITERAL:
                out.append(head)
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
                    vattus.append(token)
                elif token == 'ARKAVATTU':
                    arka.append(token)
                else:
                    break
                i += 1

            out.extend(arka)
            out.append(head)
            out.extend(vattus)
            out.extend(matras)
            out.extend(signs)
        return out

    def get_lexer(self, encoding):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        rules = {}
        for tokenName, char in self.glyphchars[encoding].items():
            # token strings are regular expressions for ply, so the
            # character has to be escaped
            rules['t_' + tokenName] = re.escape(char)

        def t_error(t):
            # a byte that this font has no glyph for here is either a glyph
            # of the font that these documents never draw, which nothing
            # can turn into a character, or a character that the extraction
            # put in of its own - a zero width joiner, an ellipsis - and
            # that has to come out the way it went in
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
