from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QFrame, QLabel
)
from PyQt6.QtCore import Qt
from app.gui.registergui import RegistrationTab
from app.gui.enrollmentgui import EnrolledTab
from app.gui.dashboardgui import DashboardTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Justin D. Nabunturan SHS Enrollment System")
        self.setMinimumSize(1355, 650)

        central = QWidget()
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left sidebar menu
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-right: 2px solid #34495e;
            }
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #3498db;
                border-left: 4px solid #2980b9;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 20px 15px;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # System title
        title_label = QLabel("SHS Enrollment\nSystem")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title_label)

        # Menu buttons
        self.dashboard_btn = QPushButton("Dashboard")
        self.dashboard_btn.setCheckable(True)
        self.dashboard_btn.setChecked(True)

        self.registration_btn = QPushButton("Register Students")
        self.registration_btn.setCheckable(True)

        self.enrolled_btn = QPushButton("Enrolled Students")
        self.enrolled_btn.setCheckable(True)

        sidebar_layout.addWidget(self.dashboard_btn)
        sidebar_layout.addWidget(self.registration_btn)
        sidebar_layout.addWidget(self.enrolled_btn)
        sidebar_layout.addStretch()

        # Right content area with stacked widget
        self.content_stack = QStackedWidget()

        self.dashboard_tab = DashboardTab()
        self.registration_tab = RegistrationTab()
        self.enrolled_tab = EnrolledTab()

        self.content_stack.addWidget(self.dashboard_tab)
        self.content_stack.addWidget(self.registration_tab)
        self.content_stack.addWidget(self.enrolled_tab)

        # Add to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack)

        self.setCentralWidget(central)

        # Connect buttons
        self.dashboard_btn.clicked.connect(lambda: self.switch_page(0))
        self.registration_btn.clicked.connect(lambda: self.switch_page(1))
        self.enrolled_btn.clicked.connect(lambda: self.switch_page(2))

        # Connect signal: when a student is enrolled in registration tab
        self.registration_tab.student_enrolled.connect(self.on_student_enrolled)

    def switch_page(self, index):
        # Uncheck all buttons
        self.dashboard_btn.setChecked(False)
        self.registration_btn.setChecked(False)
        self.enrolled_btn.setChecked(False)

        # Check the clicked button
        if index == 0:
            self.dashboard_btn.setChecked(True)
        elif index == 1:
            self.registration_btn.setChecked(True)
        elif index == 2:
            self.enrolled_btn.setChecked(True)

        # Switch to the corresponding page
        self.content_stack.setCurrentIndex(index)

    def on_student_enrolled(self, data: dict):
        # Add to enrolled tab & refresh dashboard
        self.enrolled_tab.add_student_to_table(data)
        self.enrolled_tab.load_enrolled()
