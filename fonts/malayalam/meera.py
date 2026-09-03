import re
import types

from indic2unicode.langs import malayalam
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

# the script this converter reads. A token is built for every string of
# langs/malayalam.py that carries one of these characters, and everything else
# of a run - the latin of the document, its digits, its punctuation - travels
# through as itself, see get_lexer below
MALAYALAM_RE = re.compile('[ഀ-ൿ]')

class MeeraGlyphs(BaseFont):
    '''The text of a pdf that is set in Meera - the malayalam of the Kerala
       gazette - and whose ToUnicode map has been repaired by
       tools/fix_tounicode.py.

       WHY THIS FONT NEEDS A REPAIR AND NOT A DECODER

       fonts/malayalam/revathi.py reads ML-Revathi-Normal, a legacy 8 bit
       font of the same gazette: there every glyph sits on a byte, the pdf
       names the glyphs after the latin characters that live on those bytes
       and the text extracts as latin gibberish, so it has to be decoded.
       Meera is a unicode opentype font and its glyphs really are malayalam -
       what is wrong is the map that says which.

       The producer re-encodes the font subset by subset: a byte of the
       content stream is the number that subset gave the glyph, in the order
       that document happened to want them, and it writes a ToUnicode map
       naming each of those bytes. That map is right about nearly every
       glyph - a byte that draws the one glyph of ക്ക says ക്ക - and it fails
       on exactly the glyphs malayalam draws out of order: െ, േ and ൈ are
       drawn in front of the consonant they belong to, and the producer hands
       the *first* glyph of such a cluster the whole cluster and the glyph
       behind it nothing at all. So the െ of ലെ, the first word of the
       document to use it, is handed 'ലെ' and is then drawn in front of every
       other letter too, and the ല behind it is left with no entry anywhere:
       കേരള extracts as കേ(cid:2)രള and യുടെ as യുലെ<, the ട having no entry
       either and pdfminer falling back on the encoding for it.

       No reordering can undo that - the ട of a second cluster is not in the
       map to be moved - so tools/fix_tounicode.py rebuilds the map out of
       MEERA_OUTLINES before anything reads the pdf, and what is left for
       this pass is what is left for fonts/tamil/tauelango.py: the order.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       The vowel signs െ, േ and ൈ are drawn to the left of their consonant
       and unicode writes them behind it, so each of them waits for one token
       and is emitted after it - േകരള is കേരള and െചയ്യുന്നു is ചെയ്യുന്നു.
       A cluster is one token here however many letters it is written out of,
       which is what makes the wait a one rather than a count of letters: a േ
       in front of the single glyph of ക്ക belongs behind both letters and
       the chandrakkala between them, which is why langs/malayalam.py names
       every cluster this font draws.

       The signs ൊ and ോ are drawn in two halves with the letter between
       them, so they arrive as a െ or a േ in front and a ാ behind and are put
       back together by composeTokens once the front half has jumped -
       േപ്രാവിേസാ is പ്രോവിസോ. This is why to_unicode runs its passes the
       other way round from BaseFont.to_unicode: a െ and the ാ of the same
       sign have the letter between them until the െ has jumped over it.

       ൌ, the third sign that could be drawn in two halves, needs no rule
       beside them: this font draws the length mark ൗ as a glyph of its own
       and behind the letter it belongs to rather than in front of it, and
       the documents write the au of a syllable with that mark alone -
       അക്കൗണ്ട് is drawn അ ക്ക ൗ ണ് ട ്, and every one of the 169 ൗ that
       test/test_pdfs/malayalam-meera.pdf draws stands directly behind its
       own consonant. So there is no half of a sign left in front of a
       letter for anything to be composed with.

       WHAT IS CARRIED THROUGH RATHER THAN READ

       ്യ and ്വ - two of the three consonants that malayalam writes as a
       mark on the letter they are bound to - are glyphs of their own and are
       typed under that letter, so a vowel sign that is on its way past the
       letter has not passed the syllable until it has passed them as well:
       േന്വ is ന്വേ and ൈദ്വ is ദ്വൈ. They are in waitover for that, exactly
       as they are in fonts/malayalam/revathi.py. ്ര, the third of them, is
       drawn behind its letter in this font rather than in front of it and is
       part of the one glyph of the cluster, so unlike revathi's it needs no
       rule at all.

       A character no rule matched - the latin of the document, its digits,
       its punctuation - comes out the way it went in.

       WHAT THIS WAS CHECKED AGAINST

       The producer writes an /ActualText over each cluster it reorders,
       which is an answer key for exactly the thing this pass does: of the
       22,117 spans of test/test_pdfs/malayalam-meera.pdf, 17,215 come out of
       here character for character as the ActualText says, 2,323 differ only
       by the vowel sign the producer itself drops from some of those
       strings, 2,310 are the ാ of a two part sign whose ActualText names the
       whole ോ or ൊ it ends up as, and the remaining 269 are the space glyph,
       over which the producer writes a zero width joiner or non-joiner.

       And a tesseract -l mal ocr of the pages themselves, all 73 of them: of
       the 19,399 malayalam words this pass produces, 17,461 (90.0%) match
       the ocr of their own page character for character once the chillus are
       spelled alike on both sides. Over the whole document it produces
       188,607 malayalam characters and no (cid:N), 13 words beginning with a
       vowel sign and 15 with two vowel signs in a row - three distinct words
       between them, and all three the gazette's own typing, which the page
       shows as it is: 13-ാാം with the ാ drawn twice, അവയുമാി for അവയുമായി
       and ആക്റ്റുിൽ for ആക്റ്റിൽ.
    '''
    # the vowel signs that are drawn in front of the letter they belong to.
    # Each of them waits for one token
    prefix_matras = ('MATRA_E', 'MATRA_EE', 'MATRA_AI')

    # the marks that belong to the letter in front of them, which a sign that
    # is waiting to jump has to stay behind rather than count. ാ is
    # deliberately not among them - it is the back half of ൊ and has to end
    # up behind the െ that jumped, or the two could not be composed
    trailing_signs = ('YA_SIGN', 'VA_SIGN')

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(malayalam.MalayalamUnicode())
        self.langobjs.append(malayalam.Conjuncts())

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
        }

    def to_unicode(self, data):
        '''the vowel signs have to be put where unicode wants them before the
           two halves of a two part sign can be joined, so the passes run the
           other way round here from BaseFont.to_unicode: a െ and the ാ of
           the same sign have the letter between them until the െ has jumped
           over it'''
        tokentypes = self.tokenize(data)

        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def get_lexer(self):
        '''a rule per token of langs/malayalam.py whose string is malayalam.
           The repaired map hands out those strings themselves - a glyph of
           this font is a letter, a cluster, a sign or a syllable of one
           letter and one sign, and MEERA_OUTLINES writes each of them the
           way langs/malayalam.py does - so the tokens are read straight off
           the language rather than listed again here.

           ply orders its string rules by falling length, so the longer
           reading of a string that is the head of another always wins:
           ക്ട്ര before ക്ട, ക്ട before ക, ന്ത്ര before ന്ത'''
        rules  = {}
        tokens = []

        for obj in self.langobjs:
            for tokenName, ustr in obj.tokendict.items():
                # the punctuation, the spaces and the latin that
                # langs/malayalam.py also names are text rather than glyphs
                # of this font's malayalam, and reach the output through the
                # literal path of t_error
                if not MALAYALAM_RE.search(ustr) or 't_' + tokenName in rules:
                    continue
                rules['t_' + tokenName] = re.escape(ustr)
                tokens.append(tokenName)

        def t_error(t):
            # a character this font's malayalam has no token for: the latin
            # of the document, a digit, the punctuation, or a glyph of the
            # font that the repair could not name and that nothing can turn
            # into a character
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
