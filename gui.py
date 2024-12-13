import tkinter as tk
from tkinter import messagebox
from lexer_parser import parse_morse_code
from morse_code_logic import text_to_morse, morse_to_text, play_morse_sound

# Mode Selection
current_mode = "Morse to Text"

# Global widget references
mode_label = None
input_text = None
output_text = None

def interpret_text():
    """Callback to interpret based on the selected mode."""
    input_value = input_text.get("1.0", tk.END).strip()
    if not input_value:
        messagebox.showerror("Error", "Input cannot be empty!")
        return
    try:
        if current_mode == "Morse to Text":
            result = parse_morse_code(input_value)  # Using parser for Morse-to-Text
            play_morse_sound(input_value)  # Play sound for the Morse code input
        elif current_mode == "Text to Morse":
            result = text_to_morse(input_value)  # Using utility for Text-to-Morse
            play_morse_sound(result)  # Play sound for the generated Morse code
        else:
            result = "Invalid Mode"
        
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
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

def start_gui():
    """Function to start the GUI."""
    global mode_label, input_text, output_text
    
    # Create the main GUI window
    root = tk.Tk()
    root.title("Morse Code Interpreter")
    root.geometry("500x400")

    # Mode Label
    mode_label = tk.Label(root, text=f"Mode: {current_mode}", font=("Arial", 14))
    mode_label.pack(pady=10)

    # Input Textbox
    input_text = tk.Text(root, height=5, width=50)
    input_text.pack(pady=10)

    # Output Textbox
    output_text = tk.Text(root, height=5, width=50)
    output_text.pack(pady=10)

    # Buttons
    btn_interpret = tk.Button(root, text="Interpret", command=interpret_text, font=("Arial", 12))
    btn_interpret.pack(pady=5)

    btn_clear = tk.Button(root, text="Clear", command=clear_fields, font=("Arial", 12))
    btn_clear.pack(pady=5)

    btn_morse_to_text = tk.Button(root, text="Morse to Text", command=lambda: set_mode("Morse to Text"), font=("Arial", 12))
    btn_morse_to_text.pack(pady=5)

    btn_text_to_morse = tk.Button(root, text="Text to Morse", command=lambda: set_mode("Text to Morse"), font=("Arial", 12))
    btn_text_to_morse.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
