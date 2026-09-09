import re
import string
import types

from indic2unicode.langs import gujarati
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class KrishnaUni(BaseFont):
    '''KrishnaUni is the unicode gujarati font that the Gujarat Government
       Gazette is set in, and the pdfs of it carry the same kind of broken
       ToUnicode map as the ones that are set in Arial Unicode MS and in
       Nirmala UI: the map was built by pairing the glyphs of a run with the
       characters of that run one by one, and gujarati shaping draws a
       syllable in a different number of glyphs than it is written in, so the
       pairing slips on every glyph that was moved or made. The text that
       comes out of such a pdf is therefore gujarati that is

       1. in the visual order of the glyphs and not in the order of unicode,
          so િ sits in front of the cluster it belongs to and the reph behind
          the whole syllable it sits on, and

       2. spelled with the wrong characters for a part of the alphabet, e.g.
          'ર્' for ka and 'િ' for ca, which are the two that were paired with
          the neighbour they were first drawn beside.

       So the text is treated like any other font of this package: every
       glyph of the font is a token, the token is given the unicode string it
       really stands for and the tokens are put back in the order that
       unicode wants. કરવા comes out of the pdf as ર્રવા, વિભાગ as ચવભાગ and
       પ્રસિદ્ધ as િચસદ્ધ.

       WHAT EVERY GLYPH REALLY SAYS

       The readings below are not guessed off the page. The pdf embeds the
       font and this subset keeps its cmap and the whole of its GSUB, so what
       a glyph draws is in the document itself: the cmap says which character
       draws which glyph, and the GSUB says which glyphs the shaper made out
       of which other ones, so a half form spells out as its consonant and a
       virama, a rakar as a virama and a ra, and a ligature as the glyphs it
       was made of. Every one of the 90 glyphs the regular face of this
       document draws was read that way, and the text that those readings
       make of the document is the text an OCR of the same pages reads.

       WHAT IS LOST

       The map cannot be inverted completely, and what is lost is what two
       glyphs were handed the same string for.

       * sha. ક and શ were both first drawn in a syllable that carries a
         reph, so both of them are handed the 'ર્' of it. 'ર્' is read as ka,
         which this document draws 33 times against sha's 7, and sha is lost
         - વપરાશના comes out as વપરાર્ના and is converted as વપરાકના.

       * the conjuncts પ્ર and ક્ત. Both of them were first drawn in a
         cluster that carries a િ, as ca was, so all three are handed that
         'િ'. It is read as ca, which this document draws 13 times against
         the other two's 6 together, so પ્રસિદ્ધ comes out as િચસદ્ધ and is
         converted as ચસિદ્ધ.

       * seven of the eight rephs. The font draws the reph with a glyph of
         its own and with a glyph that carries the vowel sign of the syllable
         it sits on, and this document draws two of the first and one of the
         second. Of the two plain ones, one is handed a 'મ', which ma is
         handed as well and draws 65 times against its 5, and the other is
         handed a 'ક' - ka itself is handed the 'ર્' above, so nothing else
         of this face says 'ક', and that is the one reph that is kept, નેટવર્ક
         coming out as નેટવર્ક. The reph over a ે is handed that 'ે': સર્વે
         comes out as સવે and is converted as સવે.

       * the ુ that hangs under a ક. Its glyph is handed no string at all and
         comes out of the pdf as the space of its own advance, so કુંભારા
         comes out as "ક ુંભારા". A space that an anusvara follows is read
         back as that ુ, no real space of this document being followed by a
         sign of any kind, which brings back કુંભારા and કુંવારા. The third,
         the કુમાર that a consonant follows, is lost.

       WHAT IS NOT LOST, AND WHY

       The three glyphs of િ are handed the character of the letter they were
       first drawn in front of, which is how 'ચ' comes to be a vowel sign and
       'િ' a consonant. Two of the three are brought back:

       * 'ચ' is read as િ outright. ca is handed the 'િ' above, so no glyph
         of this face says 'ચ' but that one.

       * 'દ' is da as well as િ, and the િ of it is the glyph the font draws
         in front of a દ or a ડ - which is what this document draws it in
         front of every one of the six times it uses it, no da of the
         document being followed by either letter. So a 'દ' that દ or ડ
         follows is read as િ, દિવસની coming out as દદવસની and સંપાદિત as
         સાંપાદદત.

       The anusvara has four glyphs here and three of them carry the vowel
       sign of the letter they were first drawn over, so they are handed
       'ાં', 'ું' and 'ીં' rather than a plain 'ં'. Each of those is one
       anusvara and not two characters - ગાંધીનગર comes out as ગાાંધીનગર and
       બિલ્ડીંગ as ચબલ્ડીંગ.

       276 of the words the regular face of the test document draws carry a
       gujarati letter rather than nothing but digits, and 257 of them come
       out of this converter as the pdf itself says they were drawn.

       THE BOLD FACE

       The gazette sets its headings in KrishnaUni,Bold, and that is a subset
       of its own with a map that was broken over its own first drawings:
       'ર્' is ma there rather than ka, 'ક' is ka rather than a reph, 'િ' is
       ca, dha or ત્ત rather than ca alone, 'ત્ત' is a િ and 'ાં' is a ા and
       an anusvara rather than an anusvara on its own. The two faces cannot
       be told apart in the text, one string of characters being all that
       reaches a converter, so this one reads the regular face, which draws
       24993 of the 25694 glyphs of the test document against the bold face's
       701. The headings are read as the regular face would say them and come
       out wrong - નર્મદા, જળસંપત્તિ, પાણી પુરવઠા અને કલ્પસર વિભાગ comes out
       of the pdf as નર્મદા, જળસંપત્તિ, પાણી પુરવઠા અને કલ્પસર ત્તવભાગ and is
       converted as નકમદા, જળસંપત્તચ, પાણી પુરવઠા અનેર્ લ્પસર ત્તવભાગ.
    '''
    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(gujarati.GujaratiUnicode())
        self.langobjs.append(gujarati.Conjuncts())
        self.langobjs.append(gujarati.KrishnaUni())

        self.lexer = self.get_lexer()

        # િ is drawn in front of the cluster it belongs to
        self.waitdict   = {'MATRA_I': 1}

        # the reph is drawn as a stroke over the syllable it belongs to and
        # is stored behind the whole of it
        self.jumpbefore = {'REPH': 1}

        # the half forms, which are the head of the cluster that follows
        # them, and the vowel signs and the marks that are drawn on a letter
        self.deadtokens = set()
        self.signtokens = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                ustr = obj.get_unicode_string(tokenName)
                if tokenName.startswith('DEAD_'):
                    self.deadtokens.add(tokenName)
                elif tokenName == 'REPH':
                    continue
                elif self.is_sign(ustr):
                    self.signtokens.add(tokenName)

        # while the reph jumps back to the head of its syllable it has to
        # jump over the vowel signs and the marks of that syllable
        self.jumpover = set(self.signtokens)

        # a half form is not the letter િ is waiting for, it is the head of
        # the cluster that િ belongs to, and so is a reph that has already
        # jumped to the head of the syllable
        self.halftokens = set(self.deadtokens)
        self.halftokens.add('REPH')

        self.composeTokens = { \
            # the િ that is handed a 'દ', which is the glyph the font draws
            # in front of a દ or a ડ - see the class comment
            ('DA', 'DA')          : ['MATRA_I', 'DA'],       \
            ('DA', 'DDA')         : ['MATRA_I', 'DDA'],      \
            # the ુ under a ક, which is handed the space of its own
            # advance. No real space of this document is followed by a sign
            ('SPACE', 'ANUSVARA') : ['MATRA_U', 'ANUSVARA'], \
        }

    def is_sign(self, ustr):
        '''whether the string of a token is a vowel sign or a mark that is
           drawn on the letter of its syllable'''
        if ustr == None or len(ustr) != 1:
            return False

        # the vowel signs and the virama, the marks that are drawn over a
        # letter - ઁ ં ઃ - the nukta and the two vowel signs that unicode
        # puts behind the letters, ૢ and ૣ
        return '\u0abe' <= ustr <= '\u0acd' or \
               '\u0a81' <= ustr <= '\u0a83' or ustr == '\u0abc' or \
               '\u0ae2' <= ustr <= '\u0ae3'

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
        t_A              = pat('અ')
        t_AA             = pat('આ')
        t_I              = pat('ઇ')
        t_II             = pat('ઈ')
        t_U              = pat('ઉ')
        t_E              = pat('એ')

        # CONSONANTS. ka is handed the reph of the syllable it was first
        # drawn in and ca the િ of the cluster it was first drawn in
        t_KA             = pat('ર્')
        t_KHA            = pat('ખ')
        t_GA             = pat('ગ')
        t_GHA            = pat('ઘ')

        t_CA             = pat('િ')
        t_CHA            = pat('છ')
        t_JA             = pat('જ')

        t_TTA            = pat('ટ')
        t_TTHA           = pat('ઠ')
        t_DDA            = pat('ડ')
        t_DDHA           = pat('ઢ')
        t_NNA            = pat('ણ')

        t_TA             = pat('ત')
        t_THA            = pat('થ')
        t_DA             = pat('દ')
        t_DHA            = pat('ધ')
        t_NA             = pat('ન')

        t_PA             = pat('પ')
        t_PHA            = pat('ફ')
        t_BA             = pat('બ')
        t_BHA            = pat('ભ')
        t_MA             = pat('મ')

        t_YA             = pat('ય')
        t_RA             = pat('ર')
        t_LA             = pat('લ')
        t_LLA            = pat('ળ')
        t_VA             = pat('વ')
        t_SHA            = pat('શ')
        t_SA             = pat('સ')
        t_HA             = pat('હ')

        # HALF FORMS, which is what the font draws a cluster it has no
        # ligature of its own for with
        t_DEAD_KA        = pat('ક્')
        t_DEAD_KHA       = pat('ખ્')
        t_DEAD_GA        = pat('ગ્')
        t_DEAD_JA        = pat('જ્')
        t_DEAD_NA        = pat('ન્')
        t_DEAD_LA        = pat('લ્')
        t_DEAD_VA        = pat('વ્')
        t_DEAD_SA        = pat('સ્')

        # CONJUNCTS, each of them a ligature of its own in the font
        t_KA_KA          = pat('ક્ક')
        t_TA_TA          = pat('ત્ત')
        t_TA_RA          = pat('ત્ર')
        t_DA_DHA         = pat('દ્ધ')
        t_LA_LA          = pat('લ્લ')
        t_SHA_RA         = pat('શ્ર')

        # the letters that the font draws together with the sign behind them
        t_JA_MATRA_AA    = pat('જા')
        t_JA_MATRA_II    = pat('જી')
        t_JA_MATRA_O     = pat('જો')
        t_RA_MATRA_U     = pat('રુ')

        # MATRAS. િ is handed the letter it was first drawn in front of, and
        # the 'દ' of the second of its glyphs is da as well, see
        # self.composeTokens
        t_MATRA_AA       = pat('ા')
        t_MATRA_I        = pat('ચ')
        t_MATRA_II       = pat('ી')
        t_MATRA_U        = pat('ુ')
        t_MATRA_UU       = pat('ૂ')
        t_MATRA_E        = pat('ે')
        t_MATRA_O        = pat('ો')

        # SIGNS. three of the four anusvara glyphs carry the vowel sign of
        # the letter they were first drawn over, and the reph is handed a
        # 'ક', ka itself being handed the 'ર્' above
        t_ANUSVARA          = pat('ાં', 'ું', 'ં')
        t_MATRA_II_ANUSVARA = pat('ીં')
        t_MATRA_E_ANUSVARA  = pat('ેં')
        t_REPH              = pat('ક')

        # DIGITS
        t_ZERO           = pat('૦')
        t_ONE            = pat('૧')
        t_TWO            = pat('૨')
        t_THREE          = pat('૩')
        t_FOUR           = pat('૪')
        t_FIVE           = pat('૫')
        t_SIX            = pat('૬')
        t_SEVEN          = pat('૭')
        t_EIGHT          = pat('૮')
        t_NINE           = pat('૯')

        # PUNCTUATIONS
        t_LEFTPARAN      = pat('(')
        t_RIGHTPARAN     = pat(')')
        t_LEFTSQBRACE    = pat('[')
        t_RIGHTSQBRACE   = pat(']')
        t_COMMA          = pat(',')
        t_DOT            = pat('.')
        t_DASH           = pat('-')
        t_ENDASH         = pat('–')
        t_SLASH          = pat('/')
        t_COLON          = pat(':')
        t_LDQUOTE        = pat('“')
        t_RDQUOTE        = pat('”')
        t_SPACE          = pat(' ')
        t_NEWLINE        = pat('\n')
        t_CARRIAGERET    = pat('\r')
        t_TAB            = pat('\t')
        t_FORMFEED       = pat('\f')

        def t_error(t):
            # the text of this font is unicode already and only its
            # characters and its order are wrong, so a character with no
            # token of its own is not a glyph waiting to be reordered, it is
            # text - a bullet, an ellipsis, a zero width joiner - and has to
            # come out the way it went in rather than be dropped. Only a
            # glyph code that no map could turn into a character is dropped,
            # and that is reported
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
