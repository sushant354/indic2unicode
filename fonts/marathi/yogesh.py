import re

from indic2unicode.langs import devanagari, marathi
from ..basefont import BaseFont
import ply.lex as lex


class Yogesh(BaseFont):
    '''The marathi of a pdf that is set in DVBW-TTYogesh, the font of the
       Maharashtra gazette.

       It is an 8 bit display font: every glyph of it sits on a byte of the
       windows 1252 table and the pdf hands each glyph the character of the
       byte it stands on, so the text an extractor gives out is latin and
       not marathi at all - ´ÖÆüÖ¸üÖÂ™Òü is महाराष्ट्र and ¿ÖÖÃÖ®Ö is शासन.

       WHAT THE GLYPHS ARE

       Devanagari draws most of its letters as a body and a vertical bar on
       the right of it, and the half form of such a letter is that body
       without the bar. This font has a glyph for the body and one for the
       bar, and the bar is the same glyph that draws the matra aa - ¯ is प्,
       Ö is ा, and प is the two of them, ¯Ö. So a full consonant here is
       the half consonant and the bar, which is what full() below builds,
       and प्रसाद is ¯ÖÏÃÖÖ¤ü: प् ्र स् ा द.

       The letters that are drawn without a bar - क, ट, ठ, ड, ढ, द, र, ह, ळ
       and the conjuncts द्द, द्ध, द्व, ह्य - are one glyph and stand for
       themselves.

       Several of those overflow the box the font gives them, so an empty
       glyph behind the letter pays for the rest of its width, and the
       matras of the syllable are drawn over the letter in between the two.
       क is Ûú and के is Ûêú - the body, the matra e and the width. That
       empty glyph is SPACER and it is no character: it is dropped.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       Two things travel.

       1. The matra i is drawn in front of the consonant it belongs to and
          unicode writes it behind that consonant - ×¤ü®ÖÖÓÛú is
          ि द ना ं क and दिनांक. So is the glyph that draws the matra i
          with an anusvar on it, and so is the one that draws it with a
          reph, but the reph of that one is already in front of the letter
          it is drawn on and stays where it is: ×®ÖÙ¤üÂ™ü is
          ि न र्+ि द ष् ट and निर्दिष्ट.
       2. The reph is drawn on the last letter of the syllable it opens and
          unicode writes it in front of that syllable, so it is typed after
          it and moves back over it - ×®Ö´ÖÖÔÞÖ is ि न मा र् ण and
          निर्माण. It jumps over the matras of the syllable on its way, so
          it lands in front of the consonant and not in front of the matra.

       WHAT IS ON THE DIGIT KEYS

       The devanagari digits, so १४ is typed 14. The english of the
       document is set in Arial and never reaches this converter.
    '''

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(marathi.MarathiUnicode())
        self.langobjs.append(devanagari.Conjuncts())
        self.langobjs.append(marathi.Yogesh())

        self.lexer = self.get_lexer()

        # matra_i, and the two glyphs that draw it with a sign on it, are
        # drawn in front of the consonant they belong to
        self.waitdict   = {'MATRA_I': 1, 'MATRAIBINDU': 1}

        # the reph is typed after the whole syllable it is drawn on
        self.jumpbefore = {'ADHA_RA': 1}

        self.composeTokens = {\
            # the anusvar does not touch the matra of its syllable, so the
            # two get typed in either order. Unicode always wants the matra
            # first
            ('BINDU', 'MATRA_AA') : ['MATRA_AA', 'BINDU'], \
            ('BINDU', 'MATRA_II') : ['MATRA_II', 'BINDU'], \
            ('BINDU', 'MATRA_U')  : ['MATRA_U',  'BINDU'], \
            ('BINDU', 'MATRA_UU') : ['MATRA_UU', 'BINDU'], \
            ('BINDU', 'MATRA_E')  : ['MATRA_E',  'BINDU'], \
            ('BINDU', 'MATRA_O')  : ['MATRA_O',  'BINDU'], \
        }

        # while the reph jumps back to the head of its syllable it has to
        # jump over the matras and the signs of that syllable, and over the
        # width that pays for a letter that overflows its box
        self.jumpover = set([\
            'SPACER', 'MATRA_AA', 'MATRA_I', 'MATRA_II', 'MATRA_U',        \
            'MATRA_UU', 'MATRA_RI', 'MATRA_E', 'MATRA_AI', 'MATRA_O',      \
            'MATRA_AU', 'MATRA_CHANDRA_O', 'CHANDRA', 'BINDU', 'HALANT',   \
            'MATRAIBINDU', 'MATRAIIBINDU', 'MATRAEBINDU', 'MATRAOBINDU',   \
            'RAKAR',                                                       \
        ])

        # the rakar hangs under the syllable that matra_i has already
        # passed, and so does the width behind a letter that overflows its
        # box, so matra_i has to stay behind both of them
        self.waitover = set(['RAKAR', 'SPACER'])

        # a half consonant is not the consonant matra_i is waiting for, but
        # it is the head of the syllable that matra_i belongs to
        self.halftokens = set()
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName.startswith('ADHA_'):
                    self.halftokens.add(tokenName)

    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            for tokenName in obj.get_tokens():
                if tokenName not in tokens:
                    tokens.append(tokenName)

        def pat(*glyphs):
            # token strings are regular expressions for ply, so the glyphs
            # have to be escaped. Alternate glyphs of the same token are
            # joined into one pattern
            return '|'.join([re.escape(glyph) for glyph in glyphs])

        # the vertical bar that makes a half consonant full. It is the same
        # glyph that draws the matra aa
        bar = 'Ö'

        def full(*glyphs):
            return pat(*[glyph + bar for glyph in glyphs])

        # VOWELS. aa, o, au and the chandra o are the vowel a and a matra,
        # ii is the vowel i and the stroke that also draws the reph
        t_A                = pat('†')
        t_AA               = pat('†Ö')
        t_OO               = pat('†Öê')
        t_AU               = pat('†Öî')
        t_CHANDRA_O        = pat('†Öò')
        t_I                = pat('‡')
        t_II               = pat('‡Ô')
        t_U                = pat('ˆ')
        t_UU               = pat('‰')
        t_E                = pat('‹')
        t_AI               = pat('‹ê')
        t_CHANDRA_E        = pat('‹ò')

        # CONSONANTS
        t_ADHA_KA          = pat('Œ')
        t_KA               = pat('Û')
        t_ADHA_KHA         = pat('Ü')
        t_KHA              = full('Ü')
        t_ADHA_GA          = pat('Ý')
        t_GA               = full('Ý')
        t_ADHA_GHA         = pat('‘')
        t_GHA              = full('‘')

        t_ADHA_CA          = pat('“')
        t_CA               = full('“')
        t_ADHA_JA          = pat('•')
        t_JA               = full('•')
        t_ADHA_JHA         = pat('—')
        t_JHA              = full('—')

        t_TTA              = pat('™')
        t_TTHA             = pat('š')
        t_DDA              = pat('›')
        t_DDHA             = pat('œ')
        t_ADHA_NNA         = pat('Þ')
        t_NNA              = full('Þ')

        t_ADHA_TA          = pat('Ÿ')
        t_TA               = full('Ÿ')
        t_ADHA_THA         = pat('£')
        t_THA              = full('£')
        t_DA               = pat('¤')
        t_ADHA_DHA         = pat('¬')
        t_DHA              = full('¬')
        t_ADHA_NA          = pat('®')
        t_NA               = full('®')

        t_ADHA_PA          = pat('¯')
        t_PA               = full('¯')
        t_ADHA_BA          = pat('²')
        t_BA               = full('²')
        t_ADHA_BHA         = pat('³')
        t_BHA              = full('³')
        t_ADHA_MA          = pat('´')
        t_MA               = full('´')

        t_ADHA_YA          = pat('µ')
        t_YA               = full('µ')
        t_RA               = pat('¸')
        t_ADHA_LA          = pat('»')
        t_LA               = full('»')
        t_LLA              = pat('ô')
        t_ADHA_VA          = pat('¾')
        t_VA               = full('¾')

        # the font has a second half sha, the one it draws in front of va
        # and of ra
        t_ADHA_SHA         = pat('¿', 'À')
        t_SHA              = full('¿', 'À')
        t_ADHA_SSA         = pat('Â')
        t_SSA              = full('Â')
        t_ADHA_SA          = pat('Ã')
        t_SA               = full('Ã')
        t_HA               = pat('Æ')

        # THE CONJUNCTS THE FONT DRAWS AS ONE LETTER
        t_ADHA_TRA         = pat('¡')
        t_TRA              = full('¡')
        t_ADHA_TATA        = pat('¢')
        t_TATA             = full('¢')
        t_DADA             = pat('§')
        t_DADHA            = pat('¨')
        t_DAWA             = pat('«')
        t_ADHA_SHRA        = pat('Á')
        t_SHRA             = full('Á')
        t_HAYA             = pat('Ê')
        t_ADHA_CHHHA       = pat('õ')
        t_CHHHA            = full('õ')
        # ra with the matra u, and with the matra uu, are a glyph of their
        # own: the matra is drawn inside the letter
        t_RAU              = pat('¹')
        t_RAUU             = pat('º')

        # MATRAS. o, au and the chandra o are the vertical bar and a matra
        t_MATRA_AA         = pat('Ö')
        t_MATRA_O          = pat('Öê')
        t_MATRAOBINDU      = pat('Öë')
        t_MATRA_AU         = pat('Öî')
        t_MATRA_CHANDRA_O  = pat('Öò')
        t_MATRA_I          = pat('×')
        t_MATRAIBINDU      = pat('Ø')
        t_MATRAIRI2        = pat('Ù')
        t_MATRA_II         = pat('ß')
        t_MATRAIIBINDU     = pat('à')
        t_MATRAIIRI        = pat('á')
        t_MATRA_U          = pat('ã')
        t_MATRA_UU         = pat('æ')
        t_MATRA_RI         = pat('é')
        t_MATRA_E          = pat('ê')
        t_MATRAEBINDU      = pat('ë')
        t_MATRA_AI         = pat('î')
        t_CHANDRA          = pat('ò')

        # SIGNS
        t_BINDU            = pat('Ó')
        t_ADHA_RA          = pat('Ô')
        # the ra that hangs under its consonant. The font has one stroke
        # for ka, one for tta and one for every other letter
        t_RAKAR            = pat('Î', 'Ï', 'Ò')

        # the width that pays for a letter that overflows the box the font
        # gives it. It draws nothing and stands for nothing
        t_SPACER           = pat('ú', 'û', 'ü', 'ý', 'þ')

        # DIGITS. The keys of the digits draw the devanagari ones
        t_ZERO             = pat('0')
        t_ONE              = pat('1')
        t_TWO              = pat('2')
        t_THREE            = pat('3')
        t_FOUR             = pat('4')
        t_FIVE             = pat('5')
        t_SIX              = pat('6')
        t_SEVEN            = pat('7')
        t_EIGHT            = pat('8')
        t_NINE             = pat('9')

        # PUNCTUATION
        t_SPACE            = pat(' ')
        t_NEWLINE          = pat('\n')
        t_CARRIAGERET      = pat('\r')
        t_COMMA            = pat(',')
        t_DOT              = pat('.')
        t_DASH             = pat('-')
        t_SLASH            = pat('/')
        t_COLON            = pat(':')
        t_SEMICOLON        = pat(';')
        t_QUESTION         = pat('?')
        t_PLUS             = pat('+')
        t_LEFTPARAN        = pat('(')
        t_RIGHTPARAN       = pat(')')
        t_LEFTSQBRACE      = pat('[')
        t_RIGHTSQBRACE     = pat(']')

        def t_error(t):
            self.report_error(t)
            t.lexer.skip(1)

        return lex.lex()
