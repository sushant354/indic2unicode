from indic2unicode.langs import devanagari
from .basefont import BaseFont
import ply.lex as lex
import logging

class Surekh(BaseFont):
    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs  = []
        self.langobjs.append(devanagari.DevanagariUnicode())
        self.langobjs.append(devanagari.Conjuncts())
        self.langobjs.append(devanagari.Surekh())

        self.lexer = self.get_lexer()
        self.waitdict = {'MATRA_I': 1, 'MATRAIBINDU' : 1, 'MATRAIBINDU2': 1, \
                         'MATRA_I2': 2}

        self.composeTokens = {\
            ('A', 'MATRA_AA') : 'AA',                         \
            ('MATRA_I', 'ADHA_RA'): ['ADHA_RA', 'MATRA_I'],   \
            ('MATRA_II', 'ADHA_RA'): ['ADHA_RA', 'MATRA_II'], \
        }

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

        danda   = '\u00c9'
        chandra = '\u00ec'
        matra_e = '\u00e4'

        # MATRAS
        t_MATRA_AA     = danda 
        t_MATRA_I      = '\u00ca'
        t_MATRA_I2     = '\u00ce'
        t_MATRA_II     = '\u00d2'
        t_MATRA_U      = '\u00d6'
        t_MATRA_U2     = '\u00d9'
        t_MATRA_UU     = '\u00da'
        t_MATRA_UU2    = '\u00dd'
        t_YA2          = '\u00ac' 
        t_MATRA_RI     = '\u00de'
        t_MATRA_RR     = '\u00df'
        t_CHANDRA      = chandra
        t_MATRA_SHORT_E = '\u00e0'

        t_MATRA_E      = matra_e
        t_MATRA_AI     = '\u00e8'
        t_MATRA_CHANDRA_O  = danda + chandra 
        t_MATRA_SHORT_O  = t_MATRA_SHORT_E + danda
        t_MATRA_O      = danda + t_MATRA_E 
        t_MATRA_AU     = danda + t_MATRA_AI 

        # conjuncts
        tokens.remove('KALA')  # t_KALA                = u'\u'
        t_KHARA              = '\u004c' + danda 
        tokens.remove('NGAKA') # t_NGAKA              = u'' 
        tokens.remove('NGAGA') # t_NGAGA              = u'' 
        t_ADHA_CHHHA         = '\u0049' 
        t_CHHHA              = t_ADHA_CHHHA + danda
        t_GRA                = '\u004f' + danda
        t_GRHA               = '\u0051' + danda 
        t_CHRA               = '\u0054' + danda 
        t_JRA                = '\u0058' + danda
        t_GYAN               = '\u0059' + danda
        t_JHRA               = '\\\u005b' + danda
        tokens.remove('NYAJA') # t_NYAJA              = u''
        tokens.remove('NYACHA') # t_NYACHA             = u''

        t_TTATTA             = '\\\u005e'
        t_TTATTHA            = '\u005f'
        t_TTHATTHA           = '\u0061'
        t_DDADDA             = '\u0064'
        t_DDADDHA            = '\u0065'

        t_SHRA               = '\u00b8' + danda
        t_SHA_VA             = '\u00b7' + danda
        t_SA_RA              = '\u00bb' + danda
        t_TRA                = '\u006a' + danda 
        t_TATA               = '\u006b' + danda
        t_THRA               = '\u006d' + danda
        t_DRI                = '\u006f' 
        t_DRA                = '\u0070'
        t_DADA               = '\u0071'
        t_DADHA              = '\u0072'
        t_DAMA               = '\u0073' 
        t_DAYA               = '\u0074' 
        t_DAWA               = '\u0075'
        tokens.remove('DABHA') # t_DABHA              = u''
        t_DHARA              = '\u0077' + danda

        t_NARA               = '\u0079' + danda
        t_NANA               = '\u007a' + danda
        t_PRA                = '\\\u007c' + danda 

        tokens.remove('JAJA')  # t_JAJA               = u'' 
        tokens.remove('DHADHA')# t_DHADHA            = u''

        t_BRA                = '\u00a5' + danda 
        t_BRHA               = '\u00a7' + danda
        t_MRA                = '\u00a9' + danda
        t_RAUU               = '\u00b0'
        tokens.remove('SHACHA') # t_SHACHA             = u'' 
        tokens.remove('SHANA') #  t_SHANA             = u'' 
        tokens.remove('SSATTA') #  t_SSATTA           = u''
        t_VRA                = '\u00b5' + danda
        t_KRA                = '\u0047' 
        tokens.remove('SHAVA') # t_SHAVA              = u''
        t_YARA               = '\u00ab' + danda
        t_RAU                = '\u00af'
        tokens.remove('RAU2') # t_RAU2               = u''

        t_HARA               = '\u00bf' 
        t_HAMA               = '\u00c0' 
        t_HAYA               = '\u00c1' + danda
        t_MATRA_RA           = '\u00c5'
        tokens.remove('HARI') # t_HARI               = u''
        tokens.remove('HALA') # t_HALA               = u''
        tokens.remove('HAVA') # t_HAVA               = u''
        tokens.remove('HANA') # t_HANA              = u''

        tokens.remove('NGAGHA') # t_NGAGHA             = u''
        tokens.remove('NGAKHA') # t_NGAKHA             = u''
        t_ADHA_RA            = '\u00c7'
        t_ADHA_RA_BINDU      = '\u00c8'
        
        t_MATRAIBINDU        = '\u00cb'
        t_MATRAIBINDU2       = '\u00cf'
        t_MATRAIRI           = '\u00cc'
        t_MATRAIRI2          = '\u00d0'
        t_MATRAIRIBINDU      = '\u00cd'
        t_MATRAIRIBINDU2     = '\u00d1'

        t_MATRAIIBINDU       = '\u00d3'
        t_MATRAIIRI          = '\u00d4' 
        t_MATRAIIRIBINDU     = '\u00d5'

        t_MATRAU_ADHARA      = '\u00d8'
        t_MATRAUU_ADHARA     = '\u00dc'
        t_MATRA_AA_ADHARA    = danda + t_ADHA_RA

        t_MATRA_SHORT_E_BINDU       = '\u00e1'
        t_MATRA_SHORT_E_ADHARA      = '\u00e2'
        t_MATRA_SHORT_E_ADHARABINDU = '\u00e3'

        t_MATRAEBINDU        = '\u00e5' 
        t_MATRAERI           = '\u00e6' 
        t_MATRAERIBINDU      = '\u00e7' 

        t_MATRAAIBINDU        = '\u00e9' 
        t_MATRAAIRI           = '\u00ea' 
        t_MATRAAIRIBINDU      = '\u00eb' 

        t_MATRACHANDRABINDU  = '\u00ed'
        t_MATRACHANDRAADHRA  = '\u00ee'
        t_MATRACHANDRAADHRA_BINDU  = '\u00ef'

        t_MATRAOBINDU        = danda + t_MATRAEBINDU 
        t_MATRAORI           = danda + t_MATRAERI
        t_MATRAORIBINDU      = danda + t_MATRAERIBINDU

        t_MATRAAUBINDU       = danda + t_MATRAAIBINDU
        t_MATRAAURI          = danda + t_MATRAAIRI
        t_MATRAAURIBINDU     = danda + t_MATRAAIRIBINDU
        
        # PUNCTUATION 
        t_EXCLAMATION        = '\u0021'
        tokens.remove('QUOT')
        t_PROMPT             = '\u003a'
        t_SINGLE_QUOT_OPEN   = '\u0022'
        t_SINGLE_QUOT_CLOSE  = '\u0027'
        tokens.remove('PLUS')
        tokens.remove('EQ')
        tokens.remove('PERCENT')
        t_SPACE              = '\\\u0020'
        t_NEWLINE            = '\\\u000a'
        t_LEFTPARAN          = '\\\u0028'
        t_RIGHTPARAN         = '\\\u0029'
        t_COMMA              = '\u002c'
        t_DASH               = '\u002d'
        t_DOT                = '\\\u002e'
        t_SLASH              = '\\\u002f'
        t_COLON              = '\u003a'
        t_SEMICOLON          = '\u003b'
        t_QUESTION           = '\\\u003f'
 

        t_PHA_RA             = '\u00a3' 
        # Half Letters
        tokens.remove('ADHA_A') # t_ADHA_A       = u''
        t_ADHA_KA      = '\u0043'
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
        t_ADHA_PHA     = '\u007d' 
        t_ADHA_BA      = '\u00a4'
        t_ADHA_BHA     = '\u00a6' 
        t_ADHA_MA      = '\u00a8' 
  
        t_ADHA_YA      = '\u00aa'
        t_ADHA_LA      = '\u00b1' 
        t_ADHA_VA      = '\u00b4'
        t_ADHA_HA      = '\u00bc'

        t_ADHA_SHA     = '\u00b6' 
        t_ADHA_SSA     = '\u00b9' 
        t_ADHA_SA      = '\u00ba'
 
        t_ADHA_QA      = '\u0044' 
        t_ADHA_KHHA    = '\u004b' 
        t_ADHA_GHHA    = '\u004e' 
        t_ADHA_ZA      = '\u0057' 
        t_ADHA_FA      = '\u007e' 

        t_ADHA_LLA     = '\u00b2'
        # UNICODE
        # signs
        t_CHANDRABINDU = '\u00c4' 
        t_BINDU        = '\u00c6'
        t_VISARGA      = '\u0026'

        # VOWELS
        tokens.remove('SHORT_A') # t_SHORT_A      = u''
        t_A            = '\\\u002b' 
        t_I            = '\u003c'
        t_II           = t_I + t_ADHA_RA 
        t_U            = '\u003d'
        t_UU           = '\u003e'
        t_RE           = '\u0040'
        tokens.remove('LI') # t_LI           = u''
        t_E            = '\u0042'
        t_CHANDRA_E    = t_E + chandra
        t_AI           = t_E + matra_e 
        t_CHANDRA_O    = t_A + danda + chandra 
        t_SHORT_O      = t_A + t_MATRA_SHORT_O

        t_OO           = t_A + t_MATRA_O 
        t_AU           = t_A + t_MATRA_AU 
        # CONSONANTS 
        t_KA           = '\u0045'
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
        t_TTHA         = '\u0060'
        t_DDA          = '\u0062'
        t_DDHA         = '\u0066'
 
        t_TA           = t_ADHA_TA + danda 
        t_THA          = t_ADHA_THA + danda 
        t_DA           = '\u006e'
        t_DHA          = t_ADHA_DHA + danda 
        t_NA           = t_ADHA_NA  + danda 
        t_NNA          = t_ADHA_NNA + danda 
 
        t_PA           = t_ADHA_PA + danda 
        t_PHA          = '\u00a1'
        t_BA           = t_ADHA_BA + danda 
        t_BHA          = t_ADHA_BHA + danda 
        t_MA           = t_ADHA_MA + danda 
  
        t_YA           = t_ADHA_YA + danda 
        t_RA           = '\u00ae'
        tokens.remove('RRA') # t_RRA) #          = u''
        t_LA           = t_ADHA_LA + danda 
        t_LLA          = '\u00b3'
        tokens.remove('LLLA') # t_LLLA) #         = u''
        t_VA           = t_ADHA_VA + danda 
        t_SHA          = t_ADHA_SHA + danda 
        t_SSA          = t_ADHA_SSA + danda
        t_SA           = t_ADHA_SA  + danda
        t_HA           = '\u00bd'
  
        # SIGNS
        t_NUKTA        = '\u00c3'
        t_AVAGRAHA     = '\u0025'
 
        # SIGNA
        t_HALANT       = '\u00c2'
        t_OM           = '\\\u0024'
        tokens.remove('UDATTA') # t_UDATTA       = u''
          
        tokens.remove('ANUDATTA') # t_ANUDATTA     = u''
        tokens.remove('GRAVE_ACCENT') # t_GRAVE_ACCENT = u''
        tokens.remove('ACUTE_ACCENT') # t_ACUTE_ACCENT = u''

        # ADDITIONAL CONSONANTS
        t_QA           = '\u0046'
        t_KHHA         = t_ADHA_KHHA + danda 
        t_GHHA         = t_ADHA_GHHA + danda 
        t_ZA           = t_ADHA_ZA + danda 
        t_DDDHA        = '\u0063'
        t_RHA          = '\u0067'
        t_FA           = '\u00a2'
        tokens.remove('YYA') # t_YYA          = u''

        # GENERIC ADDITIONS
        t_RRE         = '\u0041'
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

        #t_ignore_IGCHAR1 = u''
        #t_ignore_IGCHAR2 = u''
        #t_ignore_IGCHAR3 = u''
        t_CARRIAGERET = '\\\u000d'
        def t_error(t):
            self.report_error(t)
            t.lexer.skip(1)

        return lex.lex()
       
       
