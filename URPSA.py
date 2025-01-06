from PyQt5 import QtWidgets, QtGui
import sys


class ConfigApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration Input")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.currentChanged.connect(self.generate_preview)  # Event to handle tab change

        self.inputs = {}

        # General Tab
        self.general_tab = QtWidgets.QWidget()
        self.general_layout = QtWidgets.QVBoxLayout()
        self.project_group = self.create_section("Project", [
            ("Project Name", "test48927")
        ])
        self.gaussian_group = self.create_section("Gaussian", [
            ("Number of Cores", "8", int),
            ("Memory", "8GB"),
            ("Method", "#N opt(maxcycle=600,AddGIC) PM6 scf(maxcyc=600,xqc) nosymm")
        ])
        self.molecules_group = self.create_section("Molecules", [
            ("Charge", "0", int),
            ("Multiplicity", "1", int),
            ("Number of Molecules", "2", int)
        ])
        self.molecules_group_multy_line = self.create_multiline_section("Molecules", "")

        self.general_layout.addWidget(self.project_group)
        self.general_layout.addWidget(self.gaussian_group)
        self.general_layout.addWidget(self.molecules_group)
        self.general_layout.addWidget(self.molecules_group_multy_line)
        self.general_tab.setLayout(self.general_layout)

        # Advanced Tab
        self.advanced_tab = QtWidgets.QWidget()
        self.advanced_layout = QtWidgets.QVBoxLayout()
        self.controls_group = self.create_section("Controls", [
            ("Step Size", "0.1", float),
            ("Step Count", "40", int),
            ("Stop Distance Factor", "0.8", float),
            ("Stress Release", "0:1:-1"),
            ("Sphere Radius", "3", float),
            ("N Iterations", "10", int),
            ("Spherical Placement", "statistically_even"),
            ("Cutoff Energy Gap", "3.0", float)
        ])
        self.exit_controls_group = self.create_combobox_section("Exit Controls", [
            ("Energy Surpass Options", "exit"),
            ("Convergence Error", "exit")
        ])
        self.boolean_controls_group = self.create_checkbox_section("Boolean Controls", [
            ("Update with Optimized Coordinates", True),
            ("Add COM Constraints", True),
            ("Add Spherical Constraints", False),
            ("Dynamic Fragment Replacement", False),
            ("Optimize the Final Particle", True)
        ])
        self.additional_group = self.create_multiline_section("Additional", "")

        self.advanced_layout.addWidget(self.controls_group)
        self.advanced_layout.addWidget(self.exit_controls_group)
        self.advanced_layout.addWidget(self.boolean_controls_group)
        self.advanced_layout.addWidget(self.additional_group)
        self.advanced_tab.setLayout(self.advanced_layout)

        # Preview Tab
        self.preview_tab = QtWidgets.QWidget()
        self.preview_layout = QtWidgets.QVBoxLayout()
        self.preview_text = QtWidgets.QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_layout.addWidget(self.preview_text)

        self.save_button = QtWidgets.QPushButton("Save File")
        self.save_button.clicked.connect(self.save_file)
        self.preview_layout.addWidget(self.save_button)

        self.preview_tab.setLayout(self.preview_layout)

        # Add tabs to the main widget
        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.advanced_tab, "Advanced")
        self.tabs.addTab(self.preview_tab, "Preview")

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.tabs)
        self.setLayout(self.main_layout)

    def create_section(self, title, fields):
        group_box = QtWidgets.QGroupBox(title)
        layout = QtWidgets.QFormLayout()

        for field in fields:
            label, default = field[0], field[1]
            input_type = field[2] if len(field) > 2 else str

            line_edit = QtWidgets.QLineEdit()
            line_edit.setText(default)
            if input_type == int:
                line_edit.setValidator(QtGui.QIntValidator())
            elif input_type == float:
                line_edit.setValidator(QtGui.QDoubleValidator())

            self.inputs[label] = line_edit
            layout.addRow(label, line_edit)

        group_box.setLayout(layout)
        return group_box

    def create_combobox_section(self, title, fields):
        group_box = QtWidgets.QGroupBox(title)
        layout = QtWidgets.QFormLayout()

        for field in fields:
            label, default = field[0], field[1]
            combo_box = QtWidgets.QComboBox()
            combo_box.addItems(["continue", "exit"])
            combo_box.setCurrentText(default)
            self.inputs[label] = combo_box
            layout.addRow(label, combo_box)

        group_box.setLayout(layout)
        return group_box

    def create_checkbox_section(self, title, fields):
        group_box = QtWidgets.QGroupBox(title)
        layout = QtWidgets.QFormLayout()

        for field in fields:
            label, default = field[0], field[1]
            checkbox = QtWidgets.QCheckBox()
            checkbox.setChecked(default)
            self.inputs[label] = checkbox
            layout.addRow(label, checkbox)

        group_box.setLayout(layout)
        return group_box

    def create_multiline_section(self, title, default_text):
        group_box = QtWidgets.QGroupBox(title)
        layout = QtWidgets.QVBoxLayout()
        text_edit = QtWidgets.QPlainTextEdit()
        text_edit.setPlainText(default_text)
        self.inputs[title] = text_edit
        layout.addWidget(text_edit)
        group_box.setLayout(layout)
        return group_box

    def generate_preview(self, index):
        if index != 2:  # Only generate preview when the Preview tab is clicked
            return

        config_lines = ""

        # General section
        config_lines += "[Project]\n"
        config_lines += f"project_name = {self.inputs['Project Name'].text()}\n\n"

        config_lines += "[Gaussian]\n"
        config_lines += f"number_of_cores = {self.inputs['Number of Cores'].text()}\n"
        config_lines += f"memory = {self.inputs['Memory'].text()}\n"
        config_lines += f"method = {self.inputs['Method'].text()}\n\n"

        # Molecules section
        config_lines += "[Molecules]\n"
        config_lines += f"charge = {self.inputs['Charge'].text()}\n"
        config_lines += f"multiplicity = {self.inputs['Multiplicity'].text()}\n"
        config_lines += f"number_of_molecules = {self.inputs['Number of Molecules'].text()}\n\n"
        config_lines += self.inputs["Molecules"].toPlainText() + "\n"

        # Controls section
        config_lines += "[Controls]\n"
        for key in self.inputs:
            if isinstance(self.inputs[key], QtWidgets.QLineEdit):
                config_lines += f"{key.replace(' ', '_').lower()} = {self.inputs[key].text()}\n"
            elif isinstance(self.inputs[key], QtWidgets.QCheckBox):
                config_lines += f"{key.replace(' ', '_').lower()} = {str(self.inputs[key].isChecked()).lower()}\n"
            elif isinstance(self.inputs[key], QtWidgets.QComboBox):
                config_lines += f"{key.replace(' ', '_').lower()} = {self.inputs[key].currentText()}\n"

        # Additional section
        config_lines += "\n[Additional]\n"
        config_lines += self.inputs["Additional"].toPlainText()

        # Set the preview text
        self.preview_text.setText(config_lines)

    def save_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save Configuration File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.preview_text.toPlainText())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ConfigApp()
    window.show()
    sys.exit(app.exec())

