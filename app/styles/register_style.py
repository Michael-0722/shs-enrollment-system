def get_register_style():
    return """
    QWidget#RegistrationTab {
        background-color: #F9FAFB;
        color: #2C2C2C;
        font-family: "Helvetica Neue";
        font-size: 11pt;
    }

    /* Group Box */
    QGroupBox {
        background-color: #FFFFFF;
        border: 1px solid #D1D1D1;
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
        font-size: 14px;
    }

    /* Inputs */
    QLineEdit, QComboBox, QDateEdit {
        border: 1px solid #CCCCCC;
        border-radius: 6px;
        padding: 6px;
        background: #FFFFFF;
        color: #2C2C2C;
    }

    /* Hover effect only (no blur/dim when clicked) */
    QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
        border: 1px solid #0078D4;
        background: #FFFFFF;
        color: #2C2C2C;
    }

    /* Combobox popup */
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

    QPushButton#clear_btn {
        background-color: #F4B400;
        color: black;
    }
    QPushButton#clear_btn:hover {
        background-color: #DFA100;
    }

    QPushButton#delete_btn {
        background-color: #EA4335;
    }
    QPushButton#delete_btn:hover {
        background-color: #C62828;
    }

    /* Table */
    QTableWidget {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        gridline-color: #E0E0E0;
        selection-background-color: palette(highlight); /* default system color */
        selection-color: palette(highlighted-text);    /* default text color */
    }

    QTableWidget::item:hover {
        background: #F2F9FF; /* gentle hover effect */
        color: #2C2C2C;
    }

    QHeaderView::section {
        background-color: #F3F4F6;
        padding: 6px;
        border: none;
        font-weight: bold;
    }
    """
