import ply.lex as lex
import ply.yacc as yacc
from morse_code_logic import MORSE_CODE_DICT

# Lexer Tokens
tokens = ('DOT', 'DASH', 'SLASH')

# Token Definitions
t_DOT = r'\.'
t_DASH = r'-'
t_SLASH = r'/'

# Ignored Characters
t_ignore = ''

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Parser Grammar
def p_message(p):
    '''message : words'''
    p[0] = ''.join(p[1])

def p_words(p):
    '''words : words word
             | word'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_word(p):
    '''word : morse SLASH'''
    p[0] = MORSE_CODE_DICT.get(p[1], '?')  

def p_morse(p):
    '''morse : morse DOT
             | morse DASH
             | DOT
             | DASH'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

def parse_morse_code(code):
    """Parse Morse code input and return the interpreted text."""
    return parser.parse(code)
