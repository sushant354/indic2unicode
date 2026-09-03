from ..malayalam.meera import MeeraGlyphs

class MeeraUniGlyphs(MeeraGlyphs):
    '''The text of a pdf set in Meera whose ToUnicode map has been repaired
       by tools/fix_tounicode.py, named here beside the other converters that
       read a repaired pdf so the family is in one place.

       The pass itself lives in fonts/malayalam/meera.py, beside
       fonts/malayalam/revathi.py, which decodes the legacy 8 bit malayalam
       of the same gazette - the two are one script and one order and only
       differ in whether the characters have to be decoded before they are
       put in it
    '''
    pass
