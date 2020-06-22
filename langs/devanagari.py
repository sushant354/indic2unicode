from .baselang import BaseLang
class DevanagariUnicode(BaseLang):
    def __init__(self):
        BaseLang.__init__(self)
        self.tokendict = { \
          'CHANDRABINDU': '\u0901', \
          'BINDU'       : '\u0902', \
          'VISARGA'     : '\u0903', \
          # PUNCTUATIONS             \
          'STAR'             : '*',        \
          'QUOT'             : '"',        \
          'SINGLE_QUOT_OPEN' : '\u0022',   \
          'PROMPT'           : '\u003a',   \
          'SINGLE_QUOT_CLOSE': '\u0022',   \
          'PLUS'             : '\u002b',   \
          'EQ'               : '\u003d',   \
          'SPACE'            : '\u0020',   \
          'NEWLINE'          : '\u000a',   \
          'CARRIAGERET'      : '\u000d',   \
          'PERCENT'          : '\u0025',   \
          'LEFTPARAN'        : '\u0028',   \
          'RIGHTPARAN'       : '\u0029',   \
          'COMMA'            : '\u002c',   \
          'DASH'             : '\u002d',   \
          'DOT'              : '\u002e',   \
          'SLASH'            : '\u002f',   \
          'COLON'            : '\u003a',   \
          'SEMICOLON'        : '\u003b',   \
          'QUESTION'         : '\u003f',   \
                                            \
          # VOWELS                   \
          'SHORT_A'     : '\u0904', \
          'A'           : '\u0905', \
          'AA'          : '\u0906', \
          'I'           : '\u0907', \
          'II'          : '\u0908', \
          'U'           : '\u0909', \
          'UU'          : '\u090a', \
          'RE'          : '\u090b', \
          'LI'          : '\u090c', \
          'CHANDRA_E'   : '\u090d', \
          'SHORT_E'     : '\u090e', \
          'E'           : '\u090f', \
          'AI'          : '\u0910', \
          'CHANDRA_O'   : '\u0911', \
          'SHORT_O'     : '\u0912', \
          'OO'          : '\u0913', \
          'AU'          : '\u0914', \
                                     \
          # CONSONANTS               \
          'KA'          : '\u0915', \
          'KHA'         : '\u0916', \
          'GA'          : '\u0917', \
          'GHA'         : '\u0918', \
          'NGA'         : '\u0919', \
                                     \
          'CA'          : '\u091a', \
          'CHA'         : '\u091b', \
          'JA'          : '\u091c', \
          'JHA'         : '\u091d', \
          'NYA'         : '\u091e', \
                                     \
          'TTA'         : '\u091f', \
          'TTHA'        : '\u0920', \
          'DDA'         : '\u0921', \
          'DDHA'        : '\u0922', \
          'NNA'         : '\u0923', \
          'TA'          : '\u0924', \
          'THA'         : '\u0925', \
          'DA'          : '\u0926', \
          'DHA'         : '\u0927', \
          'NA'          : '\u0928', \
          'NNNA'        : '\u0929', \
                                     \
          'PA'          : '\u092a', \
          'PHA'         : '\u092b', \
          'BA'          : '\u092c', \
          'BHA'         : '\u092d', \
          'MA'          : '\u092e', \
                                     \
          'YA'          : '\u092f', \
          'RA'          : '\u0930', \
          'RRA'         : '\u0931', \
          'LA'          : '\u0932', \
          'LLA'         : '\u0933', \
          'LLLA'        : '\u0934', \
          'VA'          : '\u0935', \
                                     \
          'SHA'         : '\u0936', \
          'SSA'         : '\u0937', \
          'SA'          : '\u0938', \
          'HA'          : '\u0939', \
          # SIGNS                    \
          'NUKTA'       : '\u093c', \
          'AVAGRAHA'    : '\u093d', \
          # MATRAS                   \
          'MATRA_AA'    : '\u093e', \
          'MATRA_I'     : '\u093f', \
          'MATRA_II'    : '\u0940', \
          'MATRA_U'     : '\u0941', \
          'MATRA_UU'    : '\u0942', \
                                      \
          'MATRA_RI'    : '\u0943', \
          'MATRA_RR'    : '\u0944', \
          'CHANDRA'     : '\u0945', \
          'MATRA_SHORT_E': '\u0946', \
          'MATRA_E'     : '\u0947', \
          'MATRA_AI'    : '\u0948', \
          'MATRA_CHANDRA_O': '\u0949', \
          'MATRA_SHORT_O': '\u094a', \
          'MATRA_O'     : '\u094b', \
          'MATRA_AU'    : '\u094c', \
          # SIGNA                    \
          'HALANT'      : '\u094d', \
          #'RESERVERD_1': u'\u094e', \
          #'RESERVED_2' : u'\u094f', \
          'OM'          : '\u0950', \
          'UDATTA'      : '\u0951', \
          'ANUDATTA'    : '\u0952', \
          'GRAVE_ACCENT': '\u0953', \
          'ACUTE_ACCENT': '\u0954', \
          # UNKNOWNS                 \
          #'UNKNOWN1'   : u'\u0955', \
          #'UNKNOWN2'   : u'\u0956', \
          #'UNKNOWN3'   : u'\u0957', \
          # ADDITIONAL CONSONANTS     \
          'QA'          : '\u0958', \
          'KHHA'        : '\u0959', \
          'GHHA'        : '\u095a', \
          'ZA'          : '\u095b', \
          'DDDHA'       : '\u095c', \
          'RHA'         : '\u095d', \
          'FA'          : '\u095e', \
          'YYA'         : '\u095f', \
          # GENERIC ADDITIONS        \
          'RRE'         : '\u0960', \
          'LLE'         : '\u0961', \
          'MATRA_L'     : '\u0962', \
          'MATRA_LL'    : '\u0963', \
          'VIRAM'       : '\u0964', \
          'DEERGH_VIRAM': '\u0965', \
                                       \
          # DIGITS                     \
          'ZERO'        : '\u0966', \
          'ONE'         : '\u0967', \
          'TWO'         : '\u0968', \
          'THREE'       : '\u0969', \
          'FOUR'        : '\u096a', \
          'FIVE'        : '\u096b', \
          'SIX'         : '\u096c', \
          'SEVEN'       : '\u096d', \
          'EIGHT'       : '\u096e', \
          'NINE'        : '\u096f', \
          'ABBREV'      : '\u0970', \
        }

