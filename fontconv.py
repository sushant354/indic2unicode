from fonts import aryan2, surekh

class FontConv:
    def __init__(self):
        aryanObj = aryan2.Aryan2()
        surekhObj = surekh.Surekh()
        self.converters = {'aryan2': aryanObj, 'divya':  aryanObj, \
                           'surekh': surekhObj}
   
        self.uniqfonts = ['aryan2', 'surekh']
 
    def to_unicode(self, fontname, text):
        return self.converters[fontname].to_unicode(text)

def print_usage():
    print '''
USAGE:    
    python fontconv.py [-e encoding] -f fontname input_file output_file
    default encoding is utf8
'''
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
        print 'ERR: Supply a fontname'
        print_usage()
        sys.exit(0)
 
    if fontname not in font_convertor.converters:
        print 'ERR: %s font not supported yet. Supported fonts are %s' % \
               (fontname, font_convertor.converters.keys())
        sys.exit(0)

    f = codecs.open(inputfile, 'r', encoding)
    testdata = f.read()
    f.close()

    out = font_convertor.to_unicode(fontname, testdata)
    f = codecs.open(outputfile, 'w', 'utf8')
    f.write(out)
    f.close()


