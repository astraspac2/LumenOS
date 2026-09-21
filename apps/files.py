from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont

from core.window import LunaWindow


class FilesApp(LunaWindow):
    def __init__(self, window):
        self.window = window

        super().__init__(
            title="Files",
            x=170,
            y=90,
            w=820,
            h=520,
        )

        self.sidebar = [
            "Home",
            "Desktop",
            "Downloads",
            "Documents",
            "Pictures",
            "Music",
        ]

        self.current = "Desktop"

        self.visible = False
        self.minimized = False
        self.launching = False

        self.launch_timer = QTimer()
        self.launch_timer.setSingleShot(True)
        self.launch_timer.timeout.connect(self.finish_launch)

    # ---------------------------------------------------------
    # Open / Launch / Restore
    # ---------------------------------------------------------

    def open(self):
        """Called by desktop.py"""
        self.launch()

    def launch(self):
        if self.visible and not self.minimized:
            return

        self.visible = False
        self.minimized = False
        self.launching = True

        self.launch_timer.start(1000)

        if self.window:
            self.window.update()

    def finish_launch(self):
     self.launching = False

     self.visible = True
     self.minimized = False

     # Trigger the fade animation from LunaWindow
     self.opening = True
     self.opacity = 0.0

     if self.window:
        self.window.update()

    # ---------------------------------------------------------
    # Mouse
    # ---------------------------------------------------------

    def mouse_press(self, px, py):
        handled = super().mouse_press(px, py)

        if self.window:
            self.window.update()

        return handled

    # ---------------------------------------------------------
    # Draw
    # ---------------------------------------------------------

    def draw(self, painter):
        if self.launching:
            return

        if not self.visible:
            return

        super().draw(painter)

        if self.minimized:
            return

        # Sidebar
        painter.setBrush(QColor(34, 37, 42))
        painter.drawRoundedRect(
            self.x + 16,
            self.y + 58,
            170,
            self.h - 74,
            10,
            10,
        )

        painter.setFont(QFont("Segoe UI", 10))

        for i, item in enumerate(self.sidebar):
            yy = self.y + 78 + i * 42

            if item == self.current:
                painter.setBrush(QColor(143, 184, 255, 45))
                painter.drawRoundedRect(
                    self.x + 22,
                    yy - 6,
                    158,
                    30,
                    8,
                    8,
                )
                painter.setPen(QColor("#D6DCE5"))
            else:
                painter.setPen(QColor("#9EA9B8"))

            painter.drawText(self.x + 36, yy + 12, item)

        # Main area
        painter.setBrush(QColor(24, 26, 31))
        painter.drawRoundedRect(
            self.x + 196,
            self.y + 58,
            self.w - 212,
            self.h - 74,
            10,
            10,
        )

        painter.setPen(QColor("#D6DCE5"))
        painter.setFont(QFont("Segoe UI", 16, QFont.DemiBold))
        painter.drawText(
            self.x + 216,
            self.y + 88,
            self.current,
        )

        folders = [
            "Projects",
            "Wallpapers",
            "Games",
            "School",
            "Music",
            "Videos",
        ]

        painter.setFont(QFont("Segoe UI", 9))

        for i, folder in enumerate(folders):
            col = i % 3
            row = i // 3

            fx = self.x + 225 + col * 150
            fy = self.y + 125 + row * 120

            painter.setBrush(QColor("#8FB8FF"))
            painter.drawRoundedRect(
                fx,
                fy,
                52,
                42,
                8,
                8,
            )

            painter.drawRoundedRect(
                fx + 6,
                fy - 6,
                22,
                10,
                4,
                4,
            )

            painter.setPen(QColor("#E8EDF5"))
            painter.drawText(
                fx - 10,
                fy + 60,
                72,
                18,
                Qt.AlignCenter,
                folder,
            )