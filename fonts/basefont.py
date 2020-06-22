import logging
import types

class BaseFont:
    def __init__(self):
        self.langobjs      = []
        self.lexer         = None
        self.composeTokens = {}
        self.jumpbefore    = {}
        self.waitdict      = {} 
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

    def token_to_unicode(self, tokenName):
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
             multipleTokens = self.multiple_tokens(tok.type)
             if multipleTokens:
                 tokentypes.extend(multipleTokens)
             else:
                 tokentypes.append(tok.type)
        return tokentypes

    def jump_before_tokens(self, tokentypes):
        out = []
        for t in tokentypes:
            num = self.num_before(t)
            if num == 0 or num > len(out):
                out.append(t)
            else:
                index = len(out) - num
                out.insert(index, t)
        return out

    def jump_after_tokens(self, tokentypes): 
        out = []
        waitTokens = {} 
        for toktype in tokentypes:
             num = self.num_after(toktype)
             if num == 0:
                 for k in list(waitTokens.keys()):
                     if waitTokens[k] == 0:
                         waitTokens.pop(k)
                         out.append(k)
                     else:
                         waitTokens[k] -= 1
                 out.append(toktype)
             else:
                 waitTokens[toktype] = num
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

        errs = list(self.errchars.keys())
        if errs:
            errs.sort(key = lambda x: self.errchars[x], reverse=True)
            self.logger.debug('Num of err chars %d' % len(errs))
            for char in errs:
                self.logger.error('Err char: %s count: %d' % \
                                   (char, self.errchars[char]))

        return self.tokens_to_unicode(tokentypes)

    def report_error(self, token):
        pos = endpos = startpos = token.lexer.lexpos
        window = 10 
        if startpos > window:
            startpos -= window
        if endpos + window < len(token.lexer.lexdata):
            endpos += window

        s = token.lexer.lexdata[startpos:endpos]
        char = token.lexer.lexdata[pos]
        if char in self.errchars:
            self.errchars[char] += 1
        else:
            self.errchars[char] = 1
        self.logger.debug('TokenError. char: %s string: %s' % (char, s))
