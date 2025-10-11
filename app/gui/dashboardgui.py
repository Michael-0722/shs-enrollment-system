from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen, QFont
from app.items.service import StudentService
from app.styles.dashboard_styles import Colors, Styles, Dimensions, ChartColors


class SimpleStatCard(QFrame):
    def __init__(self, label_text):
        super().__init__()
        self.init_layout(label_text)

    def init_layout(self, label_text):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            Dimensions.CARD_PADDING_H,
            Dimensions.CARD_PADDING_V,
            Dimensions.CARD_PADDING_H,
            Dimensions.CARD_PADDING_V
        )
        layout.setSpacing(Dimensions.CARD_SPACING)

        self.label = QLabel(label_text)
        self.label.setStyleSheet(Styles.STAT_CARD_LABEL)

        self.number = QLabel("0")
        self.number.setStyleSheet(Styles.STAT_CARD_NUMBER)

        layout.addWidget(self.label)
        layout.addWidget(self.number)
        layout.addStretch()

    def update_value(self, val):
        self.number.setText(str(val))


class GroupedBarChart(QWidget):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.data = {}
        self.setMinimumHeight(Dimensions.CHART_MIN_HEIGHT)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        if not self.data:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        # Define chart area
        left_margin = Dimensions.CHART_LEFT_MARGIN
        right_margin = Dimensions.CHART_RIGHT_MARGIN
        top_margin = Dimensions.CHART_TOP_MARGIN
        bottom_margin = Dimensions.CHART_BOTTOM_MARGIN

        chart_width = width - left_margin - right_margin
        chart_height = height - top_margin - bottom_margin

        # Draw title
        font = QFont()
        font.setPointSize(Dimensions.FONT_CHART_TITLE)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(Colors.PRIMARY_TEXT)
        painter.drawText(left_margin, 30, self.title)

        if not self.data or all(v["g11"] == 0 and v["g12"] == 0 for v in self.data.values()):
            font.setBold(False)
            font.setPointSize(Dimensions.FONT_CHART_LABEL)
            painter.setFont(font)
            painter.setPen(Colors.MUTED_TEXT)
            painter.drawText(left_margin, top_margin + chart_height // 2, "No data available")
            return


        max_val = max((v["g11"] + v["g12"]) for v in self.data.values())
        if max_val == 0:
            max_val = 10


        y_max = ((max_val + 9) // 10) * 10


        painter.setPen(QPen(Colors.AXIS_LINE, 2))
        painter.drawLine(left_margin, top_margin, left_margin, top_margin + chart_height)


        font.setBold(False)
        font.setPointSize(Dimensions.FONT_CHART_AXIS)
        painter.setFont(font)

        num_ticks = 5
        for i in range(num_ticks + 1):
            y_value = (y_max // num_ticks) * i
            y_pos = top_margin + chart_height - (i * chart_height // num_ticks)


            painter.setPen(QPen(Colors.GRID_LINE, 1))
            painter.drawLine(left_margin, y_pos, left_margin + chart_width, y_pos)


            painter.setPen(Colors.SECONDARY_TEXT)
            painter.drawText(left_margin - 35, y_pos + 5, str(y_value))


        painter.setPen(QPen(Colors.AXIS_LINE, 2))
        painter.drawLine(left_margin, top_margin + chart_height,
                         left_margin + chart_width, top_margin + chart_height)


        num_groups = len(self.data)
        group_width = chart_width / num_groups
        bar_width = (group_width * 0.35)
        bar_spacing = bar_width * 0.2

        x_offset = left_margin + (group_width * 0.5) - (bar_width + bar_spacing / 2)

        font.setPointSize(Dimensions.FONT_CHART_AXIS)
        painter.setFont(font)

        for idx, (strand, values) in enumerate(self.data.items()):
            g11_val = values["g11"]
            g12_val = values["g12"]

            center_x = left_margin + (idx * group_width) + (group_width / 2)
            bar_x = center_x - (bar_width + bar_spacing / 2)


            if y_max > 0:
                g11_height = (g11_val / y_max) * chart_height
            else:
                g11_height = 0

            if g11_height > 0:
                painter.fillRect(
                    int(bar_x),
                    int(top_margin + chart_height - g11_height),
                    int(bar_width),
                    int(g11_height),
                    Colors.GRADE_11
                )

                # Value label on bar
                if g11_val > 0:
                    painter.setPen(Colors.PRIMARY_TEXT)
                    value_y = top_margin + chart_height - g11_height - 8
                    if g11_height < 25:
                        value_y = top_margin + chart_height - g11_height - 15
                    painter.drawText(
                        int(bar_x),
                        int(value_y),
                        int(bar_width),
                        20,
                        Qt.AlignmentFlag.AlignCenter,
                        str(g11_val)
                    )

            # Draw Grade 12 bar
            if y_max > 0:
                g12_height = (g12_val / y_max) * chart_height
            else:
                g12_height = 0

            if g12_height > 0:
                painter.fillRect(
                    int(bar_x + bar_width + bar_spacing),
                    int(top_margin + chart_height - g12_height),
                    int(bar_width),
                    int(g12_height),
                    Colors.GRADE_12
                )

                # Value label on bar
                if g12_val > 0:
                    painter.setPen(Colors.PRIMARY_TEXT)
                    value_y = top_margin + chart_height - g12_height - 8
                    if g12_height < 25:
                        value_y = top_margin + chart_height - g12_height - 15
                    painter.drawText(
                        int(bar_x + bar_width + bar_spacing),
                        int(value_y),
                        int(bar_width),
                        20,
                        Qt.AlignmentFlag.AlignCenter,
                        str(g12_val)
                    )

            # Draw strand label
            painter.setPen(Colors.PRIMARY_TEXT)
            font.setBold(True)
            font.setPointSize(Dimensions.FONT_CHART_LABEL)
            painter.setFont(font)
            painter.drawText(
                int(center_x - group_width / 2),
                int(top_margin + chart_height + 25),
                int(group_width),
                20,
                Qt.AlignmentFlag.AlignCenter,
                strand
            )
            font.setBold(False)
            font.setPointSize(Dimensions.FONT_CHART_AXIS)
            painter.setFont(font)

        # Draw legend
        legend_y = top_margin + chart_height + 55
        legend_x = left_margin + (chart_width // 2) - 100

        # Grade 11 legend
        painter.fillRect(legend_x, legend_y, 20, 15, Colors.GRADE_11)
        painter.setPen(Colors.PRIMARY_TEXT)
        painter.drawText(legend_x + 25, legend_y + 12, "Grade 11")

        # Grade 12 legend
        painter.fillRect(legend_x + 110, legend_y, 20, 15, Colors.GRADE_12)
        painter.drawText(legend_x + 135, legend_y + 12, "Grade 12")


class DonutChart(QWidget):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.data = {}
        self.setMinimumHeight(Dimensions.CHART_MIN_HEIGHT)

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        if not self.data:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        # Draw title
        font = QFont()
        font.setPointSize(Dimensions.FONT_CHART_TITLE)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(Colors.PRIMARY_TEXT)
        painter.drawText(30, 30, self.title)

        total = sum(self.data.values())
        if total == 0:
            font.setBold(False)
            font.setPointSize(Dimensions.FONT_CHART_LABEL)
            painter.setFont(font)
            painter.setPen(Colors.MUTED_TEXT)
            painter.drawText(30, height // 2, "No data available")
            return

        # Calculate donut dimensions
        donut_size = min(width - 80, height - 140)
        donut_x = (width - donut_size) // 2
        donut_y = 60

        inner_size = int(donut_size * 0.6)
        inner_x = donut_x + (donut_size - inner_size) // 2
        inner_y = donut_y + (donut_size - inner_size) // 2

        # Draw donut slices
        start_angle = 90 * 16  # Start at top

        for label, value in self.data.items():
            if value == 0:
                continue

            span_angle = int((value / total) * 360 * 16)
            color = ChartColors.get_grade_color(label)

            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(donut_x, donut_y, donut_size, donut_size, start_angle, span_angle)

            start_angle += span_angle

        # Draw inner white circle to create donut effect
        painter.setBrush(Colors.WHITE)
        painter.drawEllipse(inner_x, inner_y, inner_size, inner_size)

        # Draw total in center
        font.setBold(True)
        font.setPointSize(Dimensions.FONT_CHART_CENTER)
        painter.setFont(font)
        painter.setPen(Colors.PRIMARY_TEXT)
        painter.drawText(inner_x, inner_y, inner_size, inner_size,
                         Qt.AlignmentFlag.AlignCenter, str(total))

        font.setBold(False)
        font.setPointSize(Dimensions.FONT_CHART_LABEL)
        painter.setFont(font)
        painter.setPen(Colors.SECONDARY_TEXT)
        painter.drawText(inner_x, inner_y + inner_size // 2 + 20, inner_size, 20,
                         Qt.AlignmentFlag.AlignCenter, "Total Students")

        # Draw legend with percentages
        legend_y = donut_y + donut_size + 30
        legend_x = (width - 250) // 2

        font.setPointSize(Dimensions.FONT_CHART_LABEL)
        painter.setFont(font)

        for idx, (label, value) in enumerate(self.data.items()):
            color = ChartColors.get_grade_color(label)
            x_pos = legend_x + (idx * 130)

            # Color box
            painter.fillRect(x_pos, legend_y, 20, 15, color)

            # Label and percentage
            painter.setPen(Colors.PRIMARY_TEXT)
            percentage = (value / total * 100) if total > 0 else 0
            text = f"{label}: {value} ({percentage:.1f}%)"
            painter.drawText(x_pos + 25, legend_y + 12, text)


class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        QTimer.singleShot(100, self.load_data)

    def setup_ui(self):
        # Apply stylesheet
        self.setStyleSheet(Styles.get_full_stylesheet())

        main = QVBoxLayout(self)
        main.setContentsMargins(
            Dimensions.MAIN_MARGIN,
            Dimensions.MAIN_MARGIN,
            Dimensions.MAIN_MARGIN,
            Dimensions.MAIN_MARGIN
        )
        main.setSpacing(Dimensions.MAIN_SPACING)

        # Header
        header = QLabel("Dashboard")
        header.setStyleSheet(Styles.HEADER)
        main.addWidget(header)

        # Stats cards
        stats_grid = QGridLayout()
        stats_grid.setSpacing(Dimensions.STATS_SPACING)

        self.stats = {
            "enrolled": SimpleStatCard("Total Enrolled"),
            "registered": SimpleStatCard("Registered"),
            "g11": SimpleStatCard("Grade 11"),
            "g12": SimpleStatCard("Grade 12")
        }

        stats_grid.addWidget(self.stats["enrolled"], 0, 0)
        stats_grid.addWidget(self.stats["registered"], 0, 1)
        stats_grid.addWidget(self.stats["g11"], 0, 2)
        stats_grid.addWidget(self.stats["g12"], 0, 3)

        main.addLayout(stats_grid)

        # Charts container
        charts_container = QFrame()
        charts_container.setObjectName("chartsContainer")
        charts_layout = QGridLayout(charts_container)
        charts_layout.setContentsMargins(
            Dimensions.CARD_MARGIN,
            Dimensions.CARD_MARGIN,
            Dimensions.CARD_MARGIN,
            Dimensions.CARD_MARGIN
        )
        charts_layout.setSpacing(Dimensions.CHARTS_SPACING)

        # Create charts
        self.strand_chart = GroupedBarChart("Students by Strand")
        self.grade_chart = DonutChart("Grade Level Distribution")

        charts_layout.addWidget(self.strand_chart, 0, 0)
        charts_layout.addWidget(self.grade_chart, 0, 1)

        main.addWidget(charts_container, 1)

        # Refresh button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.load_data)
        refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_layout.addWidget(refresh)

        main.addLayout(btn_layout)

    def load_data(self):
        try:
            registered = StudentService.list_registered() or []
            enrolled = StudentService.list_enrolled() or []

            # Update stat cards
            self.stats["enrolled"].update_value(len(enrolled))
            self.stats["registered"].update_value(len(registered))

            g11_list = [s for s in enrolled if s.get("grade_level") == "11"]
            g12_list = [s for s in enrolled if s.get("grade_level") == "12"]

            self.stats["g11"].update_value(len(g11_list))
            self.stats["g12"].update_value(len(g12_list))

            # Prepare chart data
            strand_data = {}
            for strand_name in ["STEM", "ICT", "HUMSS", "GAS"]:
                g11_cnt = sum(1 for s in g11_list if s.get("strand") == strand_name)
                g12_cnt = sum(1 for s in g12_list if s.get("strand") == strand_name)
                strand_data[strand_name] = {
                    "g11": g11_cnt,
                    "g12": g12_cnt
                }

            grade_data = {
                "Grade 11": len(g11_list),
                "Grade 12": len(g12_list)
            }

            # Update charts
            self.strand_chart.set_data(strand_data)
            self.grade_chart.set_data(grade_data)

        except Exception as e:
            print(f"Error loading dashboard: {e}")