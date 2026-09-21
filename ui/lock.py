from pathlib import Path

from PySide6.QtCore import Qt, QDateTime, QSize
from PySide6.QtGui import QColor, QFont, QPixmap


class LockScreen:
    def __init__(self):
        self.wallpaper = QPixmap(
            str(
                Path(__file__).resolve().parent.parent
                / "assets"
                / "wallpapers"
                / "lock.jpg"
            )
        )

        self.cached = QPixmap()
        self.cached_size = QSize()

    def get_wallpaper(self, window):
        if self.cached_size != window.size():
            self.cached = self.wallpaper.scaled(
                window.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation,
            )
            self.cached_size = window.size()

        return self.cached

    def draw(self, painter, window):
        # FIXED ↓
        wp = self.get_wallpaper(window)

        x = (window.width() - wp.width()) // 2
        y = (window.height() - wp.height()) // 2
        painter.drawPixmap(x, y, wp)

        now = QDateTime.currentDateTime()

        if window.screen == "lock":
            opacity = window.lockOpacity
            offset = 0
        else:
            opacity = 1 - window.loginOpacity
            offset = int(window.loginOpacity * -80)

        painter.setOpacity(opacity)

        # Moon icon
        painter.setPen(QColor("#E8EDF5"))
        painter.setFont(QFont("Segoe UI Symbol", 26))
        painter.drawText(
            0, 70 + offset, window.width(), 30,
            Qt.AlignCenter, "☾"
        )

        # Time
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Segoe UI", 76, QFont.Light))
        painter.drawText(
            0,
            window.height() // 2 - 120 + offset,
            window.width(),
            90,
            Qt.AlignCenter,
            now.toString("HH:mm")
        )

        # Date
        painter.setPen(QColor("#D6DCE5"))
        painter.setFont(QFont("Segoe UI", 18))
        painter.drawText(
            0,
            window.height() // 2 - 5 + offset,
            window.width(),
            30,
            Qt.AlignCenter,
            now.toString("dddd, d MMMM")
        )

        # Hint
        painter.setBrush(QColor(255, 255, 255, 28))
        painter.setPen(QColor(255, 255, 255, 40))
        painter.drawRoundedRect(
            window.width() // 2 - 95,
            window.height() - 78 + offset,
            190,
            36,
            18,
            18
        )

        painter.setPen(QColor("white"))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(
            window.width() // 2 - 95,
            window.height() - 78 + offset,
            190,
            36,
            Qt.AlignCenter,
            "Press any key"
        )