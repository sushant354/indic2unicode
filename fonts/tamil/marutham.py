from .tauelango import TauElangoGlyphs

class MaruthamGlyphs(TauElangoGlyphs):
    '''The text of a pdf that is set in TAU-Marutham - the third tamil of the
       Tamil Nadu gazette, drawn in 163 of the 8,248 documents of that corpus
       and very often beside TAM_ELANGO_Panchali on the same page - and whose
       ToUnicode map has been rebuilt by tools/fix_tounicode.py.

       WHY THE FONT NEEDS A REPAIR AND NOT A DECODER

       It looks at first like the legacy 8 bit fonts of the same gazette:
       much of a document's text is drawn by simple TrueType fonts with
       WinAnsiEncoding or MacRomanEncoding and no ToUnicode at all, and it
       extracts as latin gibberish exactly as TAM_ELANGO_Panchali's does. It
       is not one of those, and a decoder of the kind fonts/tamil/tamelango.py
       is could not read it: this producer re-encodes the font per subset,
       handing each one whatever latin bytes it needs in the order that
       document wanted them, so the same character is a different glyph in
       the next subset of the same document - 'k' is கு in one and கூ in the
       next. The rest of the text is drawn by Type0/Identity-H embeddings of
       the same font, whose own maps name the letters and the pulli forms and
       hand every syllable the font draws as one glyph either one of those
       latin letters or nothing at all. What every embedding does agree on is
       the glyph id, so the repair is done there, before anything reads the
       pdf - see TAU_MARUTHAM in tools/fix_tounicode.py - and what is left for
       this pass is what is left for fonts/tamil/tauelango.py: the order.

       WHY IT IS THAT PASS AND NOTHING MORE

       Once the map is right the two fonts are one script drawn one way.
       TAU-Marutham draws the vowel signs ெ, ே and ை in front of the letter
       they belong to, draws ொ and ோ in two halves with the letter between
       them - அச்சகத் தொழிலில் is drawn அ ச் ச க த் ெ த ா ழி ல ி ல் - and
       draws a consonant with the pulli or with one of ி, ீ, ு and ூ on it
       as a single glyph, which is the whole of what TauElangoGlyphs reads.
       Everything that differs between the two fonts differs in which glyph
       id carries what, and that is a question for the repair table and not
       for this pass, so this class is that pass whole, the way
       fonts/tamil/ilasundaram.py is.

       The one rule it inherits without being exercised on it is ௌ. This
       font draws that sign the way TAU Elango does, out of a ெ in front of
       the letter and the length mark ௗ behind it, but no subset of this
       corpus carries a glyph for the mark and no map of it names one, so
       TAU_MARUTHAM has no reading for it and the ெ in front of it has
       nothing to be composed with
    '''
    pass
