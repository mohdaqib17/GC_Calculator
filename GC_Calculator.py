import tkinter as tk
from tkinter import filedialog, messagebox
from Bio import SeqIO
import os

class GCContentCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GC Content Calculator")

       
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.file_listbox = tk.Listbox(self.left_frame, width=30, height=10)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.file_paths = {} 
        self.add_file_button = tk.Button(self.left_frame, text="Import", command=self.add_files)
        self.add_file_button.pack(pady=5)

        self.remove_file_button = tk.Button(self.left_frame, text="Remove", command=self.remove_selection)
        self.remove_file_button.pack(pady=5)

        
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.results_text = tk.Text(self.right_frame, width=40, height=15, state="disabled")
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.calculate_button = tk.Button(self.right_frame, text="Calculate GC Content", command=self.calculate_gc_content)
        self.calculate_button.pack(pady=5)

        # Menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="About", menu=about_menu)

    def add_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("FASTA files", "*.fasta"), ("All files", "*.*")])
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            self.file_listbox.insert(tk.END, file_name)
            self.file_paths[file_name] = file_path

    def remove_selection(self):
        selected_indices = self.file_listbox.curselection()
        for index in selected_indices[::-1]:
            file_name = self.file_listbox.get(index)
            del self.file_paths[file_name]
            self.file_listbox.delete(index)

    def calculate_gc_content(self):
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)
        for selected_file_index in self.file_listbox.curselection():
            file_name = self.file_listbox.get(selected_file_index)
            file_path = self.file_paths[file_name]
            gc_count = 0
            total_count = 0
            nucleotide_counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}

            for record in SeqIO.parse(file_path, "fasta"):
                sequence = str(record.seq).upper()
                for base in sequence:
                    if base in nucleotide_counts:
                        nucleotide_counts[base] += 1
                        total_count += 1
                        if base in ['G', 'C']:
                            gc_count += 1

            # Calculate GC content
            gc_content = (gc_count / total_count) * 100 if total_count > 0 else 0

            self.results_text.insert(tk.END, f"{file_name}\n\n", "bold")
   

            self.results_text.insert(tk.END, f"A = {nucleotide_counts['A']}\n")
            self.results_text.insert(tk.END, f"T = {nucleotide_counts['T']}\n")
            self.results_text.insert(tk.END, f"G = {nucleotide_counts['G']}\n")
            self.results_text.insert(tk.END, f"C = {nucleotide_counts['C']}\n\n")


            self.results_text.insert(tk.END, f"Total GC Content= {gc_content:.2f}\n", "bold")

        self.results_text.tag_configure("bold", font="TkDefaultFont 9 bold")
        self.results_text.config(state="disabled")

    def show_about(self):
        about_text = "Mohammed Aqib\nEmail: mohdaqib@live.in"
        messagebox.showinfo("About", about_text)

if __name__ == "__main__":
    app = GCContentCalculator()
    app.mainloop()
