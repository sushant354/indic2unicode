from .tamelango import TamElango

class Vanavil(TamElango):
    '''The text of a pdf that is set in VANAVILAvvaiyar, the tamil font of
       the Vanavil typing package - 541 of the 8,248 documents of the Tamil
       Nadu gazette corpus draw 443,414 words in it, which is more than any
       font of that corpus but TAM_ELANGO_Panchali and TAUElangoPanchali -
       and in the rest of the VANAVIL family, which share its encoding
       (VANAVILAvvaiyarBold, VANAVIL-Avvaiyar, VANAVILDBAvvaiyarBold,
       VANAVILAlayarasi).

       It is an 8 bit font of the same kind fonts/tamil/tamelango.py reads:
       every glyph of it sits on a byte, the pdf calls it a TrueType font
       with WinAnsiEncoding and names its glyphs after the latin characters
       that live on those bytes, so what an extractor hands out is cp1252
       and not tamil at all - jäœehL r£lk‹w¥ nguitæ‹ is
       தமிழ்நாடு சட்டமன்றப் பேரவையின். A document that carries the font a
       second time as a CID font names its glyphs in a ToUnicode map of its
       own, and those maps hand out the very same cp1252 characters, so both
       embeddings reach this converter alike.

       THE LAYOUT IS THE TYPIST'S AND NOT THE SCRIPT'S

       It needs a glyph for what any tamil font needs one for - the vowels
       and the aytham, the letters, each letter with a pulli on it, each of
       them with the vowel sign i, ii, u or uu written into it, and the
       signs that are drawn beside the letter rather than into it - but
       where TAM lays those out one block per line of that list, this font
       lays them out the way a typist reaches them: the commonest letters
       sit on the lowercase keys, in among the vowel signs aa, e, ee and ai
       (0x68, 0x62, 0x6E, 0x69), and everything else is spread over the
       capitals and the upper half in no order this table could be
       generated from. Only the vowel sign i has a run of its own worth the
       name, ணி..ஹி over 0xE2..0xEF. So the table is written out byte by
       byte, and the tokens are the ones langs/tamil.py defines.

       Every reading in it was established from the font itself: the glyphs
       were rendered out of the embedded subsets of 400 documents of the
       corpus - no one document carries them all, the readings here being
       the union over those - and identified against the same syllable drawn
       by TAM_ELANGO_Panchali, whose byte each glyph sits on
       fonts/tamil/tamelango.py already names, with a tesseract -l tam pass
       over the pages and the words of the documents themselves as the check.

       ONLY A SUBSET WHOSE FONT NAME STARTS WITH VANAVIL MAY BE READ

       The Vanavil faces are cut in three layouts and a font of the other
       two says so by putting the layout in front of the face -
       TAMVANAVILAvvaiyar and TAM-VANAVIL-Avvaiyar are the TAM layout that
       fonts/tamil/tamelango.py reads, TABVanavilAvvaiyar is the TAB one
       that nothing here reads - so a caller matching a pdf font name
       against this converter has to hold the name to one that *starts*
       with the family, and so does anything reading glyphs out of a corpus
       to build a table like this one. Both layouts draw the same typeface,
       so a subset of one is indistinguishable from a subset of the other
       by anything but the name it is filed under, and a table built from
       the two mixed together comes out right for the bytes the documents
       actually use in bulk and quietly wrong for the rest: it was 0xEC as
       ட rather than ஸி, 0xF5 as வ rather than ஷ, 0xA8 as ூ rather than ி
       and 0xAC as ை rather than ீ, every one of them a real tamil letter,
       so the decoded text read perfectly well and said nothing. What
       caught it was a page of a document that spells its syllables out -
       fy¨a}h¦ - read against the pdf itself.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       This is the same script drawn the same way tamelango's font draws it,
       so the reordering is inherited whole: the vowel signs e, ee and ai
       are drawn in front of the consonant they belong to and each of them
       waits for one token - nguitæ‹ is ே ப ர ை வ யி ன் and பேரவையின் - and
       the signs o and oo are drawn in two halves with the letter between
       them and are put back together by composeTokens once the front half
       has jumped - bghJ is ெ ப ா து and பொது. The rules that read a ா
       carrying a pulli or a second vowel sign back as the ர it was typed
       for are inherited with them, and the documents here need them just as
       the TAM ones do, though far more rarely: fy¨a}h¦ is
       க ல ி ய னூ ா ் and கலியனூர்.

       What this font needs beside that is waitover. It draws the pulli and
       the four signs that are otherwise written into a letter as glyphs of
       their own as well, for the letters it has no single glyph for and for
       a document that spells a syllable out rather than typing it as one
       key - ehkf¦fy¦ is ந ா ம க ் க ல ் - so a vowel sign that is still
       waiting to jump has to stay behind those rather than count them and
       land between a letter and its own mark.

       ூ TYPED AS ு AND ா

       These documents write the sign uu as the sign u and a ா, which is
       very nearly the shape the font draws it in, and the page really does
       show that pair rather than the one glyph: ntYh® is ே வ லு ா ர் and
       the place it names is வேலூர். The letter and its u are a single
       glyph here, so what has to be read back is that syllable and the ா
       behind it rather than two signs, which is why __init__ generates a
       rule per letter the font draws a u form of rather than the one rule
       the signs would need. It is the same kind of habit the inherited ர
       rules answer and it is safe for the same reason: a vowel sign can no
       more be followed by a second vowel sign than it can carry a pulli.
       Measured over 278,297 words of 250 documents it puts 159 of them
       right and leaves 26 words carrying two signs, every one of which is
       a stray mark the document itself types (வாாடு, திங்்கள்).

       WHAT IS NOT KNOWN

       The font draws 181 glyphs in those 400 documents and nothing says
       what the rest of it draws, so the syllables no document writes are
       not in the table: ஙி, ஙீ, ஙு, ஙூ and the same four of ஞ - the two
       letters tamil almost only ever writes with a pulli - ழீ and ழூ, ஸீ,
       the grantha letters with the signs u and uu, and க்ஷ with any sign
       at all. ஔ and the vowel sign ௌ are not in it either, and for the
       reason fonts/tamil/tamelango.py has neither: a font of this kind
       draws them out of a ெ and a length mark of its own, and no document
       of the corpus draws that mark.

       0x42 is left out for a different reason: it *is* drawn, and it draws
       a க and a ஷ ligated with no pulli on the க - which is the க்ஷ glyph
       of 0xBA with the pulli taken off, and so is not க்ஷ, that syllable
       being spelled with one. Nothing says what it is instead: the only
       two words of 400 documents that use the byte are 363/1B and EB,
       where a typist reached for a latin B without leaving the tamil font
       and the page shows the ligature. So the byte comes through as the B
       it was typed as, which is what those two words mean, and a document
       that really wanted the glyph shows a B in the middle of its tamil
       rather than quietly reading as some other syllable.

       A byte outside the table that is a character in its own right - the
       digits, the ascii punctuation, the quotes at 0x91..0x94 - comes
       through as it is, and the rest is reported and dropped.
    '''
    # the byte each glyph of the font sits on. Only what needs decoding is
    # listed; a byte the font draws as itself (the digits, the ascii
    # punctuation, the quotes at 0x91..0x94) reaches the output through the
    # literal path of t_error, see BaseFont.is_text_char
    glyphcodes = { \
        # VOWELS and the aytham. No byte of these documents draws ஔ,      \
        # which is why there is none here - see the class comment          \
        'A'            : 0x6D, 'AA'          : 0x4D, \
        'I'            : 0xCF, 'II'          : 0x3C, \
        'U'            : 0x63, 'UU'          : 0x43, \
        'E'            : 0x76, 'EE'          : 0x56, \
        'AI'           : 0x49,                       \
        'O'            : 0x78, 'OO'          : 0x58, \
        'AYTHAM'       : 0x7E,                       \
                                                     \
        # CONSONANTS, each of them the letter with its inherent vowel a.   \
        # The eighteen of tamil are all on the lowercase keys but for ழ    \
        # and ங, and the grantha five are scattered over what is left      \
        'KA'           : 0x66, 'NGA'         : 0x87, \
        'CA'           : 0x72, 'NYA'         : 0x50, \
        'TTA'          : 0x6C, 'NNA'         : 0x7A, \
        'TA'           : 0x6A, 'NA'          : 0x65, \
        'PA'           : 0x67, 'MA'          : 0x6B, \
        'YA'           : 0x61, 'RA'          : 0x75, \
        'LA'           : 0x79, 'VA'          : 0x74, \
        'LLLA'         : 0x48, 'LLA'         : 0x73, \
        'RRA'          : 0x77, 'NNNA'        : 0x64, \
        'SA'           : 0x5B, 'SSA'         : 0xF5, \
        'JA'           : 0x23, 'HA'          : 0x41, \
        'KSSA'         : 0xBA, 'SHRI'        : 0x24, \
                                                     \
        # THE PULLI FORMS. the letter with a pulli on it, i.e. carrying    \
        # no vowel. Every letter of the script but க்ஷ has one here, which \
        # no other row of this table can say                              \
        'KA_PULLI'     : 0xA1, 'NGA_PULLI'   : 0xA7, \
        'CA_PULLI'     : 0xA2, 'NYA_PULLI'   : 0x8A, \
        'TTA_PULLI'    : 0xA3, 'NNA_PULLI'   : 0xA9, \
        'TA_PULLI'     : 0xA4, 'NA_PULLI'    : 0xAA, \
        'PA_PULLI'     : 0xA5, 'MA_PULLI'    : 0xAB, \
        'YA_PULLI'     : 0x8C, 'RA_PULLI'    : 0xAE, \
        'LA_PULLI'     : 0x9A, 'VA_PULLI'    : 0x9B, \
        'LLLA_PULLI'   : 0x9C, 'LLA_PULLI'   : 0x9F, \
        'RRA_PULLI'    : 0x89, 'NNNA_PULLI'  : 0x8B, \
        'SA_PULLI'     : 0xB0, 'SSA_PULLI'   : 0x5A, \
        'JA_PULLI'     : 0x7B, 'HA_PULLI'    : 0xC0, \
                                                     \
        # THE VOWEL SIGN I WRITTEN INTO THE LETTER. ணி..ஹி run unbroken    \
        # over 0xE2..0xEF and the other six sit where they fit             \
        'KA_I'         : 0xBB, 'CA_I'        : 0xC1, \
        'TTA_I'        : 0x6F, 'NNA_I'       : 0xE2, \
        'TA_I'         : 0xC2, 'NA_I'        : 0xE3, \
        'PA_I'         : 0xC3, 'MA_I'        : 0xE4, \
        'YA_I'         : 0xE6, 'RA_I'        : 0xE7, \
        'LA_I'         : 0xE8, 'VA_I'        : 0xE9, \
        'LLLA_I'       : 0xEA, 'LLA_I'       : 0xEB, \
        'RRA_I'        : 0xBF, 'NNNA_I'      : 0xE5, \
        'SA_I'         : 0xEC, 'SSA_I'       : 0xEE, \
        'JA_I'         : 0xED, 'HA_I'        : 0xEF, \
                                                     \
        # THE VOWEL SIGN II                                               \
        'KA_II'        : 0xD1, 'CA_II'       : 0xD3, \
        'TTA_II'       : 0x4F, 'NNA_II'      : 0xD9, \
        'TA_II'        : 0xD4, 'NA_II'       : 0xDA, \
        'PA_II'        : 0xD5, 'MA_II'       : 0xDB, \
        'YA_II'        : 0x70, 'RA_II'       : 0xDF, \
        'LA_II'        : 0xC4, 'VA_II'       : 0xC5, \
        'LLA_II'       : 0xC7, 'RRA_II'      : 0xD6, \
        'NNNA_II'      : 0xDC, 'SSA_II'      : 0xCA, \
        'JA_II'        : 0xC9, 'HA_II'       : 0xCB, \
                                                     \
        # THE VOWEL SIGN U                                                \
        'KA_U'         : 0x46, 'CA_U'        : 0x52, \
        'TTA_U'        : 0x4C, 'NNA_U'       : 0x51, \
        'TA_U'         : 0x4A, 'NA_U'        : 0x45, \
        'PA_U'         : 0xF2, 'MA_U'        : 0x4B, \
        'YA_U'         : 0xCD, 'RA_U'        : 0x55, \
        'LA_U'         : 0x59, 'VA_U'        : 0xCE, \
        'LLLA_U'       : 0x47, 'LLA_U'       : 0x53, \
        'RRA_U'        : 0x57, 'NNNA_U'      : 0x44, \
                                                     \
        # THE VOWEL SIGN UU                                               \
        'KA_UU'        : 0x54, 'CA_UU'       : 0x4E, \
        'TTA_UU'       : 0x5E, 'NNA_UU'      : 0xFB, \
        'TA_UU'        : 0xF6, 'NA_UU'       : 0xFC, \
        'PA_UU'        : 0xF3, 'MA_UU'       : 0x5F, \
        'YA_UU'        : 0xF4, 'RA_UU'       : 0x25, \
        'LA_UU'        : 0xFF, 'VA_UU'       : 0xF1, \
        'LLA_UU'       : 0x71, 'RRA_UU'      : 0xF9, \
        'NNNA_UU'      : 0x7D,                       \
                                                     \
        # THE SIGNS THAT ARE GLYPHS OF THEIR OWN. the pulli and the four   \
        # signs the font otherwise writes into a letter are here for the   \
        # letters it draws no single glyph for and for a document that     \
        # spells a syllable out rather than typing it as one key. aa, e,   \
        # ee and ai are drawn beside the letter by every font and are      \
        # always these                                                    \
        'PULLI'        : 0xA6,                       \
        'MATRA_AA'     : 0x68, 'MATRA_I'     : 0xA8, \
        'MATRA_II'     : 0xAC, 'MATRA_U'     : 0x26, \
        'MATRA_UU'     : 0x5D,                       \
        'MATRA_E'      : 0x62, 'MATRA_EE'    : 0x6E, \
        'MATRA_AI'     : 0x69,                       \
                                                     \
        # the one piece of punctuation of the font that does not come out  \
        # of the pdf as itself: the byte the grave accent lives on draws   \
        # an opening quote                                                \
        'LSQUOTE'      : 0x60,                       \
    }

    # no second character any glyph of this font reaches the converter as.
    # fonts/tamil/tamelango.py has one because a producer writes the byte
    # its font draws ணு on, the micro sign, as the greek mu that unicode
    # normalises it to; this font draws ணு on 0x51 and nothing on 0xB5, so
    # that alias would be a rule for a byte the table does not have. The
    # empty dict is the point - it is what keeps the inherited one out
    glyph_aliases = {}

    # the marks that belong to the letter in front of them, which a vowel
    # sign that is waiting to jump has to stay behind rather than count
    trailing_signs = ('PULLI', 'MATRA_I', 'MATRA_II', 'MATRA_U', 'MATRA_UU')

    def __init__(self):
        TamElango.__init__(self)

        self.waitover = set(self.trailing_signs)

        # ூ typed as ு and a ா - see the class comment. One rule per
        # letter the font draws a u form of, and MATRA_U for the syllable
        # a document spells out; generated rather than listed, there being
        # nothing to say about any one of them
        for tokenName in list(self.glyphcodes):
            if tokenName.endswith('_U'):
                self.composeTokens[(tokenName, 'MATRA_AA')] = tokenName + 'U'
