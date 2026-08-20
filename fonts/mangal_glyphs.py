from .arialuni_glyphs import ArialUniGlyphs

class MangalGlyphs(ArialUniGlyphs):
    '''The text of a pdf set in Mangal whose ToUnicode map has been repaired
       by tools/fix_tounicode.py.

       Mangal is not broken the way Arial Unicode MS and Nirmala UI are.
       Their maps hand a glyph the wrong character, so their text extracts as
       readable devanagari that says something else; the Mangal of these
       gazettes hands every glyph the shaper made <0000> instead - no
       character at all - so its half forms, its conjuncts, its matra_i and
       its reph are not wrong in the extracted text, they are missing from
       it, and a raw NUL sits where each of them belongs. निम्नलिखित extracts
       as "न न ल खत" and राष्ट्रपति as "रा प त".

       The subset carries neither a cmap nor a post nor a GSUB, so there is
       nothing in it to read those glyphs back out of and they are repaired
       from MANGAL_OUTLINES in tools/fix_tounicode.py, which is keyed by what
       a glyph draws because this subset renumbers its glyph ids.

       What is left after the repair is the order, and there Mangal is the
       same font as the other two: the glyphs are stored in the order they
       are drawn in, so matra_i sits in front of the cluster it belongs to
       and the reph behind the whole syllable it sits on - निम्नलिखित comes
       out of the repaired pdf as िनम्निलखत and सहर्ष as सहषर्. That is the
       order Arial Unicode MS draws in and the same two passes put it right,
       so this font is that one.

       Mangal draws a reph that sits on a syllable carrying matra_ii or
       matra_e as a single glyph, ीर् and ेर्, the way Arial Unicode MS draws
       ीर्: the syllable keeps its matra, so कुर्रे comes out as कुर्रे and
       not as कुर्र.
    '''
    pass
