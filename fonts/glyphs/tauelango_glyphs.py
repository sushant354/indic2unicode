from ..tamil.tauelango import TauElangoGlyphs

class TauElangoPanchaliGlyphs(TauElangoGlyphs):
    '''The text of a pdf set in TAUElangoPanchali whose ToUnicode map has
       been repaired by tools/fix_tounicode.py, named here beside the other
       converters that read a repaired pdf so the family is in one place.

       The pass itself lives in fonts/tamil/tauelango.py, beside
       fonts/tamil/tamelango.py, which decodes the legacy 8 bit font of the
       same foundry - the two are one script and one order and only differ
       in whether the characters have to be decoded before they are put in
       it
    '''
    pass
