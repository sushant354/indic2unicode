class BaseLang:
    def __init__(self):
        # just empty token dict
        self.tokendict       = {} 
        self.conjunct_tokens = {}
 
    def get_unicode_string(self, tokenName):
        if self.tokendict.has_key(tokenName):
            return self.tokendict[tokenName]
        else:
            return None

    def multiple_tokens(self, tokenName):
        if self.conjunct_tokens.has_key(tokenName):
            return self.conjunct_tokens[tokenName]
        else:
            return None

    def get_tokens(self):
        return self.tokendict.keys() + self.conjunct_tokens.keys()

