from indic2unicode.langs import devanagari
from basefont import BaseFont
import ply.lex as lex
import logging

class Aryan2(BaseFont):
    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs  = []
        self.langobjs.append(devanagari.DevanagariUnicode())
        self.langobjs.append(devanagari.Conjuncts())
        self.langobjs.append(devanagari.Aryan2())

        self.lexer = self.get_lexer()
        self.waitdict = {'MATRA_I': 1, 'MATRAIBINDU' : 1, 'MATRAIBINDU2': 1, \
                         'MATRA_I2': 2}

        self.composeTokens = {('A', 'MATRA_AA') : 'AA'}
        self.jumpbefore    = {'ADHA_RA': 1}

    def num_wait(self, tokenName):
        if self.waitdict.has_key(tokenName):
            return self.waitdict[tokenName]
        else:
            return 0
 
    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend( obj.get_tokens())

        danda  = u'\u00c9'

        # conjuncts
        t_KALA               = u'\u201a'
        t_KHARA              = u'\u004c' + danda
        t_NGAKA              = u'\u2030' 
        t_NGAGA              = u'\u2039' 
        t_ADHA_CHHHA         = u'\u0046' 
        t_CHHHA              = t_ADHA_CHHHA + danda
        t_GRA                = u'\u004f' + danda
        t_GRHA               = u'\u0051' + danda
        t_CHRA               = u'\u0054' + danda
        t_JRA                = u'\u0058' + danda
        t_GYAN               = u'\u0059' + danda
        t_JHRA               = u'\\\u005b' + danda
        t_NYAJA              = u'\u201d' + danda
        t_NYACHA             = u'\u2022' + danda

        t_TTATTA             = u'\\\u005e'
        t_TTATTHA            = u'\u005f'
        t_TTHATTHA           = u'\u0061'
        t_DDADDA             = u'\u0064'
        t_DDADDHA            = u'\u0065'

        t_SHRA               = u'\u0067' + danda
        t_TRA                = u'\u006a' + danda
        t_TATA               = u'\u006b' + danda
        t_THRA               = u'\u006d' + danda
        t_DRI                = u'\u006f' 
        t_DRA                = u'\u0070'
        t_DADA               = u'\u0071'
        t_DADHA              = u'\u0072'
        t_DAMA               = u'\u0073' + danda
        t_DAYA               = u'\u0074' + danda
        t_DAWA               = u'\u0075'
        t_DABHA              = u'\u2013'
        t_DHARA              = u'\u0077'

        t_NARA               = u'\u0079' + danda
        t_NANA               = u'\u007a' + danda
        t_PRA                = u'\\\u007c' + danda

        t_JAJA               = u'\u00a1' + danda
        t_DHADHA             = u'\u00a2'

        t_BRA                = u'\u00a5' + danda 
        t_BRHA               = u'\u00a7' + danda 
        t_MRA                = u'\u00a9' + danda 
        t_RAUU               = u'\u00b0'
        t_SHACHA             = u'\u00b2' + danda
        t_SHANA              = u'\u2014' + danda
        t_SSATTA             = u'\u00b3'
        t_VRA                = u'\u00b5' + danda
        t_KRA                = t_VRA + u'\u0045' 
        t_SHAVA              = u'\u00b7' + danda
        t_YARA               = u'\u00b9' + danda
        t_RAU                = u'\u00bb'
        t_RAU2               = u'\u00e2'

        t_HARA               = u'\u00bf' + danda
        t_HAMA               = u'\u00c0' + danda
        t_HAYA               = u'\u00c1' + danda
        t_MATRA_RA           = u'\u00c5'
        t_HARI               = u'\u00d8'
        t_HALA               = u'\u2026'
        t_HAVA               = u'\u2020'
        t_HANA               = u'\u2021'

        t_NGAGHA             = u'\u0152'
        t_NGAKHA             = u'\u0160'
        t_ADHA_RA            = u'\u00c7'
        t_ADHA_RA_BINDU      = u'\u00c8'
        t_AA_ADHARA          = danda + t_ADHA_RA 
        
        t_MATRAIBINDU        = danda + u'\u00cb'
        t_MATRAIBINDU2       = danda + u'\u00cf'
        t_MATRAIRI           = danda + u'\u00cc'
        t_MATRAIRI2          = danda + u'\u00d0'
        t_MATRAIRIBINDU      = danda + u'\u00cd'
        t_MATRAIRIBINDU2     = danda + u'\u00d1'

        t_MATRAIIBINDU       = danda + u'\u00d3'
        t_MATRAIIRI          = danda + u'\u00d4' 
        t_MATRAIIRIBINDU     = danda + u'\u00d5'

        t_MATRAEBINDU        = u'\u00e5' 
        t_MATRAERI           = u'\u00e6' 
        t_MATRAERIBINDU      = u'\u00e7' 

        t_MATRAAIBINDU        = u'\u00e9' 
        t_MATRAAIRI           = u'\u00ea' 
        t_MATRAAIRIBINDU      = u'\u00eb' 

        t_MATRAOBINDU        = danda + u'\u00e5' 
        t_MATRAORI           = danda + u'\u00e6' 
        t_MATRAORIBINDU      = danda + u'\u00e7' 

        t_MATRAAUBINDU       = danda + u'\u00e9' 
        t_MATRAAURI          = danda + u'\u00ea' 
        t_MATRAAURIBINDU     = danda + u'\u00eb' 
        
        # Aryan2 Lang specific
        t_STAR               = u'\u00af'
        t_QUOT               = u'\u00de'
        t_PROMPT             = u'\u0026'
        t_SINGLE_QUOT_OPEN   = u'\u0022'
        t_SINGLE_QUOT_CLOSE  = u'\u0027'
        t_PLUS               = u'\u00a8'
        t_EQ                 = u'\u00ac'
        t_PERCENT            = u'\u00b1'
        t_SPACE              = u'\\\u0020'
        t_NEWLINE            = u'\\\u000a'
        t_LEFTPARAN          = u'\\\u0028'
        t_RIGHTPARAN         = u'\\\u0029'
        t_COMMA              = u'\\\u002c'
        t_DASH               = u'\\\u002d'
        t_DOT                = u'\\\u002e'
        t_SLASH              = u'\\\u002f'
        t_COLON              = u'\u003a'
        t_SEMICOLON          = u'\u003b'
        t_QUESTION           = u'\\\u003f'
 
        t_KA_U               = u'\u0042' + danda + u'\u00d6' + u'\u0045' 
        t_KA_UU              = u'\u0042' + danda + u'\u00da' + u'\u0045'
        t_KA_RI              = u'\u0042' + danda + u'\u00df' + u'\u0045'
        t_ADHA_KA_U          = u'\u0042' + danda + u'\u00d6' + u'\u0044'
        t_ADHA_KA_UU         = u'\u0042' + danda + u'\u00da' + u'\u0044'
        t_ADHA_KA_RI         = u'\u0042' + danda + u'\u00df' + u'\u0044'
        t_ADHA_SSA2          = u'\u00ad' 
        t_SSA2               = t_ADHA_SSA2 + danda

        t_PHA_U              = u'\u007b' + danda + u'\u00d6' + u'\u0045' 
        t_PHA_UU             = u'\u007b' + danda + u'\u00da' + u'\u0045'
        t_PHA_RI             = u'\u007b' + danda + u'\u00df' + u'\u0045'
        t_PHA_RA             = u'\\\u007c' + danda + u'\u0045'
        # Half Letters
        t_ADHA_A       = u'\\\u002b'
        t_ADHA_KA      = u'\u0042' + danda + u'\u0044'
        t_ADHA_KHA     = u'\u004a'
        t_ADHA_GA      = u'\u004d'
        t_ADHA_GHA     = u'\u0050'
 
        t_ADHA_CA      = u'\u0053' 
        t_ADHA_JA      = u'\u0056' 
        t_ADHA_JHA     = u'\u005a' 
        t_ADHA_NYA     = u'\\\u005c' 

        t_ADHA_NNA     = u'\u0068' 
 
        t_ADHA_TA      = u'\u0069' 
        t_ADHA_THA     = u'\u006c' 
        t_ADHA_DHA     = u'\u0076'
        t_ADHA_NA      = u'\u0078' 
        tokens.remove('NNNA')

        t_ADHA_PA      = u'\u007b' 
        t_ADHA_PHA     = t_ADHA_PA + danda + u'\u0044' 
        t_ADHA_BA      = u'\u00a4'
        t_ADHA_BHA     = u'\u00a3' 
        t_ADHA_MA      = u'\u00e0' 
  
        t_ADHA_YA      = u'\u00aa'
        t_ADHA_LA      = u'\u00e3' 
        t_ADHA_VA      = u'\u0042'
        t_ADHA_VA2     = u'\u00b4'
        t_ADHA_SHA     = u'\u00b6' 
        t_ADHA_SSA     = u'\u2212' 
        t_ADHA_SA      = u'\u00ba'
 
        t_ADHA_QA      = u'\u0043' + danda 
        t_ADHA_KHHA    = u'\u004b' 
        t_ADHA_GHHA    = u'\u004e' 
        t_ADHA_ZA      = u'\u0057' 
        t_ADHA_FA      = u'\u007d' + danda 

        t_ADHA_LLA     = u'\u0153'
        # UNICODE
        # signs
        t_CHANDRABINDU = u'\u00c4' 
        t_BINDU        = u'\u00c6'
        tokens.remove('VISARGA') # t_VISARGA      = u'\u003a'

        # VOWELS
        chandra = u'\u00ec'
        tokens.remove('SHORT_A') # t_SHORT_A      = u''
        t_A            = t_ADHA_A + danda
        t_I            = u'\u003c'
        t_II           = t_I + u'\u00c7'
        t_U            = u'\u003d'
        t_UU           = u'\u003e'
        t_RE           = t_TRA + u'\u0040'
        t_LI           = u'\u0161\u00df'
        t_E            = u'\u0041'
        t_CHANDRA_E    = t_E + chandra
        t_AI           = t_E + u'\u00e4'
        t_CHANDRA_O    = t_A + danda + chandra
        tokens.remove('SHORT_O') # t_SHORT_O      = u''
        t_OO           = t_A + danda + u'\u00e4'
        t_AU           = t_A + danda + u'\u00e8'
        # CONSONANTS 
        t_KA           = u'\u0042' + danda + u'\u0045'
        t_KHA          = t_ADHA_KHA + danda
        t_GA           = t_ADHA_GA + danda
        t_GHA          = t_ADHA_GHA + danda
        t_NGA          = u'\u0052'

        t_CA           = t_ADHA_CA + danda
        t_CHA          = u'\u0055'
        t_JA           = t_ADHA_JA + danda
        t_JHA          = t_ADHA_JHA + danda
        t_NYA          = t_ADHA_NYA + danda

        t_TTA          = u'\u005d'
        t_TTHA         = u'\u007e'
        t_DDA          = u'\u0062'
        t_DDHA         = u'\u0066'
 
        t_TA           = t_ADHA_TA + danda
        t_THA          = t_ADHA_THA + danda
        t_DA           = u'\u006e'
        t_DHA          = t_ADHA_DHA + danda
        t_NA           = t_ADHA_NA + danda
        t_NNA          = t_ADHA_NNA + danda
 
        t_PA           = t_ADHA_PA + danda
        t_PHA          = t_PA + u'\u0045'
        t_BA           = t_ADHA_BA + danda
        t_BHA          = t_ADHA_BHA + danda
        t_MA           = t_ADHA_MA + danda
  
        t_YA           = t_ADHA_YA + danda
        t_RA           = u'\u00ae'
        t_RRA          = u'\u00c3' + t_RA
        t_LA           = t_ADHA_LA + danda
        t_LLA          = u'\u0178'
        t_LLLA         = u'\u00c3'+ t_LLA
        t_VA           = t_ADHA_VA + danda
        t_VA2          = t_ADHA_VA2 + danda
        t_SHA          = t_ADHA_SHA + danda
        t_SSA          = t_ADHA_SSA + danda
        t_SA           = t_ADHA_SA + danda
        t_HA           = u'\u0063'
        t_HA2          = u'\u00ff'
  
        # SIGNS
        t_NUKTA        = u'\u00c3'
        t_AVAGRAHA     = u'\u0025'
 
        # MATRAS
        t_MATRA_AA     = danda 
        t_MATRA_I      = danda + u'\u00ca'
        t_MATRA_I2     = danda + u'\u00ce'
        t_MATRA_II     = danda + u'\u00d2'
        t_MATRA_U      = u'\u00d9'
        t_MATRA_U2     = u'\u00d6'
        t_MATRA_UU     = u'\u00da'
        t_MATRA_UU2    = u'\u00dd'
        t_ADHA_YA2     = u'\u00e1'
        t_YA2          = u'\u00e1' + danda
        t_MATRA_RI     = u'\u00df'
        tokens.remove('MATRA_RR') # t_MATRA_RR     = u''
        t_CHANDRA      = chandra 
        tokens.remove('MATRA_SHORT_E') # t_MATRA_SHORT_E = u''
        t_MATRA_E      = u'\u00e4'
        t_MATRA_AI     = u'\u00e8'
        t_MATRA_CHANDRA_O  = danda + chandra
        t_MATRA_SHORT_O  = u'\u00f1'
        t_MATRA_O      = u'\u00c9' + t_MATRA_E
        t_MATRA_AU     = u'\u00c9' + t_MATRA_AI

        # SIGNA
        t_HALANT       = u'\u00c2'
        t_OM           = u'\\\u0024'
        tokens.remove('UDATTA') # t_UDATTA       = u''
          
        tokens.remove('ANUDATTA') # t_ANUDATTA     = u''
        tokens.remove('GRAVE_ACCENT') # t_GRAVE_ACCENT = u''
        tokens.remove('ACUTE_ACCENT') # t_ACUTE_ACCENT = u''

        # ADDITIONAL CONSONANTS
        t_QA           = t_ADHA_QA + u'\u0045'
        t_KHHA         = t_ADHA_KHHA + danda
        t_GHHA         = t_ADHA_GHHA + danda
        t_ZA           = t_ADHA_ZA + danda
        t_DDDHA        = u'\u00bd'
        t_RHA          = u'\u00b8'
        t_FA           = t_ADHA_FA + u'\u0045'
        tokens.remove('YYA') # t_YYA          = u''

        # GENERIC ADDITIONS
        tokens.remove('RRE') #t_RRE          = u''
        tokens.remove('LLE') #t_LLE          = u''
        tokens.remove('MATRA_L') # t_MATRA_L      = u''
        tokens.remove('MATRA_LL') #t_MATRA_LL     = u''
        t_VIRAM        = u'\\\u002a'
        t_DEERGH_VIRAM = t_VIRAM + t_VIRAM 
  
        # DIGITS
        t_ZERO         = u'\u0030'
        t_ONE          = u'\u0031'
        t_TWO          = u'\u0032'
        t_THREE        = u'\u0033'
        t_FOUR         = u'\u0034'
        t_FIVE         = u'\u0035'
        t_SIX          = u'\u0036'
        t_SEVEN        = u'\u0037'
        t_EIGHT        = u'\u0038'
        t_NINE         = u'\u0039'
        tokens.remove('ABBREV') #t_ABBREV       = ''  

        t_ignore_IGCHAR1 = u'\u00f3'
        t_ignore_IGCHAR2 = u'\u00f4'
        t_ignore_IGCHAR3 = u'\u00a0'
        t_ignore_CARRIAGERET = u'\\\u000d'
        def t_error(t):
            self.report_error(t)
            t.lexer.skip(1)

        return lex.lex()
       
       
