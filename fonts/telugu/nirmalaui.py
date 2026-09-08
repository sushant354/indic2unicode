import re

from indic2unicode.langs import telugu
from .nats import NatsGlyphs

class NirmalaUITeluguGlyphs(NatsGlyphs):
    '''The telugu of a pdf set in Nirmala UI whose ToUnicode map has been
       repaired by tools/fix_tounicode.py, the Andhra Pradesh gazette being
       set in Nirmala UI as well as in NATS. Every glyph now carries the
       characters it really stands for - the letters that the font writes
       the vowel sign u into, which the broken map hands the wrong syllable
       of the document and which nothing in the subset names, are all back -
       so వార్డుల no longer extracts as వార్డ్డల and ఒడ్డు no longer as ఒడ్డ్డ.

       What is left is the order, and there this font draws telugu the way
       NATS draws it, so this is that pass with one thing added.

       WHAT NATS ALREADY PUTS RIGHT

       Telugu draws the mark of a syllable on the body of it and hangs the
       vattus under that body, so the mark is drawn before them and unicode
       writes it behind them: ముగుస్తుంది is drawn ము గు సు ్త ం ది and
       వార్డుల is drawn వా రు ్డ ల. reorder_vattus() moves every vattu in
       front of the marks it was drawn behind, and the pollu of a dead
       consonant is one of those marks, so it ends up behind the whole
       cluster where unicode writes it.

       THE VATTU OF RA THAT IS DRAWN IN FRONT OF ITS LETTER

       Nirmala UI draws that one vattu in two places. Under the letter it
       belongs to, the way every other vattu is drawn, in శ్రీ - and in front
       of that letter otherwise, as the stroke ప్రభుత్వం and క్రింద are drawn
       with, where the glyph is stored in front of its letter too. So
       ప్రభుత్వం comes out of the repaired pdf as ్రపభుత్వం, ఆంధ్రప్రదేశ్ as
       ఆం్రధ్రపదేశ్ and రిజిస్ట్రార్ as రిజి్రసా్టర్.

       Both are spelled ్ర and the two could not be told apart in the text -
       శీ్ర and మే్రసి్త are the same run of a letter, a vowel sign, a ్ర and
       a letter, and the first of them is శ్రీ while the second is మేస్త్రి -
       so the repair writes langs/telugu.PREBASE_RA_MARK into the pre-base
       one, between its virama and its ra, and the lexer holds PREBASE_RA to
       that mark.

       It jumps over the letter it was drawn in front of and lands behind
       the vattus of that letter, which is where unicode writes it: the
       ్ట of రిజిస్ట్రార్ is drawn behind the స and the ్ర belongs behind
       both. The vattus have already been moved in front of the marks of
       their syllable by then, so the jump is over the letter alone and
       over the vattus that now follow it, and a second pre-base ra is not
       one of those - it belongs to the letter after it, which is what
       carries the two ్ర of ఆంధ్రప్రదేశ్ to the letters they belong to.

       WHAT THE EXTRACTOR PUTS IN THE MIDDLE OF A WORD

       The glyph of that vattu has almost no width of its own, so an
       extractor writes a line break behind it every now and then, ప్రభుత్వం
       coming out as "్ర\\nపభుత్వం". That whitespace is no glyph of the font
       and a converter cannot tell it from a real space, so it is left where
       it is - but the pre-base ra steps over it on its way to its letter,
       there being no word that ends with one.
    '''
    def __init__(self):
        NatsGlyphs.__init__(self)
        # the pre-base ra, which the language names the two characters of.
        # Its rule is made by extra_rules() rather than read off this, the
        # pattern of it being those characters with the mark between them,
        # so this is only what the token is written back out as
        self.langobjs.append(telugu.NirmalaUI())

        # the vattu of ra that is drawn in front of the letter it belongs to
        # and is stored in front of it as well
        self.waitdict = {'PREBASE_RA': 1}

        # while it waits for its letter it steps over the whitespace that
        # the extractor writes behind it, and once it has that letter it
        # steps over the vattus that hang under it as well - those have been
        # moved in front of the marks of the syllable already, so they
        # follow the letter by the time this runs
        self.waitover = set(self.WHITESPACE)
        self.waitover.update(self.vattus)

    # the whitespace that the extractor writes behind the pre-base ra, which
    # that ra has to step over on its way to its letter. NATS needs no token
    # for any of it - a character that no rule matched comes out the way it
    # went in - but a token is what makes it transparent to the pass below
    WHITESPACE = ('SPACE', 'NEWLINE', 'CARRIAGERET', 'TAB')

    def extra_rules(self):
        '''the pre-base ra, which is spelled like the vattu of ra that the
           font hangs under its letter and is held apart from it by the mark
           the repair writes into it - see langs/telugu.PREBASE_RA_MARK -
           and the whitespace it steps over. ply orders its string rules by
           falling length, so the pattern of the pre-base ra always wins
           over the VATTU_RA it starts with'''
        uMap  = telugu.TeluguUnicode().tokendict
        rules = {tokenName: re.escape(uMap[tokenName]) \
                 for tokenName in self.WHITESPACE}

        rules['PREBASE_RA'] = re.escape(uMap['VIRAMA'] + \
                                        telugu.PREBASE_RA_MARK + uMap['RA'])
        return rules

    def to_unicode(self, data):
        '''the passes in the order this font needs them: the vattus are
           moved in front of the marks of their syllable before the pre-base
           ra jumps, so that it lands behind them, and the two halves of a
           sign the font draws in two pieces are joined last, as they are
           for NATS'''
        tokentypes = self.tokenize(data)

        tokentypes = self.reorder_vattus(tokentypes)
        tokentypes = self.jump_after_tokens(tokentypes)
        tokentypes = self.compose_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)
