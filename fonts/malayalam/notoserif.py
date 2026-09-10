import re
import types

from indic2unicode.langs import malayalam
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class NotoSerifMalayalam(BaseFont):
    '''Noto Serif Malayalam is the unicode malayalam of Google's Noto family,
       and the pdfs of the Kerala Gazette that are set in it carry the same
       kind of broken ToUnicode map as the ones that are set in Kartika: the
       map was built by pairing the glyphs of a run with the characters of
       that run one by one, and malayalam draws a syllable in a different
       number of glyphs than it is written in, so the pairing slips on every
       glyph that shaping moved or made. The text that comes out of such a
       pdf is therefore malayalam that is

       1. in the visual order of the glyphs and not in the order of unicode,
          so െ, േ and ൈ sit in front of the letter they belong to and the
          ്ര of a cluster in front of the whole of it, and

       2. spelled with the wrong characters wherever the pairing slipped:
          'ക' is the vowel sign േ and 'േ' is the letter ക, 'ല' is the sign
          െ and 'െ' is the letter ല, 'ക്ക' is the sign ൈ as well as the
          cluster ക്ക, and 'പ്' is the ്ര that is drawn in front of its
          letter.

       So the text is treated like any other font of this package: every
       glyph of the font is a token, the token is given the unicode string
       it really stands for and the tokens are put back in the order that
       unicode wants. കേരള comes out of the pdf as itself, the swapped ക
       and േ cancelling out, but പ്രകാരം comes out as പ്പോരം, വകുപ്പ് as
       വേുപ്പ്, പുറപ്പെടുവിച്ച as പുറലപ്പടുവിച്ച and ചെയർമാൻ as ലെയർമാൻ.

       WHERE THE READINGS COME FROM

       The pdf embeds the font as a subset that keeps both its cmap and its
       GSUB, so what every glyph of it draws is in the document itself. The
       cmap maps 76 characters to the glyph that draws each of them - the
       letters, the vowel signs, the chandrakkala and the anusvara - and the
       ligature lookups of the GSUB name the rest: the chillus and the
       clusters the font draws as one glyph (akhn), the ്ര that is drawn in
       front of its letter (pref) and the ്യ and ്വ that are drawn behind it
       (pstf). The one glyph neither names is the dotted circle, which the
       post table calls uni25CC. Every glyph the document draws was read
       that way, and the readings were checked in the words they stand in
       against a tesseract -l mal ocr of the first 30 pages.

       Every dead consonant is drawn as the letter and a visible
       chandrakkala, two glyphs that the map spells as the letter and a
       virama, so none of them is named below - they are read by the letter
       and the VIRAMA of it.

       WHAT IS LOST, AND WHAT THE TEXT AROUND A GLYPH BRINGS BACK

       The map cannot be inverted completely, and what is lost is what two
       glyphs of the subset were handed the same string for. The counts
       below are the glyphs of the 262 pages of the test document. Where the
       document itself says which of the two a string is, the rule is in
       glyphpatterns or in preComposeTokens below and is this:

       * 'െ' is ല, ച and ന്റ - 5,082, 1,164 and 133. ച is the letter of the
         three that begins a word, and it does so behind a chillu or an
         anusvara as well where two words are written as one; behind a െ
         or a േ the letter that the syllable ends on says which: a ചെ or a
         ചേ that another letter follows, as in ചെയർമാൻ and ചേർത്ത, and a
         ലെ at the end of a word, as in 1994-ലെ and ജില്ലയിലെ. That reads
         1,124 of the ച and costs 27 ല, ലഭിച്ച and ലക്ഷം being the two words
         held back from it. The ന്റ of ന്റെ ends a word exactly the way the
         ല of ലെ does and so only 41 of the 133 are read: behind a ട -
         വീടിന്റെ, തോടിന്റെ, which no ടിലെ of the document is - in front of
         a ഷ - പ്ലാന്റേഷൻ - and in സെന്റ്. റോഡിന്റെ comes out as റോഡിലെ,
         റോഡിലെ being a word of the document as often.

       * 'േ' is ക, ക്ഷ, ശ്ശ, സ്റ്റ, ദ്ദ and ഥ - 8,474, 255, 222, 221, 168 and
         21. Nothing but the word tells these apart, so the clusters are
         read in the words the gazette writes them in: ക്ഷ in ആക്ഷേപം,
         ക്ഷേത്രം and ലക്ഷം, ദ്ദ in നിർദ്ദേശം, തദ്ദേശ and ഉദ്ദേശം, ശ്ശ in
         the ശ്ശേരി of a place name and സ്റ്റ in സ്റ്റേഷൻ, സ്റ്റേഡിയം,
         എസ്റ്റേറ്റ്, പോസ്റ്റോഫീസ് and at the end of a word, where ക് is an
         english word's ending - ട്രാഫിക് - and സ്റ്റ് a far commoner one:
         പോസ്റ്റ്, ഫോറസ്റ്റ്, ഈസ്റ്റ്. That reads 245 of the ക്ഷ, all 168 ദ്ദ,
         197 ശ്ശ and 185 സ്റ്റ, and misreads 9 ക. ഥ is not read at all -
         ഗുരുനാഥൻ comes out as ഗുരുനാകൻ.

       * 'ക്ക' is the cluster ക്ക and the sign ൈ - 6,498 against 382. No
         word begins with ക്ക, so a 'ക്ക' that no malayalam character stands
         in front of is ൈ: 354 of them, at the cost of 5 ക്ക where a word
         of the pdf was broken in two. The 28 left are inside a word -
         പൂക്കൈത comes out as പൂക്കക്കത.

       * 'പ്' is the sign ്ര and the dead പ് - 1,975 against 7 - and is read
         as the sign wherever a letter follows it. 'പ്പ' is then both the
         cluster പ്പ and a ്ര in front of a പ - 2,527 against 842. No word
         begins with പ്പ and few end in it, so a 'പ്പ' at either end of a
         word is the ്ര and the പ, and so is one behind അ - അപ്രകാരം - and
         in അഭിപ്രായം and in the പ്രം that ends a place name. That reads 1,916
         of the ്ര and costs 22 പ്പ; മേപ്രാൽ comes out as മേപ്പാൽ.

       * 'ല' is the sign െ and the cluster ബ്ല - 6,428 against 60. A sign
         never follows another sign, and െ is never followed by a vowel
         sign, so a 'ല' behind the 'ക' of േ, or in front of a vowel sign, is
         ബ്ല - ബ്ലോക്ക്, പബ്ലിക്, പി.ഡബ്ല്യൂ.ഡി: 59 of the 60.

       * 'യ' is the letter യ and the sign ്യ - 5,488 against 251 - and 'വ'
         is the letter വ, the sign ്വ and the cluster വ്വ - 8,366, 158 and
         50. The signs are read behind the letters that this document never
         writes a bare യ or വ behind - ഖ്യ, ഗ്യ, ഷ്യ and the like, and സ്വ -
         and in അന്വേഷണം and the ശ്വര of ഈശ്വരൻ. That is 122 of the ്യ and
         127 of the ്വ at the cost of 3 യ; വാര്യാപുരം comes out as
         വാരയാപുരം, the ര being a letter a bare യ follows a dozen times as
         often. വ്വ is lost outright, the gazette spelling the one word it
         is drawn in both ways - റിസർവ്വ് 43 times and റിസർവ് 33.

       * 'ാ' is ാ and the dotted circle - 18,574 against 257. The ordinal
         ending -ാം is typed without a letter for its signs to sit on, so the
         shaper draws a dotted circle in front of each of them and 10-ാം comes
         out of the pdf as 10-ാാാം. A 'ാ' that begins a word in front of a
         sign, and one behind a ാ in front of ം, is the circle, which is no
         character of the text and is dropped: 253 of the 257.

       * 'സ്' is the dead സ് and the cluster സ്ല - 1,043 against 8 - the
         string of the one being the letter and the chandrakkala of the
         other. A dead consonant is never followed by a vowel sign, so a
         'സ്' that is is സ്ല - മുസ്ലീം.

       And what nothing brings back is ങ and ഗ്ഗ, one drawing each, which are
       read as ര and ഗ.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       The vowel signs െ, േ and ൈ are drawn in front of the letter they
       belong to and unicode writes them behind it, so each of them waits
       for one token. A cluster is one token here however many letters it is
       written out of, which is what makes the wait a one rather than a
       count of letters. Where the font draws a cluster as a dead consonant
       and a letter rather than as one glyph the sign is drawn between the
       two, behind the chandrakkala - സ്നേഹ is drawn സ ് േ ന ഹ - so the one
       token is the right wait there too.

       ൊ, ോ and ൌ are drawn in two halves with the letter between them, so
       they arrive as a െ or a േ in front and a ാ or a ൗ behind and are put
       back together by composeTokens once the front half has jumped -
       ഹൗസ് is typed with ൌ and drawn െ ഹ ൗ സ ്.

       ്ര is drawn in front of its letter as well, and inside whatever vowel
       sign is drawn there, so a sign and the ്ര of the same syllable are
       swapped by preComposeTokens before either jumps - unicode writes the
       ്ര first and the jump emits what was waiting longest first. ്യ and ്വ
       are drawn behind the letter they are bound to, so a vowel sign that
       is on its way past that letter has not passed the syllable until it
       has passed them as well.

       THE OTHER FACES

       The masthead of the gazette is set in a subset of Kartika-Bold, with
       a map of its own that was broken over its own first drawings, and a
       line of each issue is in Meera. Their text reaches this converter in
       the same string as the rest and cannot be told apart in it, so it
       comes out wrong - കേരള ഗസറ്റ് comes out of the pdf as േകരള ഗസറ്
       and is converted as കരേള ഗസറ്. They draw 144 glyphs of the test
       document against this font's 323,955.

       WHAT THIS WAS CHECKED AGAINST

       The pdf's own glyphs first. Every glyph the document draws was read
       off the embedded subset as above, and the text those readings make
       is the yardstick: of the 39,110 malayalam words of the document, this
       pass produces 38,524 (98.5 per cent) exactly as the glyphs say they
       were drawn, and what is left is the readings listed above as lost.

       And a tesseract -l mal ocr of the first 30 pages: of the 4,156
       malayalam words this pass produces over them, 3,787 (91.1 per cent)
       match the ocr of their own page character for character once the
       chillus and ന്റ are spelled alike on both sides. The text that the
       glyphs themselves make matches it 91.8 per cent of the time, the rest
       being the ocr's own misreadings - it reads ഒപ്പ് as ഒപ്പ, turns the
       -ാം of 10-ാം into digits and loses the chandrakkala of തെക്ക്.
    '''
    # the string the pdf hands each glyph of the font, against the token
    # that glyph really draws. Only what needs decoding is listed - a
    # character the font draws as itself (the latin of the document, the
    # digits, the punctuation) reaches the output through the literal path
    # of t_error, see BaseFont.is_text_char - and a dead consonant, which
    # comes through as its letter and a chandrakkala, is read by the two
    # tokens of it
    glyphstrings = { \
        # VOWELS. ഋ and the malayalam digits the document never draws      \
        'A'    : 'അ', 'AA'   : 'ആ', 'I'    : 'ഇ', 'II'   : 'ഈ', \
        'U'    : 'ഉ', 'UU'   : 'ഊ', 'E'    : 'എ', 'EE'   : 'ഏ', \
        'AI'   : 'ഐ', 'O'    : 'ഒ', 'OO'   : 'ഓ', 'AU'   : 'ഔ', \
                                                              \
        # CONSONANTS. ച and ല are read by a pattern below, both of them    \
        # sharing their string with ന്റ                                     \
        'KA'   : 'േ', 'KHA'  : 'ഖ', 'GA'   : 'ഗ', 'JA'   : 'ജ', \
        'NYA'  : 'ഞ', 'TTA'  : 'ട', 'TTHA' : 'ഠ', 'DDA'  : 'ഡ', \
        'NNA'  : 'ണ', 'TA'   : 'ത', 'DA'   : 'ദ', 'DHA'  : 'ധ', \
        'NA'   : 'ന', 'PA'   : 'പ', 'PHA'  : 'ഫ', 'BA'   : 'ബ', \
        'BHA'  : 'ഭ', 'MA'   : 'മ', 'YA'   : 'യ', 'RA'   : 'ര', \
        'RRA'  : 'റ', 'LLA'  : 'ള', 'LLLA' : 'ഴ', 'VA'   : 'വ', \
        'SHA'  : 'ശ', 'SSA'  : 'ഷ', 'SA'   : 'സ', 'HA'   : 'ഹ', \
                                                              \
        # THE CHILLUS. the letters that end a syllable with no vowel, each \
        # of them a character of its own - see langs/malayalam.py          \
        'CHILLU_NN' : 'ൺ', 'CHILLU_N'  : 'ൻ', 'CHILLU_RR' : 'ർ', \
        'CHILLU_L'  : 'ൽ', 'CHILLU_LL' : 'ൾ', 'CHILLU_K'  : 'ൿ', \
                                                                \
        # THE SIGNS. the vowel signs, the chandrakkala and the anusvara.   \
        # ൈ and ്ര are read by a pattern below, and ്യ and ്വ by the rules  \
        # of preComposeTokens, each of them sharing its string with a      \
        # glyph that is a letter                                           \
        'MATRA_AA' : 'ാ', 'MATRA_I'  : 'ി', 'MATRA_II' : 'ീ', \
        'MATRA_U'  : 'ു', 'MATRA_UU' : 'ൂ', \
        'MATRA_VOCALIC_R' : 'ൃ', \
        'MATRA_E'  : 'ല', 'MATRA_EE' : 'ക', \
        'VIRAMA'   : '്', 'ANUSVARA' : 'ം', 'AU_LENGTH_MARK' : 'ൌ', \
                                                                  \
        # THE CLUSTERS THE FONT DRAWS AS ONE GLYPH. A cluster that is not  \
        # here the font draws as a dead consonant and a letter, which      \
        # needs no glyph of its own. The ones whose string is a letter's   \
        # or a sign's are read by a pattern below                          \
        'KA_KA'   : 'ക്ക',  'KA_TTA'  : 'ക്ട',  'KA_TA'   : 'ക്ത',  \
        'KA_LA'   : 'ക്ല',  'GA_LA'   : 'ഗ്ല',  'NGA_KA'  : 'ങ്ക',  \
        'NGA_NGA' : 'ങ്ങ',  'CA_CA'   : 'ച്ച',  'JA_JA'   : 'ജ്ജ',  \
        'JA_NYA'  : 'ജ്ഞ',  'NYA_CA'  : 'ഞ്ച',  'NYA_JA'  : 'ഞ്ജ',  \
        'NYA_NYA' : 'ഞ്ഞ',  'TTA_TTA' : 'ട്ട',  'NNA_TTA' : 'ണ്ട',  \
        'NNA_DDA' : 'ണ്ഡ',  'NNA_NNA' : 'ണ്ണ',  'TA_TA'   : 'ത്ത',  \
        'TA_NA'   : 'ത്ന',  'TA_MA'   : 'ത്മ',  'DA_DHA'  : 'ദ്ധ',  \
        'NA_TA'   : 'ന്ത',  'NA_DA'   : 'ന്ദ',  'NA_DHA'  : 'ന്ധ',  \
        'NA_NA'   : 'ന്ന',  'NA_MA'   : 'ന്മ',  'PA_PA'   : 'പ്പ',  \
        'PA_LA'   : 'പ്ല',  'PHA_LA'  : 'ഫ്ല',  'BA_BA'   : 'ബ്ബ',  \
        'MA_PA'   : 'മ്പ',  'MA_MA'   : 'മ്മ',  'MA_LA'   : 'മ്ല',  \
        'YA_YA'   : 'യ്യ',  'RRA_RRA' : 'റ്റ',  'LA_PA'   : 'ല്പ',  \
        'LA_LA'   : 'ല്ല',  'LLA_LLA' : 'ള്ള',  'SHA_CA'  : 'ശ്ച',  \
        'SA_THA'  : 'സ്ഥ',  'SA_SA'   : 'സ്സ',  'HA_NA'   : 'ഹ്ന',  \
    }

    # the glyphs whose string another glyph of the same subset is handed as
    # well, and that the text around them tells apart. Each of these is a
    # regular expression rather than a string and stands in glyphstrings'
    # place. ply orders its rules by falling length and takes the first one
    # that matches, so a pattern is always tried before a bare string - the
    # one it competes with, but also any longer one it is the start of,
    # which is why the patterns for ല and പ് look past the chandrakkala of
    # ല്ല and of പ്ല. See the class comment for what each of them brings
    # back and what it costs
    glyphpatterns = { \
        # ച begins a word, on its own or behind a chillu or an anusvara,   \
        # and it is the letter a ചെ or a ചേ that another letter follows    \
        # ends on. ലഭിച്ച and ലക്ഷം begin with the ല that shares its string  \
        'CA'      : '(?<![ഀ-ൿ])െ(?!ഭ|േ[ം്])|(?<=[ൺ-ൿം])െ' \
                    '|(?<=ല)(?<!്ല)െ(?=[യറങടമനകലളപ])' \
                    '|(?<=ക)(?<!്ക)െ(?=[ർനരറ])', \
        'NA_RRA'  : '(?<=ടില)(?<!്ടില)െ(?![ഀ-ൿ])|(?<=ക)(?<!്ക)െ(?=ഷ)' \
                    '|(?<=ലസ)െ(?=്)', \
        'LA'      : 'െ', \
                         \
        # the clusters that share their string with ക, in the words the   \
        # gazette writes them in - ആക്ഷേപം, ക്ഷേത്രം, ലക്ഷം; നിർദ്ദേശം,    \
        # തദ്ദേശ, ഉദ്ദേശം; -ശ്ശേരി; സ്റ്റേഷൻ, സ്റ്റേഡിയം, എസ്റ്റേറ്റ്,       \
        # പോസ്റ്റോഫീസ് and a സ്റ്റ് that ends a word                        \
        'KA_SSA'  : '(?<=ആക)േ(?=പ)|(?<=ക)േ(?=പ്ത)|(?<=െ)േ(?=[ം്])', \
        'DA_DA'   : '(?<=ർക)േ|(?<=[തഉ]ക)േ(?=ശ)', \
        'SHA_SHA' : '(?<=ക)േ(?=രി)', \
        'SA_RRA_RRA' : '(?<![ിും])േ(?=്(?![ഀ-ൿ]))|(?<=ക)േ(?=റ്റ|[ഡഷ])' \
                       '|(?<=കപാക)േ(?=ാഫ)|(?<=കപാ)േ(?=ാഫ)', \
                                                          \
        # ബ്ല stands where the sign െ cannot - behind the sign േ, or in    \
        # front of a vowel sign                                            \
        'BA_LA'   : '(?<=ക)(?<!്ക)ല(?!്)|ല(?=യ?[ി-ൃ])', \
                                                        \
        # no word begins with the cluster ക്ക                              \
        'MATRA_AI' : '(?<![ഀ-ൿ])ക്ക', \
                                     \
        # the dotted circles of -ാം, typed with no letter to sit on         \
        'DOTTED_CIRCLE' : '(?<![ഀ-ൿ])ാ(?=[ാ-ൃം്])|(?<=ാ)ാ(?=ം)', \
                                                               \
        # ്ര wherever a letter follows it, and a ്ര and a പ rather than     \
        # the cluster പ്പ at either end of a word, behind അ, in അഭിപ്രായം  \
        # and in the പ്രം that ends a place name                           \
        'RA_SIGN' : '(?<![ഀ-ൿ])പ്(?=പ)|(?<=[ഀ-ൿ])പ്(?=പ(?![ഀ-ൿ]))' \
                    '|(?<=അ)പ്(?=പ)|(?<=അഭി)പ്(?=പ)' \
                    '|(?<=[ിൂ])പ്(?=പം(?![ഀ-ൿ]))' \
                    '|പ്(?=[ക-ഹേെ])(?![പല])', \
                                              \
        # a dead consonant is never followed by a vowel sign, so a 'സ്'    \
        # that is is the cluster സ്ല                                        \
        'SA_LA'   : 'സ്(?=[ാ-ൃ])', \
    }

    # the signs that are drawn in front of the letter they belong to. Each
    # of them waits for one token - a cluster is one token here however many
    # letters it is written out of
    prefix_signs = ('MATRA_E', 'MATRA_EE', 'MATRA_AI', 'RA_SIGN')

    # the marks that belong to the letter in front of them, which a sign
    # that is waiting to jump has to stay behind rather than count. ാ and ൗ
    # are deliberately not among them - they are the back halves of ൊ, ോ and
    # ൌ and have to end up behind the sign that jumped, or the two could not
    # be composed
    trailing_signs = ('YA_SIGN', 'VA_SIGN')

    # the letters that a 'യ' behind them is the sign ്യ and not the letter
    # യ. They are the ones this document draws a ്യ under and a bare യ behind
    # at most once - see the class comment
    ya_sign_after = ('KHA', 'GA', 'SSA', 'HA', 'BHA', 'BA', 'NNA', 'BA_LA', \
                     'NA_TA', 'DA_DHA', 'MA_MA', 'KA_SSA', 'SA_RRA_RRA')

    def __init__(self):
        BaseFont.__init__(self)
        self.langobjs = []
        self.langobjs.append(malayalam.MalayalamUnicode())
        self.langobjs.append(malayalam.Conjuncts())

        self.lexer = self.get_lexer()

        self.waitdict = {}
        for tokenName in self.prefix_signs:
            self.waitdict[tokenName] = 1

        self.waitover = set(self.trailing_signs)

        # the rules that run before the reordering, each of them naming what
        # a syllable really is before any of it jumps
        self.preComposeTokens = { \
            # the sign ്വ, which is handed the string of the letter വ. സ is \
            # the one letter this document never writes a bare വ behind,   \
            # and അന്വേഷണം and ഈശ്വരൻ are read as the words they are        \
            ('SA', 'VA')        : ['SA', 'VA_SIGN'], \
            ('NA', 'VA', 'SSA') : ['NA', 'VA_SIGN', 'SSA'], \
            ('SHA', 'VA', 'RA') : ['SHA', 'VA_SIGN', 'RA'], \
                                                            \
            # a vowel sign and the ്ര of the same syllable are both drawn  \
            # in front of its letter, the sign outside the ്ര, and unicode \
            # writes the ്ര first. Swapping them here is what makes them   \
            # come out of the jump in that order, the jump emitting what   \
            # was waiting longest first                                    \
            ('MATRA_E',  'RA_SIGN') : ['RA_SIGN', 'MATRA_E'],  \
            ('MATRA_EE', 'RA_SIGN') : ['RA_SIGN', 'MATRA_EE'], \
            ('MATRA_AI', 'RA_SIGN') : ['RA_SIGN', 'MATRA_AI'], \
        }

        # and the sign ്യ, which is handed the string of the letter യ
        for tokenName in self.ya_sign_after:
            self.preComposeTokens[(tokenName, 'YA')] = [tokenName, 'YA_SIGN']

        # the rules that run after it
        self.composeTokens = { \
            # the two halves of a vowel sign that is drawn with the letter \
            # between them, put back together once the front half has      \
            # jumped over that letter - െഹൗസ് is ഹൗസ്                         \
            ('MATRA_E',  'MATRA_AA')       : 'MATRA_O',  \
            ('MATRA_EE', 'MATRA_AA')       : 'MATRA_OO', \
            ('MATRA_E',  'AU_LENGTH_MARK') : 'MATRA_AU', \
        }

    def to_unicode(self, data):
        '''the passes run in the order this font's own reordering needs: a
           syllable's ്യ and ്വ are named and a vowel sign and the ്ര of it
           are put in the order unicode writes them before either jumps, and
           the two halves of ൊ, ോ and ൌ are joined after the jump, the letter
           having been between them until then'''
        tokentypes = self.tokenize(data)

        tokentypes = self.compose_tokens(tokentypes, self.preComposeTokens)
        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def token_to_unicode(self, tokenName):
        # the dotted circle the shaper drew under a sign that had no letter
        # to sit on is no character of the text
        if tokenName == 'DOTTED_CIRCLE':
            return ''

        return BaseFont.token_to_unicode(self, tokenName)

    def get_lexer(self):
        # the dotted circle is no token of the language, so it is added to
        # the ones langs/malayalam.py has
        tokens = ['DOTTED_CIRCLE']
        for obj in self.langobjs:
            tokens.extend(obj.get_tokens())

        # token strings are regular expressions for ply, so the strings of
        # the table have to be escaped and the patterns are handed over as
        # they are
        rules = {}
        for tokenName, glyphstr in self.glyphstrings.items():
            rules['t_' + tokenName] = re.escape(glyphstr)

        for tokenName, pattern in self.glyphpatterns.items():
            rules['t_' + tokenName] = pattern

        def t_error(t):
            # a character that is not in the tables above is one the font
            # draws as itself - the latin of the document, a digit, the
            # punctuation - which is text and comes through as it is
            char = t.value[0]

            if not self.is_text_char(char):
                self.report_error(t)
                t.lexer.skip(1)
                return None

            t.lexer.skip(1)
            t.type  = LITERAL
            t.value = char
            return t

        rules['t_error'] = t_error

        # only the tokens that the font has a glyph for
        rules['tokens'] = [tokenName for tokenName in tokens \
                                     if 't_' + tokenName in rules]

        # the rules are made in a loop, so they are handed to ply in an
        # object of their own rather than in the locals of this function.
        # ply looks up the module of that object
        rules['__module__'] = self.__class__.__module__
        return lex.lex(object = types.SimpleNamespace(**rules))
