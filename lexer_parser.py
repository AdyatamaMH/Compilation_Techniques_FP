import ply.lex as lex
import ply.yacc as yacc
from morse_code_logic import MORSE_CODE_DICT

# Define Lexer Tokens
tokens = ('DOT', 'DASH', 'SLASH') 

# Token Definitions
t_DOT = r'\.'
t_DASH = r'-'
t_SLASH = r'/' 

# Ignore spaces entirely
t_ignore = ' \t\n'

def t_error(t):
    """Handle illegal characters in the input."""
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build Lexer
def build_lexer():
    """Build and return the lexer."""
    return lex.lex()

# Define Parser Grammar
def p_message(p):
    '''message : words'''
    p[0] = ''.join(p[1])  

def p_words(p):
    '''words : words word
             | word'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]  
    else:
        p[0] = [p[1]] 
def p_word(p):
    '''word : morse SLASH
            | morse'''
    p[0] = MORSE_CODE_DICT.get(p[1], '?')  # Decode Morse word or '?' for invalid

def p_morse(p):
    '''morse : morse DOT
             | morse DASH
             | DOT
             | DASH'''
    if len(p) == 3:
        p[0] = p[1] + p[2]  # Append DOT or DASH to the sequence
    else:
        p[0] = p[1]  # Single DOT or DASH

def p_error(p):
    """Handle syntax errors in the input."""
    print("Syntax error in input!")

# Build Parser
def build_parser():
    """Build and return the parser."""
    return yacc.yacc()

# Parse Function
def parse_morse_code(code):
    """Parse Morse code input and return the interpreted text."""
    lexer = build_lexer()  # Build lexer
    parser = build_parser()  # Build parser
    return parser.parse(code, lexer=lexer)  # Parse input using custom lexer
