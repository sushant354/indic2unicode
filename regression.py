import difflib
import codecs
import getopt
import sys
import os
import logging

from indic2unicode.fontconv import FontConv

class Regression:
    def __init__(self, populate, fontlist):
        self.populate        = populate
  
        self.fontConverter = FontConv()
        if fontlist:
            self.fontnames = fontlist 
        else:
            self.fontnames = self.fontConverter.uniqfonts

        self.testdir     = 'testdata'
        self.outdir      = 'output'
        self.diffdir     = 'diffs'
        self.expectdir   = 'expected'

        self.mk_dir(self.outdir)
        self.mk_dir(self.diffdir)
  
    def mk_dir(self, dirname):
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    def compute_diff(self, fontname):
        outfile    = os.path.join(self.outdir,    fontname)
        expectfile = os.path.join(self.expectdir, fontname)
        diffFile   = os.path.join(self.diffdir,   fontname)

        f = codecs.open(outfile, 'r', 'utf8')
        out = f.read()
        f.close()
        f = codecs.open(expectfile, 'r', 'utf8')
        expected = f.read()
        f.close()

        diffobj = difflib.unified_diff(expected.splitlines(1), \
                                       out.splitlines(1))
        lines   = list(diffobj)
        if len(lines) > 0:
            print('%s ... Failed. Check %s' %  (fontname, diffFile))
            diffhandle = codecs.open(diffFile, 'w', 'utf8')
            diffhandle.write(''.join(lines))
            diffhandle.close()
        else:
            print('%s ... OK' % fontname)

    def to_unicode(self, fontname):
        f = codecs.open(os.path.join(self.testdir, fontname), 'r', 'utf-8')
        testdata = f.read()
        f.close()
        out = self.fontConverter.to_unicode(fontname, testdata)

        if self.populate:
            outdir = self.expectdir
        else:
            outdir = self.outdir

        f = codecs.open(os.path.join(outdir, fontname), 'w', 'utf8') 
        f.write(out)
        f.close()       

    def run_tests(self):
        for fontname in self.fontnames:
            self.to_unicode(fontname)
            if not self.populate:
                self.compute_diff(fontname)

def print_usage(progname):
    print('Usage: %s [-f font1 -f font2 ...] [-p (populate)] [-h (help)]' % progname)
    sys.exit(0)

if __name__ == '__main__': 
    optlist = getopt.getopt(sys.argv[1:], 'f:ph')

    fontlist = []
    populate = False

    for  o, v in optlist[0]:
        if o == '-p':
            populate = True
        elif o == '-f':
            fontlist.append(v)
        elif o == '-h':
            print_usage(sys.argv[0])
        else:
            print_usage(sys.argv[0])

    logging.basicConfig(\
        level    = logging.DEBUG,  \
        format   = '%(asctime)s: %(name)s: %(levelname)s %(message)s', \
        datefmt  = '%Y-%m-%d %H:%M:%S', \
        filename = 'conv.log', \
        filemode = 'w' \
    )

    regressionObj = Regression(populate, fontlist)
    regressionObj.run_tests()
