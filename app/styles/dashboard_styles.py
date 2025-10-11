"""
Dashboard Styles Module
Centralized styling for the dashboard components
"""

from PyQt6.QtGui import QColor


class Colors:
    """Color palette for the dashboard"""

    # Chart colors
    GRADE_11 = QColor("#e67e22")  # Orange
    GRADE_12 = QColor("#9b59b6")  # Purple

    # Text colors
    PRIMARY_TEXT = QColor("#2c3e50")
    SECONDARY_TEXT = QColor("#7f8c8d")
    MUTED_TEXT = QColor("#95a5a6")

    # UI colors
    BACKGROUND = "#f5f5f5"
    WHITE = QColor("#ffffff")
    CARD_BACKGROUND = "white"
    BORDER = "#e0e0e0"

    # Chart elements
    GRID_LINE = QColor("#ecf0f1")
    AXIS_LINE = QColor("#bdc3c7")

    # Button colors
    BUTTON_PRIMARY = "#3498db"
    BUTTON_HOVER = "#2980b9"
    BUTTON_PRESSED = "#21618c"


class Styles:
    """Qt StyleSheet definitions"""

    MAIN_WIDGET = f"""
        QWidget {{
            background-color: {Colors.BACKGROUND};
            BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        }}
    """

    BUTTON = f"""
        QPushButton {{
            background-color: {Colors.BUTTON_PRIMARY};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 13px;
        }}

        QPushButton:hover {{
            background-color: {Colors.BUTTON_HOVER};
        }}

        QPushButton:pressed {{
            background-color: {Colors.BUTTON_PRESSED};
        }}
    """

    STAT_CARD = f"""
        SimpleStatCard {{
            background-color: {Colors.CARD_BACKGROUND};
            border: 1px solid {Colors.BORDER};
            border-radius: 4px;
        }}
    """

    STAT_CARD_LABEL = "color: #666; font-size: 11px; font-weight: 500;"

    STAT_CARD_NUMBER = "color: #222; font-size: 32px; font-weight: 600;"

    CHARTS_CONTAINER = f"""
        QFrame#chartsContainer {{
            background-color: {Colors.CARD_BACKGROUND};
            border: 1px solid {Colors.BORDER};
            border-radius: 4px;
        }}
    """

    HEADER = f"""
        font-size: 24px; 
        font-weight: 600; 
        color: {Colors.PRIMARY_TEXT.name()}; 
        background: transparent;
    """

    @classmethod
    def get_full_stylesheet(cls):
        """Combine all styles into one stylesheet"""
        return f"""
            {cls.MAIN_WIDGET}
            {cls.BUTTON}
            {cls.STAT_CARD}
            {cls.CHARTS_CONTAINER}
        """


class Dimensions:
    """Layout dimensions and spacing"""

    # Margins
    MAIN_MARGIN = 30
    CARD_MARGIN = 20
    CARD_PADDING_V = 15
    CARD_PADDING_H = 20

    # Spacing
    MAIN_SPACING = 20
    STATS_SPACING = 15
    CHARTS_SPACING = 30
    CARD_SPACING = 8

    # Chart dimensions
    CHART_MIN_HEIGHT = 320
    CHART_LEFT_MARGIN = 60
    CHART_RIGHT_MARGIN = 40
    CHART_TOP_MARGIN = 60
    CHART_BOTTOM_MARGIN = 100

    # Font sizes
    FONT_HEADER = 24
    FONT_CHART_TITLE = 11
    FONT_CHART_LABEL = 10
    FONT_CHART_AXIS = 9
    FONT_CHART_CENTER = 24


class ChartColors:
    """Color mappings for charts"""

    GRADE_COLORS = {
        "Grade 11": Colors.GRADE_11,
        "Grade 12": Colors.GRADE_12
    }

    @classmethod
    def get_grade_color(cls, grade_label, default=None):
        """Get color for a grade level"""
        if default is None:
            default = Colors.MUTED_TEXT
        return cls.GRADE_COLORS.get(grade_label, default)