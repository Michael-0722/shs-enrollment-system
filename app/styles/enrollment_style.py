def get_enrollment_style():
    """Return the stylesheet for EnrolledTab."""
    return """
    QWidget#EnrolledTab {
        background-color: #F9FAFB;
        color: #2C2C2C;
        font-family: "Helvetica Neue";
        font-size: 11pt;
    }

    /* GroupBox style if used */
    QGroupBox {
        background-color: #FFFFFF;
        border: 1px solid #D1D1D1;
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
        font-size: 14px;
    }

    /* Inputs */
    QLineEdit, QComboBox {
        border: 1px solid #CCCCCC;
        border-radius: 6px;
        padding: 6px;
        background: #FFFFFF;
        color: #2C2C2C;
    }

    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #0078D4;
        background: #FFFFFF; /* keep default color when clicked */
        color: #2C2C2C;
    }

    QComboBox QAbstractItemView {
        selection-background-color: #CCE5FF;
        selection-color: #2C2C2C;
        background: #FFFFFF;
    }

    /* Buttons */
    QPushButton {
        background-color: #0078D4;
        color: white;
        border-radius: 6px;
        padding: 6px 10px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #005EA6;
    }

    QPushButton#update_btn {
        background-color: #34A853;
    }
    QPushButton#update_btn:hover {
        background-color: #2C8A44;
    }

    QPushButton#delete_btn {
        background-color: #EA4335;
    }
    QPushButton#delete_btn:hover {
        background-color: #C62828;
    }

    QPushButton#clear_btn {
        background-color: #F4B400;
        color: black;
    }
    QPushButton#clear_btn:hover {
        background-color: #DFA100;
    }

    /* Table */
    QTableWidget {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        gridline-color: #E0E0E0;
        selection-background-color: palette(highlight);  /* system default */
        selection-color: palette(highlighted-text);       /* system default */
    }

    QTableWidget::item:hover {
        background: #F2F9FF; /* subtle hover effect */
        color: #2C2C2C;
    }

    QHeaderView::section {
        background-color: #F3F4F6;
        padding: 6px;
        border: none;
        font-weight: bold;
    }
    """
