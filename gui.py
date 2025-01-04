import tkinter as tk
from tkinter import ttk
import pygame
import time
from tkinter import messagebox
from morse_code_logic import text_to_morse

# Mode Selection
current_mode = "Text to Morse"

# Morse Code Dictionary
MORSE_CODE = {
    'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',  'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',  'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',  'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',  'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.'
}

# Sound Player Class
class MorseCodeSoundPlayer:
    def __init__(self):
        pygame.mixer.init()
        
        # Use relative paths for sound files
        dot_wav_path = "dot_sound.wav"
        dash_wav_path = "dash_sound.wav"
        
        try:
            self.dot_sound = pygame.mixer.Sound(dot_wav_path)
            self.dash_sound = pygame.mixer.Sound(dash_wav_path)
        except Exception as e:
            print(f"Error loading sound files: {e}")
            messagebox.showerror("Sound Error", f"Could not load sound files: {e}")
            self.dot_sound = None
            self.dash_sound = None
        
        self.speed_multiplier = 1.0
    
    def play_morse_code(self, message):
        if not self.dot_sound or not self.dash_sound:
            return
        
        # Base timings
        dot_duration = 0.1 * self.speed_multiplier
        dash_duration = 0.3 * self.speed_multiplier
        symbol_space = 0.2 * self.speed_multiplier
        word_space = 0.7 * self.speed_multiplier
        
        for symbol in message:
            if symbol == '.':
                self.dot_sound.play()
                time.sleep(dot_duration)
            elif symbol == '-':
                self.dash_sound.play()
                time.sleep(dash_duration)
            elif symbol == '/':
                time.sleep(word_space)
            elif symbol == ' ':
                time.sleep(symbol_space)
    
    def set_speed(self, speed_value):
        """Set the speed multiplier (1.0 is normal speed)"""
        self.speed_multiplier = 2.0 - (float(speed_value) / 50)
    
    def close(self):
        pygame.mixer.quit()
        pygame.quit()

# Global sound player
sound_player = None

def validate_speed_input(P):
    """Validate speed input to only allow numbers between 0-100."""
    if P == "":
        return True
    try:
        value = int(P)
        return 0 <= value <= 100
    except ValueError:
        return False

def update_speed(value, from_slider=True):
    """Update the morse code playback speed."""
    try:
        if from_slider:
            # Update from slider
            speed_value = int(float(value))
            speed_entry.delete(0, tk.END)
            speed_entry.insert(0, str(speed_value))
        else:
            # Update from text entry
            speed_value = int(value)
            speed_slider.set(speed_value)
        
        if sound_player:
            sound_player.set_speed(speed_value)
            speed_label.config(text=f"Speed: {speed_value}%")
    except ValueError:
        pass

def on_speed_entry_return(event):
    """Handle Return key press in speed entry."""
    value = speed_entry.get()
    if value.strip():
        update_speed(value, from_slider=False)

def validate_and_update_speed(event=None):
    """Validate and update speed when focus leaves the entry."""
    value = speed_entry.get()
    if not value.strip():
        speed_entry.insert(0, "50")
        value = "50"
    try:
        speed_value = int(value)
        if speed_value < 0:
            speed_value = 0
        elif speed_value > 100:
            speed_value = 100
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, str(speed_value))
        update_speed(speed_value, from_slider=False)
    except ValueError:
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, "50")
        update_speed(50, from_slider=False)

def initialize_sound_player():
    """Initialize the sound player."""
    global sound_player
    try:
        sound_player = MorseCodeSoundPlayer()
    except Exception as e:
        messagebox.showerror("Sound Initialization Error", str(e))

def play_morse_sound():
    """Play Morse code sound for current output."""
    if sound_player:
        morse_code = output_text.get("1.0", tk.END).strip()
        try:
            import threading
            sound_thread = threading.Thread(target=sound_player.play_morse_code, args=(morse_code,))
            sound_thread.start()
        except Exception as e:
            messagebox.showerror("Sound Playback Error", str(e))

def interpret_text():
    """Convert text to Morse code."""
    input_value = input_text.get("1.0", tk.END).strip()
    if not input_value:
        messagebox.showerror("Error", "Input cannot be empty!")
        return
    try:
        result = text_to_morse(input_value)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        play_morse_sound()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process: {e}")

def clear_fields():
    """Clears both input and output fields."""
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

# Create the main GUI window
root = tk.Tk()
root.title("Text to Morse Code Converter")
root.geometry("800x600")

# Create main content frame and dictionary frame
main_frame = tk.Frame(root)
main_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

dictionary_frame = tk.Frame(root, relief=tk.GROOVE, bd=2)
dictionary_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH)

# Title Label
title_label = tk.Label(main_frame, text="Text to Morse Code Converter", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

# Input Text Area
tk.Label(main_frame, text="Enter Text:", font=("Arial", 12)).pack(pady=5)
input_text = tk.Text(main_frame, height=5, width=50, wrap=tk.WORD, font=("Arial", 10))
input_text.pack(pady=5)

# Speed Control
speed_frame = tk.Frame(main_frame)
speed_frame.pack(pady=5)
speed_label = tk.Label(speed_frame, text="Speed: 50%", font=("Arial", 10))
speed_label.pack()

# Speed control container
speed_control_frame = tk.Frame(speed_frame)
speed_control_frame.pack(pady=5)

# Slider
speed_slider = ttk.Scale(speed_control_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                        command=lambda v: update_speed(v, from_slider=True),
                        value=50, length=200)
speed_slider.pack(side=tk.LEFT, padx=(0, 10))

# Speed entry validation
vcmd = (root.register(validate_speed_input), '%P')

# Speed entry
speed_entry = tk.Entry(speed_control_frame, width=5, validate='key', 
                      validatecommand=vcmd)
speed_entry.insert(0, "50")
speed_entry.pack(side=tk.LEFT)
tk.Label(speed_control_frame, text="%", font=("Arial", 10)).pack(side=tk.LEFT)

# Bind events for speed entry
speed_entry.bind('<Return>', on_speed_entry_return)
speed_entry.bind('<FocusOut>', validate_and_update_speed)

# Convert Button
tk.Button(main_frame, text="Convert to Morse", command=interpret_text, width=20,
          bg="blue", fg="white").pack(pady=10)

# Output Text Area
tk.Label(main_frame, text="Morse Code Output:", font=("Arial", 12)).pack(pady=5)
output_text = tk.Text(main_frame, height=5, width=50, wrap=tk.WORD, font=("Arial", 10))
output_text.pack(pady=5)

# Sound Playback Button
tk.Button(main_frame, text="Play Sound", command=play_morse_sound,
          width=10, bg="green", fg="white").pack(pady=5)

# Clear Button
tk.Button(main_frame, text="Clear", command=clear_fields,
          width=10, bg="red", fg="white").pack(pady=10)

# Dictionary Panel
tk.Label(dictionary_frame, text="Morse Code Dictionary",
         font=("Arial", 12, "bold")).pack(pady=5)

# Create a Text widget for the dictionary
dictionary_text = tk.Text(dictionary_frame, width=20, height=30, font=("Courier", 10))
dictionary_text.pack(padx=5, pady=5)

# Populate dictionary
for char, code in sorted(MORSE_CODE.items()):
    if char != ' ': 
        dictionary_text.insert(tk.END, f"{char}: {code}\n")
dictionary_text.config(state=tk.DISABLED)  

def start_gui():
    """Start the GUI event loop."""
    initialize_sound_player()
    root.mainloop()
    
    if sound_player:
        sound_player.close()

# Run the GUI
if __name__ == "__main__":
    start_gui()
