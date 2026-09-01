import re
import types

from indic2unicode.langs import tamil
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

# the script this converter reads. A token is built for every string of
# langs/tamil.py that carries one of these characters, and everything else of
# a run - the latin of the document, its digits, its punctuation - travels
# through as itself, see get_lexer below
TAMIL_RE = re.compile('[\u0b80-\u0bff]')

class TauElangoGlyphs(BaseFont):
    '''The text of a pdf that is set in TAUElangoPanchali - the tamil of the
       Tamil Nadu gazette, drawn in 2,764 of the 8,248 documents of that
       corpus - and whose ToUnicode map has been repaired by
       tools/fix_tounicode.py. It is the one face of the TAU Elango family
       that carries a broken map: TAUElangoPanchali-SC700 and
       TAUElangoValluvan extract correctly and must not be sent through
       here, a reorder of text that is already in order being what destroys
       it.

       WHY THIS FONT NEEDS A PASS AT ALL

       fonts/tamil/tamelango.py reads TAM_ELANGO_Panchali, the legacy 8 bit
       font of the same foundry: there every glyph sits on a byte and the
       text of a pdf is the keys the typist pressed, so it has to be decoded.
       TAUElangoPanchali is the unicode font of that family and its glyphs
       really are tamil - what is wrong is the map that says which. The
       subsets carry neither a cmap nor a post nor a GSUB, only outlines, and
       the producer built the map by pairing the glyphs of a run with the
       characters of that run one by one, which tamil shaping makes slip:
       கூறிற்காக extracts as கூறிற்்கநா்க, the one glyph of கா being handed a
       '்க' and the ா a 'நா'. tools/fix_tounicode.py builds that map again
       from TAU_ELANGO_PANCHALI, a table of what the glyphs really draw.

       What the repair leaves is the order. A glyph carries the characters it
       stands for, but the glyphs are still stored in the order they are
       drawn in, and tamil draws three of its vowel signs in front of the
       letter they belong to. So the two reordering passes are the whole of
       this converter, exactly as they are the whole of
       fonts/glyphs/arialuni_glyphs.py for the devanagari of a repaired pdf.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       The vowel signs ெ, ே and ை are drawn to the left of their consonant
       and unicode writes them behind it, so each of them waits for one token
       and is emitted after it - அைமக்கப்படுதல் is அமைக்கப்படுதல் and
       ேவண்டும் is வேண்டும். A letter is one token here however many glyphs
       the font draws it in, which is what makes the wait a one rather than a
       count of glyphs: a ெ in front of the single glyph of ன் is emitted
       behind the whole of it and not between the letter and its pulli.

       The signs ொ and ோ are drawn in two halves with the letter between
       them, so they arrive as a ெ or a ே in front and a ா behind and are put
       back together by composeTokens once the front half has jumped. ௌ is
       drawn the same way out of a ெ and the length mark ௗ, which this font
       does draw - கௌசல்யா is ெ + க + ௗ + ச + ல் + ய + ா - so unlike
       fonts/tamil/tamelango.py, whose 8 bit font puts that mark on a byte no
       document of the corpus draws, this pass has the rule for it.

       This is why to_unicode runs its passes the other way round from
       BaseFont.to_unicode: a ெ and the ா of the same sign have the letter
       between them until the ெ has jumped over it.

       WHAT IS CARRIED THROUGH RATHER THAN READ

       The pulli and the four signs the font writes into a letter are glyphs
       of their own as well as parts of the single glyph syllables, and each
       of them belongs to the letter in front of it: க்ஷி is drawn as the one
       glyph of க்ஷ and a ி of its own. They are in waitover so that a sign
       that is still waiting to jump stays behind them rather than landing
       between a letter and its own mark. ா is deliberately not among them -
       it is the back half of ொ and has to end up behind the ெ that jumped,
       or the two could not be composed.

       A character no rule matched - the latin of the document, its digits,
       its punctuation, the ௐ this font does not draw - comes out the way it
       went in.
    '''
    # the vowel signs that are drawn in front of the letter they belong to.
    # Each of them waits for one token
    prefix_matras = ('MATRA_E', 'MATRA_EE', 'MATRA_AI')

    # the marks that belong to the letter in front of them, which a sign
    # that is waiting to jump has to stay behind rather than count
    trailing_signs = ('PULLI', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU')

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(tamil.TamilUnicode())
        self.langobjs.append(tamil.Conjuncts())

        self.lexer = self.get_lexer()

        self.waitdict = {}
        for tokenName in self.prefix_matras:
            self.waitdict[tokenName] = 1

        self.waitover = set(self.trailing_signs)

        self.composeTokens = { \
            # the two halves of a vowel sign that is drawn with the letter  \
            # between them, put back together once the front half has       \
            # jumped over that letter                                       \
            ('MATRA_E',  'MATRA_AA')       : 'MATRA_O',  \
            ('MATRA_EE', 'MATRA_AA')       : 'MATRA_OO', \
            # ௌ, which is drawn the same way out of a ெ and the length mark \
            # of its own - கௌசல்யா is ெ க ௗ ச ல் ய ா. The vowel ஔ needs no  \
            # rule beside it: this font draws that letter as a single glyph  \
            # (127) rather than out of a ஒ and the same mark                 \
            ('MATRA_E',  'AU_LENGTH_MARK') : 'MATRA_AU', \
        }

    def to_unicode(self, data):
        '''the vowel signs have to be put where unicode wants them before the
           two halves of a two part sign can be joined, so the passes run the
           other way round here from BaseFont.to_unicode: a ெ and the ா of
           the same sign have the letter between them until the ெ has jumped
           over it'''
        tokentypes = self.tokenize(data)

        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def get_lexer(self):
        '''a rule per token of langs/tamil.py whose string is tamil. The
           repaired map hands out those strings themselves - a glyph of this
           font is a whole syllable of one letter and one sign, and
           TAU_ELANGO_PANCHALI writes it the way tamil.Conjuncts does - so
           the tokens are read straight off the language rather than listed
           again here.

           ply orders its string rules by falling length, so the longer
           reading of a string that is the head of another always wins: க்ஷ
           before க், க் before க, ஸ்ரீ before ஸ்'''
        rules = {}
        tokens = []

        for obj in self.langobjs:
            for tokenName, ustr in obj.tokendict.items():
                # the punctuation, the spaces and the latin that
                # langs/tamil.py also names are text rather than glyphs of
                # this font's tamil, and reach the output through the
                # literal path of t_error
                if not TAMIL_RE.search(ustr) or 't_' + tokenName in rules:
                    continue
                rules['t_' + tokenName] = re.escape(ustr)
                tokens.append(tokenName)

        def t_error(t):
            # a character this font's tamil has no token for: the latin of
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
