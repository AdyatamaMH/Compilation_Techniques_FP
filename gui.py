import tkinter as tk
from tkinter import messagebox
from lexer_parser import parse_morse_code
from morse_code_logic import text_to_morse

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
            result = parse_morse_code(input_value)
        elif current_mode == "Text to Morse":
            result = text_to_morse(input_value)
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

# Create the main GUI window
root = tk.Tk()
root.title("Morse Code Interpreter")

# Mode Label
mode_label = tk.Label(root, text=f"Mode: {current_mode}", font=("Arial", 12))
mode_label.pack()

# Mode Buttons
tk.Button(root, text="Morse to Text", command=lambda: set_mode("Morse to Text")).pack()
tk.Button(root, text="Text to Morse", command=lambda: set_mode("Text to Morse")).pack()

# Input Text Area
tk.Label(root, text="Enter Input:").pack()
input_text = tk.Text(root, height=5, width=50)
input_text.pack()

# Interpret Button
tk.Button(root, text="Interpret", command=interpret_text).pack()

# Output Text Area
tk.Label(root, text="Output:").pack()
output_text = tk.Text(root, height=5, width=50)
output_text.pack()

def start_gui():
    """Start the GUI event loop."""
    root.mainloop()
