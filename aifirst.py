import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import nltk

# Ensure nltk punkt is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def summarize_text():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter some text to summarize.")
        return
    
    try:
        parser = PlaintextParser.from_string(input_text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, 3)  # Adjust sentence count as needed
        
        summary_output.delete("1.0", tk.END)
        summary_output.insert(tk.END, "\n".join(str(sentence) for sentence in summary))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text_input.delete("1.0", tk.END)
                text_input.insert(tk.END, file.read())
        except Exception as e:
            messagebox.showerror("File Error", f"Could not read file: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Text Summarizer")
root.geometry("650x500")
root.configure(bg="#f0f0f0")

# Header Label
tk.Label(root, text="Text Summarizer", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333").pack(pady=10)

# Input Text Area
tk.Label(root, text="Enter Text:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", padx=20)
text_input = scrolledtext.ScrolledText(root, height=10, width=75, font=("Arial", 10))
text_input.pack(pady=5, padx=20)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=10)

summarize_btn = tk.Button(btn_frame, text="Summarize", command=summarize_text, font=("Arial", 11), bg="#4CAF50", fg="white", padx=15, pady=5)
summarize_btn.pack(side=tk.LEFT, padx=10)

upload_btn = tk.Button(btn_frame, text="Upload File", command=upload_file, font=("Arial", 11), bg="#008CBA", fg="white", padx=15, pady=5)
upload_btn.pack(side=tk.LEFT, padx=10)

# Output Text Area
tk.Label(root, text="Summarized Text:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", padx=20)
summary_output = scrolledtext.ScrolledText(root, height=10, width=75, font=("Arial", 10), bg="#f9f9f9")
summary_output.pack(pady=5, padx=20)

root.mainloop()
