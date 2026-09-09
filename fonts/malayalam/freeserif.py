from .meera import MeeraGlyphs

class FreeSerifGlyphs(MeeraGlyphs):
    '''The text of a pdf that is set in FreeSerif - the GNU FreeFont serif,
       the other malayalam of the Kerala gazette - and whose ToUnicode map
       has been repaired by tools/fix_tounicode.py.

       WHY THIS FONT NEEDS A REPAIR AND NOT A DECODER

       FreeSerif is a unicode opentype font and its glyphs really are
       malayalam - what is wrong is the map that says which. Its producer,
       mPDF, re-encodes the font subset by subset the way the producer of
       Meera does, and names each byte by the character its own cmap gives
       the glyph: right for every letter, vowel sign and chandrakkala the
       font draws on its own, and silent about every glyph the shaper made,
       since no character maps to one. It hands each of those a private use
       codepoint instead, so a cluster or a syllable reaches an extractor as
       nothing at all - 109 of the 351 bytes of the two subsets of
       test/test_pdfs/malayalam-freeserif.pdf are named that way. A private
       use codepoint is not a wrong reading that a converter could undo, so
       tools/fix_tounicode.py rebuilds the map out of FREE_SERIF_OUTLINES
       before anything reads the pdf, and what is left for this pass is what
       is left for fonts/malayalam/meera.py: the order.

       WHY THIS PASS IS MEERA'S WHOLE

       The two fonts are one script drawn one way. The vowel signs െ, േ and
       ൈ are drawn to the left of their consonant and each waits for one
       token; ൊ and ോ are drawn in two halves with the letter between them
       and are put back together once the front half has jumped; ്യ and ്വ
       are glyphs of their own typed under the letter they are bound to, so
       a sign on its way past that letter has not passed the syllable until
       it has passed them; and ്ര is part of the one glyph of its cluster
       and needs no rule. ൗ is drawn behind its own letter here as it is in
       Meera, so no half of a sign is ever left in front of one for
       composeTokens to join.

       Everything that differs between the two fonts differs in which glyph
       carries what, which is a question for the repair table and not for
       this pass. FreeSerif draws a syllable of one cluster and one vowel
       sign as a single glyph where Meera draws the cluster and the sign
       apart - ക്കു, ത്തൂ, ഞ്ജു - and it draws some of those in two widths.
       Both are read straight off langs/malayalam.py by the lexer this
       inherits, the cluster as its own token and the sign as its own, since
       a sign written into a letter is never in front of it and so is never
       waited for.

       Six clusters this font draws as one glyph were not among the ones
       Meera does, and langs/malayalam.CONJUNCT_TOKENS names them now: ഞ്ജ,
       ദ്മ, പ്സ, ബ്ദ, ഷ്ണ and സ്ന. They have to be one token each because a
       vowel sign in front of such a syllable belongs behind the whole of it
       - സ്നേഹരാജ് is drawn േ സ്ന ഹ രാ ജ ് and is സ്നേഹരാജ്.

       WHAT THIS WAS CHECKED AGAINST

       A tesseract -l mal ocr of the pages themselves, all 41 of them: of
       the 9,138 malayalam words this pass produces, 8,404 (92.0 per cent)
       match the ocr of their own page character for character once the
       chillus are spelled alike on both sides. The words that do not are
       the table cells and the single letters the ocr itself did not read.
       Over the whole document it produces no (cid:N), no word beginning
       with a vowel sign and one word with two vowel signs in a row -
       മാാപിതാക്കൾ, which is the gazette's own typing and which the page
       shows as it is.
    '''
    pass
