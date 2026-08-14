import logging
import types
import unicodedata

# a character that the lexer of a font has no token of its own for but that
# is text rather than a glyph of that font travels through the passes as
# (LITERAL, character), see is_text_char() and fonts/arialuni_glyphs.py
LITERAL = 'LITERAL'

class BaseFont:
    def __init__(self):
        self.langobjs      = []
        self.lexer         = None
        self.composeTokens = {}
        self.jumpbefore    = {}
        self.waitdict      = {}
        # tokens that are transparent to the two reordering passes.
        # jumpover : not counted while another token jumps backwards over it
        # waitover : not counted while another token is waiting to jump
        #            ahead, and the waiting token stays behind it
        # halftokens: not counted while another token is waiting to jump
        #            ahead, but the waiting token is emitted before it as it
        #            belongs to the syllable that is still coming
        self.jumpover      = set()
        self.waitover      = set()
        self.halftokens    = set()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.errchars      = {}

    def num_before(self, tokenName): 
        if tokenName in self.jumpbefore:
            return self.jumpbefore[tokenName]
        else:
            return 0

    def num_after(self, tokenName):
        if tokenName in self.waitdict:
            return self.waitdict[tokenName]
        else:
            return 0

    def is_text_char(self, char):
        '''whether a character that the lexer has no token for is text that
           can be handed on as it is - an ellipsis, a bullet, a zero width
           joiner - rather than a glyph code that no map could turn into a
           character, which is all a control character or a private use
           character can be here'''
        if char in '\t\n\r':
            return True

        return unicodedata.category(char) not in ('Cc', 'Co', 'Cn', 'Cs')

    def is_invisible_literal(self, tokenName):
        '''whether a token is a character carried through as itself that
           marks a join in the text rather than standing on the page - a
           zero width joiner, a zero width non joiner. It is no glyph of the
           syllable it sits in, so the two reordering passes have to look
           straight through it: a matra_i that has one between itself and
           its consonant is still waiting for that consonant'''
        return type(tokenName) == tuple and tokenName[0] == LITERAL and \
               unicodedata.category(tokenName[1]) == 'Cf'

    def token_to_unicode(self, tokenName):
        if type(tokenName) == tuple and tokenName[0] == LITERAL:
            return tokenName[1]

        for obj in self.langobjs:
            ustr = obj.get_unicode_string(tokenName)
            if ustr != None:
                return ustr

        return None

    def multiple_tokens(self, tokenName):
        for obj in self.langobjs:
            tokens = obj.multiple_tokens(tokenName)
            if tokens != None:
                return tokens

        return None

    def match_tokenlist(self, composelist, tlist, i):
        if len(composelist) > len(tlist) - i:
            return False

        for x in composelist:
            if x != tlist[i]:
                return False
            i += 1
        return True

    def tokenize(self, data):
        tokentypes = []
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             if tok.type == LITERAL:
                 # a character that is text and not a glyph of the font
                 # carries itself through the passes
                 tokentypes.append((LITERAL, tok.value))
                 continue
             multipleTokens = self.multiple_tokens(tok.type)
             if multipleTokens:
                 tokentypes.extend(multipleTokens)
             else:
                 tokentypes.append(tok.type)
        return tokentypes

    def jump_before_tokens(self, tokentypes):
        out = []
        for t in tokentypes:
            num   = self.num_before(t)
            index = len(out)
            while num > 0 and index > 0:
                index -= 1
                if out[index] not in self.jumpover and \
                        not self.is_invisible_literal(out[index]):
                    num -= 1

            if num > 0:
                # not enough tokens to jump over
                out.append(t)
            else:
                out.insert(index, t)
        return out

    def jump_after_tokens(self, tokentypes):
        out = []
        waitTokens = []
        for toktype in tokentypes:
             num = self.num_after(toktype)
             if num != 0:
                 waitTokens.append([toktype, num])
             elif toktype in self.waitover or self.is_invisible_literal(toktype):
                 out.append(toktype)
             else:
                 pending = waitTokens
                 waitTokens = []
                 for waitToken in pending:
                     if waitToken[1] == 0:
                         out.append(waitToken[0])
                     elif toktype in self.halftokens:
                         waitTokens.append(waitToken)
                     else:
                         waitToken[1] -= 1
                         waitTokens.append(waitToken)
                 out.append(toktype)

        for waitToken in waitTokens:
            out.append(waitToken[0])
        return out

    def compose_tokens(self, out1):
        for compose in list(self.composeTokens.keys()):
            out2 = []
            repl = self.composeTokens[compose]
            i = 0

            while i < len(out1):
                if self.match_tokenlist(compose, out1, i): 
                    if type(repl) == list:
                        out2.extend(repl)
                    else:
                        out2.append(repl)
                    i += len(compose)
                else:
                    out2.append(out1[i])
                    i += 1
            out1 = out2
        return out1

    def tokens_to_unicode(self, out1):
        out2 = []
        for toktype in out1:
             ustr = self.token_to_unicode(toktype)
             if ustr != None:
                 out2.append(ustr)
        final = ''.join(out2)
        return final

    def to_unicode(self, data):
        tokentypes = self.tokenize(data)
    
        tokentypes = self.compose_tokens(tokentypes)
        tokentypes = self.jump_before_tokens(tokentypes)
        tokentypes = self.jump_after_tokens(tokentypes)

        return self.tokens_to_unicode(tokentypes)

    def log_error_summary(self):
        '''how often every character that could not be converted was seen.
           to_unicode() is called once per run of text of a document, so the
           totals are only whole once the whole document has gone through'''
        errs = sorted(self.errchars, key = lambda x: self.errchars[x], \
                      reverse = True)
        if not errs:
            return

        self.logger.info('%d character(s) had no token of this font', len(errs))
        for char in errs:
            self.logger.info('U+%04X %s: %d time(s)', ord(char), \
                             unicodedata.name(char, 'unnamed'), \
                             self.errchars[char])

    def report_error(self, token):
        pos    = token.lexer.lexpos
        window = 10
        # the text around the character, as much of it as there is: a run of
        # a pdf is often shorter than the window and clipping the end to
        # pos + window rather than to the end of the text left every one of
        # them without any context at all
        startpos = max(pos - window, 0)
        endpos   = min(pos + window, len(token.lexer.lexdata))

        s = token.lexer.lexdata[startpos:endpos]
        char = token.lexer.lexdata[pos]
        count = self.errchars.get(char, 0) + 1
        self.errchars[char] = count

        # a document draws the same unknown glyph over and over and
        # to_unicode() is called once per run of its text, so a character is
        # only worth a line the first time it is seen. The counts are kept
        # for log_error_summary(), which has the whole document to report on
        if count == 1:
            self.logger.warning('No token for U+%04X %s, dropping it. Seen ' \
                                'in %r', ord(char), \
                                unicodedata.name(char, 'unnamed'), s)
        else:
            self.logger.debug('TokenError. char: %r string: %r' % (char, s))
