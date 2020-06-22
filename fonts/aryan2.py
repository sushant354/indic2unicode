from indic2unicode.langs import devanagari
from .basefont import BaseFont
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
        if tokenName in self.waitdict:
            return self.waitdict[tokenName]
        else:
            return 0
 
    def get_lexer(self):
        tokens = []
        for obj in self.langobjs:
            tokens.extend( obj.get_tokens())

        danda  = '\u00c9'

        # conjuncts
        t_KALA               = '\u201a'
        t_KHARA              = '\u004c' + danda
        t_NGAKA              = '\u2030' 
        t_NGAGA              = '\u2039' 
        t_ADHA_CHHHA         = '\u0046' 
        t_CHHHA              = t_ADHA_CHHHA + danda
        t_GRA                = '\u004f' + danda
        t_GRHA               = '\u0051' + danda
        t_CHRA               = '\u0054' + danda
        t_JRA                = '\u0058' + danda
        t_GYAN               = '\u0059' + danda
        t_JHRA               = '\\\u005b' + danda
        t_NYAJA              = '\u201d' + danda
        t_NYACHA             = '\u2022' + danda

        t_TTATTA             = '\\\u005e'
        t_TTATTHA            = '\u005f'
        t_TTHATTHA           = '\u0061'
        t_DDADDA             = '\u0064'
        t_DDADDHA            = '\u0065'

        t_SHRA               = '\u0067' + danda
        t_TRA                = '\u006a' + danda
        t_TATA               = '\u006b' + danda
        t_THRA               = '\u006d' + danda
        t_DRI                = '\u006f' 
        t_DRA                = '\u0070'
        t_DADA               = '\u0071'
        t_DADHA              = '\u0072'
        t_DAMA               = '\u0073' + danda
        t_DAYA               = '\u0074' + danda
        t_DAWA               = '\u0075'
        t_DABHA              = '\u2013'
        t_DHARA              = '\u0077'

        t_NARA               = '\u0079' + danda
        t_NANA               = '\u007a' + danda
        t_PRA                = '\\\u007c' + danda

        t_JAJA               = '\u00a1' + danda
        t_DHADHA             = '\u00a2'

        t_BRA                = '\u00a5' + danda 
        t_BRHA               = '\u00a7' + danda 
        t_MRA                = '\u00a9' + danda 
        t_RAUU               = '\u00b0'
        t_SHACHA             = '\u00b2' + danda
        t_SHANA              = '\u2014' + danda
        t_SSATTA             = '\u00b3'
        t_VRA                = '\u00b5' + danda
        t_KRA                = t_VRA + '\u0045' 
        t_SHAVA              = '\u00b7' + danda
        t_YARA               = '\u00b9' + danda
        t_RAU                = '\u00bb'
        t_RAU2               = '\u00e2'

        t_HARA               = '\u00bf' + danda
        t_HAMA               = '\u00c0' + danda
        t_HAYA               = '\u00c1' + danda
        t_MATRA_RA           = '\u00c5'
        t_HARI               = '\u00d8'
        t_HALA               = '\u2026'
        t_HAVA               = '\u2020'
        t_HANA               = '\u2021'

        t_NGAGHA             = '\u0152'
        t_NGAKHA             = '\u0160'
        t_ADHA_RA            = '\u00c7'
        t_ADHA_RA_BINDU      = '\u00c8'
        t_AA_ADHARA          = danda + t_ADHA_RA 
        
        t_MATRAIBINDU        = danda + '\u00cb'
        t_MATRAIBINDU2       = danda + '\u00cf'
        t_MATRAIRI           = danda + '\u00cc'
        t_MATRAIRI2          = danda + '\u00d0'
        t_MATRAIRIBINDU      = danda + '\u00cd'
        t_MATRAIRIBINDU2     = danda + '\u00d1'

        t_MATRAIIBINDU       = danda + '\u00d3'
        t_MATRAIIRI          = danda + '\u00d4' 
        t_MATRAIIRIBINDU     = danda + '\u00d5'

        t_MATRAEBINDU        = '\u00e5' 
        t_MATRAERI           = '\u00e6' 
        t_MATRAERIBINDU      = '\u00e7' 

        t_MATRAAIBINDU        = '\u00e9' 
        t_MATRAAIRI           = '\u00ea' 
        t_MATRAAIRIBINDU      = '\u00eb' 

        t_MATRAOBINDU        = danda + '\u00e5' 
        t_MATRAORI           = danda + '\u00e6' 
        t_MATRAORIBINDU      = danda + '\u00e7' 

        t_MATRAAUBINDU       = danda + '\u00e9' 
        t_MATRAAURI          = danda + '\u00ea' 
        t_MATRAAURIBINDU     = danda + '\u00eb' 
        
        # Aryan2 Lang specific
        t_STAR               = '\u00af'
        t_QUOT               = '\u00de'
        t_PROMPT             = '\u0026'
        t_SINGLE_QUOT_OPEN   = '\u0022'
        t_SINGLE_QUOT_CLOSE  = '\u0027'
        t_PLUS               = '\u00a8'
        t_EQ                 = '\u00ac'
        t_PERCENT            = '\u00b1'
        t_SPACE              = '\\\u0020'
        t_NEWLINE            = '\\\u000a'
        t_LEFTPARAN          = '\\\u0028'
        t_RIGHTPARAN         = '\\\u0029'
        t_COMMA              = '\\\u002c'
        t_DASH               = '\\\u002d'
        t_DOT                = '\\\u002e'
        t_SLASH              = '\\\u002f'
        t_COLON              = '\u003a'
        t_SEMICOLON          = '\u003b'
        t_QUESTION           = '\\\u003f'
 
        t_KA_U               = '\u0042' + danda + '\u00d6' + '\u0045' 
        t_KA_UU              = '\u0042' + danda + '\u00da' + '\u0045'
        t_KA_RI              = '\u0042' + danda + '\u00df' + '\u0045'
        t_ADHA_KA_U          = '\u0042' + danda + '\u00d6' + '\u0044'
        t_ADHA_KA_UU         = '\u0042' + danda + '\u00da' + '\u0044'
        t_ADHA_KA_RI         = '\u0042' + danda + '\u00df' + '\u0044'
        t_ADHA_SSA2          = '\u00ad' 
        t_SSA2               = t_ADHA_SSA2 + danda

        t_PHA_U              = '\u007b' + danda + '\u00d6' + '\u0045' 
        t_PHA_UU             = '\u007b' + danda + '\u00da' + '\u0045'
        t_PHA_RI             = '\u007b' + danda + '\u00df' + '\u0045'
        t_PHA_RA             = '\\\u007c' + danda + '\u0045'
        # Half Letters
        t_ADHA_A       = '\\\u002b'
        t_ADHA_KA      = '\u0042' + danda + '\u0044'
        t_ADHA_KHA     = '\u004a'
        t_ADHA_GA      = '\u004d'
        t_ADHA_GHA     = '\u0050'
 
        t_ADHA_CA      = '\u0053' 
        t_ADHA_JA      = '\u0056' 
        t_ADHA_JHA     = '\u005a' 
        t_ADHA_NYA     = '\\\u005c' 

        t_ADHA_NNA     = '\u0068' 
 
        t_ADHA_TA      = '\u0069' 
        t_ADHA_THA     = '\u006c' 
        t_ADHA_DHA     = '\u0076'
        t_ADHA_NA      = '\u0078' 
        tokens.remove('NNNA')

        t_ADHA_PA      = '\u007b' 
        t_ADHA_PHA     = t_ADHA_PA + danda + '\u0044' 
        t_ADHA_BA      = '\u00a4'
        t_ADHA_BHA     = '\u00a3' 
        t_ADHA_MA      = '\u00e0' 
  
        t_ADHA_YA      = '\u00aa'
        t_ADHA_LA      = '\u00e3' 
        t_ADHA_VA      = '\u0042'
        t_ADHA_VA2     = '\u00b4'
        t_ADHA_SHA     = '\u00b6' 
        t_ADHA_SSA     = '\u2212' 
        t_ADHA_SA      = '\u00ba'
 
        t_ADHA_QA      = '\u0043' + danda 
        t_ADHA_KHHA    = '\u004b' 
        t_ADHA_GHHA    = '\u004e' 
        t_ADHA_ZA      = '\u0057' 
        t_ADHA_FA      = '\u007d' + danda 

        t_ADHA_LLA     = '\u0153'
        # UNICODE
        # signs
        t_CHANDRABINDU = '\u00c4' 
        t_BINDU        = '\u00c6'
        tokens.remove('VISARGA') # t_VISARGA      = u'\u003a'

        # VOWELS
        chandra = '\u00ec'
        tokens.remove('SHORT_A') # t_SHORT_A      = u''
        t_A            = t_ADHA_A + danda
        t_I            = '\u003c'
        t_II           = t_I + '\u00c7'
        t_U            = '\u003d'
        t_UU           = '\u003e'
        t_RE           = t_TRA + '\u0040'
        t_LI           = '\u0161\u00df'
        t_E            = '\u0041'
        t_CHANDRA_E    = t_E + chandra
        t_AI           = t_E + '\u00e4'
        t_CHANDRA_O    = t_A + danda + chandra
        tokens.remove('SHORT_O') # t_SHORT_O      = u''
        t_OO           = t_A + danda + '\u00e4'
        t_AU           = t_A + danda + '\u00e8'
        # CONSONANTS 
        t_KA           = '\u0042' + danda + '\u0045'
        t_KHA          = t_ADHA_KHA + danda
        t_GA           = t_ADHA_GA + danda
        t_GHA          = t_ADHA_GHA + danda
        t_NGA          = '\u0052'

        t_CA           = t_ADHA_CA + danda
        t_CHA          = '\u0055'
        t_JA           = t_ADHA_JA + danda
        t_JHA          = t_ADHA_JHA + danda
        t_NYA          = t_ADHA_NYA + danda

        t_TTA          = '\u005d'
        t_TTHA         = '\u007e'
        t_DDA          = '\u0062'
        t_DDHA         = '\u0066'
 
        t_TA           = t_ADHA_TA + danda
        t_THA          = t_ADHA_THA + danda
        t_DA           = '\u006e'
        t_DHA          = t_ADHA_DHA + danda
        t_NA           = t_ADHA_NA + danda
        t_NNA          = t_ADHA_NNA + danda
 
        t_PA           = t_ADHA_PA + danda
        t_PHA          = t_PA + '\u0045'
        t_BA           = t_ADHA_BA + danda
        t_BHA          = t_ADHA_BHA + danda
        t_MA           = t_ADHA_MA + danda
  
        t_YA           = t_ADHA_YA + danda
        t_RA           = '\u00ae'
        t_RRA          = '\u00c3' + t_RA
        t_LA           = t_ADHA_LA + danda
        t_LLA          = '\u0178'
        t_LLLA         = '\u00c3'+ t_LLA
        t_VA           = t_ADHA_VA + danda
        t_VA2          = t_ADHA_VA2 + danda
        t_SHA          = t_ADHA_SHA + danda
        t_SSA          = t_ADHA_SSA + danda
        t_SA           = t_ADHA_SA + danda
        t_HA           = '\u0063'
        t_HA2          = '\u00ff'
  
        # SIGNS
        t_NUKTA        = '\u00c3'
        t_AVAGRAHA     = '\u0025'
 
        # MATRAS
        t_MATRA_AA     = danda 
        t_MATRA_I      = danda + '\u00ca'
        t_MATRA_I2     = danda + '\u00ce'
        t_MATRA_II     = danda + '\u00d2'
        t_MATRA_U      = '\u00d9'
        t_MATRA_U2     = '\u00d6'
        t_MATRA_UU     = '\u00da'
        t_MATRA_UU2    = '\u00dd'
        t_ADHA_YA2     = '\u00e1'
        t_YA2          = '\u00e1' + danda
        t_MATRA_RI     = '\u00df'
        tokens.remove('MATRA_RR') # t_MATRA_RR     = u''
        t_CHANDRA      = chandra 
        tokens.remove('MATRA_SHORT_E') # t_MATRA_SHORT_E = u''
        t_MATRA_E      = '\u00e4'
        t_MATRA_AI     = '\u00e8'
        t_MATRA_CHANDRA_O  = danda + chandra
        t_MATRA_SHORT_O  = '\u00f1'
        t_MATRA_O      = '\u00c9' + t_MATRA_E
        t_MATRA_AU     = '\u00c9' + t_MATRA_AI

        # SIGNA
        t_HALANT       = '\u00c2'
        t_OM           = '\\\u0024'
        tokens.remove('UDATTA') # t_UDATTA       = u''
          
        tokens.remove('ANUDATTA') # t_ANUDATTA     = u''
        tokens.remove('GRAVE_ACCENT') # t_GRAVE_ACCENT = u''
        tokens.remove('ACUTE_ACCENT') # t_ACUTE_ACCENT = u''

        # ADDITIONAL CONSONANTS
        t_QA           = t_ADHA_QA + '\u0045'
        t_KHHA         = t_ADHA_KHHA + danda
        t_GHHA         = t_ADHA_GHHA + danda
        t_ZA           = t_ADHA_ZA + danda
        t_DDDHA        = '\u00bd'
        t_RHA          = '\u00b8'
        t_FA           = t_ADHA_FA + '\u0045'
        tokens.remove('YYA') # t_YYA          = u''

        # GENERIC ADDITIONS
        tokens.remove('RRE') #t_RRE          = u''
        tokens.remove('LLE') #t_LLE          = u''
        tokens.remove('MATRA_L') # t_MATRA_L      = u''
        tokens.remove('MATRA_LL') #t_MATRA_LL     = u''
        t_VIRAM        = '\\\u002a'
        t_DEERGH_VIRAM = t_VIRAM + t_VIRAM 
  
        # DIGITS
        t_ZERO         = '\u0030'
        t_ONE          = '\u0031'
        t_TWO          = '\u0032'
        t_THREE        = '\u0033'
        t_FOUR         = '\u0034'
        t_FIVE         = '\u0035'
        t_SIX          = '\u0036'
        t_SEVEN        = '\u0037'
        t_EIGHT        = '\u0038'
        t_NINE         = '\u0039'
        tokens.remove('ABBREV') #t_ABBREV       = ''  

        t_ignore_IGCHAR1 = '\u00f3'
        t_ignore_IGCHAR2 = '\u00f4'
        t_ignore_IGCHAR3 = '\u00a0'
        t_ignore_CARRIAGERET = '\\\u000d'
        def t_error(t):
            self.report_error(t)
            t.lexer.skip(1)

        return lex.lex()
       
       