class Conjuncts(BaseLang):

    def __init__(self):
        BaseLang.__init__(self)
        devUni = DevanagariUnicode()
        uMap   = devUni.tokendict
        
        halant = uMap['HALANT']

        self.tokendict = { \
          'ADHA_A'   : uMap['A']    + uMap['HALANT'], \
          'ADHA_KA'  : uMap['KA']   + uMap['HALANT'], \
          'ADHA_KHA' : uMap['KHA']  + uMap['HALANT'], \
          'ADHA_GA'  : uMap['GA']   + uMap['HALANT'], \
          'ADHA_GHA' : uMap['GHA']  + uMap['HALANT'], \
                                                      \
          'ADHA_CA'  : uMap['CA']   + uMap['HALANT'], \
          'ADHA_JA'  : uMap['JA']   + uMap['HALANT'], \
          'ADHA_JHA' : uMap['JHA']  + uMap['HALANT'], \
          'ADHA_NYA' : uMap['NYA']  + uMap['HALANT'], \
                                                      \
          'ADHA_NNA' : uMap['NNA']  + uMap['HALANT'], \
                                                      \
          'ADHA_TA'  : uMap['TA']   + uMap['HALANT'], \
          'ADHA_THA' : uMap['THA']  + uMap['HALANT'], \
          'ADHA_DHA' : uMap['DHA']  + uMap['HALANT'], \
          'ADHA_NA'  : uMap['NA']   + uMap['HALANT'], \
          'ADHA_NNA' : uMap['NNA']  + uMap['HALANT'], \
                                                      \
          'ADHA_PA'  : uMap['PA']   + uMap['HALANT'], \
          'ADHA_PHA' : uMap['PHA']  + uMap['HALANT'], \
          'ADHA_BA'  : uMap['BA']   + uMap['HALANT'], \
          'ADHA_BHA' : uMap['BHA']  + uMap['HALANT'], \
          'ADHA_YA'  : uMap['YA']   + uMap['HALANT'], \
          'ADHA_RA'  : uMap['RA']   + uMap['HALANT'], \
                                                      \
          'ADHA_LA'  : uMap['LA']   + uMap['HALANT'], \
          'ADHA_LLA' : uMap['LLA']  + uMap['HALANT'], \
          'ADHA_MA'  : uMap['MA']   + uMap['HALANT'], \
          'ADHA_VA'  : uMap['VA']   + uMap['HALANT'], \
          'ADHA_VA2' : uMap['VA']   + uMap['HALANT'], \
          'ADHA_SHA' : uMap['SHA']  + uMap['HALANT'], \
          'ADHA_SSA' : uMap['SSA']  + uMap['HALANT'], \
          'ADHA_SA'  : uMap['SA']   + uMap['HALANT'], \
                                                      \
          'ADHA_QA'  : uMap['QA']   + uMap['HALANT'], \
          'ADHA_KHHA': uMap['KHHA'] + uMap['HALANT'], \
          'ADHA_GHHA': uMap['GHHA'] + uMap['HALANT'], \
          'ADHA_ZA'  : uMap['ZA']   + uMap['HALANT'], \
          'ADHA_FA'  : uMap['FA']   + uMap['HALANT'], \

          'KALA'    : uMap['KA']   + halant + uMap['LA'],     \
          'KHARA'   : uMap['KHA']  + halant + uMap['RA'],     \
          'NGAKA'   : uMap['NGA']   + halant + uMap['KA'],     \
          'NGAGA'   : uMap['NGA']   + halant + uMap['GA'],     \
          'CHHHA'   : uMap['KA']   + halant + uMap['SSA'],    \
          'ADHA_CHHHA': uMap['KA'] + halant + uMap['SSA'] + halant,    \
          'GRA'     : uMap['GA']   + halant + uMap['RA'],     \
          'GRHA'    : uMap['GHA']  + halant + uMap['RA'],     \
          'CHRA'    : uMap['CA']   + halant + uMap['RA'],     \
          'JRA'     : uMap['JA']   + halant + uMap['RA'],     \
          'GYAN'    : uMap['JA']   + halant + uMap['NYA'],    \
          'JHRA'    : uMap['JHA']  + halant + uMap['RA'],     \
          'NYAJA'   : uMap['NYA']  + halant + uMap['JA'],     \
          'NYACHA'  : uMap['NYA']  + halant + uMap['CHA'],     \
                                                              \
          'TTATTA'  : uMap['TTA']  + halant + uMap['TTA'],    \
          'TTATTHA' : uMap['TTA']  + halant + uMap['TTHA'],   \
          'TTHATTHA': uMap['TTHA'] + halant + uMap['TTHA'],   \
          'DDADDA'  : uMap['DDA']  + halant + uMap['DDA'],    \
          'DDADDHA' : uMap['DDA']  + halant + uMap['DDHA'],   \
                                              \
          'SHRA'    : uMap['SHA']  + halant + uMap['RA'],     \
          'TATA'    : uMap['TA' ]  + halant + uMap['TA'],     \
          'TRA'     : uMap['TA']   + halant + uMap['RA'],     \
          'THRA'    : uMap['THA']  + halant + uMap['RA'],     \
                                                              \
          'DRI'     : uMap['DA']   + halant + uMap['MATRA_RI'],\
          'DRA'     : uMap['DA']   + halant + uMap['RA'],     \
          'DADA'    : uMap['DA']   + halant + uMap['DA'],     \
          'DADHA'   : uMap['DA']   + halant + uMap['DHA'],    \
          'DAMA'    : uMap['DA']   + halant + uMap['MA'],     \
          'DAYA'    : uMap['DA']   + halant + uMap['YA'],     \
          'DAWA'    : uMap['DA']   + halant + uMap['VA'],     \
          'DABHA'   : uMap['DA']   + halant + uMap['BHA'],     \
          'DHARA'   : uMap['DHA']  + halant + uMap['RA'],     \
                                                              \
          'NARA'    : uMap['DHA']  + halant + uMap['RA'],     \
          'NANA'    : uMap['NA']   + halant + uMap['NA'],     \
          'PRA'     : uMap['PA']   + halant + uMap['RA'],     \
          'JAJA'    : uMap['JA']   + halant + uMap['JA'],     \
          'DHADHA'  : uMap['DHA']  + halant + uMap['DHA'],    \
          'BRA'     : uMap['BA']   + halant + uMap['RA'],     \
          'BRHA'    : uMap['BHA']  + halant + uMap['RA'],     \
          'MRA'     : uMap['MA']   + halant + uMap['RA'],     \
          'RAUU'    : uMap['RA'] + uMap[ 'MATRA_UU'],         \
                                                              \
          'SHANA'   : uMap['SHA'] + halant + uMap['NA'],     \
          'SHACHA'  : uMap['SHA'] + halant + uMap['CHA'],     \
          'SSATTA'  : uMap['SSA'] + halant + uMap['TTA'],     \
          'VRA'     : uMap['VA'] + halant + uMap['RA'],       \
          'KRA'     : uMap['KA'] + halant + uMap['RA'],       \
          'SHAVA'   : uMap['SHA'] + halant + uMap['VA'],      \
          'YARA'    : uMap['YA'] + halant + uMap['RA'],       \
                                                              \
          'HARA'    : uMap['HA'] + halant + uMap['RA'],       \
          'HAMA'    : uMap['HA'] + halant + uMap['MA'],       \
          'HAYA'    : uMap['HA'] + halant + uMap['YA'],       \
          'HARI'    : uMap['HA'] + halant + uMap['MATRA_RI'], \
          'HALA'    : uMap['HA'] + halant + uMap['LA'],       \
          'HAVA'    : uMap['HA'] + halant + uMap['VA'],       \
          'HANA'    : uMap['HA'] + halant + uMap['NA'],       \
                                                              \
          'NGAGHA'  : uMap['NGA'] + halant + uMap['GHA'],     \
          'NGAKHA'  : uMap['NGA'] + halant + uMap['KHA'],     \

          'MATRAIBINDU': uMap['MATRA_I'] + uMap ['BINDU'],    \
          'MATRAIIBINDU'  : uMap['MATRA_II'] + uMap['BINDU'], \
          'MATRAEBINDU'   : uMap['MATRA_E']  + uMap['BINDU'], \
          'MATRAAIBINDU'  : uMap['MATRA_AI'] + uMap['BINDU'], \
          'MATRAOBINDU'   : uMap['MATRA_O']  + uMap['BINDU'], \
          'MATRAAUBINDU'  : uMap['MATRA_AU'] + uMap['BINDU'], \
        }

        self.conjunct_tokens = { \
          'RAU'     : ['RA',  'MATRA_U'],\
          'RAU2'    : ['RA',  'MATRA_U'],\
                                              \
          'MATRA_RA': ['HALANT',  'RA'],      \
                                                   \
          'MATRAIRI'       : ['MATRA_I', 'ADHA_RA'],               \
          'MATRAIRIBINDU'  : ['MATRAIBINDU', 'ADHA_RA'],       \
                                                                   \
          'MATRAIIRI'      : ['ADHA_RA', 'MATRA_II'],              \
          'MATRAIIRIBINDU' : ['MATRAIIBINDU', 'ADHA_RA'],     \
                                                                   \
          'MATRAERI'       : ['ADHA_RA', 'MATRA_E'],               \
          'MATRAERIBINDU'  : ['ADHA_RA', 'MATRA_E', 'BINDU'],      \
                                                                   \
          'MATRAAIRI'      : ['ADHA_RA', 'MATRA_AI'],              \
          'MATRAAIRIBINDU' : ['ADHA_RA', 'MATRA_AI', 'BINDU'],     \
          'MATRAORI'       : ['ADHA_RA', 'MATRA_O'],               \
          'MATRAORIBINDU'  : ['ADHA_RA', 'MATRA_O', 'BINDU'],      \
                                                                   \
          'MATRAAURI'      : ['ADHA_RA', 'MATRA_AU'],              \
          'MATRAAURIBINDU' : ['ADHA_RA', 'MATRA_AU', 'BINDU'],     \
                                                                   \
          'MATRA_AA_ADHARA': ['ADHA_RA', 'MATRA_AA'],              \
        }            

