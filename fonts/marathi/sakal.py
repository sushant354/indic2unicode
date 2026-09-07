from .dvotsurekh import DVOTSurekh


class Sakal(DVOTSurekh):
    '''The marathi of a pdf that is set in SakalMarathi, the font the Konkan
       divisional supplement of the Maharashtra gazette sets the tables and
       the notifications of its zilla parishad orders in.

       THE SAME GLYPH ORDER AS THE DVOT FAMILY

       This font numbers its glyphs the way fonts/marathi/dvotsurekh.py reads
       them: ka is 84, ra is 111, the matra aa is 123, the reph is 171, the
       half la is 202, the matra i that carries an anusvar is 523 and the
       matra aa that carries a reph is 597, exactly as they are in
       DVOTSurekhMR and DVOTYogeshMR. All 112 of the ids this document draws
       were checked - the 80 the ToUnicode map names against what it says
       they are, and the 32 it does not against the OCR of the page - and
       none of them disagrees with that table, so this converter is that
       converter with three glyphs added to its table and one pass in front
       of it.

       The two are not the same typeface and not the same font: this one
       counts 713 glyphs against DVOT's 691 and draws the la of the alphabet
       at 497 rather than at 113, which its own map names correctly. It is
       the order they number their letters in that is one order.

       WHAT THE TEXT OF SUCH A PDF LOOKS LIKE

       The same as DVOT's, and short in the same place. The font is carried
       as a Type0/Identity-H font and its ToUnicode map is not wrong about
       any glyph it names, but it names only the glyphs that stand for one
       character on their own: every half consonant, every conjunct the font
       has a ligature for, the reph and every matra that carries an anusvar
       or a reph is missing from it.

       The digits are the exception to the map being right. This font draws
       the devanagari digits twice over, at 158..167 and again at 19..28, the
       two runs of glyphs being the same ten outlines, and the map calls the
       second run the latin digits - so the ५० of a table extracts as "50".
       They are read as devanagari here, which is what the DIGITS of
       DVOT-Surekh already do for the simple embedding of that font.

       WHAT STANDS IN FOR THE GLYPHS THE MAP LEAVES OUT

       Not the glyph id, which is what an extractor is left to write for a
       DVOT pdf, but a private use character: this producer hands every glyph
       it cannot name one out of U+F000..U+F0FF. Those codes are the
       producer's own numbering and not the font's - it numbers the unnamed
       glyphs of a subset in an order of its own, and a second run of it over
       the same font numbers them differently.

       This document carries two such numberings, because it is two
       documents. Pages 4 to 19 are set from one subset, whose 16 font
       dictionaries agree glyph for glyph, and pages 2 and 3 carry a placed
       pdf that came in from somewhere else with a subset and a map of its
       own. The two agree on four codes and disagree on everything else, so
       सिंधुदुर्ग जिल्हा extracts as

           <F04E>सधुदुग<F040> िज<F03E>हा   on page 4, and
           <F043>सधुदुग<F041> िज<F032>हा   on page 2

       and six codes name one glyph in one of them and another glyph in the
       other - U+F043 above is the matra i with an anusvar on page 2 and the
       matra aa with a reph on page 4.

       So a table of these codes is a table about a producer's run and not
       about a font, and NUMBERINGS below is what the two runs of this
       document say. A pdf printed by a third run would need a third column
       of it, and the repair for a document that has one is
       tools/fix_tounicode.py, which writes the glyphs of SAKAL_MARATHI over
       whatever private use characters the map hands them and leaves nothing
       for a numbering to be wrong about. What comes out of such a repair is
       the characters the glyphs draw in the order they are drawn in, which
       is the second reading fonts/marathi/dvotsurekh.py already has, so it
       goes through this converter unchanged - the text of a repaired pdf and
       of an unrepaired one convert to the same marathi.

       WHICH NUMBERING A RUN IS IN

       Eight codes occur only in the numbering of pages 2 and 3 and
       twenty-two only in the numbering of the rest, so a line of text that
       carries any of those thirty says which numbering it is in - and a line
       of marathi that carries a private use character at all almost always
       carries one of them, the reph and the half la being among them. A line
       that carries none keeps the numbering of the line in front of it,
       since a page is set from one subset and a caller hands this converter
       the runs of a document in the order they stand on the page. The
       numbering of the 16 subsets is the one a run starts out in.
    '''

    # THE THREE GLYPHS THIS DOCUMENT DRAWS THAT THE DVOT TABLE DOES NOT
    # NAME. Each was read off the OCR of the word it stands in - संख्या,
    # याद्वारे and निश्चिती - and each sits where that table would put it, the
    # half kha next to the half ka of 175 and the two conjuncts among the
    # ligatures of the 400s
    GLYPHS = dict(DVOTSurekh.GLYPHS, **{\
        'ADHA_KHA' : [176], 'DAWA' : [462], 'SHACA' : [473], \
    })

    # THE PRIVATE USE CHARACTER EVERY UNNAMED GLYPH IS HANDED, by glyph id,
    # in each of the two numberings this document is printed in - the one of
    # the 16 subsets of pages 4 to 19 first, then the one of the placed pdf
    # of pages 2 and 3. The second is the shorter of the two because those
    # two pages draw fewer of these glyphs, not because its numbering stops
    # there: what it calls a glyph it never draws is not in this document to
    # be read
    NUMBERINGS = [\
        {169: 0xf033, 171: 0xf040, 175: 0xf04c, 176: 0xf05b, 180: 0xf011, \
         182: 0xf004, 189: 0xf048, 190: 0xf04a, 193: 0xf047, 194: 0xf03d, \
         195: 0xf056, 199: 0xf06f, 202: 0xf03e, 204: 0xf06b, 205: 0xf02f, \
         206: 0xf035, 270: 0xf012, 280: 0xf045, 285: 0xf02d, 287: 0xf068, \
         290: 0xf01e, 292: 0xf06d, 462: 0xf05a, 471: 0xf055, 473: 0xf04d, \
         514: 0xf06c, 515: 0xf060, 523: 0xf04e, 531: 0xf039, 535: 0xf066, \
         536: 0xf06a, 597: 0xf043},                                       \
                                                                          \
        {169: 0xf036, 171: 0xf041, 176: 0xf05c, 194: 0xf03f, 195: 0xf056, \
         199: 0xf06d, 202: 0xf032, 204: 0xf069, 270: 0xf012, 287: 0xf066, \
         290: 0xf01e, 292: 0xf06b, 471: 0xf055, 514: 0xf06a, 515: 0xf061, \
         523: 0xf043, 535: 0xf064, 597: 0xf04c},                          \
    ]

    def __init__(self):
        DVOTSurekh.__init__(self)

        # the character a glyph was handed -> the character of its glyph id,
        # which is what the lexer of DVOT-Surekh reads
        self.numberings = [\
            {chr(code): chr(gid) for gid, code in numbering.items()} \
            for numbering in self.NUMBERINGS]

        # the codes that one numbering alone has, or that the two of them
        # hand different glyphs. A line that carries one of them says which
        # numbering it is written in
        self.numbering_marks = []
        for i, table in enumerate(self.numberings):
            other = self.numberings[1 - i]
            self.numbering_marks.append(\
                set([code for code, gid in table.items() \
                     if other.get(code) != gid]))

        # the numbering a run starts out in, and the one every line stays in
        # until a line of it says otherwise
        self.numbering = 0

    def pick_numbering(self, line):
        '''which of the two numberings a line of a run is written in. A line
           that says nothing either way is in the numbering of the line in
           front of it'''
        counts = [len([c for c in line if c in marks]) \
                  for marks in self.numbering_marks]

        if counts[0] != counts[1]:
            return 0 if counts[0] > counts[1] else 1

        return self.numbering

    def glyph_codes(self, data):
        '''the text of a run with every private use character rewritten to
           the character of the glyph id it was handed for'''
        out = []
        for line in data.splitlines(True):
            self.numbering = self.pick_numbering(line)
            table = self.numberings[self.numbering]
            out.append(''.join([table.get(char, char) for char in line]))

        return ''.join(out)

    def to_unicode(self, data):
        return DVOTSurekh.to_unicode(self, self.glyph_codes(data))
