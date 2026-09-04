from .baselang import BaseLang
from .devanagari import DevanagariUnicode


class MarathiUnicode(DevanagariUnicode):
    '''The devanagari of a marathi text.

       langs/devanagari.py is the table hindi is set with and marathi is
       written in the same script, so almost every token of it is a token
       here as well. What marathi asks for on top of it is what this class
       adds:

       - the half forms of the letters that the conjunct table has no entry
         for. Marathi puts a half consonant in front of far more letters
         than hindi does - the half ta of उत्तर and the half da of प्रसिद्ध
         are drawn, not written with an explicit virama - so a font of it
         has a glyph for each of them and needs a token to hand it to.
       - the half forms of the conjuncts that marathi draws as a letter of
         its own. त्र, त्त, श्र and श्व are one glyph in a marathi font and
         each of them takes a half form of its own as well.
       - the matras that carry an anusvar or a reph. A matra and the sign
         that sits on it are one glyph of a marathi font, so ी and ीं are
         two glyphs and two tokens, and the conjunct table of devanagari
         only has some of the pairs.
    '''

    def __init__(self):
        DevanagariUnicode.__init__(self)

        uMap   = self.tokendict
        halant = uMap['HALANT']

        def adha(*names):
            '''the half form of the letter, or of the conjunct, that the
               tokens name: the letters joined by a virama and a virama on
               the end of them'''
            return halant.join([uMap[name] for name in names]) + halant

        def full(*names):
            '''the conjunct that the tokens name, the letters joined by a
               virama'''
            return halant.join([uMap[name] for name in names])

        self.tokendict.update({\
          # HALF CONSONANTS the conjunct table of devanagari has no entry
          # for. Everything a marathi word can end a half syllable with
          'ADHA_CHA'    : adha('CHA'),  \
          'ADHA_TTA'    : adha('TTA'),  \
          'ADHA_TTHA'   : adha('TTHA'), \
          'ADHA_DDA'    : adha('DDA'),  \
          'ADHA_DDHA'   : adha('DDHA'), \
          'ADHA_DA'     : adha('DA'),   \
          'ADHA_HA'     : adha('HA'),   \
          'ADHA_LLA'    : adha('LLA'),  \
          'ADHA_NGA'    : adha('NGA'),  \

          # HALF FORMS OF THE CONJUNCTS marathi draws as one letter
          'ADHA_TATA'   : adha('TA', 'TA'),   \
          'ADHA_TRA'    : adha('TA', 'RA'),   \
          'ADHA_SHRA'   : adha('SHA', 'RA'),  \
          'ADHA_SHAVA'  : adha('SHA', 'VA'),  \
          'ADHA_HAYA'   : adha('HA', 'YA'),   \
          'ADHA_DAWA'   : adha('DA', 'VA'),   \

          # CONJUNCTS. The conjunct table has most of them, these are the
          # ones of a marathi text that it is missing
          'TTAYA'       : full('TTA', 'YA'),  \
          'DDAYA'       : full('DDA', 'YA'),  \
          'LLAYA'       : full('LLA', 'YA'),  \
          'SSATTHA'     : full('SSA', 'TTHA'),\
          'HAVA'        : full('HA', 'VA'),   \

          # MATRAS THAT CARRY A SIGN. A marathi font draws the matra and
          # the anusvar on it as one glyph
          'MATRA_AABINDU' : uMap['MATRA_AA'] + uMap['BINDU'], \
          'MATRA_UBINDU'  : uMap['MATRA_U']  + uMap['BINDU'], \
          'MATRA_UUBINDU' : uMap['MATRA_UU'] + uMap['BINDU'], \
          'MATRA_RIBINDU' : uMap['MATRA_RI'] + uMap['BINDU'], \

          # THE RA THAT HANGS UNDER ITS CONSONANT. A ra that a virama
          # binds to the letter in front of it is drawn as a stroke under
          # that letter, and a font draws that stroke as a glyph of its own
          'RAKAR'         : halant + uMap['RA'], \

          # THE HALF RA THAT IS ALREADY IN FRONT. A reph is written before
          # the syllable it is drawn on, so a font that draws it after that
          # syllable hands it here as ADHA_RA and it is moved back. This is
          # the reph of a font that has already put it in front - it is the
          # same character and it travels no further
          'ADHA_RA2'      : uMap['RA'] + halant, \
        })


class Yogesh(BaseLang):
    '''What only DVBW-TTYogesh asks for. See fonts/marathi/yogesh.py'''

    def __init__(self):
        BaseLang.__init__(self)

        self.tokendict = {\
            # A wide letter of this font overflows the box it is given and
            # an empty glyph behind it pays for the rest of that width, so
            # that the matras of the syllable can be drawn over the letter.
            # It is width and no character at all
            'SPACER'   : '', \
                             \
            # punctuation of the font that devanagari has no token for
            'LEFTSQBRACE'  : '[', \
            'RIGHTSQBRACE' : ']', \
        }

        self.conjunct_tokens = {\
            # matra_i and the reph on it are one glyph, and it is drawn in
            # front of the consonant they both belong to, so the reph is
            # already where unicode writes it
            'MATRAIRI2': ['ADHA_RA2', 'MATRA_I'], \
        }
