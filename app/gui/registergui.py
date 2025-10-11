from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QComboBox, QDateEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QGridLayout, QGroupBox
)
from PyQt6.QtCore import QDate, pyqtSignal, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QFont
from app.items.models import RegisteredStudent, EnrolledStudent
from app.items.service import StudentService
from app.gui.enrollment_dialog import EnrollmentDialog
from app.styles.register_style import get_register_style


class RegistrationTab(QWidget):
    student_enrolled = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.id_hidden = None
        self.setObjectName("RegistrationTab")  # Important for targeted styling
        self.init_ui()
        self.apply_style()
        self.load_registered_students()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(20)

        # --- LEFT SIDE: Student Information Form ---
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(10)

        form_group = QGroupBox("Student Information")
        form_group_layout = QVBoxLayout(form_group)
        form_group_layout.setContentsMargins(15, 15, 15, 15)
        form_group_layout.setSpacing(10)

        # --- Form Fields ---
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("First Name")
        self.middle_name = QLineEdit()
        self.middle_name.setPlaceholderText("Middle Name")
        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Last Name")

        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female"])
        self.gender.setMinimumWidth(120)

        self.birth_date = QDateEdit()
        self.birth_date.setCalendarPopup(True)
        self.birth_date.setMaximumDate(QDate.currentDate())
        self.birth_date.setDate(QDate.currentDate())
        self.birth_date.setMaximumWidth(120)

        self.age = QLineEdit()
        self.age.setPlaceholderText("Generate from date")
        self.age.setReadOnly(True)

        self.contact = QLineEdit()
        self.guardian_name = QLineEdit()
        self.guardian_name.setPlaceholderText("Guardian Full Name")
        self.guardian_contact = QLineEdit()

        # Validation for Philippine mobile numbers
        regex = QRegularExpression(r"^(09\d{0,9}|\+639\d{0,9})$")
        validator = QRegularExpressionValidator(regex)
        self.contact.setValidator(validator)
        self.guardian_contact.setValidator(validator)
        self.contact.setPlaceholderText("ex.09171234567")
        self.guardian_contact.setPlaceholderText("ex.09181234567")

        # Add form rows
        form_layout.addRow("First Name:", self.first_name)
        form_layout.addRow("Middle Name:", self.middle_name)
        form_layout.addRow("Last Name:", self.last_name)
        form_layout.addRow("Gender:", self.gender)
        form_layout.addRow("Birth Date:", self.birth_date)
        form_layout.addRow("Age:", self.age)
        form_layout.addRow("Contact Number:", self.contact)
        form_layout.addRow("Guardian Name:", self.guardian_name)
        form_layout.addRow("Guardian Contact:", self.guardian_contact)

        # --- BUTTONS SECTION (2 rows × 2 columns) ---
        btn_grid = QGridLayout()
        btn_grid.setSpacing(8)

        self.register_btn = QPushButton("Register Student")
        self.update_btn = QPushButton("Update Student")
        self.clear_btn = QPushButton("Clear")
        self.delete_btn = QPushButton("Delete")

        # Button IDs for style targeting
        self.update_btn.setObjectName("update_btn")
        self.clear_btn.setObjectName("clear_btn")
        self.delete_btn.setObjectName("delete_btn")

        btn_grid.addWidget(self.register_btn, 0, 0)
        btn_grid.addWidget(self.update_btn, 0, 1)
        btn_grid.addWidget(self.clear_btn, 1, 0)
        btn_grid.addWidget(self.delete_btn, 1, 1)

        form_group_layout.addLayout(form_layout)
        form_group_layout.addLayout(btn_grid)

        # --- RIGHT SIDE: Table and Search ---
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name or ID...")
        self.search_btn = QPushButton("Search")
        self.refresh_btn = QPushButton("Refresh")

        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.refresh_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Full Name", "Gender",
            "Birth Date", "Age", "Contact",
            "Guardian Name", "Guardian Contact", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)
        self.table.cellClicked.connect(self.on_table_cell_clicked)

        self.enroll_btn = QPushButton("Enroll Selected Student")
        self.enroll_btn.clicked.connect(self.enroll_student)

        right_layout.addLayout(search_layout)
        right_layout.addWidget(self.table)
        right_layout.addWidget(self.enroll_btn)

        # --- Combine Layouts ---
        main_layout.addWidget(form_group, 2)
        main_layout.addLayout(right_layout, 5)

        # --- SIGNALS ---
        self.register_btn.clicked.connect(self.on_register)
        self.update_btn.clicked.connect(self.on_update)
        self.clear_btn.clicked.connect(self.clear_form)
        self.delete_btn.clicked.connect(self.on_delete)
        self.refresh_btn.clicked.connect(self.load_registered_students)
        self.search_btn.clicked.connect(self.on_search)
        self.birth_date.dateChanged.connect(self.on_birthdate_changed)

    # --- Apply Style ---
    def apply_style(self):
        self.setFont(QFont("Helvetica Neue", 11))
        self.setStyleSheet(get_register_style())

    # Helper Methods
    def collect_form_data(self) -> RegisteredStudent:
        birth_iso = self.birth_date.date().toString("yyyy-MM-dd")
        return RegisteredStudent(
            id=self.id_hidden,
            first_name=self.first_name.text(),
            middle_name=self.middle_name.text() or None,
            last_name=self.last_name.text(),
            gender=self.gender.currentText(),
            birth_date=birth_iso,
            age=StudentService.calculate_age_from_iso(birth_iso) or 0,
            contact=self.contact.text(),
            guardian_name=self.guardian_name.text(),
            guardian_contact=self.guardian_contact.text()
        )

    def clear_form(self):
        self.id_hidden = None
        self.first_name.clear()
        self.middle_name.clear()
        self.last_name.clear()
        self.gender.setCurrentIndex(0)
        self.birth_date.setDate(QDate.currentDate())
        self.age.clear()
        self.contact.clear()
        self.guardian_name.clear()
        self.guardian_contact.clear()
        self.search_input.clear()

    # --- Slots ---
    def on_birthdate_changed(self, qdate):
        iso = qdate.toString("yyyy-MM-dd")
        age = StudentService.calculate_age_from_iso(iso)
        if age is not None and age < 0:
            QMessageBox.warning(self, "Invalid Birth Date", "Birth date cannot be in the future.")
            self.birth_date.setDate(QDate.currentDate())
            self.age.clear()
            return
        self.age.setText(str(age) if age is not None else "")

    def on_register(self):
        student = self.collect_form_data()
        sid = StudentService.register_student(student, self)
        if sid:
            self.load_registered_students()
            self.clear_form()

    def on_update(self):
        if not self.id_hidden:
            QMessageBox.warning(self, "Select", "Please select a student row to update.")
            return
        student = self.collect_form_data()
        success =StudentService.update_registered(student, self)
        if success:
            self.clear_form()
            self.load_registered_students()

    def on_delete(self):
        if not self.id_hidden:
            QMessageBox.warning(self, "Select", "Please select a student to delete.")
            return
        ok = QMessageBox.question(self, "Confirm", "Are you sure you want to delete this student information?")
        if ok == QMessageBox.StandardButton.Yes:
            StudentService.delete_registered(self.id_hidden, self)
            self.clear_form()
            self.load_registered_students()

    def on_search(self):
        q = self.search_input.text().strip()
        if not q:
            self.load_registered_students()
            return
        students = StudentService.search_registered(q)
        self.populate_table_with_registered(students)

    def load_registered_students(self):
        students = StudentService.list_registered()
        self.populate_table_with_registered(students)

    def populate_table_with_registered(self, students):
        self.table.setRowCount(0)

        # Fetch enrolled IDs for quick lookup
        enrolled_list = StudentService.list_enrolled()
        enrolled_ids = {e["id"] for e in enrolled_list}

        for s in students:
            r = self.table.rowCount()
            self.table.insertRow(r)

            full_name = f"{s.first_name} {s.middle_name or ''} {s.last_name}".replace("  ", " ").strip()
            status = "Enrolled" if s.id in enrolled_ids else "Unenrolled"

            self.table.setItem(r, 0, QTableWidgetItem(str(s.id)))
            self.table.setItem(r, 1, QTableWidgetItem(full_name))
            self.table.setItem(r, 2, QTableWidgetItem(s.gender or ""))
            self.table.setItem(r, 3, QTableWidgetItem(s.birth_date or ""))
            self.table.setItem(r, 4, QTableWidgetItem(str(s.age) if s.age else ""))
            self.table.setItem(r, 5, QTableWidgetItem(s.contact or ""))
            self.table.setItem(r, 6, QTableWidgetItem(s.guardian_name or ""))
            self.table.setItem(r, 7, QTableWidgetItem(s.guardian_contact or ""))
            self.table.setItem(r, 8, QTableWidgetItem(status))

    def on_table_cell_clicked(self, row, col):
        sid = self.table.item(row, 0).text()
        student = StudentService.get_registered(sid)
        if student:
            self.id_hidden = student.id
            self.first_name.setText(student.first_name or "")
            self.middle_name.setText(student.middle_name or "")
            self.last_name.setText(student.last_name or "")
            idx = self.gender.findText(student.gender) if student.gender else -1
            if idx >= 0:
                self.gender.setCurrentIndex(idx)
            qd = QDate.fromString(student.birth_date, "yyyy-MM-dd")
            if qd.isValid():
                self.birth_date.setDate(qd)
            self.age.setText(str(student.age) if student.age else "")
            self.contact.setText(student.contact or "")
            self.guardian_name.setText(student.guardian_name or "")
            self.guardian_contact.setText(student.guardian_contact or "")

    def enroll_student(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a student to enroll.")
            return

        dialog = EnrollmentDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            grade_level, strand = dialog.get_values()
            sid = self.table.item(row, 0).text()
            enrollment = EnrolledStudent(id=sid, grade_level=grade_level, strand=strand)
            StudentService.enroll_student(enrollment, self)
            self.student_enrolled.emit({
                "student_id": sid,
                "full_name": self.table.item(row, 1).text(),
                "grade_level": grade_level,
                "strand": strand
            })
            self.clear_form()
            self.load_registered_students()  # refresh table to update status
