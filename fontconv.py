from indic2unicode.fonts.hindi import aryan2, surekh, chanakya, arialuni, \
                                     nirmalaui
from indic2unicode.fonts.glyphs import arialuni_glyphs, nirmalaui_glyphs, \
                                       mangal_glyphs, nudiuni_glyphs, \
                                       tauelango_glyphs, ilasundaram_glyphs, \
                                       marutham_glyphs, meera_glyphs, \
                                       freeserif_glyphs, nats_glyphs
from indic2unicode.fonts.kannada import tunga, nudi, aklite
from indic2unicode.fonts.tamil import tamelango, vanavil, tommy
from indic2unicode.fonts.gujarati import krishna, krishnauni
from indic2unicode.fonts.malayalam import revathi
from indic2unicode.fonts.marathi import abhishek, dvotsurekh, sakal, yogesh
from indic2unicode.fonts.odiya import akruti, kalinga, shree
from indic2unicode.fonts.telugu import priyaanka, gautami

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
        revathiObj   = revathi.Revathi()
        yogeshObj    = yogesh.Yogesh()
        abhishekObj  = abhishek.Abhishek()
        dvotsurekhObj = dvotsurekh.DVOTSurekh()
        sakalObj     = sakal.Sakal()
        priyaankaObj = priyaanka.Priyaanka()
        gautamiObj   = gautami.Gautami()
        kalingaObj   = kalinga.Kalinga()
        shreeObj     = shree.Shree()
        akrutiObj    = akruti.Akruti()
        krishnaObj   = krishnauni.KrishnaUni()
        krishna8Obj  = krishna.Krishna()
        tauelangoObj = tauelango_glyphs.TauElangoPanchaliGlyphs()
        ilasundaramObj = ilasundaram_glyphs.UniIlaSundaramGlyphs()
        maruthamObj    = marutham_glyphs.TauMaruthamGlyphs()
        meeraObj       = meera_glyphs.MeeraUniGlyphs()
        freeserifObj   = freeserif_glyphs.FreeSerifUniGlyphs()
        natsObj        = nats_glyphs.NatsTeluguGlyphs()
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
            # the malayalam of the Kerala gazette. An 8 bit font of the
            # same kind again, and one whose bytes are the ML-TT layout
            # that the whole ML- family of fonts shares. The pdf font name
            # is a key here beside the short one
            'revathi': revathiObj, 'ML-Revathi-Normal': revathiObj,
            # the marathi of the Maharashtra gazette. An 8 bit font of the
            # same kind again, and one whose bytes are those of the windows
            # 1252 table. The three faces of it that the gazette carries
            # share the layout - only the weight of the glyphs differs -
            # so the pdf font name of each of them is a key here beside the
            # short one
            'yogesh': yogeshObj, 'DVBWTTYogeshNormal': yogeshObj,
            'DVBWTTYogeshBold': yogeshObj, 'DVBWTTYogeshItalic': yogeshObj,
            # the other marathi of the same gazette, the one the Mumbai
            # Suburban supplement is set in. A real opentype font, unlike
            # Yogesh above, and one whose ToUnicode map is not wrong about
            # what its glyphs say but about how much: two glyphs that stand
            # next to each other are handed the character on their boundary
            # each, so the extractor writes that character twice. The bare
            # font name is a key here, unlike for the repaired fonts below:
            # this converter reads the text of a pdf that nothing has
            # repaired, and both faces the gazette carries share the fault
            'abhishek': abhishekObj, 'FourCMRAbhishek': abhishekObj,
            'FourCMRAbhishek-Bold': abhishekObj,
            # the third marathi of the same gazette, the one the
            # notifications of the Mumbai Suburban supplement are set in. A
            # real opentype font like Abhishek above, and one whose
            # ToUnicode map is not wrong about any glyph it names - it just
            # names nothing but the 58 glyphs that stand for one character
            # on their own, so every half consonant, every conjunct, every
            # reph and every matra that carries a sign is missing from it
            # and reaches an extractor as its glyph id. The bare font name
            # is a key here, as it is for Abhishek: this converter reads the
            # text of a pdf that nothing has repaired, and both faces the
            # gazette carries share the same glyph ids
            # This converter's table is keyed by glyph id and every DVOT
            # face shares one glyph order, so the whole family reaches it -
            # DVOTYogeshMR is the same layout in another typeface, checked
            # glyph by glyph against DVOTSurekhMR. Beware of the two Yogesh
            # of this gazette, which are different fonts under names that
            # differ by three letters: DVOTYogeshMR is this one and
            # DVBWTTYogesh is the legacy 8 bit font of yogesh.py above
            'dvotsurekh': dvotsurekhObj,
            'DVOTSurekhMRNormal': dvotsurekhObj,
            'DVOTSurekhMRBold': dvotsurekhObj,
            'DVOTSurekhMRItalic': dvotsurekhObj,
            'DVOTYogeshMRNormal': dvotsurekhObj,
            'DVOTYogeshMRBold': dvotsurekhObj,
            'DVOTYogeshMRItalic': dvotsurekhObj,
            # the fourth marathi of the same gazette, the one the tables of
            # the Konkan divisional supplement are set in. The same glyph
            # order as the DVOT family above and a map that is short in the
            # same place, so it is that converter with three glyphs added to
            # its table - but this producer hands a glyph it cannot name a
            # private use character out of a numbering of its own rather
            # than leaving the glyph id behind, and it numbers the glyphs of
            # a subset afresh on every run. The bare font name is a key
            # here, as it is for the two fonts above: this converter reads
            # the text of a pdf that nothing has repaired, and it reads the
            # text of a repaired one as well, that being the reading
            # dvotsurekh.py already has
            'sakal': sakalObj, 'SakalMarathi': sakalObj,
            # the telugu of the Telangana gazette. An 8 bit font of the
            # same kind again, and one whose bytes are those of mac roman
            # rather than of a windows table - the pdf embeds it as a
            # TrueType subset whose map hands every glyph the character of
            # the mac roman byte it sits on. The pdf font name is a key
            # here beside the short one
            'priyaanka': priyaankaObj, 'PriyaankaBold': priyaankaObj,
            # the telugu that the Andhra Pradesh gazette sets the
            # notifications of its municipalities in. A real opentype font,
            # unlike Priyaanka above, and one whose ToUnicode map is not
            # wrong about a single glyph it names - it is only short, the
            # way the map of the DVOT family is: it names the letters of the
            # block, the vowel signs and the digits and leaves out
            # everything the shaper made, so every vattu, every dead
            # consonant and every syllable the font draws in one glyph
            # reaches an extractor as its glyph id. The bare font name is a
            # key here, as it is for the DVOT family: this converter reads
            # the text of a pdf that nothing has repaired, and it reads the
            # text of a repaired one as well, that being the reading it
            # already has. Both faces the gazette carries share one glyph
            # order
            'gautami': gautamiObj, 'Gautami': gautamiObj,
            'Gautami-Bold': gautamiObj,
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
            # the unicode malayalam of the Kerala gazette, and no bare font
            # name key here either, for the reason the converters above have
            # none: this is a reordering pass for the text of a pdf that
            # fix_tounicode.py has already repaired. That producer re-encodes
            # the font per subset and leaves the glyph behind every െ, േ and
            # ൈ out of its map altogether, so an unrepaired Meera is not
            # merely out of order - കേരള reaches an extractor as
            # കേ(cid:2)രള, with the ക missing outright. It is reached through
            # get_font_converter(), which names only the fonts that really
            # were repaired in this document
            'meera_glyphs': meeraObj,
            # the other unicode malayalam of the same gazette, and no bare
            # font name key here either, for the reason the converters above
            # have none: this is a reordering pass for the text of a pdf
            # that fix_tounicode.py has already repaired. mPDF re-encodes
            # the font per subset and hands every glyph the shaper made a
            # private use codepoint rather than a character, so an
            # unrepaired FreeSerif is not merely out of order - every
            # cluster and every syllable of it is missing outright. The bare
            # name would be the wrong thing to match on twice over, FreeSerif
            # being a latin face as much as a malayalam one. It is reached
            # through get_font_converter(), which names only the fonts that
            # really were repaired in this document
            'freeserif_glyphs': freeserifObj,
            # the telugu of the Andhra Pradesh gazette, and no bare font
            # name key here either, for the reason the converters above have
            # none: this is a reordering pass for the text of a pdf that
            # fix_tounicode.py has already repaired. That producer built the
            # map by pairing the glyphs of a cluster with the characters of
            # it, so an unrepaired NATS is not merely out of order - the
            # first cluster a glyph was drawn in decides what it says
            # everywhere, and అంతస్తు reaches an extractor as అంతసు. It is
            # reached through get_font_converter(), which names only the
            # fonts that really were repaired in this document
            'nats_glyphs': natsObj,
            # the odiya of the Odisha Gazette. A unicode font like Arial
            # Unicode MS and Nirmala UI above, and one whose pdfs carry a
            # map that was broken the same way - the glyphs of a run were
            # paired with the characters of it one by one and odiya shaping
            # draws a syllable in a different number of glyphs than it is
            # written in, so the pairing slips and ନିର୍ବାଚନ extracts as
            # ନିବ୍ଥାଚନ. The bare font name is a key here, as it is for those
            # two: this converter reads the text of a pdf that nothing has
            # repaired
            'kalinga': kalingaObj, 'Kalinga': kalingaObj,
            # the other odiya of the same gazette, the one its land
            # acquisition notifications are set in. A legacy 8 bit font of
            # the Shree-Lipi typing package, embedded as a simple TrueType
            # font with WinAnsiEncoding and no map at all, so its text
            # extracts as the cp1252 characters of the bytes that were
            # typed and ମାଲକାନଗିରି comes out as "þæàÿLÿæ[ÿSçÀÿç". The two
            # faces the gazette carries share this layout - only the weight
            # of the glyphs differs - so the pdf font name of each of them
            # is a key here beside the short one
            'shree': shreeObj, 'SHREE-ORI7-0601': shreeObj,
            'SHREE-ORI7-0602': shreeObj,
            # the third odiya of the same gazette, the one the rest of its
            # land acquisition notifications are set in. A legacy 8 bit
            # font of the Akruti typing package, embedded the same way as
            # Shree above and with a layout of its own, so ଓଡିଶା comes out
            # as "IWògû". The three faces the gazette carries share this
            # layout - the two Ashok differ only in the weight of the
            # glyphs and Koshal is a display face on the same keys - so the
            # pdf font name of each of them is a key here beside the short
            # one
            'akruti': akrutiObj,
            'AkrutiOriAshok-99Normal': akrutiObj,
            'AkrutiOriAshok-99Bold': akrutiObj,
            'AkrutiOriKoshal-99Normal': akrutiObj,
            # the gujarati of the Gujarat Government Gazette. A unicode font
            # like Arial Unicode MS, Nirmala UI and Kalinga above, and one
            # whose pdfs carry a map that was broken the same way - the
            # glyphs of a run were paired with the characters of it one by
            # one and gujarati draws a syllable in a different number of
            # glyphs than it is written in, so the pairing slips and કરવા
            # extracts as ર્રવા. The bare font name is a key here, as it is
            # for those three: this converter reads the text of a pdf that
            # nothing has repaired.
            # The bold face is a key here as well, and it is read by the
            # converter of the regular face rather than by one of its own.
            # The two faces are subsets with a map each, and each map was
            # broken over the first drawing of its own glyphs, so 'ર્' is ka
            # in the regular face and ma in the bold one - but one string of
            # characters is all that reaches a converter and the two cannot
            # be told apart in it. The regular face draws 24993 of the 25694
            # glyphs of the test document and is the one that is read; the
            # headings the bold face sets come out wrong, see the class
            # comment of fonts/gujarati/krishnauni.py
            'krishnauni': krishnaObj, 'KrishnaUni': krishnaObj,
            'KrishnaUni,Bold': krishnaObj,
            # the other gujarati of the same gazette, the one the orders of
            # its district magistrates are set in. A legacy 8 bit font of a
            # typing package, embedded as a simple TrueType font with
            # WinAnsiEncoding and no map at all, so its text extracts as the
            # cp1252 characters of the bytes that were typed and
            # જિલ્લા મેજીસ્ટ્રેટ દ્વારા comes out as "ìÉSáë Üõ°VËÿõË ¦ëßë".
            # The four faces the gazette carries share this layout - every
            # byte the other three draw was read in the words it stands in
            # against Krishna's own reading of it - so the pdf font name of
            # each of them is a key here beside the short one. Beware of
            # KrishnaUni above, which is a different font under a name that
            # differs by three letters: it is a unicode opentype font and
            # this is the legacy 8 bit one
            'krishna': krishna8Obj, 'Krishna': krishna8Obj,
            'KrishnaBold': krishna8Obj, 'Mani': krishna8Obj,
            'Suchitra': krishna8Obj,
        }

        self.uniqfonts = ['aryan2', 'surekh', 'chanakya', 'arialuni', \
                          'arialuni_glyphs', 'nirmalaui', 'nirmalaui_glyphs', \
                          'mangal_glyphs', 'tunga', 'nudi', \
                          'nudi_kannada_digits', 'aklite', \
                          'nudiuni_glyphs', 'tamelango', 'reginet', \
                          'tauelango_glyphs', 'ilasundaram_glyphs', \
                          'marutham_glyphs', 'vanavil', 'tommy', \
                          'revathi', 'meera_glyphs', 'freeserif_glyphs', \
                          'priyaanka', \
                          'gautami', \
                          'nats_glyphs', 'yogesh', 'abhishek', \
                          'dvotsurekh', 'sakal', 'kalinga', 'shree', 'akruti', \
                          'krishnauni', 'krishna']
 
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


