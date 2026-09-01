from .tauelango import TauElangoGlyphs

class IlaSundaramGlyphs(TauElangoGlyphs):
    '''The text of a pdf that is set in Uni-Ila.Sundaram - the other tamil of
       the Tamil Nadu gazette, drawn in 929 of the 8,248 documents of that
       corpus, very often beside TAUElangoPanchali in the same page - and
       whose ToUnicode map has been repaired by tools/fix_tounicode.py.

       WHY THE FONT NEEDS A REPAIR AND NOT A DECODER

       It is a unicode font: its glyphs really are tamil, and its subsets
       carry neither a cmap nor a post nor a GSUB, only outlines. What is
       wrong is the map that says which glyph is which, and it is wrong the
       way TAUElangoPanchali's is - built by pairing the glyphs of a cluster
       with the characters of it - only this producer hands the *first* glyph
       of a cluster the whole cluster and every glyph after it the cluster's
       last character. So மாவட்டம் extracts as மாாவட்டம், the ம saying "மா"
       and the ா behind it saying "ா"; தலைவர் extracts as தலைைவர், the ை
       (which tamil draws in front of its letter, so it is the cluster's
       first glyph) saying "லை" and the ல behind it saying "ை"; and a glyph
       that a document draws in two different clusters can only be given one
       reading, so the other cluster comes out as some third word's. That is
       not a reordering and no reordering can undo it - the ல of இலத்தூர்
       reaches an extractor as a ை - so the map is rebuilt out of
       UNI_ILA_SUNDARAM before anything reads the pdf, and what is left for
       this pass is what is left for fonts/tamil/tauelango.py: the order.

       WHY IT IS THAT PASS AND NOTHING MORE

       The two fonts are one script drawn one way. Uni-Ila.Sundaram draws the
       vowel signs ெ, ே and ை in front of the letter they belong to, draws ொ
       and ோ in two halves with the letter between them, draws a consonant
       with the pulli or with one of ி, ீ, ு and ூ on it as a single glyph,
       and draws ஔ and ஸ்ரீ as single glyphs of their own - which is the
       whole of what TauElangoGlyphs reads. The two differ only in which
       glyph id carries what, and that is a question for the repair table and
       not for this pass, so this class is that pass whole, the way
       fonts/kannada/nirmalaui.py is fonts/kannada/arialuni.py's.

       The one syllable it is not exercised on is ௌ, which this font draws
       out of a ெ and a length mark of its own exactly as TAU Elango does -
       the rule for it is inherited and holds - except that no document of
       this corpus writes that syllable and no subset of it carries a glyph
       for the mark, so UNI_ILA_SUNDARAM has no reading for the mark and the
       ெ in front of it has nothing to be composed with. It comes out as a ெ
       that has jumped over its letter and a glyph the pdf's own map named,
       which is what the text of an unrepaired document looks like there.
    '''
    pass
