from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QFont


class LunaWindow:
    def __init__(self, title, x=140, y=80, w=760, h=480):
        self.title = title

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.visible = False
        self.minimized = False

        self.dragging = False
        self.drag_x = 0
        self.drag_y = 0

        self.close_rect = QRect()
        self.min_rect = QRect()

        # Smooth fade animation
        self.opacity = 0.0
        self.opening = False
        self.closing = False

    # -------------------------------------------------
    # Window states (compatible with DesktopScreen)
    # -------------------------------------------------

    def launch(self):
        self.visible = True
        self.minimized = False
        self.opening = True
        self.closing = False
        self.opacity = 0.0

    def restore(self):
        self.visible = True
        self.minimized = False
        self.opening = True
        self.closing = False
        self.opacity = 0.0

    # Backwards compatibility
    def open(self):
        self.launch()

    def minimize(self):
        self.minimized = True

    def close(self):
        self.opening = False
        self.closing = True

    # -------------------------------------------------
    # Animation
    # -------------------------------------------------

    def update_animation(self):
        if self.opening:
            self.opacity = min(1.0, self.opacity + 0.08)
            if self.opacity >= 1.0:
                self.opening = False

        if self.closing:
            self.opacity = max(0.0, self.opacity - 0.08)
            if self.opacity <= 0.0:
                self.visible = False
                self.closing = False

    # -------------------------------------------------
    # Hit testing
    # -------------------------------------------------

    def titlebar(self):
        return QRect(self.x, self.y, self.w, 42)

    def contains(self, px, py):
        if not self.visible or self.minimized:
            return False

        return (
            self.x <= px <= self.x + self.w
            and self.y <= py <= self.y + self.h
        )

    # -------------------------------------------------
    # Mouse
    # -------------------------------------------------

    def mouse_press(self, px, py):
        if not self.visible or self.minimized:
            return False

        if self.close_rect.contains(int(px), int(py)):
            self.close()
            return True

        if self.min_rect.contains(int(px), int(py)):
            self.minimize()
            return True

        if self.titlebar().contains(int(px), int(py)):
            self.dragging = True
            self.drag_x = px - self.x
            self.drag_y = py - self.y
            return True

        return self.contains(px, py)

    def mouse_move(self, px, py):
        if self.dragging:
            self.x = int(px - self.drag_x)
            self.y = int(py - self.drag_y)

    def mouse_release(self):
        self.dragging = False

    # -------------------------------------------------
    # Draw
    # -------------------------------------------------

    def draw(self, painter):
        self.update_animation()

        if not self.visible or self.minimized:
            return

        painter.save()
        painter.setOpacity(self.opacity)

        # Shadow
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 70))
        painter.drawRoundedRect(
            self.x + 6,
            self.y + 8,
            self.w,
            self.h,
            18,
            18,
        )

        # Window
        painter.setBrush(QColor(30, 33, 38, 240))
        painter.drawRoundedRect(
            self.x,
            self.y,
            self.w,
            self.h,
            18,
            18,
        )

        # Titlebar
        painter.setBrush(QColor(40, 44, 50, 245))
        painter.drawRoundedRect(
            self.x,
            self.y,
            self.w,
            42,
            18,
            18,
        )

        painter.setBrush(QColor(40, 44, 50))
        painter.drawRect(
            self.x,
            self.y + 21,
            self.w,
            21,
        )

        # Traffic lights
        r = 12

        self.close_rect = QRect(self.x + 16, self.y + 15, r, r)
        self.min_rect = QRect(self.x + 36, self.y + 15, r, r)

        painter.setBrush(QColor("#FF5F57"))
        painter.drawEllipse(self.close_rect)

        painter.setBrush(QColor("#FEBC2E"))
        painter.drawEllipse(self.min_rect)

        painter.setBrush(QColor("#28C840"))
        painter.drawEllipse(self.x + 56, self.y + 15, r, r)

        # Title (NO Luna logo)
        painter.setPen(QColor("#E8EDF5"))
        painter.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        painter.drawText(
            self.x,
            self.y,
            self.w,
            42,
            Qt.AlignCenter,
            self.title,
        )

        # Content
        painter.setBrush(QColor(22, 24, 29))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(
            self.x + 10,
            self.y + 52,
            self.w - 20,
            self.h - 62,
            12,
            12,
        )

        painter.restore()