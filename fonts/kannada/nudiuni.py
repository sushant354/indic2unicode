from .arialuni import ArialUniKannadaGlyphs

# The arkavattu of NudiUni. The font's own cmap names glyph 65 U+0CF5, a
# codepoint unicode has not assigned, which the font uses as a slot of its
# own for the ra that is drawn as a mark on top of the consonant that
# follows it. What a font says about its own glyph wins over a hand table in
# fix_font, so the repaired text keeps that character rather than the 'ರ್' of
# langs/kannada.py, and this is where it is read
NUDI_UNI_ARKAVATTU = '೵'


class NudiUniKannadaGlyphs(ArialUniKannadaGlyphs):
    '''The kannada of a pdf set in NudiUni whose ToUnicode map has been
       repaired by tools/fix_tounicode.py, the Karnataka gazette being set
       in the unicode Nudi as well as in Arial Unicode MS and Nirmala UI.

       Every glyph the repair reached now carries the characters it really
       stands for, and what is left is the order, which is the order kannada
       is drawn in whichever font draws it:

           [base] [head of the matra] [vattus] [tail of the matra] [signs]

       with the arkavattu behind the whole syllable it sits on. Read off the
       glyph streams of the gazette, ಕರ್ನಾಟಕ is drawn ಕ + ನ + ಾ + ರ್ + ಟ + ಕ,
       ಪ್ರದತ್ತವಾ is drawn ಪ + ್ರ + ದ + ತ + ್ತ + ವ + ಾ and ರವನ್ನು is drawn
       ರ + ವ + ನ + ು + ್ನ - the same order Arial Unicode MS draws in, down to
       the vattu following the matra of its own syllable, so the same pass
       puts it right and this font is that one.

       WHAT NUDIUNI SPELLS DIFFERENTLY, AND WHY ONLY ONE OF IT IS CODE

       - the arkavattu is a character of its own, U+0CF5, and not 'ರ್' and a
         mark. That is the one difference here: Arial Unicode MS and Nirmala
         UI draw the arkavattu and the dead ra with glyphs of their own but
         spell them alike, so the repair has to mark which is which, while
         NudiUni's own cmap already keeps them apart. The token is still
         written out as the plain 'ರ್', so nothing downstream of the lexer
         changes;

       - a consonant that a vowel sign or a vattu is written onto is a glyph
         of its own, as it is in Arial Unicode MS and unlike Nirmala UI. It
         reads as the plain consonant, so it is not a token of its own
         either;

       - a two part matra is split around the vattus of its syllable, ೇ as
         ೆ + ೕ, which join_matras() puts back together as it does for the
         other two fonts.

       WHAT IS STILL MISSING FROM THE TEXT THIS READS

       The repair of NudiUni is partial: no subset of it in this corpus
       carries a GSUB, so the consonants that a vowel sign is drawn into and
       the ligatures - ಕ್ಷ, ಜ್ಞ, ಷ್ಟ - are named by nothing the font says and
       are left as the pdf has them, which is nothing at all in the maps
       most producers write. Around 8% of the glyphs of such a document
       therefore reach this pass as holes. A hole is not a token, so it
       comes out the way it went in and the syllables around it are still
       reordered; it is text this pass cannot put back, not text it gets
       wrong. See NUDI_UNI_KANNADA in tools/fix_tounicode.py
    '''
    def get_arkavattu(self):
        return NUDI_UNI_ARKAVATTU
