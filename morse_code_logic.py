import pygame
import time

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

# Sound Setup
pygame.mixer.init()

# Duration for dot and dash sounds (in seconds)
DOT_DURATION = 0.2
DASH_DURATION = 0.5

# Morse Code Sound Conversion
def play_morse_sound(code):
    """Play the sound corresponding to Morse code."""
    for symbol in code:
        if symbol == '.':
            pygame.mixer.Sound('dot_sound.wav').play()  # Play dot sound
            time.sleep(DOT_DURATION)
        elif symbol == '-':
            pygame.mixer.Sound('dash_sound.wav').play()  # Play dash sound
            time.sleep(DASH_DURATION)
        time.sleep(0.1)  # Short pause between symbols

# Conversion Functions (Text to Morse and Morse to Text)
def text_to_morse(text):
    """Converts plain text to Morse code."""
    text = text.upper()
    morse = []
    for char in text:
        if char in MORSE_CODE_DICT:
            morse.append(MORSE_CODE_DICT[char])
        elif char == ' ':
            morse.append('/') 
        else:
            morse.append('?')  # Invalid characters are converted to '?'
    return ' '.join(morse)

def morse_to_text(morse):
    """Converts Morse code to plain text."""
    text = []
    morse = ' '.join(morse.split())  # Clean up any extra spaces
    words = morse.split(' / ')  # Split words by slash
    for word in words:
        letters = word.split()  # Split letters by space
        decoded_word = ''.join(MORSE_CODE_DICT.get(letter, '?') for letter in letters)
        text.append(decoded_word)
    return ' '.join(text)


