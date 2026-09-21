from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QLineEdit


class LoginScreen:
    def __init__(self, window, username, callback):
        self.window = window

        # Fix: accept either a dict or a plain string
        if isinstance(username, dict):
            self.username = username.get("name", "User")
        else:
            self.username = str(username)

        self.callback = callback

        self.password = QLineEdit(window)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Password")
        self.password.returnPressed.connect(self.callback)

        self.password.setStyleSheet("""
            QLineEdit{
                background: rgba(255,255,255,0.10);
                border: 1px solid rgba(255,255,255,0.18);
                border-radius: 16px;
                padding: 12px;
                color: white;
                font: 15px "Segoe UI";
                selection-background-color: rgba(214,220,229,0.35);
            }

            QLineEdit:focus{
                border: 1px solid rgba(214,220,229,0.70);
                background: rgba(255,255,255,0.14);
            }
        """)

        self.error_text = ""
        self.hide()

    def position(self):
        w = 320
        h = 46

        self.password.setGeometry(
            self.window.width() // 2 - w // 2,
            self.window.height() // 2 + 55,
            w,
            h
        )

    def show(self):
        self.position()
        self.password.show()
        self.password.setFocus()

    def hide(self):
        self.password.hide()

    def clear_password(self):
        self.password.clear()
        self.error_text = ""

    def get_password(self):
        return self.password.text()

    def error(self):
        self.error_text = "Incorrect password"
        self.password.clear()

    def draw(self, painter, opacity):
        painter.setOpacity(opacity)

        cx = self.window.width() // 2

        # Avatar circle
        painter.setBrush(QColor(255, 255, 255, 28))
        painter.setPen(QColor(255, 255, 255, 18))
        painter.drawEllipse(cx - 38, 145, 76, 76)

        # Moon L
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#D6DCE5"))

        painter.drawRoundedRect(cx - 12, 160, 8, 30, 4, 4)
        painter.drawRoundedRect(cx - 12, 182, 24, 8, 4, 4)

        # Username
        painter.setPen(QColor("#F5F7FB"))
        painter.setFont(QFont("Segoe UI", 16, QFont.DemiBold))
        painter.drawText(
            0, 235,
            self.window.width(), 28,
            Qt.AlignCenter,
            self.username
        )

        # Subtitle
        painter.setPen(QColor("#B8C2CF"))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(
            0, 258,
            self.window.width(), 20,
            Qt.AlignCenter,
            "Welcome back"
        )

        # Error
        if self.error_text:
            painter.setPen(QColor("#FF8E8E"))
            painter.setFont(QFont("Segoe UI", 9))
            painter.drawText(
                0,
                self.password.y() + 58,
                self.window.width(),
                20,
                Qt.AlignCenter,
                self.error_text
            )

        painter.setOpacity(1.0)