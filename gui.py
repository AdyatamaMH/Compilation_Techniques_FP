import tkinter as tk
import pygame
import time
from tkinter import messagebox
from lexer_parser import parse_morse_code
from morse_code_logic import text_to_morse, morse_to_text

# Mode Selection
current_mode = "Morse to Text"

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
    
    def play_morse_code(self, message):
        if not self.dot_sound or not self.dash_sound:
            return
        
        for symbol in message:
            if symbol == '.':
                self.dot_sound.play()
                time.sleep(0.1)  
            elif symbol == '-':
                self.dash_sound.play()
                time.sleep(0.3)  
            elif symbol == '/':
                time.sleep(0.7)
            elif symbol == ' ':
                time.sleep(0.2)
    
    def close(self):
        pygame.mixer.quit()
        pygame.quit()

# Global sound player
sound_player = None

def initialize_sound_player():
    """Initialize the sound player."""
    global sound_player
    try:
        sound_player = MorseCodeSoundPlayer()
    except Exception as e:
        messagebox.showerror("Sound Initialization Error", str(e))

def play_morse_sound():
    """Play Morse code sound for current output."""
    if sound_player and current_mode == "Text to Morse":
        # Get the Morse code from output text
        morse_code = output_text.get("1.0", tk.END).strip()
        try:
            # Play the sound in a separate thread to prevent GUI freezing
            import threading
            sound_thread = threading.Thread(target=sound_player.play_morse_code, args=(morse_code,))
            sound_thread.start()
        except Exception as e:
            messagebox.showerror("Sound Playback Error", str(e))

def interpret_text():
    """Callback to interpret based on the selected mode."""
    input_value = input_text.get("1.0", tk.END).strip()
    if not input_value:
        messagebox.showerror("Error", "Input cannot be empty!")
        return
    try:
        if current_mode == "Morse to Text":
            result = parse_morse_code(input_value)  # Using parser for Morse-to-Text
        elif current_mode == "Text to Morse":
            result = text_to_morse(input_value)  # Using utility for Text-to-Morse
        else:
            result = "Invalid Mode"
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        
        # Attempt to play sound if in Text to Morse mode
        play_morse_sound()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process: {e}")

def set_mode(mode):
    """Sets the mode for conversion."""
    global current_mode
    current_mode = mode
    mode_label.config(text=f"Mode: {current_mode}")
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

def clear_fields():
    """Clears both input and output fields."""
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

# Create the main GUI window
root = tk.Tk()
root.title("Morse Code Interpreter")
root.geometry("500x450")

# Mode Label
mode_label = tk.Label(root, text=f"Mode: {current_mode}", font=("Arial", 14))
mode_label.pack(pady=10)

# Mode Buttons
button_frame = tk.Frame(root)
tk.Button(button_frame, text="Morse to Text", command=lambda: set_mode("Morse to Text"), width=15).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Text to Morse", command=lambda: set_mode("Text to Morse"), width=15).pack(side=tk.LEFT, padx=5)
button_frame.pack(pady=10)

# Input Text Area
tk.Label(root, text="Enter Input:", font=("Arial", 12)).pack(pady=5)
input_text = tk.Text(root, height=5, width=50, wrap=tk.WORD, font=("Arial", 10))
input_text.pack(pady=5)

# Interpret Button
tk.Button(root, text="Interpret", command=interpret_text, width=20, bg="blue", fg="white").pack(pady=10)

# Output Text Area
tk.Label(root, text="Output:", font=("Arial", 12)).pack(pady=5)
output_text = tk.Text(root, height=5, width=50, wrap=tk.WORD, font=("Arial", 10))
output_text.pack(pady=5)

# Sound Playback Button
tk.Button(root, text="Play Sound", command=play_morse_sound, width=10, bg="green", fg="white").pack(pady=5)

# Clear Button
tk.Button(root, text="Clear", command=clear_fields, width=10, bg="red", fg="white").pack(pady=10)

def start_gui():
    """Start the GUI event loop."""
    # Initialize sound player when GUI starts
    initialize_sound_player()
    root.mainloop()
    
    # Cleanup sound player when GUI closes
    if sound_player:
        sound_player.close()

# Run the GUI
if __name__ == "__main__":
    start_gui()
