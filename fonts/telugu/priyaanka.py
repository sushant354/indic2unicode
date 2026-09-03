import re
import types

from indic2unicode.langs import telugu
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class Priyaanka(BaseFont):
    '''The text of a pdf that is set in PriyaankaBold, the telugu font of
       the Telangana gazette.

       It is an 8 bit display font of the Anu family: every glyph of it sits
       on a byte of the mac roman table, and the pdf embeds it as a subset
       whose ToUnicode map hands each glyph the character of the byte it
       sits on, so what an extractor hands out is latin and not telugu at
       all - Á|üuÛÑT‘·«+ is ప్రభుత్వం and Á|üø£≥q is ప్రకటన.

       WHAT THE GLYPHS ARE

       Telugu draws a consonant as a body with a mark on top of it. The mark
       of the inherent vowel a is the talakattu, the little v that stands on
       almost every letter, and a vowel sign replaces it, so this font has a
       glyph for the body of each letter and one for each mark that can
       stand on it - ø£ is the body of ka and a talakattu and is క, ø± is
       that body and the mark of aa and is కా. Where a vowel sign reshapes
       the letter it sits on rather than replacing its talakattu, which is
       what the signs i and ii do, the syllable is one glyph instead: ] is
       రి and Ø is రీ, and each of them is two tokens here - see
       langs/telugu.Priyaanka.

       A consonant that a virama binds to the one before it is written under
       that consonant, and every one of those has a glyph of its own as
       well - the vattus of langs/telugu.Vattus. ష్ట్ర is the one cluster
       this document draws in a single piece.

       So a syllable of this text is a body, a mark, and the vattus under
       it, and the mark and the vattus are drawn in the order they are
       reached rather than in the order unicode writes them. The passes
       below put them back in it.

       WHAT DRAWS LESS THAN A CHARACTER

       The talakattu is the first: it is the mark of a vowel that unicode
       has already written into the letter, so it stands for nothing at all
       and is dropped once the syllable has been put together.

       The aspiration strokes are the second. ధ is drawn as ద with a stroke
       on it, థ as ద with another, ఫ as ప with one and భ as బ with the
       stroke of ధ, and the font draws each of those strokes as a glyph of
       its own rather than drawing the letter - so <Ûä is ధ in two glyphs
       and a half - and composeTokens puts each pair back together.

       The third is the back half of ై and of ో, the two signs this font
       draws in two pieces with the letter between them.

       The fourth is the tail of మ and of య. The body of మ is the body of
       వ and its tail is the glyph that draws the vowel sign u, so eT is మ,
       eTT is ము and e÷ is మా - the body and the glyph of ూ, which is that
       same tail written with the stroke of ా. య is the same story with a
       body of its own, and యి is drawn out of the body of ర.

       The fifth is the stem of హ, which is the stroke the vowel sign ా is
       drawn with: Vü≤ is హ, a body, a talakattu and a ా that is no
       character. హా is that stem with a second stroke beside it, which is
       a glyph of its own and is the ా of the syllable - Vü‰.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       Three things travel here.

       1. A mark is drawn on the body of the syllable and the vattus hang
          under it, so the mark is typed before them and unicode writes it
          last - <ë«sê is ద ా ్వ ర ా and ద్వారా. It is moved past as many
          of them as the syllable has: <äècÕº´ is ద ృ ష ా ్ట ్య and
          దృష్ట్యా.
       2. The vattu of ra is drawn under the whole cluster but typed in
          front of it, so it waits for the body and for the vattus that
          follow it and comes to rest in front of the mark - Á|üø±s¡+ is
          ్ర ప క ా ర ం and ప్రకారం, and Áø±º is ్ర క ా ్ట and క్ట్రా.
       3. The signs e and ee are drawn in front of the letter they belong
          to on the letters whose body they reach around, and behind it on
          the rest, so the font has two glyphs for each of them and the
          front ones wait for one token - ô| is ె ప and పె while ‘Ó is
          త ె and తె.

       WHERE THE READINGS COME FROM

       This was built from one document, whose subset of the font carries an
       outline for 169 bytes, every one of which the document draws. Each of
       them was identified by rendering that outline and reading the words
       the document sets it in against a tesseract -l tel OCR of the pages
       that draw them: 151 of them are telugu and are the table below, and
       the other 18 draw themselves (the digits, the space, and ( ) , - . /
       and :).

       Where the OCR and the page disagree the page is believed. The OCR
       reads క్లయింట్ల as క్షయింట్ల on three of the five pages that carry
       it, and the glyph at A2 is the ్ల the same OCR reads correctly in
       బిడ్లను and in కోట్ల. It reads the ్థ of ఆర్థిక correctly and the
       same glyph in అర్థ సంవత్సరానికి as a ్ధ; the glyph is the subscript
       of ద with the dot of థ inside it and the tail of that letter under
       it, and ్ధ is a glyph of its own at C6 with the tail and no dot.

       WHAT IS NOT KNOWN

       Every byte the subset carries is in the table below, so nothing here
       is read off a run rather than off a glyph. What the font holds on the
       bytes the subset dropped it does not say, and the letters it says
       nothing about are in no table below: ఊ, ఋ, ఔ, the aspirates ఘ, ఛ, ఝ,
       ఠ and ఢ, ఙ, ఞ, ఱ, the visarga, the telugu digits, and every vattu
       beyond the 23 that are. A byte outside the table that is a character
       in its own right comes through as it is, and the rest is reported and
       dropped.
    '''
    # the bytes each glyph of the font sits on. The tokens are the ones
    # langs/telugu.py defines: a name of its own for a letter, a mark or a
    # vattu, <CONSONANT>_<VOWEL> for a syllable the font draws as one glyph,
    # and the names of langs/telugu.Priyaanka for the glyphs that draw less
    # than a character. A mark is drawn in as many widths as the bodies
    # it has to stand on, so most of them are on more than one byte and all
    # of those bytes are the one token. Only what needs decoding is listed -
    # a byte the font draws as itself (the digits, the space, and ( ) , - .
    # / and :) reaches the output through the literal path of t_error, see
    # BaseFont.is_text_char
    glyphcodes = { \
        # VOWELS. ఊ, ఋ and ఔ are drawn nowhere in this document and are   \
        # on no byte the subset carries                                   \
        'A'   : [0x6E], 'AA'  : [0x80], 'I'   : [0x82], 'II'  : [0x87], \
        'U'   : [0x96], 'E'   : [0x6D], 'EE'  : [0x40], 'AI'  : [0xD7], \
        'O'   : [0xFF], 'OO'  : [0x7A],                                 \
                                                                        \
        # CONSONANTS, each of them the body of the letter. A letter whose \
        # body is drawn in more than one width - one to carry the         \
        # talakattu and a wider one to carry the tail of ు, say - has all \
        # of those bytes here                                             \
        'KA'  : [0xBF, 0xC5], 'KHA' : [0x4B, 0x55],                     \
        'GA'  : [0x3E],                                                 \
        'CA'  : [0x23], 'JA'  : [0x43, 0xC8],                           \
        'TTA' : [0x66, 0x7B, 0xB3], 'DDA' : [0x26], 'NNA' : [0x44],     \
        'TA'  : [0xD4], 'DA'  : [0x3C], 'NA'  : [0x48, 0x71],           \
        'PA'  : [0x62, 0x7C], 'BA'  : [0x75, 0x8B],                     \
        'RA'  : [0x73], 'LA'  : [0x5C, 0xFD], 'LLA' : [0xDE],           \
        'VA'  : [0x65, 0x79], 'SHA' : [0x58], 'SSA' : [0x63, 0x77],     \
        'SA'  : [0x64, 0x6B], 'HA'  : [0x56],                           \
                                                                        \
        # the body of య, which is the letter without the tail it shares  \
        # with మ - see the class comment                                 \
        'YA_BASE' : [0x6A],                                             \
                                                                        \
        # THE SYLLABLES THE FONT DRAWS AS ONE GLYPH. The vowel signs i   \
        # and ii reshape the letter they sit on rather than standing on   \
        # it, so every letter that takes either of them has a glyph of    \
        # its own for that syllable. జ is the one letter that is drawn    \
        # with u and with uu written into it as well, and ష్ట్ర the one   \
        # cluster the font draws in a single piece                        \
        'GA_I'  : [0xD0], 'GA_II' : [0x5E], 'CA_I'  : [0xBA],           \
        'JA_I'  : [0x9B], 'JA_U'  : [0x45], 'JA_UU' : [0x70],           \
        'TA_I'  : [0xDC], 'TA_II' : [0x72], 'DA_I'  : [0x7E],           \
        'DA_II' : [0x42], 'NA_I'  : [0x93], 'NA_II' : [0xFA],           \
        'BA_I'  : [0x5F], 'RA_I'  : [0x5D], 'RA_II' : [0xAF],           \
        'LA_I'  : [0x2A], 'LA_II' : [0xA9], 'LLA_I' : [0x5B],           \
        'VA_I'  : [0x24], 'VA_II' : [0x4D], 'SSA_TTA_RA' : [0x68],      \
                                                                        \
        # THE MARKS THAT STAND ON THE BODY. The talakattu says the letter \
        # carries the inherent vowel a and stands for no character, see   \
        # the class comment. PRE_MATRA_E and PRE_MATRA_EE are the ె and   \
        # the ే of the letters that are drawn with the sign in front of    \
        # them, AI_MARK and OO_MARK the back halves of ై and ో, TAIL the   \
        # ు that is the tail of మ and of య as well and STEM_MATRA_AA the   \
        # ా of a హ - see the class comment for the last three              \
        'INHERENT_A' : [0x83, 0x84, 0x8A, 0x9F, 0xA3, 0xB7, 0xC1, 0xE1, \
                        0xF8],                                          \
        'MATRA_AA' : [0x86, 0x90, 0x91, 0xB1, 0xB2, 0xCD, 0xE6],        \
        'STEM_MATRA_AA' : [0xE4],                                       \
        'MATRA_I'  : [0x8D, 0xBE, 0xEC], 'MATRA_II' : [0x9E, 0xA1],     \
        'MATRA_U'  : [0x94, 0xDA], 'MATRA_UU' : [0x4C, 0x50, 0xD6],     \
        'TAIL'     : [0x54],                                            \
        'MATRA_VOCALIC_R' : [0x8F],                                     \
        'MATRA_E'  : [0xC9, 0xEE], 'PRE_MATRA_E'  : [0x99, 0xC2],       \
        'MATRA_EE' : [0xF1, 0xFB], 'PRE_MATRA_EE' : [0x9D, 0xB9],       \
        'AI_MARK'  : [0xAE, 0xD5], 'OO_MARK' : [0x41],                  \
        'MATRA_O'  : [0x3D, 0xA4, 0xF5], 'MATRA_OO' : [0xC3, 0xCB, 0xFE], \
        'MATRA_AU' : [0x85, 0x9A, 0xE5],                                \
        'ANUSVARA' : [0x2B],                                            \
        'VIRAMA'   : [0x59, 0x74, 0x8E, 0xB4, 0xD9, 0xF9],              \
                                                                        \
        # THE VATTUS, the consonants that hang under the body of the      \
        # syllable. F0 is the vattu of pa with the vowel sign u drawn      \
        # into it, which is two tokens here                               \
        'VATTU_KA'  : [0xD8], 'VATTU_GA'  : [0x5A], 'VATTU_CA' : [0xCC], \
        'VATTU_JA'  : [0xA8], 'VATTU_TTA' : [0xBC],                     \
        'VATTU_NNA' : [0x92], 'VATTU_DDA' : [0xA6], 'VATTU_TA'  : [0xEF], \
        'VATTU_THA' : [0x9C],                                           \
        'VATTU_DA'  : [0xDD], 'VATTU_DHA' : [0xC6], 'VATTU_NA' : [0x95], \
        'VATTU_PA'  : [0xCE], 'VATTU_PA_U': [0xF0], 'VATTU_BA' : [0xD2], \
        'VATTU_MA'  : [0x88], 'VATTU_YA'  : [0xAB], 'VATTU_RA' : [0xE7], \
        'VATTU_LA'  : [0xA2], 'VATTU_VA'  : [0xC7],                     \
        'VATTU_SHA' : [0xF4], 'VATTU_SSA' : [0x8C, 0xFC],               \
        'VATTU_SA'  : [0xE0], 'VATTU_HA'  : [0xBD],                     \
                                                                        \
        # THE ASPIRATION STROKES, each of them the mark that turns a      \
        # letter the font does draw into one it does not - see the class  \
        # comment                                                         \
        'STROKE_H'  : [0xF3], 'STROKE_TH' : [0xB8],                     \
        'STROKE_PH' : [0x98], 'SUB_STROKE_H' : [0xDB],                  \
                                                                        \
        # the one piece of punctuation of the font that does not come out \
        # of the pdf as itself                                           \
        'HYPHEN'    : [0x60],                                           \
    }

    # the pdf hands every glyph of this font the character of the mac roman
    # byte it sits on, so this is what an extractor hands its text out as
    encoding = 'mac-roman'

    # a second character a glyph reaches this converter as. Three bytes of
    # mac roman are of a character unicode has twice over, and which of the
    # two is written is the choice of whoever writes it: the ohm sign is
    # the greek omega it is the source of, the currency sign is the euro
    # that replaced it on that byte, and the apple logo is a private use
    # character that no two tables agree on. This document's own map writes
    # the first of each pair and python's mac roman table the second, so
    # both readings of those three glyphs are taken
    glyph_aliases = { \
        'VATTU_HA' : '\u2126', 'SUB_STROKE_H' : '\u00a4', \
        'VATTU_PA_U' : '\uf0f0', \
    }

    # the marks that can stand on the body of a syllable: the vowel signs
    # and the virama, which is the mark of a syllable that has no vowel at
    # all. A mark is typed before the vattus that hang under that body and
    # unicode writes it behind them, so these are the tokens that travel
    # over a vattu - see reorder_vattus()
    marks = ('MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU', \
             'MATRA_VOCALIC_R', 'MATRA_E', 'MATRA_EE', 'MATRA_O', \
             'MATRA_OO', 'MATRA_AU', 'PRE_MATRA_E', 'PRE_MATRA_EE', \
             'AI_MARK', 'OO_MARK', 'STEM_MATRA_AA', 'TAIL', 'VIRAMA')

    # the marks that are drawn in front of the letter they belong to. Each
    # of them waits for one token - a syllable the font draws as one glyph
    # is one token here however many characters it is, which is what makes
    # this a one rather than a count of glyphs
    prefix_marks = ('PRE_MATRA_E', 'PRE_MATRA_EE')

    # the letters that are drawn with an aspiration stroke on them rather
    # than with a glyph of their own, and the letter each pair draws
    aspirates = { \
        ('DA', 'STROKE_H')       : 'DHA', \
        ('DA', 'STROKE_TH')      : 'THA', \
        ('BA', 'STROKE_H')       : 'BHA', \
        ('PA', 'STROKE_PH')      : 'PHA', \
        ('VATTU_BA', 'SUB_STROKE_H') : 'VATTU_BHA', \
    }

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(telugu.TeluguUnicode())
        self.langobjs.append(telugu.Vattus())
        self.langobjs.append(telugu.Priyaanka())

        self.glyphchars = self.get_glyph_chars()
        self.lexer      = self.get_lexer()

        self.waitdict = {}
        for tokenName in self.prefix_marks:
            self.waitdict[tokenName] = 1

        # the vattu of ra is typed in front of the cluster it hangs under
        # and unicode writes it behind the whole of it, so it waits for the
        # body of that cluster - the vattus that follow the body are
        # transparent to it and it comes to rest in front of the vowel sign
        self.waitdict['VATTU_RA'] = 1

        # the vattus that hang under the body of a syllable and that a
        # vowel sign therefore has to travel over. The vattu of ra is not
        # one of them: it is typed in front of the body rather than behind
        # the sign, and travels itself
        self.vattus = set(telugu.Vattus().get_tokens())
        self.vattus.discard('VATTU_RA')

        # the vattu of ra is not counted while it waits for the body of its
        # cluster, so it comes to rest behind the whole of that cluster
        self.waitover = set(self.vattus)

        # the rules that run before the reordering
        self.preComposeTokens = {}

        # the aspiration strokes, each of them put back together with the
        # letter it stands on. A letter that the font draws with the vowel
        # sign i or ii written into it is one glyph and the stroke follows
        # that glyph rather than the body of it, so each pair is a rule
        # with the sign between the two as well
        for (letter, stroke), aspirate in self.aspirates.items():
            self.preComposeTokens[(letter, stroke)] = aspirate
            for mark in self.marks + ('INHERENT_A',):
                self.preComposeTokens[(letter, mark, stroke)] = \
                        [aspirate, mark]

        # the tail that మ shares with the vowel sign u, put back together
        # with the body of వ it stands on - see the class comment. య is
        # drawn the same way out of a body of its own
        for body, letter in (('VA', 'MA'), ('YA_BASE', 'YA')):
            self.preComposeTokens[(body, 'TAIL')] = letter
            for mark in self.marks + ('INHERENT_A',):
                self.preComposeTokens[(body, mark, 'TAIL')] = [letter, mark]

            # the tail written with the stroke of ా, which is the glyph
            # that draws ూ and is the back half of ో as well - so మా is
            # the body of వ and that glyph, and మో is the body, a ె and it
            self.preComposeTokens[(body, 'MATRA_UU')] = [letter, 'MATRA_AA']
            self.preComposeTokens[(body, 'INHERENT_A', 'MATRA_UU')] = \
                    [letter, 'MATRA_AA']
            self.preComposeTokens[(body, 'MATRA_E', 'MATRA_UU')] = \
                    [letter, 'MATRA_OO']

        # యి, which is drawn out of the body of ర and two of those tails
        self.preComposeTokens[('RA', 'TAIL', 'TAIL')] = ['YA', 'MATRA_I']

        # హ is drawn as a body and a stem, and the stem is the glyph that
        # draws ా - the two are the same stroke. The mark of the syllable
        # stands between them, so the ా that follows a హ carrying a mark is
        # that stem and is dropped here. హా is the body, the mark and the
        # stem written with a second stroke, which is a glyph of its own
        # and is a ా in its own right
        for mark in self.marks + ('INHERENT_A',):
            self.preComposeTokens[('HA', mark, 'MATRA_AA')] = ['HA', mark]

        # a vowel sign that is drawn in front of its letter and the vattu of
        # ra of the same syllable are both waiting to jump over that letter,
        # and unicode writes the vattu first. Swapping them here is what
        # makes them come out of the jump in that order, the jump emitting
        # what was waiting longest first
        for mark in self.prefix_marks:
            self.preComposeTokens[(mark, 'VATTU_RA')] = ['VATTU_RA', mark]

        # and the rules that run after it: the two part signs, each of them
        # put back together once the front half has jumped over the letter
        # that was drawn between them
        self.composeTokens = { \
            ('PRE_MATRA_E', 'AI_MARK')  : 'MATRA_AI', \
            ('MATRA_E',     'AI_MARK')  : 'MATRA_AI', \
            ('PRE_MATRA_E', 'OO_MARK')  : 'MATRA_OO', \
            ('MATRA_E',     'OO_MARK')  : 'MATRA_OO', \
                                                      \
            # ొ on the letters whose tail is the glyph that draws ు: the  \
            # back half of the sign is that same tail, so మొ is the body  \
            # of వ, a ె and two of them - see the class comment           \
            ('MATRA_E',     'TAIL')     : 'MATRA_O',  \
        }

    def reorder_vattus(self, tokentypes):
        '''the mark of a syllable is drawn on the body of it and the vattus
           hang under that body, so the mark is typed in front of them and
           unicode writes it behind them. Every vattu is moved in front of
           the mark, so a syllable that has more than one of them comes out
           with all of them in the order they were typed - దృష్ట్యా is
           ద ృ ష ా ్ట ్య. A sign the font draws in two pieces is two marks
           by then and the vattu goes in front of both - నట్లైతే is
           న ట ె ై ్ల'''
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
        '''the passes run in the order this font's own reordering needs:
           the glyphs that draw less than a character are put back together
           with the letter they stand on first, the talakattu is dropped
           once it has done that work, and the two part signs are joined
           after the reordering, the letter having been between them until
           then'''
        tokentypes = self.tokenize(data)

        tokentypes = self.compose_tokens(tokentypes, self.preComposeTokens)

        # the talakattu is the mark of a vowel that unicode writes into the
        # letter itself, so it stands for no character once the syllable is
        # put together and is dropped here rather than left to travel
        # through the passes between a letter and the sign of its own
        # syllable
        tokentypes = [t for t in tokentypes if t != 'INHERENT_A']

        tokentypes = self.reorder_vattus(tokentypes)
        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def get_glyph_chars(self):
        '''the characters each glyph of the font reaches this converter as:
           the bytes it sits on read as mac roman, which is how the pdf
           names them, and whatever else glyph_aliases says it also arrives
           as'''
        glyphchars = {}

        for tokenName, codes in self.glyphcodes.items():
            chars = ''.join([bytes([code]).decode(self.encoding) \
                             for code in codes])
            glyphchars[tokenName] = chars + \
                                    self.glyph_aliases.get(tokenName, '')

        return glyphchars

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        rules = {}
        for tokenName, chars in self.glyphchars.items():
            # token strings are regular expressions for ply, so the
            # characters have to be escaped. A mark that is drawn in more
            # than one width sits on a byte for each of them and is one
            # rule matching any of those characters
            rules['t_' + tokenName] = \
                    '|'.join([re.escape(char) for char in chars])

        def t_error(t):
            # a byte that is not in the table above is one the font draws
            # as itself - a digit, the space, ( ) , - . / : - which is text
            # and comes through as it is
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
