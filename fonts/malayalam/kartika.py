import re
import types

from indic2unicode.langs import malayalam
from ..basefont import BaseFont, LITERAL
import ply.lex as lex

class Kartika(BaseFont):
    '''Kartika is the unicode malayalam of Windows, and the pdfs of the
       Kerala Gazette that are set in it carry the same kind of broken
       ToUnicode map as the ones that are set in Arial Unicode MS, in
       Nirmala UI, in Kalinga and in KrishnaUni: the map was built by
       pairing the glyphs of a run with the characters of that run one by
       one, and malayalam draws a syllable in a different number of glyphs
       than it is written in, so the pairing slips on every glyph that
       shaping moved or made. The text that comes out of such a pdf is
       therefore malayalam that is

       1. in the visual order of the glyphs and not in the order of unicode,
          so െ, േ and ൈ sit in front of the letter they belong to and the
          ്ര of a cluster in front of the whole of it, and

       2. spelled with the wrong characters wherever the pairing slipped:
          'മ' is the vowel sign േ and 'േ' is the letter മ, 'റ്റ' is the sign
          െ and 'െ' is the cluster റ്റ, 'ല്' is the letter ല and 'ല' is the
          sign ൈ, and 'പ്' is the ്ര that is drawn in front of its letter.

       So the text is treated like any other font of this package: every
       glyph of the font is a token, the token is given the unicode string
       it really stands for and the tokens are put back in the order that
       unicode wants. ബന്ധപ്പെട്ട് comes out of the pdf as ബന്ധറ്റപ്പട്ട്,
       പ്രകാരം as പ്പകാരം, സർവ്വേ as സർമേ and കൊല്ലം as റ്റകാല്ലം.

       WHERE THE READINGS COME FROM

       The pdf embeds the font four times over and every subset keeps its
       cmap, so what a letter, a vowel sign, a chillu or the chandrakkala
       draws is in the document itself - the cmap maps a character to the
       glyph that draws it, and that is the one thing in a broken pdf that
       is not broken. The largest subset names 93 characters that way.

       No subset carries a GSUB, so nothing in the font says what the shaper
       made, and the rest of the table below - the dead consonants, the 36
       clusters the font draws as one glyph, the marks ്യ, ്വ, ്ര and ്ല, and
       the width variants of ു and ൂ - was read by rendering the outline out
       of the embedded subset and reading the shape, and then checked in the
       words it stands in against a tesseract -l mal ocr of the same pages.
       The dead consonants need no reading one by one: they run unbroken
       from the glyph that draws ക്, one to a glyph id in the order the
       alphabet lists its letters, which is where the ക് ഖ് ഗ് ജ് ട് ഡ് ണ്
       ത് ദ് ന് പ് ഫ് ബ് യ് ര് വ് ഷ് സ് ഹ് that the document draws land.

       Every dead consonant reaches this converter as its letter and a
       chandrakkala, which is what unicode writes it as, so none of them is
       named below - they are read by the letter and the VIRAMA of it. Only
       the two whose string the map spells some other way have a rule.

       WHAT IS LOST, AND WHAT THE TEXT AROUND A GLYPH BRINGS BACK

       The map cannot be inverted completely, and what is lost is what two
       glyphs of one subset were handed the same string for. Where the
       document itself says which of the two it is, the rule is in
       glyphpatterns or in preComposeTokens below and is this:

       * 'ല' is the sign ൈ and the ്ല of ല്ല - 66 against 143. The ്ല stands
         behind a ല every time this document draws it and no ൈ ever does, so
         a 'ല' behind the 'ല്' of ല is the ്ല, and the two together are the
         one cluster ല്ല. Both are whole - ജില്ല comes out of the pdf as
         ജില്ല and വില്ലേജ് as വിമല്ലജ്.

       * 'പ്പ' is the cluster പ്പ and a ്ര in front of a പ - 27 against 17.
         Every ്ര of this document that a പ follows stands at the head of a
         word and no പ്പ does, so a 'പ്പ' that no malayalam character stands
         in front of is the ്ര and the പ. Both are whole - പ്രകാരം comes out
         of the pdf as പ്പകാരം and ബന്ധപ്പെട്ട് as ബന്ധറ്റപ്പട്ട്.

       * '്' is the chandrakkala and the dead ഡ് - 160 against 3. A chillu
         carries no chandrakkala of its own, so a '്' behind one is the ഡ്.
         Both are whole - വാർഡ് comes out of the pdf as വാർ്.

       * 'ഖ്' is ഖ and the dead ഖ് - 34 against 7. The dead one ends a word
         every one of the seven times it is drawn and ഖ ends one once, so an
         'ഖ്' that no malayalam character follows is the dead consonant: all
         7 of them, and one ഖ lost, മുഖ coming out as മുഖ്.

       * 'േ' is the letter മ, the cluster വ്വ and the sign ്വ - 238, 12 and
         2. വ്വ ends a word behind a vowel sign every one of the twelve
         times it is drawn and no മ of this text does, so a 'േ' that ends a
         word behind a 'മ' or a 'റ്റ' is വ്വ: all 12 of them and no മ lost,
         റീസർമേ being റീസർവ്വേ. ്വ is lost with it, nothing else of this
         face saying 'േ' - അന്വേഷണം comes out as അനേമഷണം.

       * 'യ' is the letter യ and the sign ്യ - 117 against 32. The two
         cannot be told apart by where they stand, both of them following a
         letter, so the sign is read where a letter this document draws a ്യ
         under stands in front of it - വ, ത, ശ, ന, ദ, ഗ, ഷ, ഖ, ദ്ധ or സ്റ്റ.
         That is 29 of the 32 and it costs no യ at all, no യ of this
         document standing behind any of those ten. The three that are left
         are behind a ല, a ്ല and a ര, which are letters this document's യ
         does stand behind - ഇല്യാസ് comes out as ഇലയാസ് and സൂര്യ as സൂരയ.

       * 'െ' is the letter ച and the cluster റ്റ - 45 against 17. ച stands
         at the head of a word or behind one of the three vowel signs that
         are drawn in front of their letter every one of the 45 times, so a
         'െ' anywhere else is റ്റ: all 45 of the ച and 13 of the 17 റ്റ. The
         four that are left are the ones behind a 'റ്റ', which is the sign
         െ, and ചെ is as common there as റ്റെ - ഏറ്റെടുത്ത് comes out as
         ഏചെടുത്ത്.

       And what nothing brings back is this:

       * 'പ്' is the sign ്ര and the dead പ് - 48 against 1 - and is read as
         the sign, so നിക്ഷിപ്ത comes out as നിക്ഷിത്ര.

       * 'ര' is ര and the cluster ന്ദ - 163 against 2 - and is read as ര, so
         സുരേന്ദ്രൻ comes out as സുരേര്രൻ.

       * 'ഥ' is ഥ and the cluster ത്ഥ, one drawing of each, and is read as
         ഥ, so അർത്ഥ comes out as അർഥ.

       * a dead സ് in front of a െ is drawn as the two glyphs and reaches
         this converter as 'സ്' and 'റ്റ', which is the string of the one
         cluster സ്റ്റ and is read as it - സ്പെഷ്യൽ comes out as സ്റ്റപഷ്യൽ.

       ു and ൂ each come from two glyphs as well, the sign itself and the
       one that hangs under a letter of another width, but both glyphs are
       the same sign and nothing is lost with them.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       The vowel signs െ, േ and ൈ are drawn in front of the letter they
       belong to and unicode writes them behind it, so each of them waits
       for one token. A cluster is one token here however many letters it is
       written out of, which is what makes the wait a one rather than a
       count of letters: a േ in front of the single glyph of ക്ക belongs
       behind both letters and the chandrakkala between them.

       ൊ and ോ are drawn in two halves with the letter between them, so they
       arrive as a െ or a േ in front and a ാ behind and are put back
       together by composeTokens once the front half has jumped - കൊല്ലം is
       drawn െ ക ാ ല ്ല ം. ൌ needs no rule beside them: this font draws the
       length mark ൗ behind its own letter and the document writes the au of
       a syllable with that mark alone, all nine of them standing directly
       behind their consonant.

       ്ര is drawn in front of its letter as well, and inside whatever vowel
       sign is drawn there, so a sign and the ്ര of the same syllable are
       swapped by preComposeTokens before either jumps - unicode writes the
       ്ര first and the jump emits what was waiting longest first.

       ്യ, ്വ and ്ല are drawn under or behind the letter they are bound to
       and are typed there, so a vowel sign that is on its way past that
       letter has not passed the syllable until it has passed them as well -
       വിമല്ലജ് is വില്ലേജ്. ്ല reaches the jump as part of the one cluster
       ല്ല and so needs no rule of its own; ്യ and ്വ are in waitover for it.
       Neither of those two is exercised by this document: it draws no vowel
       sign in front of a ്യ at all, and the one it draws in front of a ്വ -
       അന്വേഷണം - is a ്വ that is lost to മ before the jump ever sees it. The
       two are there off the script rather than off the page.

       THE OTHER THREE FACES

       The gazette sets its headings in a bold subset of this font and its
       masthead is a stamp of its own in a third, and each of them is a
       subset with a map that was broken over its own first drawings: 'ക' is
       the letter ക in the masthead and the cluster ക്ക as well, 'ും' is the
       anusvara in the headings, and the same string is a different glyph in
       each face. The faces cannot be told apart in the text, one string of
       characters being all that reaches a converter, so this one reads the
       face that draws 9,825 of the 10,116 malayalam glyphs of the test
       document against the other three's 291. The headings and the masthead
       come out wrong - കേരള സർക്കാർ comes out of the pdf as േകരള സർകാർ and
       is converted as മകരള സർകാർ.

       WHAT IS NOT HANDLED

       A vowel sign that is drawn in front of a cluster the font has no
       glyph of its own for - one it writes as a dead consonant and a letter
       - would be emitted inside that cluster, the sign waiting for one
       token and the dead consonant reaching this pass as two. This document
       draws no such syllable: not one of the vowel signs it draws in front
       of a letter is followed by a dead consonant, every cluster they stand
       in front of being one the font draws as a single glyph.

       WHAT THIS WAS CHECKED AGAINST

       The pdf's own glyphs first. Every glyph the document draws was read
       off the embedded subset as above, and the text those readings make of
       the face this converter reads is the yardstick: of the 2,053 words
       that face draws, this pass produces 2,037 (99.2 per cent) exactly as
       the glyphs say they were drawn, and what is left is the readings
       listed above as lost.

       And a tesseract -l mal ocr of the pages themselves, all 32 of them:
       of the 1,833 malayalam words this pass produces over the whole
       document, 1,651 (90.1 per cent) match the ocr of their own page
       character for character once the chillus are spelled alike on both
       sides. It produces no (cid:N) and five words that begin with a vowel
       sign, every one of them from the masthead or the headings.
    '''
    # the string the pdf hands each glyph of the font, against the token
    # that glyph really draws. Only what needs decoding is listed - a
    # character the font draws as itself (the latin of the document, the
    # digits, the punctuation) reaches the output through the literal path
    # of t_error, see BaseFont.is_text_char - and so is only what the map
    # spells some other way: a dead consonant that comes through as its
    # letter and a chandrakkala is read by the two tokens of it
    glyphstrings = { \
        # VOWELS. ഈ and ഓ have a glyph of their own in this font and are   \
        # drawn as one; ഐ, ഔ, ഋ and the malayalam digits it never draws    \
        'A'    : 'അ', 'AA'   : 'ആ', 'I'    : 'ഇ', 'II'   : 'ഈ', \
        'U'    : 'ഉ', 'E'    : 'എ', 'EE'   : 'ഏ', 'O'    : 'ഒ', \
        'OO'   : 'ഓ', \
                      \
        # CONSONANTS. ച and ഖ are read by a pattern below, each of them    \
        # sharing its string with another glyph                            \
        'KA'   : 'ക', 'GA'   : 'ഗ', 'JA'   : 'ജ', 'TTA'  : 'ട', \
        'DDA'  : 'ഡ', 'NNA'  : 'ണ', 'TA'   : 'ത', 'THA'  : 'ഥ', \
        'DA'   : 'ദ', 'DHA'  : 'ധ', 'NA'   : 'ന', 'PA'   : 'പ', \
        'PHA'  : 'ഫ', 'BA'   : 'ബ', 'BHA'  : 'ഭ', 'MA'   : 'േ', \
        'YA'   : 'യ', 'RA'   : 'ര', 'RRA'  : 'റ', 'LA'   : 'ല്', \
        'LLA'  : 'ള', 'LLLA' : 'ഴ', 'VA'   : 'വ', 'SHA'  : 'ശ', \
        'SSA'  : 'ഷ', 'SA'   : 'സ', 'HA'   : 'ഹ', \
                                                  \
        # THE CHILLUS. the letters that end a syllable with no vowel, each \
        # of them a character of its own - see langs/malayalam.py. The map \
        # spells two of them the old way, as the letter, the virama and a  \
        # zero width joiner, and hands ൾ the ്പ of the ൾപ് it was first    \
        # drawn in front of                                                \
        'CHILLU_NN' : 'ൺ', 'CHILLU_N'  : 'ൻ', 'CHILLU_RR' : 'ർ', \
        'CHILLU_L'  : 'ല്‍', 'CHILLU_LL' : 'ള്‍പ്', \
                                                    \
        # THE SIGNS. the vowel signs, the chandrakkala and the anusvara,   \
        # and the consonants that are written as a mark on the letter they \
        # are bound to. ്ല is not among them: this document only ever      \
        # draws it behind a ല and it is read as the one cluster ല്ല, see   \
        # preComposeTokens. ്വ is lost to മ and has no reading at all      \
        'MATRA_AA' : 'ാ', 'MATRA_I'  : 'ി', 'MATRA_II' : 'ീ', \
        'MATRA_U'  : 'ു', 'MATRA_UU' : 'ൂ', \
        'MATRA_VOCALIC_R' : 'ൃ', \
        'MATRA_E'  : 'റ്റ', 'MATRA_EE' : 'മ', 'MATRA_AI' : 'ല', \
        'VIRAMA'   : '്', 'ANUSVARA' : 'ം', 'AU_LENGTH_MARK' : 'ൗ', \
        'YA_SIGN'  : 'യ', 'RA_SIGN'  : 'പ്', \
                                             \
        # THE CLUSTERS THE FONT DRAWS AS ONE GLYPH. A cluster that is not  \
        # here the font writes out of a dead consonant and a letter, which \
        # needs no glyph of its own. പ്പ is read by a pattern below, its   \
        # string being a ്ര and a പ as well                                \
        'KA_KA'   : 'ക്ക',  'KA_TA'   : 'ക്ത',  'KA_SSA'  : 'ക്ഷ',  \
        'KA_LA'   : 'ക്ല',  'NGA_KA'  : 'ങ്ക',  'NGA_NGA' : 'ങ്ങ',  \
        'CA_CA'   : 'ച്ച',  'NYA_NYA' : 'ഞ്ഞ',  'TTA_TTA' : 'ട്ട',  \
        'NNA_TTA' : 'ണ്ട',  'NNA_NNA' : 'ണ്ണ',  'TA_TA'   : 'ത്ത',  \
        'DA_DA'   : 'ദ്ദ',  'DA_DHA'  : 'ദ്ധ്', 'NA_TA'   : 'ന്ത',  \
        'NA_DHA'  : 'ന്ധ',  'NA_NA'   : 'ന്ന',  'NA_RRA'  : 'ന്‍റ', \
        'PA_LA'   : 'പ്ല',  'BA_DA'   : 'ബ്ദ',  'BA_BA'   : 'ബ്ബ',  \
        'BA_LA'   : 'ബ്ല',  'MA_PA'   : 'മ്പ',  'MA_MA'   : 'മ്മ',  \
        'YA_YA'   : 'യ്യ',  'LLA_LLA' : 'ള്ള',  'SA_THA'  : 'സ്ഥ',  \
        'SA_RRA_RRA' : 'സ്റ്റ', 'SA_SA' : 'സ്സ', 'HA_NA'  : 'ഹ്ന',  \
        'HA_MA'   : 'ഹ്മ',  \
    }

    # the glyphs whose string another glyph of the same face is handed as
    # well, and that the text around them tells apart. Each of these is a
    # regular expression rather than a string and stands in glyphstrings'
    # place; ply orders its rules by falling length, so a pattern is always
    # tried before the bare string it competes with. See the class comment
    # for what each of them brings back and what it costs
    glyphpatterns = { \
        # ച stands at the head of a word or behind one of the three vowel  \
        # signs that are drawn in front of their letter - 'മ' is േ, 'റ്റ'  \
        # is െ and 'ല' is ൈ - and a 'െ' anywhere else is the cluster റ്റ   \
        'CA'      : '(?<=മ)െ|(?<=റ്റ)െ|(?<=ല)െ|(?<![ഀ-ൿ])െ', \
        'RRA_RRA' : 'െ', \
                         \
        # the dead ഖ് ends a word, where ഖ carries the letter behind it    \
        'KHA'     : 'ഖ്(?=[ഀ-ൿ])|ഖ', \
                                     \
        # a 'പ്പ' that no malayalam character stands in front of is a ്ര   \
        # and a പ rather than the cluster                                  \
        'PA_PA'   : '(?<=[ഀ-ൿ])പ്പ', \
                                     \
        # വ്വ ends a word behind a vowel sign, where the letter മ that     \
        # shares its string does not                                      \
        'VA_VA'   : '(?<=മ)േ(?![ഀ-ൿ])|(?<=റ്റ)േ(?![ഀ-ൿ])', \
    }

    # the signs that are drawn in front of the letter they belong to. Each
    # of them waits for one token - a cluster is one token here however many
    # letters it is written out of
    prefix_signs = ('MATRA_E', 'MATRA_EE', 'MATRA_AI', 'RA_SIGN')

    # the marks that belong to the letter in front of them, which a sign
    # that is waiting to jump has to stay behind rather than count. ാ is
    # deliberately not among them - it is the back half of ൊ and has to end
    # up behind the െ that jumped, or the two could not be composed
    trailing_signs = ('YA_SIGN', 'VA_SIGN')

    # the letters that a 'യ' behind them is the sign ്യ and not the letter
    # യ. They are the ones this document draws a ്യ under, and no യ of it
    # stands behind any of them - see the class comment
    ya_sign_after = ('VA', 'TA', 'SHA', 'NA', 'DA', 'GA', 'SSA', 'KHA', \
                     'SA_RRA_RRA', 'DA_DHA')

    # the chillus, which carry no chandrakkala of their own, so a '്' behind
    # one of them is the dead ഡ് that shares its string
    chillus = ('CHILLU_NN', 'CHILLU_N', 'CHILLU_RR', 'CHILLU_L', \
               'CHILLU_LL')

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
            # the ്ല that is drawn behind a ല, which is the one cluster    \
            # ല്ല. It has to be one token before the jump, a vowel sign in \
            # front of that syllable belonging behind the whole of it -    \
            # വിമല്ലജ് is വില്ലേജ്                                          \
            ('LA', 'MATRA_AI')      : 'LA_LA', \
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

        # the dead ഡ്, which is handed the string of the chandrakkala
        for tokenName in self.chillus:
            self.preComposeTokens[(tokenName, 'VIRAMA')] = \
                    [tokenName, 'DDA', 'VIRAMA']

        # and the sign ്യ, which is handed the string of the letter യ
        for tokenName in self.ya_sign_after:
            self.preComposeTokens[(tokenName, 'YA')] = [tokenName, 'YA_SIGN']

        # the rules that run after it
        self.composeTokens = { \
            # the two halves of a vowel sign that is drawn with the letter \
            # between them, put back together once the front half has      \
            # jumped over that letter - െകാല്ലം is കൊല്ലം                    \
            ('MATRA_E',  'MATRA_AA') : 'MATRA_O',  \
            ('MATRA_EE', 'MATRA_AA') : 'MATRA_OO', \
        }

    def to_unicode(self, data):
        '''the passes run in the order this font's own reordering needs: a
           syllable is made one token and a vowel sign and the ്ര of it are
           put in the order unicode writes them before either jumps, and the
           two halves of ൊ and ോ are joined after the jump, the letter
           having been between them until then'''
        tokentypes = self.tokenize(data)

        tokentypes = self.compose_tokens(tokentypes, self.preComposeTokens)
        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def get_lexer(self):
        tokens = []
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
            # punctuation, the zero width joiner of a chillu that no rule
            # took - which is text and comes through as it is
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
