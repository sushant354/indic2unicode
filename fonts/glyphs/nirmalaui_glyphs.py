from .arialuni_glyphs import ArialUniGlyphs
from ..kannada.nirmalaui import NirmalaUIKannadaGlyphs

class NirmalaUIGlyphs(ArialUniGlyphs):
    '''The text of a pdf set in Nirmala UI whose ToUnicode map has been
       repaired by tools/fix_tounicode.py. Every glyph now carries the
       characters it really stands for, ka and sha and matra_i included, and
       the conjuncts and the matra_o that the broken map dropped are back,
       so nothing of the text is lost any more - unlike fonts/hindi/nirmalaui.py,
       which works on the text of a pdf whose map is still broken.

       What is left is the order: the glyphs are stored in the order in
       which they are drawn, so matra_i sits in front of the cluster it
       belongs to and the reph behind the whole syllable it sits on, e.g.
       निर्देशांक comes out as िनदेर्शांक and निकटवर्ती as िनकटवतीर्. That is
       the same order Arial Unicode MS draws in and the same two passes put
       it right, so this font is that one.

       Nirmala UI spells out what Arial Unicode MS carries as a glyph of its
       own - a half form comes out as its consonant and a halant and a rakar
       as a halant and a ra, rather than as one character - but the lexer
       reads a half form out of that pair anyway, so a matra_i still waits
       over the whole cluster: 'ि' + 'क' + '्र' is read as matra_i, half ka,
       ra and comes out as क्रि.

       THE OTHER SCRIPT OF THE SAME FONT

       Nirmala UI sets the Karnataka gazette as well, and the kannada of it
       goes through fonts/kannada/nirmalaui.py - the same split on the script
       that Arial Unicode MS does, since the font is one font and
       get_font_converter() names one converter for it. That pass is the
       kannada pass of Arial Unicode MS whole: the two fonts draw a kannada
       syllable in a different number of glyphs but in the same order, and it
       is the repair and not the reordering that the difference is in.
    '''
    kannadaclass = NirmalaUIKannadaGlyphs
