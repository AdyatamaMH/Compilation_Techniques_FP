import tkinter as tk
from tkinter import messagebox
from lexer_parser import parse_morse_code
from morse_code_logic import text_to_morse, morse_to_text

# Mode Selection
current_mode = "Morse to Text"

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
root.geometry("500x400")

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

# Clear Button
tk.Button(root, text="Clear", command=clear_fields, width=10, bg="red", fg="white").pack(pady=10)

def start_gui():
    """Start the GUI event loop."""
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    start_gui()
