import re

class Token:
    def __init__(self, tok_type, text):
        self.tok_type = tok_type
        self.text = text 
        
def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()
    
def get_tok(f, lg):
    input_str = str(f)
    while input_str:  # Continue until whole file is read.

        # Try to match a token.
        tok = None
        for tok_type in lg.lexer_rules:
            tok_pattern = lg.lexer_rules[tok_type]
            m = re.match(tok_pattern, input_str)
            if not m:
                continue
            tok_text = m[0]
            if (not tok) or (len(tok_text) > len(tok.text)):
                tok = Token(tok_type, tok_text)
        
        if tok:
            input_str = input_str[len(tok.text):]
            yield tok
            continue
               
        # Otherwise try to consume whitespace and ignored patterns.
        m = re.match(lg.whitespace_pattern, input_str)
        if m:
            tok_text = m[0]
            input_str = input_str[len(tok_text):]
            if lg.keep_whitespace:
               yield Token("whitespace", tok_text)
            continue
        m = re.match(lg.ignore_pattern, input_str)
        if m:
            input_str = input_str[len(m[0]):]
            continue

        # No matches; stop generator.
        break
