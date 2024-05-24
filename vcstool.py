import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import json

class NucleiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VCS Scanner")
        
        # Title label
        self.title_label = tk.Label(root, text="VCS Scanner", font=("Helvetica", 16))
        self.title_label.pack(pady=10)
        
        # Target URL input
        self.url_label = tk.Label(root, text="Target URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()
        
        # Template selection
        self.template_label = tk.Label(root, text="Nuclei Templates:")
        self.template_label.pack()
        self.template_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=10)
        self.template_listbox.pack()
        self.template_button = tk.Button(root, text="Select Templates", command=self.select_templates)
        self.template_button.pack()
        
        # Dropdown to select previous results
        self.previous_results_label = tk.Label(root, text="Previous Results:")
        self.previous_results_label.pack()
        self.previous_results_var = tk.StringVar()
        self.previous_results_dropdown = ttk.Combobox(root, textvariable=self.previous_results_var)
        self.previous_results_dropdown.pack()
        self.load_previous_results()
        
        # View previous result button
        self.view_result_button = tk.Button(root, text="View Selected Result", command=self.view_result)
        self.view_result_button.pack(pady=10)
        
        # Start scan button
        self.scan_button = tk.Button(root, text="Start Scan", command=self.start_scan)
        self.scan_button.pack(pady=10)
        
        # Output text area
        self.output_text = tk.Text(root, height=20, width=80)
        self.output_text.pack(pady=10)
        
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
            self.output_text.insert(tk.END, scan_output)
            self.save_result(target_url, scan_output)
        except Exception as e:
            self.output_text.insert(tk.END, f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NucleiGUI(root)
    root.mainloop()