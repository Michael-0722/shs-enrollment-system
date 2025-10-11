from datetime import date
from PyQt6.QtWidgets import QMessageBox
from typing import List, Dict, Any, Optional
from app.items.models import RegisteredStudent, EnrolledStudent
from app.items.repository import RegisteredStudentRepo, EnrolledStudentRepo, DeletionBlockedError, RepositoryError


class StudentService:
    """Handles student registration, update, deletion, enrollment, and filtering."""

    @classmethod
    def calculate_age_from_iso(cls, birth_iso: str) -> Optional[int]:
        # Calculate age from ISO date string
        try:
            if not birth_iso:
                return None
            y, m, d = [int(x) for x in birth_iso.split("-")]
            today = date.today()
            return today.year - y - ((today.month, today.day) < (m, d))
        except Exception:
            return None

    @classmethod
    def register_student(cls, student: RegisteredStudent, parent=None) -> Optional[str]:
        # Validate required fields
        required = {
            "First Name": student.first_name,
            "Last Name": student.last_name,
            "Gender": student.gender,
            "Birth Date": student.birth_date,
            "Age": student.age,
            "Contact": student.contact,
            "Guardian Name": student.guardian_name,
            "Guardian Contact": student.guardian_contact
        }
        missing = [k for k, v in required.items() if v is None or str(v).strip() == ""]
        if missing:
            QMessageBox.warning(parent, "Missing Information", "Please fill in: " + ", ".join(missing))
            return None

        # Validate age
        age = int(student.age)
        if age < 16:
            QMessageBox.warning(parent, "Age Restriction",
                                "Student must be at least 16 years old to enroll in Senior High School.")
            return None

        # Validate contact numbers
        if not (student.contact.isdigit() and len(student.contact) == 11):
            QMessageBox.warning(parent, "Invalid Input", "Student contact number must be exactly 11 digits.")
            return None
        if not (student.guardian_contact.isdigit() and len(student.guardian_contact) == 11):
            QMessageBox.warning(parent, "Invalid Input", "Guardian contact number must be exactly 11 digits.")
            return None

        # Add student to repo
        try:
            new_id = RegisteredStudentRepo.add(student)
            QMessageBox.information(parent, "Success", "Student registered successfully!")
            return new_id
        except RepositoryError as e:
            QMessageBox.critical(parent, "Repository Error", str(e))
            return None
        except Exception as e:
            QMessageBox.critical(parent, "Database Error", f"Failed to register student:\n{e}")
            return None

    @classmethod
    def list_registered(cls) -> List[RegisteredStudent]:
        # Return all registered students
        return RegisteredStudentRepo.get_all()

    @classmethod
    def get_registered(cls, sid: str) -> Optional[RegisteredStudent]:
        # Get student by ID
        return RegisteredStudentRepo.get(sid)

    @classmethod
    def update_registered(cls, student: RegisteredStudent, parent=None) -> bool:
        # Validate fields before update
        required = {
            "First Name": student.first_name,
            "Last Name": student.last_name,
            "Gender": student.gender,
            "Birth Date": student.birth_date,
            "Age": student.age,
            "Contact": student.contact,
            "Guardian Name": student.guardian_name,
            "Guardian Contact": student.guardian_contact
        }
        missing = [k for k, v in required.items() if v is None or str(v).strip() == ""]
        if missing:
            QMessageBox.warning(parent, "Missing Information", "Please fill in: " + ", ".join(missing))
            return False

        # Validate age and contacts
        age = int(student.age)
        if age < 16:
            QMessageBox.warning(parent, "Age Restriction",
                                "Student must be at least 16 years old to enroll in Senior High School.")
            return False
        if not (student.contact.isdigit() and len(student.contact) == 11):
            QMessageBox.warning(parent, "Invalid Input", "Student contact number must be exactly 11 digits.")
            return False
        if not (student.guardian_contact.isdigit() and len(student.guardian_contact) == 11):
            QMessageBox.warning(parent, "Invalid Input", "Guardian contact number must be exactly 11 digits.")
            return False

        # Update student in repo
        try:
            RegisteredStudentRepo.update(student.id, student)
            QMessageBox.information(parent, "Success", "Student information updated successfully!")
            return True
        except RepositoryError as e:
            QMessageBox.critical(parent, "Repository Error", str(e))
            return False
        except Exception as e:
            QMessageBox.critical(parent, "Database Error", f"Failed to update student:\n{e}")
            return False

    @classmethod
    def delete_registered(cls, student_id: str, parent=None) -> bool:
        # Delete student, check if enrolled
        try:
            deleted = RegisteredStudentRepo.delete(student_id)
            if deleted and parent:
                QMessageBox.information(parent, "Deleted", "Student information deleted successfully!")
            return deleted
        except DeletionBlockedError:
            if parent:
                QMessageBox.warning(parent, "Cannot Delete", "This student is currently enrolled. Drop student first.")
            return False
        except Exception as e:
            if parent:
                QMessageBox.critical(parent, "Error", f"Deletion failed:\n{e}")
            return False

    @classmethod
    def search_registered(cls, q: str) -> List[RegisteredStudent]:
        # Search students by name/contact
        return RegisteredStudentRepo.search(q)

    # ------------------ Enrolled Student Operations ------------------

    @classmethod
    def enroll_student(cls, enrollment: EnrolledStudent, parent=None) -> Optional[str]:
        # Enroll a student
        try:
            eid = EnrolledStudentRepo.enroll(enrollment)
            if parent:
                QMessageBox.information(parent, "Success", "Student successfully enrolled!")
            return eid
        except Exception as e:
            if parent:
                QMessageBox.critical(parent, "Enrollment Error", "Student Already Enrolled")
            return None

    @classmethod
    def list_enrolled(cls) -> List[Dict[str, Any]]:
        # List all enrolled students
        return EnrolledStudentRepo.get_all()

    @classmethod
    def update_enrollment(cls, eid: str, grade: str, strand: str, parent=None) -> bool:
        # Update enrolled student's grade/strand
        if not grade or not strand:
            if parent:
                QMessageBox.warning(parent, "Missing Information", "Grade and strand are required.")
            return False
        try:
            updated = EnrolledStudentRepo.update(eid, grade, strand)
            if parent:
                if updated:
                    QMessageBox.information(parent, "Updated", "Student updated successfully!")
                else:
                    QMessageBox.warning(parent, "Not Found", "Enrollment not found!")
            return updated
        except Exception as e:
            if parent:
                QMessageBox.critical(parent, "Error", f"Update failed:\n{e}")
            return False

    @classmethod
    def delete_enrolled(cls, eid: str, parent=None) -> bool:
        # Delete enrolled student
        try:
            deleted = EnrolledStudentRepo.delete(eid)
            if parent:
                if deleted:
                    QMessageBox.information(parent, "Student dropped", "Student record dropped successfully!")
                else:
                    QMessageBox.warning(parent, "Not Found", "Enrollment not found!")
            return deleted
        except Exception as e:
            if parent:
                QMessageBox.critical(parent, "Error", f"Deletion failed:\n{e}")
            return False

    @classmethod
    def filter_enrolled(cls, grade_level: str = None, strand: str = None):
        # Filter enrolled students by grade or strand
        return EnrolledStudentRepo.filter(grade_level, strand)
