from .revathi import Revathi

class TTRevathi(Revathi):
    '''The text of a pdf that is set in ML-TTRevathi-Normal, the TrueType
       build of the ML-Revathi-Normal of fonts/malayalam/revathi.py and
       another of the malayalam fonts of the Kerala gazette.

       THE SAME FONT UNDER OTHER NAMES

       The two draw the same glyph on every key that is typed, but the pdfs
       carry them differently and so an extractor hands out a different
       character for the same glyph. The Revathi of that document is a
       Type 1 font whose glyphs are named after the characters of the mac
       roman table, and this is a TrueType subset with WinAnsiEncoding, so
       its text comes out as the windows 1252 characters of the bytes that
       were typed - ദർഘാസ് is Z¿Lmkv there and ZÀLmkv here, À being the
       byte C0 in windows 1252 and ¿ the byte C0 in mac roman.

       The two tables agree on every byte below 80, which is where the
       vowels, the alphabet and the signs are, and part company above it,
       which is where the chillus and the clusters are. So the readings of
       Revathi are taken whole and each of them is carried over to the
       byte its mac roman name stands on, which is the byte that was typed.
       The name of a glyph that mac roman does not have is one revathi.py
       reads as a second name as well, the Δ of വ്വ being the ∆ of that
       table.

       WHAT THIS DOCUMENT DRAWS THAT THAT ONE DOES NOT

       Four clusters, each of them read off its outline in the words it
       is drawn in: ശ്ച on DD (നിശ്ചിത), പ്ല on B9 (സപ്ലൈ), ക്ത on E0
       (വ്യക്തമായി) and ന്മ on B7 (കുടിയാന്മല). And ഐ, which the font draws
       as a െ in front of എ the way it draws the vowel sign ൈ in front of
       its letter - sF. is ഐ. and not എെ.

       WHAT IS NOT KNOWN

       The subset names 112 bytes of the font and every one of them comes
       out of the text of the document, each of them read here. Its one
       other byte is a 1F that has no outline at all and is dropped as the
       control character it is. The page draws no ണ്ട anywhere, the ണ്ട of
       ഗവർണ്ണർക്കുവേണ്ടി being missing from the page as well as from the
       text, so what byte the font has it on is not known and it comes out
       of this converter as ഗവർണ്ണർക്കുവേി - see the expected output of
       revathi.py, which is missing it the same way.

       WHAT THE READINGS WERE CHECKED AGAINST

       Of the 2495 words of malayalam this converter writes for the
       document, 2375 are read back word for word by an OCR of the same
       pages. Of the ones that are not, the ones the OCR has wrong are
       read right here (ചൊവ്വ, രജിസ്ട്രേഷൻ, നിരതദ്രവ്യവും, കൊയ്യം), and
       the rest are the ണ്ട the page does not draw and words the extractor
       breaks with a space - at a kerning gap as in ആന്റ ്, or between every
       glyph of a heading that is letter spaced, where a െ has no letter
       left to jump over.
    '''
    # the names the Type 1 embedding of the font gives its glyphs are the
    # characters of the mac roman table, and this embedding's text is the
    # windows 1252 character of the byte that was typed
    name_encoding = 'mac_roman'
    encoding      = 'cp1252'

    # the clusters the document of revathi.py never draws, on the byte they
    # are typed on - see the class comment
    more_glyphcodes = { \
        'SHA_CA'       : 0xDD, 'PA_LA'       : 0xB9, \
        'KA_TA'        : 0xE0, 'NA_MA'       : 0xB7, \
    }

    def __init__(self):
        Revathi.__init__(self)

        # ഐ, which the font draws as a െ in front of എ. The െ has jumped
        # over the എ by the time this runs, and a vowel sign never follows
        # a vowel in unicode, so the pair is always this letter
        self.composeTokens[('E', 'MATRA_E')] = 'AI'

    def get_glyph_chars(self):
        '''the character each glyph reaches this converter as: the byte
           that was typed for it, read as windows 1252. That byte is the
           one the name revathi.py reads the glyph under stands on in the
           mac roman table'''
        glyphcodes = {}
        for tokenName, code in Revathi.glyphcodes.items():
            if code in Revathi.code_chars:
                names = Revathi.code_chars[code]
            else:
                names = bytes([code]).decode(Revathi.encoding)
            names += Revathi.glyph_aliases.get(tokenName, '')

            for name in names:
                try:
                    glyphcodes[tokenName] = name.encode(self.name_encoding)[0]
                    break
                except UnicodeEncodeError:
                    continue

        glyphcodes.update(self.more_glyphcodes)

        glyphchars = {}
        for tokenName, code in glyphcodes.items():
            glyphchars[tokenName] = bytes([code]).decode(self.encoding)
        return glyphchars
