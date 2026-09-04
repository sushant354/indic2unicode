from ..telugu.nats import NatsGlyphs

class NatsTeluguGlyphs(NatsGlyphs):
    '''The text of a pdf set in NATS whose ToUnicode map has been repaired by
       tools/fix_tounicode.py, named here beside the other converters that
       read a repaired pdf so the family is in one place.

       The pass itself lives in fonts/telugu/nats.py, beside
       fonts/telugu/priyaanka.py, which decodes the legacy 8 bit telugu of
       the Telangana gazette - the two are one script and one order and only
       differ in whether the characters have to be decoded before they are
       put in it
    '''
    pass
