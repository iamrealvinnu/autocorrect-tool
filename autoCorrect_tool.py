# Import necessary libraries
import importlib
import subprocess

# Install required packages if not present
packages = ['happytransformer']
for package in packages:
    if importlib.util.find_spec(package) is None:
        subprocess.check_call(["pip", "install", "happytransformer"])

from happytransformer import HappyTextToText, TTSettings
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Initialize the text correction model
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

def auto_correct_text(input_text):
    """
    Corrects text using BERT-based model
    """
    try:
        if not input_text.strip():
            return ""
        
        # Process the text through the model
        result = happy_tt.generate_text(input_text, args=args)
        corrected_text = result.text
        
        # Ensure proper capitalization
        sentences = corrected_text.split('. ')
        corrected_sentences = []
        
        for sentence in sentences:
            if sentence:
                # Capitalize first letter of sentence
                sentence = sentence.strip()
                sentence = sentence[0].upper() + sentence[1:] if sentence else ''
                corrected_sentences.append(sentence)
        
        return '. '.join(corrected_sentences)
        
    except Exception as e:
        return f"Error in correction: {str(e)}"

def update_text():
    """
    Updates the corrected text area with corrected input.
    """
    input_text = text_area.get('1.0', tk.END).strip()
    if not input_text:
        messagebox.showwarning("Warning", "Please enter some text to correct")
        return
        
    corrected_text = auto_correct_text(input_text)
    corrected_text_area.delete('1.0', tk.END)
    corrected_text_area.insert('1.0', corrected_text)

# Create the main window
root = tk.Tk()
root.title("Auto Correct Tool")
root.geometry("800x600")

# Input label
input_label = tk.Label(root, text="Enter text to correct:", font=("Arial", 12))
input_label.pack(padx=5, pady=5)

# Input text area
text_area = scrolledtext.ScrolledText(root, width=50, height=10, font=("Arial", 12))
text_area.pack(padx=10, pady=5)

# Corrected text label
corrected_label = tk.Label(root, text="Corrected text:", font=("Arial", 12))
corrected_label.pack(padx=5, pady=5)

# Corrected text area
corrected_text_area = scrolledtext.ScrolledText(root, width=50, height=10, font=("Arial", 12))
corrected_text_area.pack(padx=10, pady=5)

# Correct button
update_button = tk.Button(root, text="Correct Text", command=update_text, 
                         bg="#4CAF50", fg="#fff", font=("Arial", 12))
update_button.pack(padx=10, pady=10)

# Clear button
def clear_text():
    text_area.delete('1.0', tk.END)
    corrected_text_area.delete('1.0', tk.END)

clear_button = tk.Button(root, text="Clear Text", command=clear_text, 
                        bg="#e74c3c", fg="#fff", font=("Arial", 12))
clear_button.pack(padx=10, pady=5)

# Copy button
def copy_corrected_text():
    corrected_text = corrected_text_area.get('1.0', tk.END).strip()
    if corrected_text:
        root.clipboard_clear()
        root.clipboard_append(corrected_text)
        messagebox.showinfo("Success", "Text copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No corrected text to copy")

copy_button = tk.Button(root, text="Copy Corrected Text", command=copy_corrected_text, 
                       bg="#2ecc71", fg="#fff", font=("Arial", 12))
copy_button.pack(padx=10, pady=5)

root.mainloop()