class Surekh(BaseLang):
    def __init__(self):
        BaseLang.__init__(self)
        devUnicode = DevanagariUnicode() 
        uMap = devUnicode.tokendict

        conjunctobj = Conjuncts()
        conTokendict = conjunctobj.tokendict
        conMap = conjunctobj.conjunct_tokens

        halant = uMap['HALANT']
        self.tokendict = {\
            'EXCLAMATION'      : '!', \
            'ADHA_HA'          : uMap['HA'] + halant, \
            'PHA_RA'           : uMap['PHA'] + halant + uMap['RA'], \
            'YA2'              : uMap['YA'],      \
            'MATRA_U2'         : uMap['MATRA_U'], \
            'MATRA_UU2'        : uMap['MATRA_UU'], \
            'MATRAIBINDU2'     : conTokendict['MATRAIBINDU'], \
            'MATRA_I2'         : uMap['MATRA_I'], \
            'ADHA_RA_BINDU'    : conTokendict['ADHA_RA'] + uMap['BINDU'], \
        }

        self.conjunct_tokens = { \
            'SHA_VA': ['SHA', 'HALANT', 'VA'], \
            'SA_RA' : ['SA', 'HALANT', 'RA'], \
            'MATRA_SHORT_E_BINDU' : ['MATRA_SHORT_E', 'BINDU'], \
            'MATRA_SHORT_E_ADHARA': ['MATRA_SHORT_E', 'BINDU'], \
            'MATRA_SHORT_E_ADHARABINDU' : ['ADHA_RA', 'MATRA_SHORT_E', 'BINDU'],\
            'MATRAU_ADHARA'    : ['ADHA_RA', 'MATRAU'], \
            'MATRAUU_ADHARA'   : ['ADHA_RA', 'MATRAUU'], \
            'MATRACHANDRABINDU': ['MATRA_CHANDRA_E', 'BINDU'], \
            'MATRACHANDRAADHRA': ['ADHA_RA' + 'MATRA_CHANDRA_E'], \
            'MATRACHANDRAADHRA_BINDU': ['ADHA_RA' + 'MATRA_CHANDRA_E', 'BINDU'],\
            'MATRAIRIBINDU2'   : conMap['MATRAIRIBINDU'], \
            'MATRAIRI2'        : conMap['MATRAIRI'], \
        }

