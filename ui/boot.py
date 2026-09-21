from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPixmap


class BootScreen:
    def __init__(self):
        logo_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "icons"
            / "luna_logo.png"
        )

        self.logo = QPixmap(str(logo_path))

    def draw(self, painter, window):
        painter.fillRect(window.rect(), QColor("#07090C"))

        painter.setOpacity(window.bootOpacity)

        cx = window.width() // 2
        cy = window.height() // 2 - 45

        # LunaOS logo (LARGER)
        if not self.logo.isNull():
            logo = self.logo.scaled(
                170,
                170,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

            painter.drawPixmap(
                cx - logo.width() // 2,
                cy - logo.height() // 2,
                logo,
            )

        # Title
        painter.setPen(QColor("#D6DCE5"))
        painter.setFont(QFont("Segoe UI", 22, QFont.Light))
        painter.drawText(
            0,
            cy + 108,
            window.width(),
            35,
            Qt.AlignCenter,
            "LunaOS",
        )

        # Loading dots
        dots = "." * (window.dots + 1)

        painter.setPen(QColor("#8FA4C4"))
        painter.setFont(QFont("Segoe UI", 12))
        painter.drawText(
            0,
            cy + 145,
            window.width(),
            24,
            Qt.AlignCenter,
            dots,
        )