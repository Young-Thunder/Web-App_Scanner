import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import subprocess
import os
import json

class NucleiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VCS Scanner")
        self.root.geometry("800x600")
        
        # Title label
        self.title_label = tk.Label(root, text="VCS Scanner", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=10)
        
        # Frame for input fields
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        # Target URL input
        self.url_label = tk.Label(input_frame, text="Target URL:", font=("Helvetica", 12))
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.url_entry = tk.Entry(input_frame, width=60, font=("Helvetica", 12))
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        # Template selection
        self.template_label = tk.Label(input_frame, text="Nuclei Templates:", font=("Helvetica", 12))
        self.template_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.template_listbox = tk.Listbox(input_frame, selectmode=tk.MULTIPLE, width=60, height=6, font=("Helvetica", 12))
        self.template_listbox.grid(row=1, column=1, padx=5, pady=5)
        self.template_button = tk.Button(input_frame, text="Select Templates", command=self.select_templates, font=("Helvetica", 12))
        self.template_button.grid(row=1, column=2, padx=5, pady=5)

        # Dropdown to select previous results
        self.previous_results_label = tk.Label(input_frame, text="Previous Results:", font=("Helvetica", 12))
        self.previous_results_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.previous_results_var = tk.StringVar()
        self.previous_results_dropdown = ttk.Combobox(input_frame, textvariable=self.previous_results_var, font=("Helvetica", 12))
        self.previous_results_dropdown.grid(row=2, column=1, padx=5, pady=5)
        self.load_previous_results()

        # View previous result button
        self.view_result_button = tk.Button(input_frame, text="View Selected Result", command=self.view_result, font=("Helvetica", 12))
        self.view_result_button.grid(row=2, column=2, padx=5, pady=5)
        
        # Frame for buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Start scan button
        self.scan_button = tk.Button(button_frame, text="Start Scan", command=self.start_scan, font=("Helvetica", 12))
        self.scan_button.grid(row=0, column=0, padx=5, pady=5)

        # Save result button
        self.save_button = tk.Button(button_frame, text="Save Result", command=self.save_result_to_file, font=("Helvetica", 12))
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        # Clear result button
        self.clear_button = tk.Button(button_frame, text="Clear Result", command=self.clear_result, font=("Helvetica", 12))
        self.clear_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Output text area with scrollbar
        self.output_text = scrolledtext.ScrolledText(root, height=20, width=100, font=("Helvetica", 12))
        self.output_text.pack(pady=10)

        # Load previous scan results
        self.results = {}
    
    def select_templates(self):
        template_paths = filedialog.askopenfilenames(title="Select Nuclei Templates", filetypes=[("YAML files", "*.yaml")])
        self.template_listbox.delete(0, tk.END)
        for path in template_paths:
            self.template_listbox.insert(tk.END, path)
    
    def load_previous_results(self):
        if os.path.exists("results.json"):
            with open("results.json", "r") as file:
                self.results = json.load(file)
            self.previous_results_dropdown['values'] = list(self.results.keys())
        else:
            self.results = {}
    
    def save_result(self, url, result):
        self.results[url] = result
        with open("results.json", "w") as file:
            json.dump(self.results, file)
        self.load_previous_results()
    
    def view_result(self):
        selected_result = self.previous_results_var.get()
        if selected_result in self.results:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, self.results[selected_result])
        else:
            messagebox.showwarning("Selection Error", "Please select a valid previous result.")
    
    def save_result_to_file(self):
        result = self.output_text.get(1.0, tk.END)
        if result.strip():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(result)
                messagebox.showinfo("Save Result", "Result saved successfully.")
        else:
            messagebox.showwarning("Save Error", "No result to save.")
    
    def clear_result(self):
        self.output_text.delete(1.0, tk.END)
    
    def start_scan(self):
        target_url = self.url_entry.get()
        selected_templates = self.template_listbox.curselection()
        template_paths = [self.template_listbox.get(i) for i in selected_templates]
        
        if not target_url or not template_paths:
            messagebox.showwarning("Input Error", "Please provide both target URL and at least one template path.")
            return
        
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Starting scan...\n")
        
        try:
            command = ["nuclei", "-u", target_url]
            for template in template_paths:
                command.extend(["-t", template])
            
            result = subprocess.run(command, capture_output=True, text=True)
            scan_output = result.stdout + result.stderr
            scan_output = scan_output.encode('ascii', 'ignore').decode('ascii')  # Remove unsupported unicode
            self.output_text.insert(tk.END, scan_output)
            self.save_result(target_url, scan_output)
        except Exception as e:
            self.output_text.insert(tk.END, f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NucleiGUI(root)
    root.mainloop()
