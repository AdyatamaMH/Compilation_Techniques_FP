# Terminal Morse Code Dictionary
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '-----': '0', '/': ' '
}

# Reverse Dictionary for Text to Morse
TEXT_TO_MORSE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}

# Non-terminal Dictionary
NON_TERMINAL_DICT = {
    'DOT': '.',
    'DASH': '-',
    'LETTER': '[DOT|DASH]+', 
    'WORD': 'LETTER+ /',    
    'MESSAGE': 'WORD+',      
}

# Conversion Functions
def text_to_morse(text):
    """Converts plain text to Morse code."""
    text = text.upper()
    morse = []
    for char in text:
        if char in TEXT_TO_MORSE_DICT:
            morse.append(TEXT_TO_MORSE_DICT[char])
        elif char == ' ':
            morse.append('/') 
        else:
            morse.append('?') 
    return ' '.join(morse)

def morse_to_text(morse):
    """Converts Morse code to plain text."""
    text = []
    morse = ' '.join(morse.split())  
    words = morse.split(' / ') 
    for word in words:
        letters = word.split() 
        decoded_word = ''.join(MORSE_CODE_DICT.get(letter, '?') for letter in letters)
        text.append(decoded_word)
    return ' '.join(text)
