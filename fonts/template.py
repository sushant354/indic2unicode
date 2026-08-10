import html2text.fontconv.langs.devanagari
class Aryan2:
    def __init__(self):
        pass
  
    def get_lexer(self):
        tokens = devanagari.tokens
        # signs
        t_CHANDRABINDU = '' 
        t_BINDU        = ''
        t_VISARGA      = ''

        # VOWELS
        t_SHORT_A      = ''
        t_A            = ''
        t_AA           = ''
        t_I            = ''
        t_II           = ''
        t_U            = ''
        t_UU           = ''
        t_RE           = ''
        t_LI           = ''
        t_CHANDRA_E    = ''
        t_E            = ''
        t_AI           = ''
        t_CHANDRA_O    = ''
        t_SHORT_O      = ''
        t_OO           = ''
        t_AU           = ''
 
        # CONSONANTS 
        t_KA           = ''
        t_KHA          = ''
        t_GA           = ''
        t_GHA          = ''
        t_NGA          = ''

        t_CA           = ''
        t_CHA          = ''
        t_JA           = ''
        t_JHA          = ''
        t_NYA          = ''

        t_TTA          = ''
        t_TTHA         = ''
        t_DDA          = ''
        t_DDHA         = ''
        t_NNA          = ''
 
        t_TA           = ''
        t_THA          = ''
        t_DA           = ''
        t_DHA          = ''
        t_NA           = ''
        t_NNA          = ''
 
        t_PA           = ''
        t_PHA          = ''
        t_BA           = ''
        t_BHA          = ''
        t_MA           = ''
  
        t_YA           = ''
        t_RA           = ''
        t_RRA          = ''
        t_LA           = ''
        t_LLA          = ''
        t_LLLA         = ''
        t_VA           = ''
        t_SHA          = ''
        t_SSA          = ''
        t_SA           = ''
        t_HA           = ''
  
        # SIGNS
        t_NUKTA        = ''
        t_AVAGRAHA     = ''
 
        # MATRAS
        t_MATRA_AA     = ''
        t_MATRA_I      = ''
        t_MATRA_II     = ''
        t_MATRA_U      = ''
        t_MATRA_UU     = ''
        t_MATRA_RI     = ''
        t_MATRA_RR     = ''
        t_CHANDRA      = ''
        t_MATRA_SHORT_E = ''
        t_MATRA_E      = ''
        t_MATRA_AI     = ''
        t_MATRA_CHANDRA_O  = ''
        t_MATRA_SHORT_O  = ''
        t_MATRA_O      = ''
        t_MATRA_AU     = ''

        # SIGNA
        t_HALANT       = ''
        t_RESERVERD_1  = ''
        t_RESERVED_2   = ''
        t_OM           = ''
        t_UDATTA       = ''
          
        t_ANUDATTA     = ''
        t_GRAVE_ACCENT = ''
        t_ACUTE_ACCENT = ''

        # UNKNOWNS
        t_UNKNOWN1     = ''
        t_UNKNOWN2     = ''
        t_UNKNOWN3     = ''

        # ADDITIONAL CONSONANTS
        t_QA           = ''
        t_KHHA         = ''
        t_GHHA         = ''
        t_ZA           = ''
        t_DDDHA        = ''
        t_RHA          = ''
        t_FA           = ''
        t_YYA          = ''

        # GENERIC ADDITIONS
        t_RRE          = ''
        t_LLE          = ''
        t_MATRA_L      = ''
        t_MATRA_LL     = ''
        t_VIRAM        = ''
        t_DEERGH_VIRAM = ''
  
        # DIGITS
        t_ZERO         = ''
        t_ONE          = ''
        t_TWO          = ''
        t_THREE        = ''
        t_FOUR         = ''
        t_FIVE         = ''
        t_SIX          = ''
        t_SEVEN        = ''
        t_EIGHT        = ''
        t_NINE         = ''
        t_ABBREV       = ''

       
       
