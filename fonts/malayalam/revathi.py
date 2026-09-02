import re
import types

from indic2unicode.langs import malayalam
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class Revathi(BaseFont):
    '''The text of a pdf that is set in ML-Revathi-Normal, one of the
       malayalam fonts of the Kerala gazette.

       It is an 8 bit font: every glyph of it sits on a byte, the pdf calls
       it a Type 1 font and names the glyphs of it after the latin
       characters that live on those bytes, so what an extractor hands out
       is latin and not malayalam at all - tIcf Kh¿Æ¿ is കേരള ഗവർണ്ണർ and
       Z¿Lmkv ]ckyw is ദർഘാസ് പരസ്യം. The bytes are the layout the ML-
       family of fonts shares: the vowels and then the whole alphabet run
       unbroken over the letter keys, one letter to a byte in the order the
       script lists them, the signs follow them to the end of the lower
       half, and the upper half is the clusters the font draws as one
       glyph, in no order at all.

       WHAT THE GLYPHS ARE

       Malayalam binds the consonants of a cluster into a shape of their
       own, so a font of this kind needs a glyph for each of

         - the vowels
         - the consonants
         - the five chillus, the letters that end a syllable with no vowel
         - each cluster the script writes as one shape, which is what the
           upper half of the table below is
         - the vowel signs, and the three consonants that are written as a
           mark on the letter rather than beside it - ്യ, ്വ and ്ര

       and the ones this document draws are the table below. A cluster this
       font has no glyph for is written out of the letters and the
       chandrakkala between them, which needs no glyph of its own. ഈ, ഊ,
       ൈ, ൊ, ോ and ഓ have no glyph either, each of them being drawn out
       of two that the font does have - see below.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       The vowel signs െ and േ are drawn in front of the consonant they
       belong to and unicode writes them behind it, so each of them waits
       for one token - tIcf is േ ക ര ള and കേരള. ൈ is drawn as two െ and
       is put back together before they jump, so that both halves make the
       one step together - assd≥ is മ െ െ റ ൻ and മറൈൻ. The signs ൊ and ോ
       are drawn in two halves with the letter between them, so they arrive
       as a െ or a േ in front and a ാ behind, and are put back together
       once the front half has jumped - tdmUv is േ റ ാ ഡ ് and റോഡ്.

       ്ര is drawn in front of its letter as well, and inside whatever
       vowel sign is drawn there: t{]mPIvSv is േ ്ര പ ാ ജ ക ് ട ് for
       പ്രോജക്ട്, where the േ and the ്ര both belong behind the പ and the
       ്ര belongs first. The two are swapped before they jump so that they
       come out of the jump in that order.

       ഈ AND ഊ ARE DRAWN IN TWO HALVES TOO

       The font draws no glyph for either of them: they are ഇ and ഉ with
       the stroke of ൗ on them, which is the glyph the vowel sign ൗ is
       drawn with, and composeTokens reads that pair back as the one
       letter - Cu is ഈ. The stroke on a consonant is the vowel sign
       itself, auehn being മൗലവി.

       THE HYPHEN THAT IS NOT ONE

       The dtp package that set these documents writes a hyphen into a word
       to say where the word may be broken across a line, and the font
       draws that hyphen as a glyph 9/1000 of an em wide, i.e. as nothing.
       So a word of this text carries hyphens that are not in it -
       Fd-Wm-Ipfw is എറണാകുളം and not എറ-ണാ-കുളം - and they are dropped
       here. The hyphen a document really writes is a glyph of its own, at
       1D, and comes through as one.

       WHERE THE READINGS COME FROM

       This was built from one document, whose subset of the font carries
       an outline for 111 bytes, every one of which the document draws.
       Each of them was identified by rendering that outline and reading it
       against a tesseract -l mal OCR of the pages that draw it: 89 of them
       are malayalam and are the readings below, four more are punctuation
       that does not come out of the pdf as itself, and the other 18 draw
       themselves (the digits, the space, and & ( ) + , . /).

       Six readings below are off the run of the alphabet rather than off a
       glyph - ങ, ഛ, ഝ, ഞ, ഠ and ഢ. The letters run one to a byte from 49
       to 6C and there are exactly as many bytes there as the alphabet has
       letters, so the six the document never draws are the six the
       alphabet has where that run has its gaps.

       Where the OCR and the page disagree the page is believed. The OCR
       reads am¿§w as മാര്‍ഗം, one ഗ; the glyph at A7 is the same doubled
       shape that Ω is of മ, which the OCR does read as മ്മ, so A7 is ഗ്ഗ
       and മാർഗ്ഗം is what this document writes.

       WHAT IS NOT KNOWN

       The subset names 111 bytes of the font and the document draws all
       of them, so everything here but the six letters of the alphabet run
       is read off a glyph. What the font holds on the bytes the subset
       dropped it does not say, and the letters it says nothing about are
       in no table below: ഐ, ഔ and ഋ, the visarga, the malayalam digits,
       the chillu ൿ, and every cluster beyond the 33 that are. Two of
       those bytes are in the lower half and are not in the run of the
       alphabet either - 45, which stands between ഉ and എ where the vowels
       have ഋ, and 78, which stands between the anusvara and ്യ. A byte
       outside the table that is a character in its own right comes
       through as it is, and the rest is reported and dropped.
    '''
    # the byte each glyph of the font sits on. The tokens are the ones
    # langs/malayalam.py defines: a name of its own for a letter, a sign or
    # a chillu, and <CONSONANT>_<CONSONANT> for a cluster the font draws as
    # one glyph. Only what needs decoding is listed - a byte the font draws
    # as itself (the digits, the space, and & ( ) + , . /) reaches the
    # output through the literal path of t_error, see BaseFont.is_text_char
    glyphcodes = { \
        # VOWELS. ഈ and ഊ have no byte of their own: they are ഇ and ഉ    \
        # with the stroke of ൗ on them, see the class comment            \
        'A'            : 0x41, 'AA'          : 0x42, \
        'I'            : 0x43, 'U'           : 0x44, \
        'E'            : 0x46, 'EE'          : 0x47, \
        'O'            : 0x48,                       \
                                                     \
        # CONSONANTS, each of them the letter with its inherent vowel a. \
        # The 36 letters of the alphabet run unbroken from 49 to 6C, one  \
        # to a byte in the order the script lists them - the five vargas  \
        # and then the ya-varga, with റ and ഴ among them where malayalam  \
        # puts them. Six of the six-and-thirty are drawn nowhere in this  \
        # document and are read off that run: they are the six letters    \
        # the alphabet has where the run has its six gaps, and there is   \
        # nothing else they could be                                      \
        'KA'           : 0x49, 'KHA'         : 0x4A, \
        'GA'           : 0x4B, 'GHA'         : 0x4C, \
        'NGA'          : 0x4D,                       \
        'CA'           : 0x4E, 'CHA'         : 0x4F, \
        'JA'           : 0x50, 'JHA'         : 0x51, \
        'NYA'          : 0x52,                       \
        'TTA'          : 0x53, 'TTHA'        : 0x54, \
        'DDA'          : 0x55, 'DDHA'        : 0x56, \
        'NNA'          : 0x57,                       \
        'TA'           : 0x58, 'THA'         : 0x59, \
        'DA'           : 0x5A, 'DHA'         : 0x5B, \
        'NA'           : 0x5C,                       \
        'PA'           : 0x5D, 'PHA'         : 0x5E, \
        'BA'           : 0x5F, 'BHA'         : 0x60, \
        'MA'           : 0x61,                       \
        'YA'           : 0x62, 'RA'          : 0x63, \
        'RRA'          : 0x64, 'LA'          : 0x65, \
        'LLA'          : 0x66, 'LLLA'        : 0x67, \
        'VA'           : 0x68,                       \
        'SHA'          : 0x69, 'SSA'         : 0x6A, \
        'SA'           : 0x6B, 'HA'          : 0x6C, \
                                                     \
        # THE CHILLUS. the letters that end a syllable with no vowel,    \
        # each of them a character of its own - see langs/malayalam.py   \
        'CHILLU_NN'    : 0xA8, 'CHILLU_N'    : 0x03, \
        'CHILLU_RR'    : 0xBF, 'CHILLU_L'    : 0xAC, \
        'CHILLU_LL'    : 0x86,                       \
                                                     \
        # THE CLUSTERS THE FONT DRAWS AS ONE GLYPH, which is the whole   \
        # of the upper half of the table. A cluster that is not here the \
        # font writes out of its letters and the chandrakkala between    \
        # them                                                           \
        'KA_KA'        : 0xB0, 'KA_LA'       : 0xA2, \
        'KA_SSA'       : 0xA3, 'GA_GA'       : 0xA7, \
        'NGA_KA'       : 0xB6, 'NGA_NGA'     : 0xDF, \
        'CA_CA'        : 0xAE, 'NYA_CA'      : 0xA9, \
        'NYA_NYA'      : 0x92, 'TTA_TTA'     : 0xB4, \
        'NNA_NNA'      : 0xC6, 'TA_TA'       : 0xD8, \
        'TA_SA'        : 0x90, 'DA_DA'       : 0xB1, \
        'DA_DHA'       : 0x08, 'NA_TA'       : 0xA5, \
        'NA_DA'        : 0xB5, 'NA_DHA'      : 0x8F, \
        'NA_NA'        : 0x05, 'NA_RRA'      : 0x91, \
        'PA_PA'        : 0x02, 'BA_LA'       : 0xAA, \
        'MA_PA'        : 0xBA, 'MA_MA'       : 0x07, \
        'YA_YA'        : 0xF8, 'RRA_RRA'     : 0x8B, \
        'LA_LA'        : 0x04, 'LLA_LLA'     : 0x06, \
        'VA_VA'        : 0x0A, 'SHA_SHA'     : 0xBB, \
        'SA_SA'        : 0x09, 'SA_THA'      : 0xFF, \
        'SA_RRA_RRA'   : 0xC3,                       \
                                                     \
        # THE SIGNS. the vowel signs, the chandrakkala and the anusvara, \
        # and the three consonants that are written as a mark on the     \
        # letter they are bound to rather than beside it                 \
        'MATRA_AA'     : 0x6D, 'MATRA_I'     : 0x6E, \
        'MATRA_II'     : 0x6F, 'MATRA_U'     : 0x70, \
        'MATRA_UU'     : 0x71,                       \
        'MATRA_VOCALIC_R' : 0x72,                    \
        'MATRA_E'      : 0x73, 'MATRA_EE'    : 0x74, \
        'AU_LENGTH_MARK'  : 0x75,                    \
        'VIRAMA'       : 0x76, 'ANUSVARA'    : 0x77, \
        'YA_SIGN'      : 0x79, 'VA_SIGN'     : 0x7A, \
        'RA_SIGN'      : 0x7B,                       \
                                                     \
        # the punctuation of the font that does not come out of the pdf  \
        # as itself. The quotes are the curly ones however they are      \
        # named, 1D is the hyphen a document really writes and 2D is the \
        # one the dtp package writes to break a word - see the class     \
        # comment                                                        \
        'LSQUOTE'      : 0x22, 'RSQUOTE'     : 0x27, \
        'DASH'         : 0x1D, 'SOFT_HYPHEN' : 0x2D, \
    }

    # the pdf names the glyphs of this font after the characters of latin
    # 1, so this is what an extractor hands its text out as
    encoding = 'latin-1'

    # the bytes whose glyph is named after a character latin 1 does not
    # have. The names are the ones the font's own encoding gives them -
    # product, radical, partialdiff, florin, perthousand, and nbspace for
    # the byte that draws സ്സ - so they say nothing about what is drawn,
    # and an extractor turns each of them into the character of that name
    code_chars = { \
        0x02 : '\u220f', 0x03 : '\u2265', 0x04 : '\u221a', \
        0x05 : '\u2202', 0x06 : '\u2248', 0x07 : '\u03a9', \
        0x08 : '\u2264', 0x09 : '\u00a0', 0x0a : '\u0394', \
        0x1d : '\u02db', 0x86 : '\u0192', 0x8b : '\u2030', \
        0x8f : '\u2018', 0x90 : '\u2019', 0x91 : '\u201a', \
        0x92 : '\u2122', \
    }

    # a second character a glyph reaches this converter as. Three of the
    # glyph names above are of characters that unicode has twice over, and
    # which of the two an extractor writes is its own choice: Omega is the
    # greek letter or the ohm sign it is the source of, Delta is the greek
    # letter or the increment sign, and mu is the micro sign of latin 1 or
    # the greek letter unicode normalises that sign to - this document's
    # own map writes the greek letter for all three. The glyph is the same
    # glyph, so both readings of it are taken
    glyph_aliases = { \
        'MA_MA' : 'Ω', 'VA_VA' : '∆', 'NA_DA' : 'μ', \
    }

    # the signs that are drawn in front of the letter they belong to. Each
    # of them waits for one token - a cluster is one token here however
    # many letters it is written out of, which is what makes this a one
    # rather than a count of glyphs
    prefix_signs = ('MATRA_E', 'MATRA_EE', 'MATRA_AI', 'RA_SIGN')

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(malayalam.MalayalamUnicode())
        self.langobjs.append(malayalam.Conjuncts())

        self.glyphchars = self.get_glyph_chars()
        self.lexer      = self.get_lexer()

        self.waitdict = {}
        for tokenName in self.prefix_signs:
            self.waitdict[tokenName] = 1

        # ്യ and ്വ are drawn under the letter they are bound to and are
        # typed there, so a vowel sign that is on its way past that letter
        # has not passed the syllable until it has passed them as well and
        # belongs behind them: DtZym is ഉ േ ദ ്യ ാ and ഉദ്യോഗം, AtIz is
        # അ േ ക ്വ and അക്വേറിയം. ്ര is the one of the three that is drawn
        # in front instead, which is why it is in prefix_signs above and
        # not here
        self.waitover = set(['YA_SIGN', 'VA_SIGN'])

        # the rules that run before the reordering. ൈ is drawn as two െ
        # and has to be one token before they jump, or the two halves of
        # it would make a step each and land on either side of the letter
        self.preComposeTokens = { \
            ('MATRA_E', 'MATRA_E')  : 'MATRA_AI', \
                                                  \
            # a vowel sign and the ്ra of the same syllable are both      \
            # drawn in front of its letter, the sign outside the ്ര, and  \
            # unicode writes the ്ര first. Swapping them here is what      \
            # makes them come out of the jump in that order, the jump     \
            # emitting what was waiting longest first - t{]m is പ്രോ      \
            ('MATRA_E',  'RA_SIGN') : ['RA_SIGN', 'MATRA_E'],  \
            ('MATRA_EE', 'RA_SIGN') : ['RA_SIGN', 'MATRA_EE'], \
            ('MATRA_AI', 'RA_SIGN') : ['RA_SIGN', 'MATRA_AI'], \
        }

        # and the rules that run after it
        self.composeTokens = { \
            # the two halves of a vowel sign that is drawn with the       \
            # letter between them, put back together once the front half  \
            # has jumped over that letter                                 \
            ('MATRA_E',  'MATRA_AA')       : 'MATRA_O',  \
            ('MATRA_EE', 'MATRA_AA')       : 'MATRA_OO', \
            ('MATRA_E',  'AU_LENGTH_MARK') : 'MATRA_AU', \
                                                         \
            # ഓ, which the font draws as ഒ and the sign ാ the way it     \
            # draws ോ out of a േ and a ാ                                 \
            ('O', 'MATRA_AA')              : 'OO', \
                                                         \
            # ഈ and ഊ, which the font draws as ഇ and ഉ with the stroke   \
            # of ൗ on them - see the class comment                        \
            ('I', 'AU_LENGTH_MARK')        : 'II', \
            ('U', 'AU_LENGTH_MARK')        : 'UU', \
        }

    def get_glyph_chars(self):
        '''the characters each glyph of the font reaches this converter
           as: the byte it sits on read the way the pdf names that byte's
           glyph, and whatever else glyph_aliases says it also arrives as'''
        glyphchars = {}

        for tokenName, code in self.glyphcodes.items():
            if code in self.code_chars:
                char = self.code_chars[code]
            else:
                char = bytes([code]).decode(self.encoding)

            glyphchars[tokenName] = char + self.glyph_aliases.get(tokenName, '')

        return glyphchars

    def to_unicode(self, data):
        '''the passes run in the order this font's own reordering needs:
           the two halves of ൈ are joined and a vowel sign and the ്ര of
           the same syllable are put in the order unicode writes them
           before either jumps, and the two halves of ൊ and ോ are joined
           after the jump, the letter having been between them until then'''
        tokentypes = self.tokenize(data)

        # the hyphen the dtp package writes to break a word across a line
        # is a glyph of no width and no character at all, so it is dropped
        # here rather than left to travel through the passes as a token
        # that stands between a letter and the sign of its own syllable
        tokentypes = [t for t in tokentypes if t != 'SOFT_HYPHEN']

        tokentypes = self.compose_tokens(tokentypes, self.preComposeTokens)
        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        rules = {}
        for tokenName, chars in self.glyphchars.items():
            # token strings are regular expressions for ply, so the
            # characters have to be escaped. A glyph that reaches this
            # converter under more than one character - see glyph_aliases -
            # is one rule matching any of them
            rules['t_' + tokenName] = \
                    '|'.join([re.escape(char) for char in chars])

        def t_error(t):
            # a byte that is not in the table above is one the font draws
            # as itself - a digit, the space, & ( ) + , . / - which is text
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
