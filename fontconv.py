from indic2unicode.fonts.hindi import aryan2, surekh, chanakya, arialuni, \
                                     nirmalaui
from indic2unicode.fonts.glyphs import arialuni_glyphs, nirmalaui_glyphs, \
                                       mangal_glyphs, nudiuni_glyphs, \
                                       tauelango_glyphs, ilasundaram_glyphs, \
                                       marutham_glyphs
from indic2unicode.fonts.kannada import tunga, nudi, aklite
from indic2unicode.fonts.tamil import tamelango, vanavil, tommy

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
        vanavilObj   = vanavil.Vanavil()
        tommyObj     = tommy.Tommy()
        tauelangoObj = tauelango_glyphs.TauElangoPanchaliGlyphs()
        ilasundaramObj = ilasundaram_glyphs.UniIlaSundaramGlyphs()
        maruthamObj    = marutham_glyphs.TauMaruthamGlyphs()
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
            # Reginet, the tamil font of the Tamil Nadu Registrar of
            # Societies gazette notifications. Its text extracts as the
            # same cp1252 byte-per-glyph gibberish as TAM_ELANGO's and every
            # byte of it was checked against tamelango's table with no
            # exception, so it is the same encoding under another name
            # rather than a font of its own
            'reginet': tamelangoObj,
            # the tamil of the Vanavil typing package, an 8 bit font of
            # the same kind and, after those two, the most drawn font of the
            # Tamil Nadu gazette. One key for the family: every face of it a
            # document carries (VANAVILAvvaiyar, VANAVILAvvaiyarBold,
            # VANAVIL-Avvaiyar, VANAVILDBAvvaiyarBold, VANAVILAlayarasi)
            # shares this encoding. The same typeface is also carried in the
            # TAM layout and in the TAB one, and those name themselves with
            # the layout in front of the typeface (TAMVANAVILAvvaiyar,
            # TAM-VANAVIL-Avvaiyar, TABVanavilAvvaiyar) - the first of those
            # two is tamelango's above and the second has no converter here
            # at all, so a caller matching this key on a pdf font name has
            # to hold it to a name that starts with it
            'vanavil': vanavilObj,
            # the tamil of the Sun typing package. An 8 bit font of the same
            # kind again, and one whose layout is neither TAM's nor
            # Vanavil's: the letters sit on the lowercase keys and the shift
            # of a key is the long form of what the key draws. The pdf font
            # name is a key here beside the short one, this font naming
            # itself after nothing but itself
            'tommy': tommyObj, 'Sun-TommyTamilNormal': tommyObj,
            # no bare 'TAUElangoPanchali' key here, for the reason
            # mangal_glyphs and nudiuni_glyphs have none: this is a
            # reordering pass for the text of a pdf that fix_tounicode.py
            # has already repaired, and an unrepaired TAUElangoPanchali is
            # not merely out of order - its map hands the glyphs the wrong
            # characters outright, and reordering those would only move the
            # wrong text about. It is reached through get_font_converter(),
            # which names only the fonts that really were repaired in this
            # document
            'tauelango_glyphs': tauelangoObj,
            # the other tamil of the same gazette, and no bare font name key
            # here either, for the same reason: an unrepaired
            # Uni-Ila.Sundaram is not merely out of order - its map hands the
            # first glyph of every cluster the whole cluster and the glyphs
            # behind it the cluster's last character, so மாவட்டம் extracts as
            # மாாவட்டம். It is reached through get_font_converter(), which
            # names only the fonts that really were repaired in this document
            'ilasundaram_glyphs': ilasundaramObj,
            # the third tamil of the same gazette, and no bare font name key
            # here either. That producer re-encodes the font per subset, so
            # an unrepaired TAU-Marutham does not carry one wrong reading of
            # its glyphs but a different one in every subset - the same
            # latin letter is கு in one of them and கூ in the next - and
            # nothing a converter could be given would decode it. It is
            # reached through get_font_converter(), which names only the
            # fonts that really were repaired in this document
            'marutham_glyphs': maruthamObj,
        }

        self.uniqfonts = ['aryan2', 'surekh', 'chanakya', 'arialuni', \
                          'arialuni_glyphs', 'nirmalaui', 'nirmalaui_glyphs', \
                          'mangal_glyphs', 'tunga', 'nudi', \
                          'nudi_kannada_digits', 'aklite', \
                          'nudiuni_glyphs', 'tamelango', 'reginet', \
                          'tauelango_glyphs', 'ilasundaram_glyphs', \
                          'marutham_glyphs', 'vanavil', 'tommy']
 
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


