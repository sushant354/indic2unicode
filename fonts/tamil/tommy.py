from .tamelango import TamElango

class Tommy(TamElango):
    '''The text of a pdf that is set in Sun-TommyTamilNormal, one of the
       tamil fonts of the Tamil Nadu gazette.

       It is an 8 bit font of the kind fonts/tamil/tamelango.py reads: every
       glyph of it sits on a byte, the pdf calls it a TrueType font with
       WinAnsiEncoding and names its glyphs after the latin characters that
       live on those bytes, so what an extractor hands out is cp1252 and not
       tamil at all - jkpo;ehL epy rPh;jpUj;jk; is
       தமிழ்நாடு நில சீர்திருத்தம்.

       THE LAYOUT IS THE TYPIST'S AND NOT THE SCRIPT'S

       Where TAM lays its glyphs out one block per row of what a tamil font
       needs, this font lays them out the way a typist reaches them, and the
       whole of the alphabet it needs in bulk is on the letter keys: the
       eighteen consonants but ஞ are on the lowercase ones, in among the
       vowel signs ா, ி, ெ and ை (0x68, 0x70, 0x6E, 0x69), and the shift of
       a key is the long form of what the key itself draws - the shift of a
       consonant is that letter with the vowel sign u written into it (f/F
       is க/கு), the shift of a vowel is the long vowel (m/M is அ/ஆ) and the
       shift of a vowel sign is the long sign (n/N is ெ/ே, p/P is ி/ீ). So
       the table is written out byte by byte, and the tokens are the ones
       langs/tamil.py defines.

       It differs from the TAM layout in what is one glyph as well as in
       where the glyphs sit. Only ட takes the vowel signs i and ii as a
       ligature here (0x62, 0x42); every other letter is written with the
       sign behind it, and so is every letter that carries a pulli, so this
       font needs a glyph for ண and one for ி rather than one for ணி, and
       the syllables of langs/tamil.Conjuncts are almost all absent from the
       table below.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       This is the same script drawn the same way tamelango's font draws it,
       so the reordering is inherited whole: the vowel signs e, ee and ai are
       drawn in front of the consonant they belong to and each of them waits
       for one token - ngah; is ெ ப ய ா ் and பெயர் - and the signs o and oo
       are drawn in two halves with the letter between them and are put back
       together by composeTokens once the front half has jumped - Nfhg;G is
       ே க ா ப ் பு and கோப்பு.

       The rules that read a ா carrying a pulli or a second vowel sign back
       as the ர it was typed for are inherited with them, and this document
       needs them everywhere rather than here and there: it writes ர with
       the ா it is drawn alike and then puts the sign that belongs on the ர
       behind it, all through - ghh;f;fTk; is ப ா ா ் க ் க வு ம ் and
       பார்க்கவும், gphpT is ப ி ா ி வு and பிரிவு.

       WHERE THE READINGS COME FROM

       This was built from one document. The pdf embeds a subset that keeps
       the font's whole cmap - 124 bytes of latin glyph names, which say
       nothing about what is drawn - but carries an outline for 63 of those
       bytes alone, so those 63 are everything the font itself says. Each of
       them was identified by rendering the outline the subset carries and
       reading it against a tesseract -l tam OCR of the words of the pages
       that draw it: 47 of them are tamil and are the readings below, and
       the other 16 draw themselves (the digits, and ( ) - . / :).

       Where the OCR and the page disagree the page is believed. This
       document abbreviates the rupee as ரு. and the OCR of every one of
       those lines reads ரூ. - the money the reader expects - which would
       have made 0x55 ரூ; the glyph it draws is ரு, and so is the glyph the
       page shows in ஏக்கருக்கு and in தருமபுரி, where the OCR agrees.

       Two of the words are a latin letter that a typist reached for without
       leaving the tamil font, and both are read as the syllable the page
       shows: the survey numbers 353/2B and 353/3A are 353/2டீ and 353/3யு,
       and the OCR reads that யு back as a latin u. 0x42 is drawn nowhere
       else in the document and 0x41 only in முகவரியும்.

       WHAT IS NOT KNOWN

       Eight bytes below are read off the run rather than off a glyph this
       document draws - ஈ, ஊ, ஓ and the u forms of ச, ண, ந, ழ and ன - each
       of them the shift of a key whose own reading is known and whose long
       form nothing else can be. The shift of a consonant is that letter
       with the sign u on it in all eleven of the keys that are drawn, and
       the shift of a vowel or of a vowel sign is the long one in all five.

       The rest is left out because nothing here says anything about it. ஞ
       is the one consonant that is on no lowercase key and no byte of this
       document draws it, so where it sits is unknown, and so is ஙு - one of
       the two has to be somewhere other than the shift of ங. ஐ, ஔ, ஃ, the
       grantha letters beyond ஜ and ஸ, ஸ்ரீ, the sign ௌ and the length mark
       it is drawn with, and a standalone ு or ூ are not drawn either. The
       document writes no ூ at all, and it writes the one ணு it needs in
       TAM_ELANGO_Panchali rather than in this font - fhµk; is காணும் and
       the µ of it is that font's byte for ணு, not this one's.

       A byte outside the table that is a character in its own right - the
       digits, the ascii punctuation - comes through as it is, and the rest
       is reported and dropped.
    '''
    # the byte each glyph of the font sits on. Only what needs decoding is
    # listed; a byte the font draws as itself (the digits, and ( ) - . / :)
    # reaches the output through the literal path of t_error, see
    # BaseFont.is_text_char
    glyphcodes = { \
        # VOWELS. அ, இ, உ, எ and ஒ sit on a key and the long vowel of each  \
        # on the shift of it, so ஈ, ஊ and ஓ are read off that pairing       \
        # rather than off a glyph this document draws                       \
        'A'            : 0x6D, 'AA'          : 0x4D, \
        'I'            : 0x2C, 'II'          : 0x3C, \
        'U'            : 0x63, 'UU'          : 0x43, \
        'E'            : 0x76, 'EE'          : 0x56, \
        'O'            : 0x78, 'OO'          : 0x58, \
                                                     \
        # CONSONANTS, each of them the letter with its inherent vowel a.    \
        # The eighteen of tamil are on the lowercase keys but for ஞ, which  \
        # is on none of them and which no byte of this document draws; ஜ    \
        # and ஸ are the two grantha letters it does draw                    \
        'KA'           : 0x66, 'NGA'         : 0x71, \
        'CA'           : 0x72,                       \
        'TTA'          : 0x6C, 'NNA'         : 0x7A, \
        'TA'           : 0x6A, 'NA'          : 0x65, \
        'PA'           : 0x67, 'MA'          : 0x6B, \
        'YA'           : 0x61, 'RA'          : 0x75, \
        'LA'           : 0x79, 'VA'          : 0x74, \
        'LLLA'         : 0x6F, 'LLA'         : 0x73, \
        'RRA'          : 0x77, 'NNNA'        : 0x64, \
        'SA'           : 0x5D, 'JA'          : 0x5B, \
                                                     \
        # THE VOWEL SIGN U WRITTEN INTO THE LETTER, on the shift of the     \
        # letter's own key. சு, ணு, நு, ழு and னு are read off that pairing \
        # rather than off a glyph this document draws                       \
        'KA_U'         : 0x46, 'CA_U'        : 0x52, \
        'TTA_U'        : 0x4C, 'NNA_U'       : 0x5A, \
        'TA_U'         : 0x4A, 'NA_U'        : 0x45, \
        'PA_U'         : 0x47, 'MA_U'        : 0x4B, \
        'YA_U'         : 0x41, 'RA_U'        : 0x55, \
        'LA_U'         : 0x59, 'VA_U'        : 0x54, \
        'LLLA_U'       : 0x4F, 'LLA_U'       : 0x53, \
        'RRA_U'        : 0x57, 'NNNA_U'      : 0x44, \
                                                     \
        # ட WITH THE VOWEL SIGN I AND WITH II, the one letter of this font  \
        # that takes either of them as a ligature                           \
        'TTA_I'        : 0x62, 'TTA_II'      : 0x42, \
                                                     \
        # THE SIGNS. every letter but ட is written with the sign behind it  \
        # rather than into it, so these do the work the pulli forms and the \
        # i, ii, u and uu forms of a TAM font do                            \
        'PULLI'        : 0x3B,                       \
        'MATRA_AA'     : 0x68, 'MATRA_I'     : 0x70, \
        'MATRA_II'     : 0x50,                       \
        'MATRA_E'      : 0x6E, 'MATRA_EE'    : 0x4E, \
        'MATRA_AI'     : 0x69,                       \
                                                     \
        # the one piece of punctuation of the font that does not come out   \
        # of the pdf as itself: இ is on the comma key, so the comma is on   \
        # the shift of it                                                   \
        'COMMA'        : 0x3E,                       \
    }

    # no second character any glyph of this font reaches the converter as.
    # fonts/tamil/tamelango.py has one because a producer writes the byte
    # its font draws ணு on, the micro sign, as the greek mu that unicode
    # normalises it to; every byte of this font is ascii and an extractor
    # hands each of them out as itself. The empty dict is the point - it is
    # what keeps the inherited one out
    glyph_aliases = {}