class Aryan2(BaseLang):
    def __init__(self):
        BaseLang.__init__(self)
        devUnicode = DevanagariUnicode() 
        uMap = devUnicode.tokendict

        conjunctobj = Conjuncts()
        conTokendict = conjunctobj.tokendict
        conMap = conjunctobj.conjunct_tokens

        halant     = uMap['HALANT']

        self.conjunct_tokens = { \
            'MATRAIRI2'        : conMap['MATRAIRI'], \
            'MATRAIRIBINDU2'   : conMap['MATRAIRIBINDU'], \
            'AA_ADHARA'        : ['ADHA_RA', 'MATRA_AA'], \
        }

        self.tokendict = {\
            'IGCHAR1'          : '',         \
            'IGCHAR2'          : '',         \
            'IGCHAR3'          : ' ',        \
            'ADHA_YA2'         : conTokendict['ADHA_YA'], \
            'ADHA_SSA2'        : conTokendict['ADHA_SSA'], \
            'VA2'              : uMap['VA'], \
            'YA2'              : uMap['YA'],      \
            'HA2'              : uMap['HA'],      \
            'SSA2'             : uMap['SSA'], \
            'MATRA_I2'         : uMap['MATRA_I'], \
            'MATRA_U2'         : uMap['MATRA_U'], \
            'MATRA_UU2'        : uMap['MATRA_UU'], \
            'MATRAIBINDU2'     : conTokendict['MATRAIBINDU'], \
            'KA_U'             : uMap['KA'] + uMap['MATRA_U'], \
            'KA_UU'            : uMap['KA'] + uMap['MATRA_UU'], \
            'KA_RI'            : uMap['KA'] + uMap['MATRA_RI'], \
            'ADHA_KA_U'        : uMap['KA'] + halant + uMap['MATRA_U'], \
            'ADHA_KA_UU'       : uMap['KA'] + halant + uMap['MATRA_UU'], \
            'ADHA_KA_RI'       : uMap['KA'] + halant + uMap['MATRA_RI'], \
            'ADHA_RA_BINDU'    : conTokendict['ADHA_RA'] + uMap['BINDU'], \
            'PHA_U'             : uMap['PHA'] + uMap['MATRA_U'], \
            'PHA_UU'            : uMap['PHA'] + uMap['MATRA_UU'], \
            'PHA_RI'            : uMap['PHA'] + uMap['MATRA_RI'], \
            'PHA_RA'            : uMap['PHA'] + halant + uMap['RA'], \
        }

