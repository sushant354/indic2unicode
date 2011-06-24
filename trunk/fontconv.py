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
