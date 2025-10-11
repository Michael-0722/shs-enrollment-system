from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QLineEdit, QGroupBox
)
from PyQt6.QtGui import QFont
from app.items.service import StudentService
from app.styles.enrollment_style import get_enrollment_style


class EnrolledTab(QWidget):
    """Tab widget for managing enrolled students"""

    def __init__(self):
        super().__init__()
        self.setObjectName("EnrolledTab")
        self.init_ui()
        self.apply_style()
        self.load_enrolled()  # Load initial data

    def init_ui(self):
        """Initialize UI components"""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)

        # Left: Enrolled student information form
        form_group = QGroupBox("Enrolled Student Information")
        form_group_layout = QVBoxLayout(form_group)
        form_group_layout.setSpacing(10)

        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(8)

        self.id = QLineEdit()
        self.id.setReadOnly(True)  # ID cannot be edited
        self.name = QLineEdit()
        self.name.setReadOnly(True)
        self.name.setFixedWidth(160)

        self.grade_level = QComboBox()
        self.grade_level.addItems(["11", "12"])
        self.grade_level.setFixedWidth(100)
        self.strand = QComboBox()
        self.strand.addItems(["STEM", "HUMSS", "GAS", "ICT"])
        self.strand.setFixedWidth(100)

        form_layout.addRow("ID:", self.id)
        form_layout.addRow("Name:", self.name)
        form_layout.addRow("Grade Level:", self.grade_level)
        form_layout.addRow("Strand:", self.strand)

        # Buttons for updating, dropping, clearing
        button_row = QHBoxLayout()
        self.update_btn = QPushButton("Update")
        self.delete_enrolled_btn = QPushButton("Drop")
        self.clear_btn = QPushButton("Clear")
        button_row.addWidget(self.update_btn)
        button_row.addWidget(self.delete_enrolled_btn)
        button_row.addWidget(self.clear_btn)
        form_layout.addRow(button_row)

        form_group_layout.addLayout(form_layout)

        # Right: Table and filter controls
        right_layout = QVBoxLayout()
        right_layout.setSpacing(12)

        filter_layout = QHBoxLayout()
        self.filter_grade = QComboBox()
        self.filter_grade.addItems(["All", "11", "12"])
        self.filter_strand = QComboBox()
        self.filter_strand.addItems(["All", "STEM", "HUMSS", "GAS", "ICT"])
        self.filter_btn = QPushButton("Filter")
        self.refresh_btn = QPushButton("Refresh")

        filter_layout.addWidget(QLabel("Grade Level:"))
        filter_layout.addWidget(self.filter_grade)
        filter_layout.addWidget(QLabel("Strand:"))
        filter_layout.addWidget(self.filter_strand)
        filter_layout.addWidget(self.filter_btn)
        filter_layout.addWidget(self.refresh_btn)

        # Table for enrolled students
        self.enrolled_table = QTableWidget()
        self.enrolled_table.setColumnCount(4)
        self.enrolled_table.setHorizontalHeaderLabels(["ID", "Full Name", "Grade Level", "Strand"])
        self.enrolled_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.enrolled_table.setSelectionBehavior(self.enrolled_table.SelectionBehavior.SelectRows)
        self.enrolled_table.setEditTriggers(self.enrolled_table.EditTrigger.NoEditTriggers)

        right_layout.addLayout(filter_layout)
        right_layout.addWidget(self.enrolled_table)

        main_layout.addWidget(form_group, 2)
        main_layout.addLayout(right_layout, 5)

        # Connect buttons to their methods
        self.filter_btn.clicked.connect(self.on_filter)
        self.refresh_btn.clicked.connect(self.load_enrolled)
        self.update_btn.clicked.connect(self.on_update_selected)
        self.delete_enrolled_btn.clicked.connect(self.on_delete_selected)
        self.clear_btn.clicked.connect(self.clear)
        self.enrolled_table.cellClicked.connect(self.cell_table_clicked)

    def apply_style(self):
        """Apply fonts and styles"""
        self.setFont(QFont("Helvetica Neue", 11))
        self.setStyleSheet(get_enrollment_style())

        # Object names for styling
        self.update_btn.setObjectName("update_btn")
        self.delete_enrolled_btn.setObjectName("delete_btn")
        self.filter_btn.setObjectName("clear_btn")
        self.refresh_btn.setObjectName("clear_btn")
        self.clear_btn.setObjectName("clear_btn")

    def load_enrolled(self):
        """Load all enrolled students into the table"""
        rows = StudentService.list_enrolled()
        self.populate_enrolled(rows)

    def populate_enrolled(self, students):
        """Fill table with student data"""
        self.enrolled_table.setRowCount(0)
        for s in students:
            r = self.enrolled_table.rowCount()
            self.enrolled_table.insertRow(r)
            self.enrolled_table.setItem(r, 0, QTableWidgetItem(s["id"]))
            self.enrolled_table.setItem(r, 1, QTableWidgetItem(s["full_name"]))
            self.enrolled_table.setItem(r, 2, QTableWidgetItem(s["grade_level"]))
            self.enrolled_table.setItem(r, 3, QTableWidgetItem(s["strand"]))

    def on_filter(self):
        """Filter table by grade and strand"""
        g = self.filter_grade.currentText()
        s = self.filter_strand.currentText()
        rows = StudentService.filter_enrolled(g, s)
        results = []
        for row in rows:
            full_name = f"{row['first_name']} {row['middle_name'] or ''} {row['last_name']}".replace("  ", " ").strip()
            results.append({
                "id": row["id"],
                "full_name": full_name,
                "grade_level": row["grade_level"],
                "strand": row["strand"]
            })
        self.populate_enrolled(results)

    def on_update_selected(self):
        """Update selected enrollment"""
        row = self.enrolled_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Select", "Select student to update.")
            return
        eid = self.enrolled_table.item(row, 0).text()
        grade = self.grade_level.currentText()
        strand = self.strand.currentText()
        success = StudentService.update_enrollment(eid, grade, strand, self)
        if success:
            self.load_enrolled()
            self.clear()
        else:
            QMessageBox.warning(self, "Error", f"No enrollment found with ID {eid}.")

    def on_delete_selected(self):
        """Delete selected enrollment"""
        row = self.enrolled_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Select", "Select student to drop.")
            return
        eid = self.enrolled_table.item(row, 0).text()
        ok = QMessageBox.question(self, "Confirm", "Are you sure to drop this student?")
        if ok == QMessageBox.StandardButton.Yes:
            StudentService.delete_enrolled(eid, self)
            self.load_enrolled()
            self.clear()

    def cell_table_clicked(self, row, col):
        """Populate form fields when table row is clicked"""
        self.id.setText(self.enrolled_table.item(row, 0).text())
        self.name.setText(self.enrolled_table.item(row, 1).text())
        grade = self.enrolled_table.item(row, 2).text()
        strand = self.enrolled_table.item(row, 3).text()
        idx_g = self.grade_level.findText(grade)
        if idx_g >= 0:
            self.grade_level.setCurrentIndex(idx_g)
        idx_s = self.strand.findText(strand)
        if idx_s >= 0:
            self.strand.setCurrentIndex(idx_s)

    def clear(self):
        """Clear form fields"""
        self.id.clear()
        self.name.clear()
        self.grade_level.setCurrentIndex(0)
        self.strand.setCurrentIndex(0)

    def add_student_to_table(self, student_data: dict):
        """Add a single student to the table"""
        row = self.enrolled_table.rowCount()
        self.enrolled_table.insertRow(row)
        self.enrolled_table.setItem(row, 0, QTableWidgetItem(str(student_data.get("student_id", ""))))
        self.enrolled_table.setItem(row, 1, QTableWidgetItem(student_data.get("full_name", "")))
        self.enrolled_table.setItem(row, 2, QTableWidgetItem(student_data.get("grade_level", "")))
        self.enrolled_table.setItem(row, 3, QTableWidgetItem(student_data.get("strand", "")))
