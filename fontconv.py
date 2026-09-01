from indic2unicode.fonts.hindi import aryan2, surekh, chanakya, arialuni, \
                                     nirmalaui
from indic2unicode.fonts.glyphs import arialuni_glyphs, nirmalaui_glyphs, \
                                       mangal_glyphs, nudiuni_glyphs
from indic2unicode.fonts.kannada import tunga, nudi, aklite
from indic2unicode.fonts.tamil import tamelango

class FontConv:
    def __init__(self):
        aryanObj = aryan2.Aryan2()
        surekhObj = surekh.Surekh()
        chanakyaObj = chanakya.Chanakya()
        arialuniObj = arialuni.ArialUni()
        glyphsObj   = arialuni_glyphs.ArialUniGlyphs()
        nirmalaObj  = nirmalaui.NirmalaUI()
        nirglyphObj = nirmalaui_glyphs.NirmalaUIGlyphs()
        mangalObj   = mangal_glyphs.MangalGlyphs()
        tungaObj    = tunga.Tunga()
        nudiObj     = nudi.Nudi()
        nudikObj    = nudi.NudiKannadaDigits()
        akliteObj   = aklite.Aklite()
        nudiuniObj  = nudiuni_glyphs.NudiUniGlyphs()
        tamelangoObj = tamelango.TamElango()
        self.converters = { 
            'aryan2': aryanObj, 'divya':  aryanObj, 'surekh': surekhObj,
            'chanakya': chanakyaObj, 'krutidev': chanakyaObj,  
            'vivek': chanakyaObj, 'devlys': chanakyaObj, 
            'arialuni': arialuniObj, 
            'Arial Unicode MS': arialuniObj,  'arialuni_glyphs': glyphsObj, 
            'nirmalaui': nirmalaObj, 'Nirmala UI': nirmalaObj, 
            'nirmalaui_glyphs': nirglyphObj, 
            # no bare 'Mangal' key here, unlike the two fonts above: theirs
            # name the lossy converters, which are for the text of a pdf that
            # was never repaired, while mangal_glyphs only reorders text the
            # repair already put right. A Mangal whose map is sound extracts
            # correct text, and name matching it onto a reordering pass would
            # turn निर्माण into नर्मिाण - so this converter is reached through
            # get_repaired_font_res() alone, which names only the fonts that
            # were actually repaired in this document
            'mangal_glyphs': mangalObj,
            'tunga': tungaObj, 'Tunga': tungaObj, 'Tunga-Bold': tungaObj,
            # the weights of Nudi differ only in what the digit keys draw,
            # the roman ones the latin digits and the kannada ones the
            # kannada digits, so the 15 on the cover of a gazette is ೧೫
            'nudi': nudiObj, 'Nudi01e': nudiObj, 'Nudi01e,Bold': nudiObj,
            'Nudi05e': nudiObj,
            'nudi_kannada_digits': nudikObj, 'Nudi01k': nudikObj,
            'Nudi01k,Bold': nudikObj,
            # the masthead of the Karnataka gazette. An 8-bit font like
            # Nudi, and named after nothing but itself in the pdfs that
            # carry it, so the whole pdf font name is a key here too
            'aklite': akliteObj, 'AkliteKndIpsita': akliteObj,
            # no bare 'NudiUni01e' key here, for the reason mangal_glyphs
            # has none: this is a reordering pass for the text of a pdf
            # that fix_tounicode.py has already repaired, and a NudiUni
            # that was not repaired is not in that order - its shaped
            # glyphs are missing from the text rather than misplaced in it.
            # It is reached through get_font_converter(), which names only
            # the fonts that really were repaired in this document
            'nudiuni_glyphs': nudiuniObj,
            # the tamil of the Tamil Nadu gazette. An 8-bit font like Nudi,
            # and the whole TAM_ELANGO family shares the TAM layout, so the
            # family name is a key here beside the faces the corpus carries
            'tamelango': tamelangoObj, 'tam_elango': tamelangoObj,
            'TAM_ELANGO_Panchali': tamelangoObj,
            'TAM_ELANGO_Kapilan': tamelangoObj,
        }

        self.uniqfonts = ['aryan2', 'surekh', 'chanakya', 'arialuni', \
                          'arialuni_glyphs', 'nirmalaui', 'nirmalaui_glyphs', \
                          'mangal_glyphs', 'tunga', 'nudi', \
                          'nudi_kannada_digits', 'aklite', \
                          'nudiuni_glyphs', 'tamelango']
 
    def to_unicode(self, fontname, text):
        return self.converters[fontname].to_unicode(text)

def print_usage():
    print('''
USAGE:    
    python fontconv.py [-e encoding] -f fontname input_file output_file
    default encoding is utf8
''')
if __name__ == '__main__':
    import codecs
    import getopt
    import sys

    optlist = getopt.getopt(sys.argv[1:], 'e:f:h')

    fontname = None

    encoding = 'utf-8'
    for o, v in optlist[0]:
        if o == '-e':
            encoding = v
        elif o == '-h':
            print_usage()
            sys.exit(0)
        elif o == '-f':
            fontname = v

    if len(optlist[1]) != 2:
        print_usage()
        sys.exit(0)

    inputfile  = optlist[1][0]
    outputfile = optlist[1][1]

    font_convertor = FontConv()
    if not fontname:
        print('ERR: Supply a fontname')
        print_usage()
        sys.exit(0)
 
    if fontname not in font_convertor.converters:
        print('ERR: %s font not supported yet. Supported fonts are %s' % \
               (fontname, list(font_convertor.converters.keys())))
        sys.exit(0)

    f = codecs.open(inputfile, 'r', encoding)
    testdata = f.read()
    f.close()

    out = font_convertor.to_unicode(fontname, testdata)
    # every character that the font has no token for was reported the first
    # time it was seen, here is how often each of them turned up
    font_convertor.converters[fontname].log_error_summary()

    f = codecs.open(outputfile, 'w', 'utf8')
    f.write(out)
    f.close()


