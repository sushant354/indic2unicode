import re
import types

from indic2unicode.langs import telugu
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

# the script this converter reads. A token is built for every string of
# langs/telugu.py that carries one of these characters, and everything else of
# a run - the latin of the document, its digits, its punctuation - travels
# through as itself, see get_lexer below
TELUGU_RE = re.compile('[ఀ-౿]')

class NatsGlyphs(BaseFont):
    '''The text of a pdf that is set in NATS - the telugu of the Andhra
       Pradesh gazette - and whose ToUnicode map has been repaired by
       tools/fix_tounicode.py.

       WHY THIS FONT NEEDS A PASS AT ALL

       fonts/telugu/priyaanka.py reads PriyaankaBold, the legacy 8 bit
       telugu of the Telangana gazette: there every glyph sits on a byte of
       the mac roman table and the text of a pdf is the keys the typist
       pressed, so it has to be decoded. NATS is a real opentype font and
       its glyphs really are telugu - what is wrong is the map that says
       which. The producer built that map by pairing the glyphs of a cluster
       with the characters of the cluster in order, so the first cluster a
       glyph was drawn in decides what it says everywhere: the one glyph of
       ని is handed 'న్న' out of the first న్ని of the document and the ్న
       behind it the 'ి' that was left over, which reads correctly for
       ఎన్నికల and for nothing else - అంతస్తు extracts as అంతసు and
       గ్రామ పంచాయతీ as గ్రమ ప్ంచాయతీ. tools/fix_tounicode.py builds the map
       again from NATS, a table of what the glyphs really draw, read off the
       blocks the font lays them out in and checked against its own GSUB.

       What the repair leaves is the order, and the two passes below are the
       whole of this converter - exactly as they are the whole of
       fonts/tamil/tauelango.py for the tamil of a repaired pdf.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       Telugu draws the mark of a syllable on the body of it and hangs the
       vattus - the consonants that a virama binds to the one before them -
       under that body. So the mark is drawn before them and unicode writes
       it behind them, and every vattu is moved in front of the marks it was
       drawn behind: ఎన్నికల is drawn ఎ ని ్న క ల, గ్రామ is drawn గా ్ర మ
       and అంతస్తు is drawn అ ం త సు ్త. A syllable with more than one vattu
       comes out with all of them in the order they were drawn - దృష్ట్యా is
       drawn దృ షా ్ట ్య - and a mark the font draws in two pieces is two
       marks by the time this runs, so the vattu goes in front of both.

       WHAT DRAWS LESS THAN A CHARACTER

       Two glyphs of the font do. The first is the ai length mark, the back
       half of ై: this font draws that sign as the ె it draws anyway and a
       mark of its own, so హై is హె and ౖ and composeTokens reads the pair
       back as the one sign. Unicode says the same thing - ై is canonically
       ె and ౖ - so the rule is a normalisation as much as a reordering.

       The second is the pollu, the virama a dead consonant is written with.
       The font has a glyph per letter for it and draws it on the body of
       the syllable like any other mark, so it is drawn in front of the
       vattus and unicode writes it at the end of the whole cluster - కోర్ట్
       is drawn కో ర్ ్ట and జడ్జ్ is drawn జ డ్ ్జ. It is one of the marks
       a vattu travels over, which is all it takes to put it where it
       belongs. A ర that is not written with the pollu is a different glyph
       of the font, so this costs కార్య - drawn కా ర ్య - nothing.

       A character no rule matched - the latin of the document, its digits,
       its punctuation - comes out the way it went in.
    '''
    # the marks that stand on the body of a syllable: the vowel signs, the
    # two length marks that are the back half of a two part sign, and the
    # pollu, which is the mark of a syllable that has no vowel at all. A
    # mark is drawn in front of the vattus that hang under that body and
    # unicode writes it behind them, so these are the tokens that a vattu
    # travels over - see reorder_vattus(). The anusvara and the visarga are
    # deliberately not among them: both are written behind the vowel sign of
    # their syllable and drawn there too, so nothing of a syllable ever
    # follows them
    marks = ('MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU', \
             'MATRA_VOCALIC_R', 'MATRA_VOCALIC_RR', 'MATRA_E', 'MATRA_EE', \
             'MATRA_AI', 'MATRA_O', 'MATRA_OO', 'MATRA_AU', \
             'LENGTH_MARK', 'AI_LENGTH_MARK', 'VIRAMA')

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(telugu.TeluguUnicode())
        self.langobjs.append(telugu.Vattus())

        self.lexer  = self.get_lexer()
        self.vattus = set(telugu.Vattus().get_tokens())

        self.composeTokens = { \
            # the two halves of ై, put back together once the vattus of the \
            # syllable have been moved in front of them - this font draws   \
            # that sign as a ె and a length mark of its own, and unicode    \
            # spells it the same way \
            ('MATRA_E', 'AI_LENGTH_MARK') : 'MATRA_AI', \
        }

    def reorder_vattus(self, tokentypes):
        '''the mark of a syllable is drawn on the body of it and the vattus
           hang under that body, so the mark is drawn in front of them and
           unicode writes it behind them. Every vattu is moved in front of
           the marks it follows, so a syllable that has more than one of
           them comes out with all of them in the order they were drawn -
           దృష్ట్యా is drawn దృ షా ్ట ్య. The pollu of a dead consonant is
           one of those marks and ends up behind the whole cluster, which is
           where unicode writes it: కోర్ట్ is drawn కో ర్ ్ట'''
        out = []
        for toktype in tokentypes:
            if toktype not in self.vattus:
                out.append(toktype)
                continue

            index = len(out)
            while index > 0 and out[index - 1] in self.marks:
                index -= 1
            out.insert(index, toktype)
        return out

    def to_unicode(self, data):
        '''the two halves of ై are joined after the reordering and not
           before it: a vattu of the same syllable is drawn between them -
           నట్లైతే is ట ె ్ల ౖ - and has to be moved out from between them
           first'''
        tokentypes = self.tokenize(data)

        tokentypes = self.reorder_vattus(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def extra_rules(self):
        '''the rules of a font of this script whose pattern is more than the
           string of the token it reads, as a token name -> pattern dict.
           NATS has none - every glyph of it says exactly what it stands for
           - and fonts/telugu/nirmalaui.py has one, the vattu of ra that is
           drawn in front of its letter and carries a mark to say so'''
        return {}

    def get_lexer(self):
        '''a rule per token of langs/telugu.py whose string is telugu. The
           repaired map hands out those strings themselves - a glyph of this
           font is a letter, a mark, a vattu or a letter with one mark
           written into it, and NATS writes each of them the way
           langs/telugu.py does - so the tokens are read straight off the
           language rather than listed again here.

           ply orders its string rules by falling length, so the vattu of a
           letter always wins over the virama and the letter apart: ్క is
           one token and not two'''
        rules  = {}
        tokens = []

        # the rules that a font of this script needs beyond the strings the
        # language names, which are read first: a token that has one here is
        # skipped by the loop below, its pattern being more than its string
        for tokenName, pattern in self.extra_rules().items():
            rules['t_' + tokenName] = pattern
            tokens.append(tokenName)

        for obj in self.langobjs:
            for tokenName, ustr in obj.tokendict.items():
                # the punctuation, the spaces and the latin that
                # langs/telugu.py also names are text rather than glyphs of
                # this font's telugu, and reach the output through the
                # literal path of t_error
                if not TELUGU_RE.search(ustr) or 't_' + tokenName in rules:
                    continue
                rules['t_' + tokenName] = re.escape(ustr)
                tokens.append(tokenName)

        def t_error(t):
            # a character this font's telugu has no token for: the latin of
            # the document, a digit, the punctuation, or a glyph of the font
            # that the repair could not name and that nothing can turn into
            # a character
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
        rules['tokens']  = tokens

        # the rules are made in a loop, so they are handed to ply in an
        # object of their own rather than in the locals of this function.
        # ply looks up the module of that object
        rules['__module__'] = self.__class__.__module__
        return lex.lex(object = types.SimpleNamespace(**rules))
