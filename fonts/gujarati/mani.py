from .krishna import Krishna

class Mani(Krishna):
    '''Mani is a face of the same legacy 8 bit typing package as Krishna, and
       the Gujarat Government Gazette sets the headings of the orders of its
       district magistrates and the tables of their forms in it. The pdf
       embeds it the way it embeds Krishna, as a simple TrueType font with
       WinAnsiEncoding, and the ToUnicode map it carries hands every byte
       back as the latin-1 character of that byte - so its text extracts as
       the same cp1252 characters of the bytes that were typed, and
       ભારતીય નાગરિક સુરક્ષા સંહિતા comes out as "ÛëßÖíÝ ÞëÃßíÀ çðßZëë ç_ìèÖë".

       THE SAME LAYOUT AS KRISHNA

       Every byte this face draws that fonts/gujarati/krishna.py has a
       reading for draws the glyph that reading says, which the outlines of
       the face the pdf embeds were checked against glyph by glyph - ુ has
       the same three glyphs ð, < and \\ here, ૂ the same two, ñ and ^, and
       w is the રૂ of that table and not a રુ. So this converter is that one,
       with two glyphs added to its table and one rule added to its rules.

       THE TWO HALF FORMS KRISHNA'S TABLE DOES NOT HAVE

       P is ભ્ and R is ય્, each of them the letter without its upright. The
       heading of the last order of the test document is typed out of half
       forms and uprights where the letters have keys of their own - ભારતીય
       નાગરિક as P, ા, ા, ર, ત, ી, R, ા and L, ા, ા, ગ, િ, ર, ક - which the
       rules of Krishna put back together as readily as they do ણ. The
       Krishna of the same document draws ભ્ and ય્ on those two bytes as
       well, the ય of ઉપયોગ being typed as an R and an upright, so they are
       glyphs of the layout rather than of this face; the document
       krishna.py was read off just never draws them.

       THE ANUSVARA THAT IS TYPED IN FRONT OF ુ

       ં is drawn over its letter and ુ under it, so the order the two are
       typed in does not show on the page, and માલીકનું is typed as મ, ા,
       લ, ી, ક, ન, ં, ુ. Unicode writes the vowel sign of a letter in front
       of the anusvara over it, so the two are swapped back. A sign never
       follows an anusvara in unicode gujarati, so an anusvara that a ુ or a
       ૂ follows is always this.

       WHAT THE READINGS WERE CHECKED AGAINST

       Of the 546 words of gujarati this converter writes for the runs of
       this face in the test document, 504 are read back word for word by an
       OCR of the same pages. 24 of the 42 that are not are the OCR's own:
       it reads નાગરિકતા as નાગરિક્તા and રેફરન્સ as રેકરન્સ, drops the reph
       of ઓળખકાર્ડ, runs અગાઉ into the જે behind it and garbles the digits of
       a date. The other 18 are what the typist typed rather than what the
       word is - પુરૂં for પૂરું, મુળ for મૂળ, વ્યકિત for વ્યક્તિ and ઃ, the
       visarga, for the colon that ends a heading. Those come out here as
       the pdf says they were drawn, as they do in krishna.py.
    '''
    MORE_GLYPHS = {'DEAD_BHA': ['P'], 'DEAD_YA': ['R']}

    def get_compose_tokens(self):
        '''the rules of Krishna and the anusvara that is typed in front of a
           ુ or a ૂ, see the class comment'''
        composeTokens = Krishna.get_compose_tokens(self)

        composeTokens[('ANUSVARA', 'MATRA_U')]  = ['MATRA_U', 'ANUSVARA']
        composeTokens[('ANUSVARA', 'MATRA_UU')] = ['MATRA_UU', 'ANUSVARA']

        return composeTokens
