from .tamelango import TamElango

class TMChanakya(TamElango):
    '''The text of a pdf that is set in TM-Chanakya-Normal, the tamil font
       the Kerala gazette sets the tamil translations of its acts in, and in
       the Bold and the Italic faces of it, which share its layout.

       It is an 8 bit font of the kind fonts/tamil/tamelango.py reads: every
       glyph of it sits on a byte, the pdf calls it a Type 1 font and names
       its glyphs after the latin characters that live on those bytes, so
       what an extractor hands out is latin and not tamil at all - ˙LW[ AW—
       is கேரள அரசு and ˘TÙ’jR-L-Y-¤d-˘L] is பொதுத்தகவலுக்கென. The pdf that
       this was built from is a Malayalam gazette, but what the font draws
       is tamil through and through - the TM of its name is Tamil - and so
       it reads through langs/tamil.py.

       THE LAYOUT

       The lower half of the table runs in the order of the script. The
       vowels are on 41..4B, அ to ஓ, the eighteen letters of tamil follow
       them unbroken on 4C..5D in the order langs/tamil.CONSONANT_TOKENS
       gives, the grantha letters ஸ ஜ ஷ ஹ க்ஷ come after them on 5E..62,
       and the pulli form of every one of those letters sits 0x18 above it,
       க் on 64 to க்ஷ் on 7A. The vowel signs that are drawn beside the
       letter are glyphs of their own. The upper half, and the bytes below
       the space, are the letters that take the vowel sign i, ii, u or uu
       written into them, in no order at all.

       The pdf names those glyphs by PDFDocEncoding on 18..9F - so ெ is
       breve and ே dotaccent - by latin 1 above that, and by the names of
       the mac symbol characters below the space, radical, infinity, product
       and the like. None of that says anything about what is drawn, and an
       extractor turns every name into the character it is the name of.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       This is the same script drawn the same way tamelango's font draws it,
       so the reordering is inherited whole: the vowel signs e, ee and ai
       are drawn in front of the letter they belong to and each of them
       waits for one token - ˙LW[ is ே க ர ள and கேரள - and the signs o and
       oo are drawn in two halves with the letter between them and are put
       back together once the front half has jumped - ˘TÙ is ெ ப ா and பொ.

       ௌ is drawn the same way, out of a ெ in front of the letter and the
       length mark behind it, and the length mark of this font is the glyph
       of ள, the two being the same shape: ˙LÙm˘T[uh is கோம்பௌன்ட். A ள that
       is its own syllable cannot stand there, ளி, ளு and ள் being glyphs of
       their own, so a ெ and a ள that the letter was between are read back
       as ௌ once the ெ has jumped. ஔ is ஒ and that same length mark.

       THE HYPHEN THAT IS NOT ONE

       PageMaker, which set this document, writes a hyphen into a word to
       say where the word may be broken across a line, and the font draws
       that hyphen, the byte 2D, as a glyph 4/1000 of an em wide, i.e. as
       nothing - ©W-—-Wm is பிரசுரம். Where a line does break at one the
       page shows no hyphen either, the word simply goes on on the next
       line, so every one of them is dropped here. The hyphen a document
       really writes is a glyph of its own, at 1D, and comes through as
       one: 2017˛u is 2017-ன். The dash that follows a heading is not this
       font's - it is set in Times New Roman - and the character — that
       this font hands out is the byte 84, which draws சு.

       WHERE THE READINGS COME FROM

       This was built from one document, whose subset of the Normal face
       carries an outline for 122 bytes, every one of which the document
       draws. Each of them was identified by rendering that outline and
       reading it against a tesseract -l tam OCR of the pages that draw it:
       102 of them are tamil and are the readings below, two are the
       hyphens, and the other 18 draw themselves (the digits, the space and
       ( ) , . / : ;). The subsets of the Bold and the Italic face
       carry 20 and 16 of those bytes, and every one of them draws the same
       letter the Normal face does.

       Where the eye and the OCR disagree the OCR is believed: D3 looks as
       much like லூ as like வூ, and the one word it is drawn in, L⁄ÓXLj, is
       கருவூலகத் as the OCR reads it.

       WHAT IS NOT KNOWN

       Eight bytes below are read off the run of the lower half rather than
       off a glyph this document draws - ஊ and ஓ on 46 and 4B, the gaps the
       vowels leave for them, ங and ஞ on 4D and 4F, the gaps the letters
       leave for them, ஸ on 5E, the byte 0x18 under its ஸ் at 76, and ஜ்,
       ஹ் and க்ஷ் on 77, 79 and 7A, the bytes 0x18 above ஜ, ஹ and க்ஷ. The
       offset holds for every one of the twenty letters whose byte and whose
       pulli form this document both draw.

       The rest is left out because nothing here says anything about it:
       63, which stands between க்ஷ and க் and may be ஸ்ரீ, the i, ii, u
       and uu forms that no word of this document writes, and the
       standalone vowel signs ி, ீ and ு that a grantha letter would take.
       A byte outside the table that is a character in its own right - the
       digits, the ascii punctuation - comes through as it is, and the rest
       is reported and dropped.
    '''
    # the byte each glyph of the font sits on. Only what needs decoding is
    # listed; a byte the font draws as itself (the digits, the space and
    # ( ) , . / : ;) reaches the output through the literal path of
    # t_error, see BaseFont.is_text_char
    glyphcodes = { \
        # VOWELS and the aytham. The eleven vowels but ஔ run from 41 to   \
        # 4B in the order of the script, so ஊ and ஓ are read off the two  \
        # gaps in that run rather than off a glyph this document draws    \
        'A'            : 0x41, 'AA'          : 0x42, \
        'I'            : 0x43, 'II'          : 0x44, \
        'U'            : 0x45, 'UU'          : 0x46, \
        'E'            : 0x47, 'EE'          : 0x48, \
        'AI'           : 0x49,                       \
        'O'            : 0x4A, 'OO'          : 0x4B, \
        'AYTHAM'       : 0x40,                       \
                                                     \
        # CONSONANTS, each of them the letter with its inherent vowel a.  \
        # The eighteen of tamil run unbroken from 4C to 5D and the        \
        # grantha letters follow them. ங, ஞ and ஸ are drawn nowhere in    \
        # this document and are read off that run, see the class comment  \
        'KA'           : 0x4C, 'NGA'         : 0x4D, \
        'CA'           : 0x4E, 'NYA'         : 0x4F, \
        'TTA'          : 0x50, 'NNA'         : 0x51, \
        'TA'           : 0x52, 'NA'          : 0x53, \
        'PA'           : 0x54, 'MA'          : 0x55, \
        'YA'           : 0x56, 'RA'          : 0x57, \
        'LA'           : 0x58, 'VA'          : 0x59, \
        'LLLA'         : 0x5A, 'LLA'         : 0x5B, \
        'RRA'          : 0x5C, 'NNNA'        : 0x5D, \
        'SA'           : 0x5E, 'JA'          : 0x5F, \
        'SSA'          : 0x60, 'HA'          : 0x61, \
        'KSSA'         : 0x62,                       \
                                                     \
        # THE PULLI FORMS, each of them 0x18 above its letter. ஜ், ஹ் and \
        # க்ஷ் are read off that offset rather than off a glyph           \
        'KA_PULLI'     : 0x64, 'NGA_PULLI'   : 0x65, \
        'CA_PULLI'     : 0x66, 'NYA_PULLI'   : 0x67, \
        'TTA_PULLI'    : 0x68, 'NNA_PULLI'   : 0x69, \
        'TA_PULLI'     : 0x6A, 'NA_PULLI'    : 0x6B, \
        'PA_PULLI'     : 0x6C, 'MA_PULLI'    : 0x6D, \
        'YA_PULLI'     : 0x6E, 'RA_PULLI'    : 0x6F, \
        'LA_PULLI'     : 0x70, 'VA_PULLI'    : 0x71, \
        'LLLA_PULLI'   : 0x72, 'LLA_PULLI'   : 0x73, \
        'RRA_PULLI'    : 0x74, 'NNNA_PULLI'  : 0x75, \
        'SA_PULLI'     : 0x76, 'JA_PULLI'    : 0x77, \
        'SSA_PULLI'    : 0x78, 'HA_PULLI'    : 0x79, \
        'KSSA_PULLI'   : 0x7A,                       \
                                                     \
        # THE VOWEL SIGN I WRITTEN INTO THE LETTER. this and the three    \
        # blocks after it are spread over the upper half and the bytes    \
        # below the space in no order, and hold only what this document   \
        # draws                                                           \
        'KA_I'         : 0xB0, 'CA_I'        : 0xA3, \
        'TTA_I'        : 0x80, 'TA_I'        : 0xDF, \
        'NA_I'         : 0xAE, 'PA_I'        : 0xA9, \
        'MA_I'         : 0x92, 'YA_I'        : 0xB4, \
        'RA_I'         : 0xA8, 'LA_I'        : 0x08, \
        'VA_I'         : 0xC6, 'LLLA_I'      : 0xD8, \
        'LLA_I'        : 0x04, 'RRA_I'       : 0xB1, \
        'NNNA_I'       : 0x06, 'JA_I'        : 0xA5, \
                                                     \
        # THE VOWEL SIGN II                                               \
        'KA_II'        : 0x05, 'CA_II'       : 0x09, \
        'TA_II'        : 0xE6, 'NA_II'       : 0xF8, \
        'PA_II'        : 0xBF, 'MA_II'       : 0xA1, \
        'YA_II'        : 0xAC, 'RA_II'       : 0x03, \
        'VA_II'        : 0x07,                       \
                                                     \
        # THE VOWEL SIGN U                                                \
        'KA_U'         : 0x9C, 'CA_U'        : 0x84, \
        'TTA_U'        : 0x8E, 'NNA_U'       : 0x8F, \
        'TA_U'         : 0x90, 'PA_U'        : 0x02, \
        'MA_U'         : 0xFF, 'YA_U'        : 0x98, \
        'RA_U'         : 0x87, 'LA_U'        : 0xA4, \
        'VA_U'         : 0x88, 'LLLA_U'      : 0x89, \
        'LLA_U'        : 0x93, 'RRA_U'       : 0x94, \
        'NNNA_U'       : 0x82,                       \
                                                     \
        # THE VOWEL SIGN UU                                               \
        'KA_UU'        : 0xB7, 'CA_UU'       : 0x8C, \
        'PA_UU'        : 0xC8, 'MA_UU'       : 0xCD, \
        'YA_UU'        : 0xCE, 'RA_UU'       : 0xCF, \
        'VA_UU'        : 0xD3,                       \
                                                     \
        # THE SIGNS THAT ARE GLYPHS OF THEIR OWN. aa, e, ee and ai are    \
        # drawn beside the letter, and uu stands on its own behind a      \
        # grantha letter, which takes no ligature of it - _¯u is ஜூன்      \
        'MATRA_AA'     : 0xD9,                       \
        'MATRA_E'      : 0x18, 'MATRA_EE'    : 0x1B, \
        'MATRA_AI'     : 0x1E,                       \
        'MATRA_UU'     : 0xAF,                       \
                                                     \
        # the two hyphens, 1D the one a document really writes and 2D the \
        # one PageMaker writes to break a word - see the class comment    \
        'DASH'         : 0x1D, 'SOFT_HYPHEN' : 0x2D, \
    }

    # the pdf names the glyphs of the ascii bytes and of A0..FF after the
    # characters latin 1 has there, so that is what an extractor hands
    # those out as
    encoding = 'latin-1'

    # the bytes whose glyph is named after a character latin 1 does not
    # put there: PDFDocEncoding's names on 18..9F, and the mac symbol ones -
    # lozenge, radical, infinity, product, lessequal, approxequal, notequal
    # and integral - on 02..09
    code_chars = { \
        0x02 : '◊', 0x03 : '√', 0x04 : '∞', \
        0x05 : '∏', 0x06 : '≤', 0x07 : '≈', \
        0x08 : '≠', 0x09 : '∫', \
        0x18 : '˘', 0x1b : '˙', 0x1d : '˛', \
        0x1e : '˚', \
        0x80 : '•', 0x82 : '‡', 0x84 : '—', \
        0x87 : '⁄', 0x88 : '‹', 0x89 : '›', \
        0x8c : '„', 0x8e : '”', 0x8f : '‘', \
        0x90 : '’', 0x92 : '™', 0x93 : 'ﬁ', \
        0x94 : 'ﬂ', 0x98 : 'Ÿ', 0x9c : 'œ', \
    }

    # no second character any glyph of this font reaches the converter as,
    # and the empty dict is what keeps tamelango's out
    glyph_aliases = {}

    def __init__(self):
        TamElango.__init__(self)

        # ௌ and ஔ, whose length mark this font draws with the glyph of ள -
        # see the class comment. They run after the jump like the rules of
        # ொ and ோ, the letter being between the ெ and the mark until then
        self.composeTokens[('MATRA_E', 'LLA')] = 'MATRA_AU'
        self.composeTokens[('O', 'LLA')]       = 'AU'

    def to_unicode(self, data):
        '''tamelango's passes, with the hyphen PageMaker writes to break a
           word dropped first: it is a glyph of no width and no character
           at all, and left in it would stand between a vowel sign and the
           letter it waits for'''
        tokentypes = self.tokenize(data)
        tokentypes = [t for t in tokentypes if t != 'SOFT_HYPHEN']

        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)
