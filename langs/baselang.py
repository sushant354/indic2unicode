class BaseLang:
    def __init__(self):
        # just empty token dict
        self.tokendict       = {} 
        self.conjunct_tokens = {}
 
    def get_unicode_string(self, tokenName):
        if tokenName in self.tokendict:
            return self.tokendict[tokenName]
        else:
            return None

    def multiple_tokens(self, tokenName):
        if tokenName in self.conjunct_tokens:
            return self.conjunct_tokens[tokenName]
        else:
            return None

    def get_tokens(self):
        return list(self.tokendict.keys()) + list(self.conjunct_tokens.keys())

