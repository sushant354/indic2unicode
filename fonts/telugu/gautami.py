import re
import types

from indic2unicode.langs import telugu
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

# the script this converter reads straight through. A token is built for
# every string of the language tables that is telugu - the letters, the
# vowel signs, the vattus and the signs that even a short map hands out
# correctly - see get_lexer() below
TELUGU_RE = re.compile('[ఀ-౿]')


class Gautami(BaseFont):
    '''The telugu of a pdf that is set in Gautami, the font the Andhra
       Pradesh gazette sets the notifications of its municipalities in, or
       in Gautami-Bold, the other face of it.

       WHAT THE TEXT OF SUCH A PDF LOOKS LIKE

       The font is carried as a Type0/Identity-H font, so a glyph of it is
       written into the page as its glyph id and the ToUnicode map says what
       each of those ids stands for. That map is not wrong about a single
       glyph it names - a ka really is 'క' and the vowel sign aa really is
       'ా' - it is only short, exactly as the map of the DVOT family is in
       fonts/marathi/dvotsurekh.py: it names the letters of the block, the
       vowel signs and the digits and stops there, 46 glyphs of the 221 the
       test document draws. Everything the shaper made is missing from it -
       every vattu, every dead consonant, every syllable the font draws in a
       single glyph, and every width variant of a vowel sign - so the text
       of such a pdf is telugu with holes in it.

       What fills a hole depends on the extractor. One that falls back on
       the glyph id when the map has nothing to say - pymupdf and mutool do
       - writes that id as a character, and that is the text this converter
       reads: ఫారం comes out as 'Ǹారం', where U+01F8 is glyph 504 and glyph
       504 is the ఫ that stands in front of a ా. One that drops what the map
       does not name - pdftotext does - loses those glyphs outright and no
       converter can put them back; the text of such an extraction still
       goes through this one and still comes out in the right order, but its
       vattus and its dead consonants are simply gone. Writing the missing
       glyphs into the map of the pdf itself, the way tools/fix_tounicode.py
       does it for the fonts it carries a table for, is what would give
       every extractor the whole text; this font has no table there yet.

       So this converter reads a glyph two ways, as fonts/marathi/dvotsurekh.py
       does - as the glyph id of a pdf that nothing has repaired, and as the
       characters that a repaired map hands it - and the two are the same
       rule with two spellings. It can be, because an unrepaired Gautami is
       not wrong about anything it does say: the text of a repaired pdf and
       of an unrepaired one are the same text in the same order, one of them
       merely short of the glyphs the shaper made.

       WHERE THE TABLE COMES FROM

       From the font itself. The subsets these pdfs carry keep the whole
       post table of Gautami, which names every one of its 872 glyphs and
       names them in a scheme that says what each of them draws: matraAa2 is
       a second width of ా, lvl1Ta1 is the vattu of త, kaHalant is the క of
       a dead consonant, naI is the one glyph the syllable ని is drawn in.
       They keep the cmap of the font as well, which is what says that
       glyphs 130 and up are the ones no character reaches - the letters,
       the signs, the digits, the latin and the punctuation that the cmap
       does name are the glyphs a short map still hands out, and are read
       here as the characters they arrive as rather than as ids.

       Every reading below was checked against the OCR of the test document,
       which is the only thing that can tell a lvl1Ra from a lvl2Ra - the
       font's own names say which glyph, not which character. Eleven glyphs
       that no page of that document draws are left out of the table rather
       than guessed at: lvl1KaRa, taKaRa and ssaKaRa with the four forms
       they are drawn in, altAa and nukta. Their names do not say what they
       are, the subsets carry no outline for them and no GSUB to spell them
       out of, and a glyph left alone loses a letter while a glyph read
       wrongly destroys the text around it.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       Telugu draws a syllable as a body with a mark on top of it and hangs
       the vattus - the consonants that a virama binds to the one before
       them - under that body. So the mark is drawn in front of them and
       unicode writes it behind them, and the whole of the reordering is
       moving every vattu in front of the marks it was drawn behind, exactly
       as fonts/telugu/nats.py does it for the other telugu of the same
       gazette: సర్వే is drawn సరే ్వ, ట్రాక్ is drawn టా ్ర క్ and
       షెడ్యూల్ is drawn షెడూ ్య ల్. A syllable with more than one vattu
       comes out with all of them in the order they were drawn.

       The pollu of a dead consonant is one of those marks. The font draws
       it on the body of the syllable like any other mark, so it is drawn in
       front of the vattus and unicode writes it at the end of the whole
       cluster, and moving the vattus over it puts it there.

       WHAT DRAWS LESS THAN A CHARACTER

       One glyph does: the ai length mark, the back half of ై. This font
       draws that sign as the ె it draws anyway and a mark of its own - in
       40 widths, aiLengthMark and matraAiBelow1 through matraAiBelow39 -
       so రైల్వే is drawn ర ె ౖ ల ే ్వ, and composeTokens reads the pair
       back as the one sign. Unicode says the same thing, ై being
       canonically ె and ౖ, so the rule is a normalisation as much as a
       reordering. It runs after the reordering and not before it: a vattu
       of the same syllable is drawn between the two halves - నట్లైతే is
       ట ె ్ల ౖ - and has to be moved out from between them first.

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
    marks = ('MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU',     \
             'MATRA_VOCALIC_R', 'MATRA_VOCALIC_RR', 'MATRA_VOCALIC_L',     \
             'MATRA_VOCALIC_LL', 'MATRA_E', 'MATRA_EE', 'MATRA_AI',        \
             'MATRA_O', 'MATRA_OO', 'MATRA_AU', 'LENGTH_MARK',             \
             'AI_LENGTH_MARK', 'VIRAMA')

    # THE VOWEL SIGNS, in the widths the font draws each of them in. The
    # sign that reaches an extractor as a character is the first width of
    # each of them - matraAa1, matraI1 and so on, the glyphs the cmap of the
    # font names - and every other width is a glyph the shaper chose and a
    # hole in the map. matraIAlt and matraIiAlt are the forms of the two
    # signs that are drawn beside a letter rather than into it
    MATRA_GLYPHS = {\
        'MATRA_AA'         : [130, 131, 132, 133, 134, 135, 136, 137],     \
        'MATRA_I'          : [138, 140, 141, 142, 143, 144, 145, 152, 153, \
                              154],                                       \
        'MATRA_II'         : [139, 146, 147, 148, 149, 150, 151, 155, 156, \
                              157],                                       \
        'MATRA_U'          : [158, 159, 160, 161, 166, 167, 168, 171, 173, \
                              175],                                       \
        'MATRA_UU'         : [162, 163, 164, 165, 169, 170, 172, 174, 176],\
        'MATRA_E'          : [177, 178, 179, 180, 181, 182, 183, 184, 185, \
                              186, 187, 188, 189, 190, 191, 192, 193],    \
        'MATRA_EE'         : [194, 195, 196, 197, 198, 199, 200, 201, 202, \
                              203, 204, 205, 206, 207, 208, 209, 210],    \
        'MATRA_O'          : [242, 243, 244, 245, 246, 247, 248, 249, 250, \
                              251, 252, 253, 254, 255, 256, 257, 258, 259],\
        'MATRA_OO'         : [260, 261, 262, 263, 264, 265, 266, 267, 268, \
                              269, 270, 271, 272, 273, 274, 275, 276, 277],\
        'MATRA_AU'         : [278, 279, 280, 281, 282, 283, 284, 285, 286, \
                              287, 288, 289, 290],                        \
        'MATRA_VOCALIC_R'  : [593],                                       \
        'MATRA_VOCALIC_RR' : [594],                                       \
                                                                          \
        # the back half of ై, which is a mark of its own here and is       \
        # joined to the ె in front of it once the vattus of the syllable   \
        # have been moved out from between the two - see to_unicode()      \
        'AI_LENGTH_MARK'   : [211, 212, 213, 214, 215, 216, 217, 218, 219, \
                              220, 221, 222, 223, 224, 225, 226, 227, 228, \
                              229, 230, 231, 232, 233, 234, 235, 236, 237, \
                              238, 239, 240, 241, 603, 604, 605, 606, 607, \
                              608, 609, 610],                             \
    }

    # THE LETTERS AS THEY ARE DRAWN IN A SYLLABLE. The plain form of a
    # letter, the one the cmap names, is the form it is drawn in on its own;
    # a letter that carries a vowel sign or a vattu is drawn in a form of
    # its own - kaP and the rest - and the four aspirates that are written
    # with a dot are drawn in a narrower one again wherever the dot has to
    # move. None of them is a character of its own: each is the letter
    LETTER_GLYPHS = {\
        'KA'   : [293], 'KHA'  : [319],           'GA'   : [294],         \
        'GHA'  : [295, 320, 328],                 'CA'   : [296],         \
        'CHA'  : [297, 321, 329],                 'JHA'  : [298, 322, 330],\
        'TTHA' : [299], 'DDA'  : [300],                                   \
        'DDHA' : [301, 323, 331],                 'TA'   : [302],         \
        'THA'  : [303, 324, 332],                 'DA'   : [304],         \
        'DHA'  : [305, 325, 333],                 'NA'   : [306],         \
        'PA'   : [307, 503],                                              \
        'PHA'  : [308, 326, 334, 504, 536],                               \
        'BHA'  : [309, 327, 335],                 'MA'   : [310],         \
        'YA'   : [311], 'RA'   : [312],           'LLA'  : [313],         \
        'VA'   : [314], 'SHA'  : [315],           'SSA'  : [316, 525],    \
        'SA'   : [317, 526],                      'HA'   : [318],         \
        'TSA'  : [855, 856, 857],                 'DZA'  : [861, 862],    \
        # క్ష and జ్ఞ, which the font draws as letters of their own and    \
        # which langs/telugu.Gautami spells out as the clusters they are   \
        'KSSA' : [470, 472],                      'JNYA' : [471],         \
    }

    # THE VATTUS, the consonants that a virama binds to the one before them.
    # Telugu hangs them under the letter and the font draws each of them in
    # two shapes - lvl1 for the one that hangs straight under the letter,
    # lvl2 for the one that hangs under a vattu that is already there - and
    # in as many widths of each shape as the letters above them are wide.
    # The ra of a vattu is the letter this font draws the most widths of
    VATTU_GLYPHS = {\
        'VATTU_KA'   : [336, 337, 378, 417], 'VATTU_KHA'  : [338, 379, 418],\
        'VATTU_GA'   : [339, 380, 419],      'VATTU_GHA'  : [340, 381, 420],\
        'VATTU_NGA'  : [341, 382, 421],      'VATTU_CA'   : [342, 383, 422],\
        'VATTU_CHA'  : [343, 384, 423],      'VATTU_JA'   : [344, 385, 424],\
        'VATTU_JHA'  : [345, 386, 425],      'VATTU_NYA'  : [346, 387, 426],\
        'VATTU_TTA'  : [347, 388, 427],      'VATTU_TTHA' : [348, 389, 428],\
        'VATTU_DDA'  : [349, 390, 429],      'VATTU_DDHA' : [350, 391, 430],\
        'VATTU_NNA'  : [351, 392, 431],      'VATTU_TA'   : [352, 432],     \
        'VATTU_THA'  : [353, 393, 433],      'VATTU_DA'   : [354, 394, 434],\
        'VATTU_DHA'  : [355, 395, 435],      'VATTU_NA'   : [356, 396, 436],\
        'VATTU_PA'   : [357, 397, 437],      'VATTU_PHA'  : [358, 398, 438],\
        'VATTU_BA'   : [359, 399, 439],      'VATTU_BHA'  : [360, 400, 440],\
        'VATTU_MA'   : [361, 401, 441],      'VATTU_YA'   : [362, 402, 442],\
        'VATTU_RRA'  : [370, 409, 449],      'VATTU_LA'   : [371, 410, 450],\
        'VATTU_LLA'  : [372, 411, 451],      'VATTU_VA'   : [373, 412, 452],\
        'VATTU_SHA'  : [374, 413, 453],      'VATTU_SSA'  : [375, 414, 454],\
        'VATTU_SA'   : [376, 415, 455],      'VATTU_HA'   : [377, 416, 456],\
        'VATTU_TSA'  : [864, 865, 870],      'VATTU_DZA'  : [866, 867, 871],\
        'VATTU_KSSA' : [473, 475, 477],      'VATTU_JNYA' : [474, 476, 478],\
        'VATTU_RA'   : [363, 364, 365, 366, 367, 368, 403, 404, 405, 406,  \
                        407, 408, 443, 444, 445, 446, 447, 448, 457, 458,  \
                        459, 460, 461, 462, 463, 464, 465, 466, 467, 468,  \
                        598, 599, 600, 601, 602],                          \
                                                                           \
        # the vattu of pa with the vowel sign u drawn into it, one glyph of \
        # the font and two characters                                      \
        'VATTU_PA_U' : [469],                                              \
    }

    # THE DEAD CONSONANTS, a letter written with the pollu of its cluster.
    # The font has a glyph per letter for it, and one more for each of the
    # aspirates whose dot has to move
    DEAD_GLYPHS = {\
        'KA_VIRAMA'   : [545], 'KHA_VIRAMA'  : [546, 580],                \
        'GA_VIRAMA'   : [547], 'GHA_VIRAMA'  : [548, 581],                \
        'NGA_VIRAMA'  : [549], 'CA_VIRAMA'   : [550],                     \
        'CHA_VIRAMA'  : [551, 582],                                       \
        'JA_VIRAMA'   : [552], 'JHA_VIRAMA'  : [553, 583],                \
        'NYA_VIRAMA'  : [554], 'TTA_VIRAMA'  : [555],                     \
        'TTHA_VIRAMA' : [556], 'DDA_VIRAMA'  : [557],                     \
        'DDHA_VIRAMA' : [558, 584],                                       \
        'NNA_VIRAMA'  : [559], 'TA_VIRAMA'   : [560],                     \
        'THA_VIRAMA'  : [561, 585],                                       \
        'DA_VIRAMA'   : [562], 'DHA_VIRAMA'  : [563, 586],                \
        'NA_VIRAMA'   : [564], 'PA_VIRAMA'   : [565],                     \
        'PHA_VIRAMA'  : [566, 587],                                       \
        'BA_VIRAMA'   : [567], 'BHA_VIRAMA'  : [568, 588],                \
        'MA_VIRAMA'   : [569], 'YA_VIRAMA'   : [570],                     \
        'RA_VIRAMA'   : [571], 'RRA_VIRAMA'  : [572],                     \
        'LA_VIRAMA'   : [573], 'LLA_VIRAMA'  : [574],                     \
        'VA_VIRAMA'   : [575], 'SHA_VIRAMA'  : [576],                     \
        'SSA_VIRAMA'  : [577], 'SA_VIRAMA'   : [578],                     \
        'HA_VIRAMA'   : [579], 'KSSA_VIRAMA' : [589],                     \
        'JNYA_VIRAMA' : [590], 'TSA_VIRAMA'  : [858],                     \
        'DZA_VIRAMA'  : [863],                                            \
    }

    # THE SYLLABLES THE FONT DRAWS IN ONE GLYPH. The vowel signs i and ii
    # replace the talakattu of a letter and reshape it, so every letter that
    # takes either of them has a glyph of its own for that syllable and one
    # more where the dot of an aspirate has to move; and so do the letters
    # that end in the stroke the sign u is drawn with, the letters the signs
    # o and oo are drawn into, and the హ of హా - see langs/telugu.Gautami
    LIGATURE_GLYPHS = {\
        'KHA_I'  : [483, 528], 'KHA_II' : [484, 529],                     \
        'CA_I'   : [489],      'CA_II'  : [490],                          \
        'CHA_I'  : [491, 532], 'CHA_II' : [492, 533],                     \
        'JA_I'   : [493],      'JA_II'  : [494],                          \
        'TA_I'   : [499],      'TA_II'  : [500],                          \
        'NA_I'   : [501],      'NA_II'  : [502],                          \
        'BA_I'   : [505],      'BA_II'  : [506],                          \
        'BHA_I'  : [507, 537], 'BHA_II' : [508, 538],                     \
        'MA_I'   : [509],      'MA_II'  : [510],                          \
        'LA_I'   : [515],      'LA_II'  : [516],                          \
        'LLA_I'  : [517],      'LLA_II' : [518],                          \
        'VA_I'   : [519],      'VA_II'  : [520],                          \
        'SHA_I'  : [523],      'SHA_II' : [524],                          \
        'TSA_I'  : [853],      'TSA_II' : [854],                          \
        'DZA_I'  : [859],      'DZA_II' : [860],                          \
                                                                          \
        'NGA_U'  : [487],      'NGA_UU' : [488],                          \
        'JA_U'   : [495],      'JA_UU'  : [496],                          \
        'SHA_U'  : [521],      'SHA_UU' : [522],                          \
        'KSSA_U' : [540],      'KSSA_UU': [541],                          \
        'DZA_U'  : [868],      'DZA_UU' : [869],                          \
                                                                          \
        'GHA_O'  : [485, 530], 'GHA_OO' : [486, 531],                     \
        'JHA_O'  : [497, 534], 'JHA_OO' : [498, 535],                     \
        'MA_O'   : [511],      'MA_OO'  : [512],                          \
        'YA_O'   : [513],      'YA_OO'  : [514],                          \
        'HA_OO'  : [539],      'HA_AA'  : [527],                          \
    }

    GLYPHS = {}
    for block in (MATRA_GLYPHS, LETTER_GLYPHS, VATTU_GLYPHS, \
                  DEAD_GLYPHS, LIGATURE_GLYPHS):
        GLYPHS.update(block)
    del block

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(telugu.TeluguUnicode())
        self.langobjs.append(telugu.Vattus())
        self.langobjs.append(telugu.Gautami())

        self.lexer = self.get_lexer()

        # the vattus, the tokens that travel. A vattu that the font draws
        # with a vowel sign written into it is more than one token by the
        # time this runs - langs/telugu.Gautami spells VATTU_PA_U out as the
        # vattu and the sign - so only the plain ones are ever reached here
        self.vattus = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName.startswith('VATTU_'):
                    self.vattus.add(tokenName)

        self.composeTokens = { \
            # the two halves of ై, put back together once the vattus of the \
            # syllable have been moved in front of them - this font draws   \
            # that sign as a ె and a length mark of its own, and unicode    \
            # spells it the same way                                        \
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

    def drawn_string(self, tokenName):
        '''the characters of a glyph in the order the font draws them, which
           is what a map that tools/fix_tounicode.py has repaired writes for
           it. Every glyph of this font draws its characters in the order
           unicode writes them - a vattu is the virama and its consonant, a
           dead consonant the letter and the virama, a syllable the letter
           and the sign - so a token is spelled out of its own tokens and
           there is nothing here that is drawn one way and written another'''
        ustr = self.token_to_unicode(tokenName)
        if ustr != None:
            return ustr

        return ''.join([self.token_to_unicode(t) \
                        for t in self.multiple_tokens(tokenName)])

    def get_lexer(self):
        '''one rule per token, and a rule is every way this font writes that
           token: the glyph id of GLYPHS, which is what a short map leaves
           out and an extractor writes as a character of its own, the
           characters that a repaired map hands the same glyph, and the
           character itself for every token of the language tables that even
           a short map does hand out correctly.

           The glyph ids never collide with the telugu. Every glyph of this
           font that the map can be short of is numbered 130 or above - the
           glyphs below that are the letters, the signs, the digits, the
           latin and the punctuation, all of them named by the cmap of the
           font and handed out as characters however short the map is - and
           a glyph id is written as the character of that codepoint, so it
           is a C1 control, a latin supplement or a latin extended
           character and never telugu.

           Nor do the characters collide with each other. A rule of more
           than one character always wins over the rules of the characters
           it is made of, ply sorting its patterns by length, so ్క is the
           vattu of ka and not the virama and a ka apart, and both readings
           are the same string anyway'''
        rules  = {}
        tokens = []

        def add(tokenName, pattern):
            name = 't_' + tokenName
            if name in rules:
                # another way of writing a token that already has a rule -
                # the character of a vowel sign whose other widths are in
                # GLYPHS. Alternate patterns of one token are one rule
                if pattern not in rules[name].split('|'):
                    rules[name] = rules[name] + '|' + pattern
            else:
                rules[name] = pattern
                tokens.append(tokenName)

        for tokenName, gids in self.GLYPHS.items():
            add(tokenName, '|'.join([re.escape(chr(gid)) for gid in gids]))
            add(tokenName, re.escape(self.drawn_string(tokenName)))

        for obj in self.langobjs:
            for tokenName, ustr in obj.tokendict.items():
                # only the tokens that are telugu. The punctuation, the
                # spaces and the latin that langs/telugu.py also names are
                # text rather than glyphs of this font's telugu, and reach
                # the output through the literal path of t_error
                if TELUGU_RE.search(ustr):
                    add(tokenName, re.escape(ustr))

        def t_error(t):
            # a character this font's telugu has no token for: the latin of
            # the document, a digit, the punctuation, or one of the eleven
            # glyphs that this table does not name and that nothing can turn
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
