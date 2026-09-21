import sys

from PySide6.QtCore import (
    Qt,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
    Property,
)
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import QApplication, QWidget

from core.auth import Auth
from ui.boot import BootScreen
from ui.lock import LockScreen
from ui.login import LoginScreen
from ui.desktop import DesktopScreen


class LunaOS(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.screen = "boot"
        self.dots = 0

        self._bootOpacity = 0.0
        self._lockOpacity = 1.0
        self._loginOpacity = 0.0
        self._desktopOpacity = 0.0
        self._systemOpacity = 1.0

        self.auth = Auth()

        self.boot = BootScreen()
        self.lock = LockScreen()
        self.desktop = DesktopScreen(self)
        self.loginUI = LoginScreen(
            self,
            self.auth.current_user,
            self.login,
        )

        # ---------------- Timers ----------------

        self.dotTimer = QTimer(self)
        self.dotTimer.timeout.connect(self.animate_dots)
        self.dotTimer.start(450)

        self.clockTimer = QTimer(self)
        self.clockTimer.timeout.connect(self.refresh_clock)
        self.clockTimer.start(1000)

        # 60 FPS animation timer
        self.animationTimer = QTimer(self)
        self.animationTimer.timeout.connect(self.update)
        self.animationTimer.start(16)

        # Boot animation
        self.bootFade = QPropertyAnimation(self, b"bootOpacity")
        self.bootFade.setDuration(1800)
        self.bootFade.setStartValue(0)
        self.bootFade.setEndValue(1)
        self.bootFade.setEasingCurve(QEasingCurve.InOutQuad)

        QTimer.singleShot(500, self.bootFade.start)
        QTimer.singleShot(4700, self.start_transition)

        self.showFullScreen()

    # -----------------------------------------------------
    # Refresh
    # -----------------------------------------------------

    def refresh_clock(self):
        if self.screen in ("lock", "login", "desktop", "unlock"):
            self.update()

    def animate_dots(self):
        self.dots = (self.dots + 1) % 4
        self.update()

    # -----------------------------------------------------
    # Properties
    # -----------------------------------------------------

    def getBootOpacity(self):
        return self._bootOpacity

    def setBootOpacity(self, value):
        self._bootOpacity = value
        self.update()

    bootOpacity = Property(float, getBootOpacity, setBootOpacity)

    def getLockOpacity(self):
        return self._lockOpacity

    def setLockOpacity(self, value):
        self._lockOpacity = value
        self.update()

    lockOpacity = Property(float, getLockOpacity, setLockOpacity)

    def getLoginOpacity(self):
        return self._loginOpacity

    def setLoginOpacity(self, value):
        self._loginOpacity = value
        self.update()

    loginOpacity = Property(float, getLoginOpacity, setLoginOpacity)

    def getDesktopOpacity(self):
        return self._desktopOpacity

    def setDesktopOpacity(self, value):
        self._desktopOpacity = value
        self.update()

    desktopOpacity = Property(
        float,
        getDesktopOpacity,
        setDesktopOpacity,
    )

    def getSystemOpacity(self):
        return self._systemOpacity

    def setSystemOpacity(self, value):
        self._systemOpacity = value
        self.update()

    systemOpacity = Property(
        float,
        getSystemOpacity,
        setSystemOpacity,
    )

    # -----------------------------------------------------
    # Boot
    # -----------------------------------------------------

    def start_transition(self):
        self.dotTimer.stop()

        self.fade = QPropertyAnimation(self, b"bootOpacity")
        self.fade.setDuration(1000)
        self.fade.setStartValue(1)
        self.fade.setEndValue(0)
        self.fade.finished.connect(self.show_transition)
        self.fade.start()

    def show_transition(self):
        self.screen = "transition"
        self.update()
        QTimer.singleShot(1200, self.show_lock)

    def show_lock(self):
        """Always return to a fresh lock screen."""

        self.loginUI.hide()
        self.loginUI.clear_password()

        self.lockOpacity = 0
        self.loginOpacity = 0
        self.desktopOpacity = 0

        self.screen = "lock"

        self.fade = QPropertyAnimation(self, b"lockOpacity")
        self.fade.setDuration(500)
        self.fade.setStartValue(0)
        self.fade.setEndValue(1)
        self.fade.setEasingCurve(QEasingCurve.OutCubic)
        self.fade.start()

        # Restore keyboard focus after lock/reboot
        self.activateWindow()
        self.raise_()
        self.setFocus()

    # -----------------------------------------------------
    # Login
    # -----------------------------------------------------

    def show_login(self):
        self.screen = "login"

        self.loginUI.clear_password()
        self.loginUI.show()

        self.loginOpacity = 0

        self.fade = QPropertyAnimation(self, b"loginOpacity")
        self.fade.setDuration(300)
        self.fade.setStartValue(0)
        self.fade.setEndValue(1)
        self.fade.setEasingCurve(QEasingCurve.OutCubic)
        self.fade.start()

    def login(self):
        if self.auth.verify(self.loginUI.get_password()):

            self.loginUI.hide()

            self.screen = "unlock"

            self.desktopOpacity = 0

            self.fade = QPropertyAnimation(
                self,
                b"desktopOpacity",
            )
            self.fade.setDuration(700)
            self.fade.setStartValue(0)
            self.fade.setEndValue(1)
            self.fade.setEasingCurve(QEasingCurve.OutCubic)
            self.fade.finished.connect(self.finish_unlock)
            self.fade.start()

        else:
            self.loginUI.error()

    def finish_unlock(self):
        self.screen = "desktop"

        self.desktop.start_open = False
        self.desktop.search_open = False
        self.desktop.power_open = False

        self.update()

    # -----------------------------------------------------
    # Power
    # -----------------------------------------------------

    def lock_system(self):
        self.desktop.start_open = False
        self.desktop.search_open = False
        self.desktop.power_open = False

        self.loginUI.hide()
        self.loginUI.clear_password()

        self.show_lock()

    def reboot_system(self):
        self.desktop.start_open = False
        self.desktop.search_open = False
        self.desktop.power_open = False

        self.loginUI.hide()
        self.loginUI.clear_password()

        self.screen = "reboot"
        self.systemOpacity = 1
        self.dotTimer.start()

        QTimer.singleShot(2500, self.finish_reboot)

    def finish_reboot(self):
        self.dotTimer.stop()

        self.loginUI.hide()
        self.loginUI.clear_password()

        self.show_lock()

        self.activateWindow()
        self.raise_()
        self.setFocus()

    def shutdown_system(self):
        self.desktop.start_open = False
        self.desktop.search_open = False
        self.desktop.power_open = False

        self.screen = "shutdown"
        self.systemOpacity = 1

        # Show shutdown screen for 3 seconds
        QTimer.singleShot(3000, self.begin_shutdown_fade)

    def begin_shutdown_fade(self):
        self.fade = QPropertyAnimation(self, b"systemOpacity")
        self.fade.setDuration(1000)
        self.fade.setStartValue(1)
        self.fade.setEndValue(0)
        self.fade.setEasingCurve(QEasingCurve.OutCubic)
        self.fade.finished.connect(QApplication.instance().quit)
        self.fade.start()

    # -----------------------------------------------------
    # Events
    # -----------------------------------------------------

    def resizeEvent(self, event):
        self.loginUI.position()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if self.screen == "desktop":
            x = int(event.position().x())
            y = int(event.position().y())

            if self.desktop.click(x, y):
                self.update()
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.screen == "desktop":
            self.desktop.files.mouse_move(
                int(event.position().x()),
                int(event.position().y()),
            )
            self.update()

    def mouseReleaseEvent(self, event):
        if self.screen == "desktop":
            self.desktop.files.mouse_release()

    def keyPressEvent(self, event):

        if self.screen == "lock":
            if event.key() != Qt.Key_Meta:
                self.show_login()
            return

        if self.screen == "desktop":
            if event.key() == Qt.Key_Meta:
                self.desktop.start_open = (
                    not self.desktop.start_open
                )
                self.desktop.search_open = False
                self.desktop.power_open = False
                self.update()
                return

        super().keyPressEvent(event)

    # -----------------------------------------------------
    # System Screen
    # -----------------------------------------------------

    def draw_system(self, painter, text):
        painter.fillRect(self.rect(), QColor("#050607"))

        painter.setOpacity(self.systemOpacity)

        painter.setPen(QColor("#D6DCE5"))
        painter.setFont(QFont("Segoe UI", 24))
        painter.drawText(
            0,
            self.height() // 2 - 20,
            self.width(),
            40,
            Qt.AlignCenter,
            text,
        )

        painter.setFont(QFont("Segoe UI", 16))
        painter.drawText(
            0,
            self.height() // 2 + 18,
            self.width(),
            30,
            Qt.AlignCenter,
            "." * (self.dots + 1),
        )

    # -----------------------------------------------------
    # Paint
    # -----------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.screen == "boot":
            self.boot.draw(painter, self)

        elif self.screen == "transition":
            painter.fillRect(self.rect(), QColor("#111318"))

        elif self.screen == "lock":
            painter.setOpacity(self.lockOpacity)
            self.lock.draw(painter, self)

        elif self.screen == "login":
            self.lock.draw(painter, self)
            self.loginUI.draw(
                painter,
                self.loginOpacity,
            )

        elif self.screen == "unlock":
            self.desktop.draw(painter)

            painter.setOpacity(1 - self.desktopOpacity)
            painter.fillRect(self.rect(), QColor("#07090C"))

        elif self.screen == "desktop":
            self.desktop.draw(painter)

        elif self.screen == "reboot":
            self.draw_system(painter, "Rebooting")

        elif self.screen == "shutdown":
            self.draw_system(painter, "Shutting down")


app = QApplication(sys.argv)

window = LunaOS()
window.show()

sys.exit(app.exec())