from .arialuni_glyphs import ArialUniGlyphs

class MangalGlyphs(ArialUniGlyphs):
    '''The text of a pdf set in Mangal whose ToUnicode map has been repaired
       by tools/fix_tounicode.py.

       Two producers carry this font and their maps are broken differently.
       The gazettes of the one hand every glyph the shaper made <0000>
       instead - no character at all - so their half forms, their conjuncts,
       their matra_i and their reph are not wrong in the extracted text, they
       are missing from it, and a raw NUL sits where each of them belongs:
       निम्नलिखित extracts as "न न ल खत" and राष्ट्रपति as "रा प त". Those
       subsets carry neither a cmap nor a post nor a GSUB, so there is
       nothing in them to read those glyphs back out of and they are repaired
       from MANGAL_OUTLINES in tools/fix_tounicode.py, which is keyed by what
       a glyph draws because that producer renumbers its subsets.

       The union gazettes of the other - Word - are broken the way Arial
       Unicode MS is instead: nothing is missing from their map, the glyphs
       of a run were simply paired with the characters of the run one by one
       and the pairing slips on the glyphs shaping moved, so खंड extracts as
       िंर् and किया as ककया. Those subsets do keep a cmap, a post and a
       GSUB, and the glyphs the shaper made that they still say nothing about
       are repaired from MANGAL, a table of the 890 glyph numbering that
       producer leaves alone.

       What is left after either repair is the order, and there Mangal is the
       same font as Arial Unicode MS: the glyphs are stored in the order they
       are drawn in, so matra_i sits in front of the cluster it belongs to
       and the reph behind the whole syllable it sits on - निम्नलिखित comes
       out of the repaired pdf as िनम्निलखत and सहर्ष as सहषर्. That is the
       order Arial Unicode MS draws in and the same two passes put it right,
       so this font is that one.

       Mangal draws a reph that sits on a syllable carrying a matra or an
       anusvar as a single glyph, ीर् and ेर् and ोर् and ंर्, the way Arial
       Unicode MS draws ीर्: the syllable keeps its own sign, so कुर्रे comes
       out as कुर्रे and not as कुर्र, and बोर्डों as बोर्डों and not as
       बोर्ड.
    '''
    pass
