import re
import types

from indic2unicode.langs import devanagari, marathi
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

# the script this converter reads. A token is built for every string of
# langs/devanagari.py that is one character of it, and everything else of a
# run - the latin of the document, its punctuation, its line breaks - travels
# through as itself, see get_lexer below
DEVANAGARI_RE = re.compile('[ऀ-ॿ]')


class Abhishek(BaseFont):
    '''The marathi of a pdf that is set in FourCMRAbhishek, the font of the
       Mumbai Suburban supplement of the Maharashtra gazette.

       WHY THIS FONT NEEDS A PASS AT ALL

       fonts/marathi/yogesh.py reads DVBW-TTYogesh, the legacy 8 bit marathi
       of the same gazette: there every glyph sits on a byte of the windows
       1252 table and the text of a pdf is the keys the typist pressed, so it
       has to be decoded. FourCMRAbhishek is a real opentype font and its
       glyphs really are devanagari - what is wrong is the map that says
       which, and how much.

       The producer built that map by walking the glyphs of a run and the
       characters of the run together and handing each glyph the characters
       it had got to, up to and including the first character of the glyph
       behind it. So two glyphs that stand next to each other share the
       character on their boundary and the extractor writes that character
       twice: the ka of का carries 'का' and the matra behind it carries 'ा',
       so कारी comes out as काारीी, and the ना of दिनांक carries 'नां' and
       the anusvar behind it carries 'ं', so it comes out as दिनांंक. The
       /ActualText spans the producer writes over a part of the glyphs carry
       the same over long strings, so they say the same thing twice as well.

       A glyph that the walk had no characters left for is handed nothing at
       all, and the extractor writes a replacement character where it stands
       - the va of वि, whose 'वि' the matra_i in front of it has already been
       given, and the blank glyph the bold face ends its masthead with, which
       is handed an o with a tilde.

       WHAT IS NOT WRONG

       The order is not. A run is walked in the order of its characters and
       not in the order of its glyphs, so what comes out is in the order that
       unicode writes: matra_i sits behind its consonant and the reph in
       front of the syllable it is drawn on, because the string of the
       consonant the reph sits on carries the reph with it - the na of
       निर्णय is handed 'नि' and the nna 'र्ण'. Nothing has to be moved here,
       which is what separates this converter from the ones for the
       glyphs of Arial Unicode MS and of Nirmala UI.

       So the whole pass is to drop what the glyphs that were left nothing
       wrote, and to drop the second copy of every character that two glyphs
       share.

       WHICH SECOND COPY IS REALLY A SECOND COPY

       A matra or a sign is: no devanagari syllable carries the same one
       twice, so ाा, ीी, ंं and ेे are always one glyph's copy and the next
       one's.

       A letter that repeats can be a real pair - बबन, ममता, शशिकांत and
       पप्पू are all names of this document - so a letter is only a second
       copy where the pair cannot be real:

       - a letter that a reph opens, र्णण of निर्णय and र्यय of कार्य. The
         reph is drawn on that letter and is a glyph of its own, and the
         string it is handed is the letter it sits on.
       - a letter that a half form in front of it and a conjunct behind it
         share, ष्टट्र of महाराष्ट्र.

       A pair that neither describes is left alone, which costs the second
       half of a word that the extractor has run into the first: कॉपरेटिव्ह
       हाऊसिंग comes out as कॉपरेटिव्हहाऊसिंग and stays that way, rather
       than losing its ha.
    '''

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(devanagari.DevanagariUnicode())
        self.langobjs.append(marathi.Abhishek())

        self.lexer = self.get_lexer()

        # the marks a syllable is written with: the matras, the signs that
        # stand on it and the virama. None of them is ever written twice in
        # a row, so a second one of them is always the copy that the glyph
        # behind the first one was handed - see drop_shared_tokens()
        self.marks = set([\
            'CHANDRABINDU', 'BINDU', 'VISARGA', 'NUKTA', 'AVAGRAHA',       \
            'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',      \
            'MATRA_RI', 'MATRA_RR', 'CHANDRA', 'MATRA_SHORT_E', 'MATRA_E', \
            'MATRA_AI', 'MATRA_CHANDRA_O', 'MATRA_SHORT_O', 'MATRA_O',     \
            'MATRA_AU', 'HALANT', 'MATRA_L', 'MATRA_LL', 'UDATTA',         \
            'ANUDATTA', 'GRAVE_ACCENT', 'ACUTE_ACCENT',                    \
        ])

    def is_second_copy(self, out, tokentypes, i):
        '''whether the token at i, which repeats the one in front of it, is
           the copy that two glyphs sharing a character wrote and not a pair
           the text really has'''
        toktype = tokentypes[i]

        # a character that is not devanagari at all - the latin of the
        # document, its latin digits - is carried through as itself and is
        # no glyph of this font, so nothing of it was ever shared. The
        # devanagari digits are tokens and reach the tests below, and both
        # of those ask for a virama in front of the pair, which no digit of
        # an address or a date is ever written with
        if type(toktype) == tuple:
            return False

        if toktype in self.marks:
            return True

        # the reph is a glyph of its own and is drawn on the last letter of
        # the syllable it opens, so the string of that letter carries the
        # reph and the string of the reph carries the letter back: निर्णय
        # comes out as निर्णणय
        if len(out) >= 3 and out[-3] == 'RA' and out[-2] == 'HALANT':
            return True

        # a half form and the conjunct behind it share the letter they are
        # joined on, so महाराष्ट्र comes out as महाराष्टट्र. The second copy
        # is the head of the conjunct and a virama follows it
        if len(out) >= 2 and out[-2] == 'HALANT' and \
                i + 1 < len(tokentypes) and tokentypes[i + 1] == 'HALANT':
            return True

        return False

    def drop_shared_tokens(self, tokentypes):
        '''two glyphs that stand next to each other were handed the
           character on their boundary each, so it is written twice. Drop
           the second copy of it'''
        out = []
        for i, toktype in enumerate(tokentypes):
            if out and out[-1] == toktype and \
                    self.is_second_copy(out, tokentypes, i):
                continue
            out.append(toktype)
        return out

    def to_unicode(self, data):
        '''the glyphs that were left nothing are dropped before the copies
           are, so that the two characters they stand between are next to
           each other: किंमत comes out as किं�ंमत and the anusvar of it
           is only a repetition once the replacement character between the
           two is gone'''
        tokentypes = self.tokenize(data)

        tokentypes = [t for t in tokentypes if t != 'SPACER']
        tokentypes = self.drop_shared_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def get_lexer(self):
        '''a rule per token of langs/devanagari.py whose string is one
           character of the script. The map of this font hands out the
           characters themselves and only says them twice, so there is
           nothing to decode here and the tokens are read straight off the
           language rather than listed again.

           The conjuncts and the half forms are deliberately left out of it:
           a token of more than one character would swallow the boundary
           that the second copy sits on - ष्टट्र would be read as the
           conjunct ष्ट and the conjunct ट्र, with nothing repeated in
           between - so every rule here is a single character and every
           cluster is as many tokens as it has characters'''
        rules  = {}
        tokens = []

        for obj in self.langobjs:
            for tokenName, ustr in obj.tokendict.items():
                if len(ustr) != 1 or not DEVANAGARI_RE.match(ustr) or \
                        't_' + tokenName in rules:
                    continue
                rules['t_' + tokenName] = re.escape(ustr)
                tokens.append(tokenName)

        # the two characters that a glyph which was handed nothing is
        # written with. They draw nothing and stand for nothing
        rules['t_SPACER'] = '|'.join([re.escape(c) for c in ('�', 'õ')])
        tokens.append('SPACER')

        def t_error(t):
            # a character this font's devanagari has no token for: the latin
            # of the document, its latin digits, its punctuation, its line
            # breaks
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
