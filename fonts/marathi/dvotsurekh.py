import re
import types

from indic2unicode.langs import devanagari, marathi
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

# the script this converter reads straight through. A token is built for
# every string of the language tables that is one character of it - the
# letters, the matras and the signs that the map of this font does hand out
# correctly - see get_lexer() below
DEVANAGARI_RE = re.compile('[ऀ-ॿ]')


class DVOTSurekh(BaseFont):
    '''The marathi of a pdf that is set in DVOT-Surekh, the font the Mumbai
       Suburban supplement of the Maharashtra gazette sets its notifications
       in, or in any other typeface of the DVOT family.

       ONE TABLE FOR THE WHOLE FAMILY

       The table below is keyed by glyph id, and every DVOT face shares one
       glyph order - DVOTSurekhMR and DVOTYogeshMR were checked against each
       other glyph by glyph and agree on all 691 of them, the two typefaces
       drawing the same letter at the same id. So a converter for one of
       them is a converter for all of them, and the faces of a family - the
       normal, the bold, the italic - are only weights of the same order.

       WHAT THE TEXT OF SUCH A PDF LOOKS LIKE

       The font is carried as a Type0/Identity-H font, so a glyph of it is
       written into the page as its glyph id, and the ToUnicode map says
       what each of those ids stands for. That map is not wrong about any
       glyph it names - a ka really is 'क' and the matra aa really is 'ा' -
       but it names only the 58 glyphs that stand for one character on their
       own. Everything a devanagari font draws as a letter of its own is
       missing from it: every half consonant, every conjunct the font has a
       ligature for, the reph, and every matra that carries an anusvar or a
       reph.

       So the text of such a pdf is devanagari with holes in it, and what
       fills a hole depends on the extractor. An extractor that falls back
       on the glyph id when the map has nothing to say - pymupdf and mutool
       do - writes that id as a character, and that is the text this
       converter reads: जिल्हाधिकारी comes out as 'िजÊहािधकारी', where
       U+00CA is glyph 202 and glyph 202 is the half la. The glyphs of this
       font are numbered under 700 and every id is written as itself, so a
       glyph code is always a latin, a latin extended or an IPA character
       and can never be confused with the devanagari of the map.

       An extractor that drops what the map does not name - pdftotext does -
       loses those glyphs outright, and no converter can put them back. The
       text of such an extraction still goes through this one and still
       comes out in the right order, but the half consonants, the conjuncts
       and the rephs of it are simply gone. That is what
       tools/fix_tounicode.py is for: it writes the missing glyphs into the
       map of the pdf itself, out of the same table as the one below, and
       then every extractor gives the whole text.

       So this converter reads a glyph two ways - as the glyph id of a pdf
       that nothing has repaired, and as the characters that a repaired map
       hands it - and the two are the same rule with two spellings. It is
       the one converter of this package that reads a repaired pdf without
       being a fonts/glyphs pass of its own, and it can be because an
       unrepaired DVOT is not wrong about anything it does say: the text of
       both is the same text in the same order, one of them merely short of
       50 glyphs.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       The glyph ids are written into the page in the order the glyphs are
       drawn, which is not the order unicode writes them in. Two things
       travel, exactly as they do in fonts/marathi/yogesh.py:

       1. The matra i is drawn in front of the syllable it belongs to and
          unicode writes it behind that syllable's consonant, so it waits
          for one - and it waits over the half consonants on the way,
          because those are the head of the syllable it belongs to. अस्तित्वात
          is अ [ि] स् त त् व ा त and the matra i lands behind the ta of
          स्त. So do the two glyphs that draw the matra i with an anusvar on
          it, and so does the one that draws it with a reph - but the reph
          of that one is drawn in front of the letter as well, which is
          where unicode writes it, so only the matra travels there and the
          reph stays: निर्दिष्ट is ि न [ि+र्] द ष् ट.
       2. The reph is drawn on the last letter of the syllable it opens and
          unicode writes it in front of that syllable, so it is written
          after the syllable and moves back over it - निर्णय is ि न ण [र्] य.
          It jumps over the matras and the signs of the syllable on its way,
          so it lands in front of the consonant and not in front of its
          matra. The five glyphs that draw a matra with a reph on it carry a
          reph that moves the same way: होण्यापूर्वी is हो ण् य ा प ू व [ी+र्].

       Nothing else moves. The half consonants, the conjuncts and the matras
       that follow their consonant are all written where unicode wants them,
       so the whole pass is those two jumps and the table below.

       WHAT IS ON THE DIGIT KEYS

       The devanagari digits, so १४ is typed 14. A pdf carries this font
       twice - as the Type0 font the devanagari is set with, whose subset
       has no digit glyph at all, and as a simple 8 bit font with
       WinAnsiEncoding that draws the numbers of the document, the dates
       and the serial and the aadhaar numbers of these notifications. That
       one carries no ToUnicode map, so an extractor reads its bytes
       through the windows table and gives out latin digits for glyphs that
       draw devanagari ones - ५ वर्षांकरिता is extracted as "5 वषȝकिरता".
       The punctuation of that embedding is what its keys draw, so the
       commas, the dots, the slashes and the brackets are themselves.
    '''

    # THE LATIN DIGITS the simple embedding of this font is read as. The
    # keys of the digits draw the devanagari ones
    DIGITS = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', \
              'SEVEN', 'EIGHT', 'NINE']

    # THE GLYPHS THE TOUNICODE MAP DOES NOT NAME, by glyph id. Every one of
    # them was read off the outline of the glyph the id draws and checked
    # against the OCR of the document. What each id says is a fact about the
    # family and not about one document: a map names only the glyphs its own
    # document happened to draw, so the holes differ from pdf to pdf and this
    # table is the union of them.
    #
    # The font draws the matra i in a narrow form and a wide one, and the
    # matra i that carries an anusvar in both as well. Only the narrow plain
    # one is in the map, so MATRA_I has the wide id here and its own
    # character from the map, and MATRAIBINDU has the two ids and no
    # character at all.
    GLYPHS = {\
        # THE HALF CONSONANTS. Everything a marathi word can end a half
        # syllable with, in the order of the alphabet
        'ADHA_KA'    : [175], 'ADHA_GA'  : [177], 'ADHA_CA'  : [180], \
        'ADHA_JA'    : [182], 'ADHA_TTA' : [220], 'ADHA_NNA' : [189], \
        'ADHA_TA'    : [190], 'ADHA_DA'  : [192], 'ADHA_DHA' : [193], \
        'ADHA_NA'    : [194], 'ADHA_PA'  : [195], 'ADHA_BA'  : [197], \
        'ADHA_BHA'   : [198], 'ADHA_MA'  : [199], 'ADHA_LA'  : [202], \
        'ADHA_VA'    : [203], 'ADHA_SHA' : [204], 'ADHA_SSA' : [205], \
        'ADHA_SA'    : [206],                                         \

        # THE CONJUNCTS THE FONT DRAWS AS ONE LETTER, and the half form of
        # the one of them that marathi puts in front of another letter -
        # the ksha of लक्ष्मी
        'CHHHA'      : [169], 'ADHA_CHHHA' : [209], 'GYAN'    : [170], \
        'KRA'        : [270], 'GRA'        : [272], 'TTARA'   : [280], \
        'TRA'        : [285], 'DRA'        : [287], 'PRA'     : [290], \
        'BRA'        : [292], 'VRA'        : [296], 'TATA'    : [452], \
        'DADA'       : [456], 'DADHA'      : [457], 'DABHA'   : [460], \
        'DAYA'       : [463], 'SHRA'       : [475], 'HAYA'    : [489], \

        # THE RA THAT CARRIES ITS MATRA INSIDE THE LETTER. The font draws
        # the u and the uu of a ra in the bowl of the letter rather than
        # under it, so each of the two is a glyph of its own
        'RAU'        : [471], 'RAUU'     : [472], \

        # THE REPH, and the eyelash ra that is a letter rather than a reph
        'ADHA_RA'    : [171], 'ADHA_RRA' : [201], \

        # THE MATRAS THAT CARRY A SIGN. A matra and the anusvar or the reph
        # that sits on it are one glyph of this font
        'MATRA_I'         : [526],      'MATRAIBINDU'    : [523, 527], \
        'MATRAIRI2'       : [524],      'MATRAIIBINDU'   : [530],      \
        'MATRAIIRI'       : [531],      'MATRAEBINDU'    : [514],      \
        'MATRAERI'        : [515],      'MATRAOBINDU'    : [535],      \
        'MATRAORI'        : [536],      'MATRA_AA_ADHARA': [597],      \
        'MATRAAABINDURI'  : [541],                                     \
    }

    # THE GLYPHS THE FONT DRAWS IN AN ORDER OF THEIR OWN, as the string a
    # repaired map hands them. A repaired glyph carries its characters the
    # way it draws them and not the way unicode writes them - which is the
    # whole reason the text of a repaired pdf still has to be reordered -
    # and for the matras that carry a reph that is the matra first. Every
    # other glyph of GLYPHS is written as the string of its own token, which
    # get_lexer() reads off the language tables
    DRAWN = {'MATRAIRI2'      : 'िर्',  'MATRAIIRI'      : 'ीर्',  \
             'MATRAERI'       : 'ेर्',  'MATRAORI'       : 'ोर्',  \
             'MATRA_AA_ADHARA': 'ार्',  'MATRAAABINDURI' : 'ांर्'}

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(marathi.MarathiUnicode())
        self.langobjs.append(devanagari.Conjuncts())
        self.langobjs.append(marathi.DVOTSurekh())

        self.lexer = self.get_lexer()

        # matra_i, and the two glyphs that draw it with an anusvar on it,
        # are drawn in front of the consonant they belong to. The glyph
        # that draws it with a reph is not here: it is two tokens and the
        # matra_i of it is the one that waits
        self.waitdict   = {'MATRA_I': 1, 'MATRAIBINDU': 1}

        # the reph is written after the whole syllable it is drawn on
        self.jumpbefore = {'ADHA_RA': 1}

        # while the reph jumps back to the head of its syllable it has to
        # jump over the matras and the signs of that syllable, so that it
        # lands in front of the consonant and not in front of its matra
        self.jumpover = set([\
            'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',      \
            'MATRA_RI', 'MATRA_RR', 'CHANDRA', 'MATRA_E', 'MATRA_AI',      \
            'MATRA_CHANDRA_O', 'MATRA_O', 'MATRA_AU', 'HALANT', 'NUKTA',   \
            'BINDU', 'CHANDRABINDU', 'VISARGA', 'MATRAIBINDU',             \
            'MATRAIIBINDU', 'MATRAEBINDU', 'MATRAOBINDU',                  \
        ])

        # a half consonant is not the consonant matra_i is waiting for, but
        # it is the head of the syllable that matra_i belongs to, so it is
        # written in front of the matra rather than behind it
        self.halftokens = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName.startswith('ADHA_'):
                    self.halftokens.add(tokenName)

    def drawn_string(self, tokenName):
        '''the characters of a glyph in the order the font draws them, which
           is what a map that tools/fix_tounicode.py has repaired writes for
           it. A token that stands for more than one is spelled out of the
           tokens it is made of, and one whose glyph draws its characters in
           an order of its own is in DRAWN'''
        if tokenName in self.DRAWN:
            return self.DRAWN[tokenName]

        ustr = self.token_to_unicode(tokenName)
        if ustr != None:
            return ustr

        return ''.join([self.token_to_unicode(t) \
                        for t in self.multiple_tokens(tokenName)])

    def get_lexer(self):
        '''one rule per token, and a rule is every way this font writes that
           token: the glyph id of GLYPHS, which is what an unrepaired map
           leaves out and an extractor writes as a character of its own, the
           characters that a repaired map hands the same glyph, and the
           character itself for every token of the language tables that even
           an unrepaired map does hand out correctly.

           The glyph ids never collide with the characters. A glyph id of
           this font is under 700 and is written as the character of that
           codepoint, so it is latin, latin extended or IPA, while
           everything a map hands out is devanagari.

           Nor do the characters collide with each other. A rule of more
           than one character always wins over the rules of the characters
           it is made of, ply sorting its patterns by length, and the two
           readings that a shorter rule could give are the same reading
           anyway wherever they are not - क्र read as the half ka and a ra
           is the string क्र either way, and only the ि of िर् and of िं
           has to be held to the longer rule, which is where the two differ'''
        rules  = {}
        tokens = []

        def add(tokenName, pattern):
            name = 't_' + tokenName
            if name in rules:
                # another way of writing a token that already has a rule -
                # the character of a matra whose glyph id is in GLYPHS as
                # well. Alternate patterns of one token are one rule
                if pattern not in rules[name].split('|'):
                    rules[name] = rules[name] + '|' + pattern
            else:
                rules[name] = pattern
                tokens.append(tokenName)

        for tokenName, gids in self.GLYPHS.items():
            add(tokenName, '|'.join([re.escape(chr(gid)) for gid in gids]))
            add(tokenName, re.escape(self.drawn_string(tokenName)))

        for digit, tokenName in enumerate(self.DIGITS):
            add(tokenName, str(digit))

        for obj in self.langobjs:
            for tokenName, ustr in obj.tokendict.items():
                # only the tokens that are one character of the script. A
                # token of more than one - a half consonant, a conjunct -
                # is a glyph of this font and reaches the lexer as a glyph
                # id, never as the characters it stands for
                if len(ustr) == 1 and DEVANAGARI_RE.match(ustr):
                    add(tokenName, re.escape(ustr))

        def t_error(t):
            # a character this font has no token for: the punctuation of
            # the document, its brackets and quotes and dashes, its line
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
