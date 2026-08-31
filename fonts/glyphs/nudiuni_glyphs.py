from ..kannada.nudiuni import NudiUniKannadaGlyphs

class NudiUniGlyphs(NudiUniKannadaGlyphs):
    '''The text of a pdf set in NudiUni whose ToUnicode map has been repaired
       by tools/fix_tounicode.py, named here beside the other converters that
       read a repaired pdf so the family is in one place.

       WHY THIS IS THE KANNADA PASS ITSELF AND NOT A SPLIT LIKE THE OTHERS

       arialuni_glyphs and nirmalaui_glyphs are the pass of a font that draws
       two scripts: Arial Unicode MS and Nirmala UI set the Union gazette in
       devanagari and the Karnataka gazette in kannada, so a run of their
       text is split on its script and each half read by the pass that knows
       it. NudiUni draws kannada and nothing else - it is the unicode font of
       the Nudi family, which is kannada - so there is no second script to
       split off and the kannada pass is the whole converter. The latin of
       the document still comes out the way it went in, which is what that
       pass does with a character no rule matched
    '''
    pass
