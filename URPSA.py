import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import platform
import subprocess
import os

CONFIG_FILE = "config.txt"


class Section:
    def __init__(self, master, title, fields):
        self.frame = ttk.LabelFrame(master, text=title)
        self.inputs = {}

        for i, field in enumerate(fields):
            label_text = field["label"]
            default = field.get("default", "")
            field_type = field.get("type", str)

            ttk.Label(self.frame, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=3)

            if field_type == "multiline":
                text_widget = tk.Text(self.frame, width=50, height=6)
                text_widget.insert("1.0", default)
                text_widget.grid(row=i, column=1, padx=5, pady=3)
                self.inputs[label_text] = text_widget
            elif field_type == "combo":
                combo = ttk.Combobox(self.frame, values=default, state="readonly")
                combo.current(0)
                combo.grid(row=i, column=1, padx=5, pady=3)
                self.inputs[label_text] = combo
            else:
                entry = ttk.Entry(self.frame)
                entry.insert(0, default)
                entry.grid(row=i, column=1, padx=5, pady=3)
                self.inputs[label_text] = entry

    def get_values(self):
        values = {}
        for label, widget in self.inputs.items():
            if isinstance(widget, tk.Text):
                values[label] = widget.get("1.0", "end-1c").strip()
            elif isinstance(widget, ttk.Combobox):
                values[label] = widget.get()
            else:
                values[label] = widget.get()
        return values


class ConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuration Input")
        self.geometry("750x700")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.sections = {}

        # === General Tab ===
        self.general_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.general_tab, text="General")

        self.sections["project"] = Section(self.general_tab, "Project", [
            {"label": "Project Name", "default": "CH4-"}
        ])
        self.sections["project"].frame.pack(fill="x", padx=10, pady=5)

        self.sections["gaussian"] = Section(self.general_tab, "Gaussian", [
            {"label": "Number of Cores", "default": "8", "type": int},
            {"label": "Memory", "default": "8GB"},
            {"label": "Method", "default": "#N opt(maxcycle=600,AddGIC) PM6 scf(maxcyc=600,xqc) nosymm"}
        ])
        self.sections["gaussian"].frame.pack(fill="x", padx=10, pady=5)

        self.sections["molecules"] = Section(self.general_tab, "Molecules", [
            {"label": "charge", "default": "-1", "type": int},
            {"label": "multiplicity", "default": "1", "type": int},
            {"label": "number_of_molecules", "default": "5", "type": int},
            {"label": "Molecule Data", "default": """0 = C 0.000 0.000 0.0000

1 = C 0.000 0.000 0.000

2 = C 0.000 0.0000 0.0000

3 = C 0.0000 0.00 0.000

4 = H 0.000 0.000 0.000 """, "type": "multiline"}
        ])
        self.sections["molecules"].frame.pack(fill="x", padx=10, pady=5)

        # === Advanced Tab ===
        self.advanced_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.advanced_tab, text="Advanced")

        self.sections["controls"] = Section(self.advanced_tab, "Controls", [
            {"label": "Update with Optimized Coordinates", "default": "True"},
            {"label": "Step Size", "default": "0.1", "type": float},
            {"label": "Step Count", "default": "40", "type": int},
            {"label": "Stop Distance Factor", "default": "0.8", "type": float},
            {"label": "Stress Release", "default": "0:1:-1"},
            {"label": "Sphere Radius", "default": "3", "type": float},
            {"label": "N Iterations", "default": "10", "type": int},
            {"label": "Spherical Placement", "default": ["statistically_even", "random", "custom"], "type": "combo"},
            {"label": "Add COM Constraints", "default": "True"},
            {"label": "Add Spherical Constraints", "default": "False"},
            {"label": "Dynamic Fragment Replacement", "default": "False"},
            {"label": "Cutoff Energy Gap", "default": "3.0", "type": float},
            {"label": "Energy Surpass Options", "default": ["exit", "continue"], "type": "combo"},
            {"label": "Optimize the Final Particle", "default": "True"},
            {"label": "Convergence Error", "default": ["exit", "warn"], "type": "combo"},
            {"label": "unsuccessful_pathway", "default": ["archive", "delete"], "type": "combo"}
        ])
        self.sections["controls"].frame.pack(fill="x", padx=10, pady=5)

        self.sections["Additional"] = Section(self.advanced_tab, "Additional", [
            {"label": "Additional Data", "default": "", "type": "multiline"}
        ])
        self.sections["Additional"].frame.pack(fill="x", padx=10, pady=5)

        # === Preview Tab ===
        self.preview_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_tab, text="Preview")

        self.preview_text = tk.Text(self.preview_tab, wrap="word", height=25)
        self.preview_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.browse_frame = ttk.Frame(self.preview_tab)
        self.browse_frame.pack(fill="x", padx=10, pady=5)

        self.file_path_input = ttk.Entry(self.browse_frame)
        self.file_path_input.insert(0, "Select repeated.py")
        self.file_path_input.pack(side="left", expand=True, fill="x", padx=5)

        ttk.Button(self.browse_frame, text="Browse", command=self.select_repeated_file).pack(side="left")

        ttk.Button(self.preview_tab, text="Run Calculation", command=self.run_calculation).pack(pady=5)
        ttk.Button(self.preview_tab, text="Save File", command=self.save_file).pack(pady=5)

        # Bind tab switch
        self.notebook.bind("<<NotebookTabChanged>>", self.show_preview)

        self.load_repeated_file_path()

    def submit(self):
        config_lines = []
        for section_name, section_obj in self.sections.items():
            config_lines.append(f"[{section_name}]")
            for key, value in section_obj.get_values().items():
                if section_name == "Additional" and value == "":
                    continue
                elif section_name == "molecules" and key == "Molecule Data":
                    config_lines.append(value)
                    continue
                config_lines.append(f"{key.replace(' ', '_').lower()} = {value}")
            config_lines.append("")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", "\n".join(config_lines))

    def show_preview(self, event):
        tab = self.notebook.tab(self.notebook.select(), "text")
        if tab == "Preview":
            self.submit()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(self.preview_text.get("1.0", "end-1c"))
            self.input_file_path = file_path
            messagebox.showinfo("Saved", f"Configuration saved to {file_path}")

    def select_repeated_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            self.file_path_input.delete(0, "end")
            self.file_path_input.insert(0, file_path)
            self.repeated_script_path = file_path
            self.save_repeated_file_path(file_path)

    def run_calculation(self):
        if not hasattr(self, 'input_file_path'):
            messagebox.showwarning("Error", "Please save the input file before running the calculation.")
            return
        if not hasattr(self, 'repeated_script_path'):
            messagebox.showwarning("Error", "Please select the repeated.py script before running the calculation.")
            return

        command = f'cd "{os.path.dirname(self.input_file_path)}" && python "{self.repeated_script_path}" "{self.input_file_path}"'

        if platform.system() == "Linux":
            if "g16" not in os.environ:
                print("Path to g16 not found")
            subprocess.run(['gnome-terminal', '--', 'bash', '-c', command])
        else:
            os.system(command)

    def save_repeated_file_path(self, path):
        with open(CONFIG_FILE, "w") as f:
            f.write(path)

    def load_repeated_file_path(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                path = f.read().strip()
                self.file_path_input.delete(0, "end")
                self.file_path_input.insert(0, path)
                self.repeated_script_path = path


if __name__ == "__main__":
    app = ConfigApp()
    app.mainloop()
