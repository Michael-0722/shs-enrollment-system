from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QPushButton

class EnrollmentDialog(QDialog):
    """Dialog for enrolling a student"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enroll Student")
        self.setFixedSize(320, 160)  # Set fixed window size

        # Main vertical layout
        layout = QVBoxLayout(self)

        # Form layout for input fields
        form = QFormLayout()

        # Grade level dropdown
        self.grade_level = QComboBox()
        self.grade_level.addItems(["11", "12"])

        # Strand dropdown
        self.strand = QComboBox()
        self.strand.addItems(["STEM", "HUMSS", "GAS", "ICT"])

        # Add form rows
        form.addRow("Grade Level:", self.grade_level)
        form.addRow("Strand:", self.strand)
        layout.addLayout(form)

        # Confirm button to enroll student
        self.confirm_btn = QPushButton("Enroll")
        self.confirm_btn.clicked.connect(self.accept)  # Close dialog on click
        layout.addWidget(self.confirm_btn)

    def get_values(self):
        """Return selected grade level and strand"""
        return self.grade_level.currentText(), self.strand.currentText()
