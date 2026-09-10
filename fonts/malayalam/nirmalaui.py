import re

from indic2unicode.langs import malayalam
from ..basefont import LITERAL
from .meera import MeeraGlyphs

class NirmalaUIMalayalamGlyphs(MeeraGlyphs):
    '''The malayalam of a pdf set in Nirmala UI whose ToUnicode map has been
       repaired by tools/fix_tounicode.py, the Kerala gazette setting some of
       its issues in Nirmala UI - the ones Word writes - as well as in Kartika
       and Meera.

       WHAT THE REPAIR PUTS RIGHT

       Word built the map by pairing the glyphs of a run with the characters
       of it one by one, the way it does for the devanagari of the Gazette,
       and malayalam draws a syllable in a different number of glyphs than
       it is written in, so the pairing slips on every glyph that shaping
       moved or made: the sign െ is handed 'സ', േ 'ക്ഷ', ൈ 'വ', ്ര 'പ്' and
       പ a space, while ര is handed 'ര്' and the anusvara 'ും'. So കേരള
       extracts as ക്ഷകര്ള, പ്രവർത്തനം as പ് വര്‍ത്തനം and ഉദ്ദേശം as
       ഉക്ഷേശ്ും. The subsets keep the cmap and the GSUB of the font, which
       say what every one of those glyphs is, so the repair is read off the
       font and what is left for this pass is the order.

       WHAT IS DRAWN FIRST IS NOT WHAT IS WRITTEN FIRST

       This is fonts/malayalam/meera.py with the one thing Meera does not
       draw added. The vowel signs െ, േ and ൈ are drawn in front of the
       letter they belong to and each waits for one token, a cluster being
       one token however many letters it is written out of - the one glyph
       of യ്യ, the ക and ്ട that the font draws ക്ട as, the ല and ്പ of ല്പ.
       ൊ and ോ are drawn in two halves with the letter between them and are
       put back together once the front half has jumped - േഫാൺ is ഫോൺ. ്യ
       and ്വ are drawn behind the letter they are bound to, so a sign on its
       way past that letter has not passed the syllable until it has passed
       them as well.

       What is added is ്ര. Meera draws it inside the one glyph of its
       cluster and needs no rule for it; Nirmala UI draws it as a glyph of
       its own in front of the letter it belongs to, the way Kartika does,
       so ്രപവർത്തനം is പ്രവർത്തനം and മു്രദ is മുദ്ര. It waits for one token
       like the vowel signs, and a vowel sign of the same syllable is drawn
       outside it - ക്രേ is drawn േ ്ര ക - so the two are swapped before
       either jumps, unicode writing the ്ര first.

       That makes every cluster that is written with ്ര a sequence of tokens
       here rather than one: the ്ര of this font is never behind its letter,
       and a cluster token that ends in it would read the ്ര of one syllable
       as part of the syllable in front of it - മുദ്രപത്രം is drawn
       മു ്ര ദ പ ്ര ത ം, and a PA_RA would take the പ and the ്ര that
       belongs to the ത. So the lexer leaves those clusters out, see
       get_lexer.

       WHAT THE EXTRACTOR PUTS IN THE MIDDLE OF A WORD

       The glyph of ്ര is drawn at the head of its syllable and an extractor
       writes a line break behind it every now and then, when the syllable
       begins a line - പ്രവർത്തനം comes out as "്ര\\nപവർത്തനം", the ്ര
       staying on the line before. That whitespace is no glyph of the font,
       but no word ends with a sign that is drawn in front of its letter, so
       such a sign steps over it to the letter it belongs to.

       A space between a letter and a vowel sign is the other thing it
       writes. Word draws a zero width joiner that the author typed inside a
       syllable - the gazette types കൃഷി as ക‍ൃഷി here and there - as the
       space glyph of the font, and the repair reads that glyph as the space
       the font says it is. No word begins with a sign that is drawn behind
       its letter, so a space between the two is not a word boundary and is
       dropped: കൃഷി comes out whole, as the page is read.

       WHAT THIS WAS CHECKED AGAINST

       A tesseract -l mal ocr of the two Nirmala UI pages of
       test/test_pdfs/malayalam-nirmalaui.pdf - the first page is the
       masthead, which is set in Kartika-Bold. Once the chillus are spelled
       alike on both sides - the gazette types them with a zero width joiner
       and this writes the atomic chillu - and the zero width non-joiner the
       ocr writes behind a closing chandrakkala is left out, 360 of the 392
       malayalam words this pass produces match the ocr of their own page.
       Every one of the other 32 is the ocr's: it misreads the word -
       സ്റ്റേഷൻ as സ്റേഷൻ, ഡയറക്ടർ as ഡയറകുര്‍, ചാവക്കാട് as ചാവക്കാട
       with its chandrakkala dropped - or runs two words together or loses
       the last line of a page, but for സെക്യൂരിറ്റി, which the extractor
       itself breaks across a line.
    '''
    # the whitespace that an extractor writes between a sign that is drawn
    # in front of its letter and that letter, which the sign steps over
    whitespace = ' \t\r\n'

    # a space between a letter and a vowel sign that is drawn behind it,
    # which is the glyph Word draws for a zero width joiner typed there
    # rather than a word boundary - see the class comment
    joiner_space = re.compile('(?<=[ക-ഺ]) (?=[ാ-ൄൗ])')

    def __init__(self):
        MeeraGlyphs.__init__(self)

        # ്ര is drawn in front of its letter as the vowel signs are, and
        # waits for one token like them
        self.waitdict['RA_SIGN'] = 1

        # a vowel sign and the ്ര of the same syllable are both drawn in
        # front of its letter, the sign outside the ്ര, and unicode writes
        # the ്ര first. Swapping them before the jump is what makes them come
        # out of it in that order, the jump emitting what was waiting
        # longest first
        self.preComposeTokens = {}
        for tokenName in self.prefix_matras:
            self.preComposeTokens[(tokenName, 'RA_SIGN')] = \
                    ['RA_SIGN', tokenName]

    def to_unicode(self, data):
        '''the passes in the order this font needs them: the joiner is taken
           out of the syllable it was typed in, the signs that are drawn in
           front of a letter are carried over the whitespace between them and
           it and a vowel sign and the ്ര of the same syllable are put in the
           order unicode writes them before either jumps, and the two halves
           of ൊ and ോ are joined after the jump, the letter having been
           between them until then'''
        data = self.joiner_space.sub('', data)

        tokentypes = self.tokenize(data)

        tokentypes = self.step_over_whitespace(tokentypes)
        tokentypes = self.compose_tokens(tokentypes, self.preComposeTokens)
        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def is_whitespace(self, toktype):
        return type(toktype) == tuple and toktype[0] == LITERAL and \
               toktype[1] in self.whitespace

    def step_over_whitespace(self, tokentypes):
        '''the whitespace behind the signs that are drawn in front of a
           letter moved in front of them, so that they stand against the
           letter they wait for - all of them at once, a vowel sign and the
           ്ര of one syllable having to stay together for preComposeTokens.
           Only where a glyph of the font follows the whitespace - a sign
           that nothing but text follows has no letter to wait for and is
           left where it is'''
        out = list(tokentypes)
        i   = 0
        while i < len(out):
            if out[i] not in self.waitdict:
                i += 1
                continue

            k = i
            while k < len(out) and out[k] in self.waitdict:
                k += 1

            j = k
            while j < len(out) and self.is_whitespace(out[j]):
                j += 1

            if j > k and j < len(out) and type(out[j]) != tuple:
                out[i:j] = out[k:j] + out[i:k]
            i = j
        return out

    def is_glyph_string(self, tokenName, ustr):
        '''every string of the language but the clusters that are written
           with ്ര, the ്ര of this font being a glyph of its own in front of
           its letter - see the class comment. ply orders its string rules by
           falling length, so ്ര on its own is still read before the
           chandrakkala it starts with'''
        return tokenName == 'RA_SIGN' or self.RA_SIGN_STR not in ustr

    # the string of ്ര, which no cluster token of this font may carry
    RA_SIGN_STR = malayalam.MalayalamUnicode().tokendict['RA_SIGN']
