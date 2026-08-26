from .arialuni import ArialUniKannadaGlyphs

class NirmalaUIKannadaGlyphs(ArialUniKannadaGlyphs):
    '''The kannada of a pdf set in Nirmala UI whose ToUnicode map has been
       repaired by tools/fix_tounicode.py, a Karnataka gazette being set in
       Nirmala UI as well as in Arial Unicode MS. Every glyph now carries the
       characters it really stands for, and what is left is the order, which
       is the order kannada is drawn in whichever font draws it:

           [base] [head of the matra] [vattus] [tail of the matra] [signs]

       with the arkavattu behind the whole syllable it sits on. So ಕರ್ನಾಟಕ
       comes out of the repaired pdf as ಕನಾರ್ಟಕ, ಅನುಸೂಚಿಯಲ್ಲಿ as ಅನುಸೂಚಿಯಲಿ್ಲ
       and ಗ್ರಾಮ as ಗಾ್ರಮ. That is the order Arial Unicode MS draws in and the
       same pass puts it right, so this font is that one.

       WHERE THE TWO FONTS DIFFER, AND WHY IT IS NOT IN THE CODE

       Nirmala UI draws a syllable in fewer glyphs than Arial Unicode MS does
       and spells out what that font carries as a glyph of its own, but every
       one of those differences is a difference in what the *repair* writes,
       not in the order it writes it in:

       - a whole matra is drawn into the letter - ಕೇ is one glyph where Arial
         Unicode MS draws ಕಿ and a length mark - so the halves that
         join_matras() puts back together simply are not split in the first
         place. They still are when a vattu sits between them, ಸ್ವೀ being
         drawn ಸಿ + ್ವ + ೕ, so the join is needed either way;
       - ಕ್ಷ and ಜ್ಞ have no glyph of their own and are drawn as the letter
         and the vattu, ಕ + ್ಷ, which the lexer reads as those two tokens and
         the reorder puts back as ಕ್ಷ;
       - there is no separate form of a consonant for a syllable that carries
         a vattu, so a base is a base wherever it stands.

       None of that changes a token, so the pass is inherited whole. What is
       Nirmala UI's own is the table its glyphs are read out of, which is
       NIRMALA_UI_KANNADA in tools/fix_tounicode.py - the subset of it that
       these gazettes carry keeps neither a cmap nor a post nor a GSUB, so
       nothing in the font says what a glyph is and the whole of the kannada
       comes from there.
    '''
    pass
