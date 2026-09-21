from pathlib import Path

from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainterPath,
    QPixmap,
)

from apps.files import FilesApp


class DesktopScreen:
    def __init__(self, window):
        self.window = window

        # ---------------- Menus ----------------

        self.start_open = False
        self.search_open = False
        self.power_open = False

        # ---------------- Wallpaper ----------------

        wallpaper = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "wallpapers"
            / "desktop.jpg"
        )

        self.wallpaper = QPixmap()
        self.wallpaper.load(str(wallpaper))

        # ---------------- Apps ----------------

        self.files = FilesApp(window)

        # ---------------- Taskbar ----------------

        self.start_rect = (0, 0, 0, 0)
        self.search_rect = (0, 0, 0, 0)
        self.files_rect = (0, 0, 0, 0)
        self.settings_rect = (0, 0, 0, 0)
        self.terminal_rect = (0, 0, 0, 0)

        # ---------------- Desktop Icons ----------------

        self.desktop_files_rect = (0, 0, 0, 0)
        self.recycle_rect = (0, 0, 0, 0)

        # ---------------- Start Menu ----------------

        self.files_start_rect = (0, 0, 0, 0)
        self.settings_start_rect = (0, 0, 0, 0)
        self.terminal_start_rect = (0, 0, 0, 0)
        self.power_start_rect = (0, 0, 0, 0)

        # ---------------- Search ----------------

        self.search_files_rect = (0, 0, 0, 0)

        # ---------------- Power Popup ----------------

        self.lock_rect = (0, 0, 0, 0)
        self.reboot_rect = (0, 0, 0, 0)
        self.shutdown_rect = (0, 0, 0, 0)

    # =================================================
    # Helpers
    # =================================================

    def inside(self, rect, x, y):
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry <= y <= ry + rh

    def open_files(self):
        if self.files.minimized:
            self.files.restore()

        elif not self.files.visible:
            self.files.launch()

        else:
            self.files.minimized = False

        self.window.update()

    # =================================================
    # Mouse
    # =================================================

    def click(self, x, y):

        # Files window
        if self.files.visible and not self.files.minimized:
            if self.files.contains(x, y):
                self.files.mouse_press(x, y)
                return True

        # Desktop Icons
        if self.inside(self.desktop_files_rect, x, y):
            self.open_files()
            return True

        if self.inside(self.recycle_rect, x, y):
            return True

        # Start
        if self.inside(self.start_rect, x, y):
            self.start_open = not self.start_open
            self.search_open = False
            self.power_open = False
            return True

        # Search
        if self.inside(self.search_rect, x, y):
            self.search_open = not self.search_open
            self.start_open = False
            self.power_open = False
            return True

        # Files
        if self.inside(self.files_rect, x, y):

            if self.files.visible and not self.files.minimized:
                self.files.minimize()
            else:
                self.open_files()

            self.start_open = False
            self.search_open = False
            self.power_open = False
            return True

        # Settings / Terminal
        if self.inside(self.settings_rect, x, y):
            return True

        if self.inside(self.terminal_rect, x, y):
            return True

        # Start Menu
        if self.start_open:

            if self.inside(self.files_start_rect, x, y):
                self.open_files()
                self.start_open = False
                return True

            if self.inside(self.settings_start_rect, x, y):
                return True

            if self.inside(self.terminal_start_rect, x, y):
                return True

            if self.inside(self.power_start_rect, x, y):
                self.power_open = not self.power_open
                return True

        # Search Panel
        if self.search_open:

            if self.inside(self.search_files_rect, x, y):
                self.open_files()
                self.search_open = False
                return True

        # Power Popup
        if self.power_open:

            if self.inside(self.lock_rect, x, y):
                self.window.lock_system()
                return True

            if self.inside(self.reboot_rect, x, y):
                self.window.reboot_system()
                return True

            if self.inside(self.shutdown_rect, x, y):
                self.window.shutdown_system()
                return True

        self.start_open = False
        self.search_open = False
        self.power_open = False
        return False
        # =================================================
    # Draw
    # =================================================

    def draw(self, painter):

        # ---------------- Wallpaper ----------------

        if not self.wallpaper.isNull():
            scaled = self.wallpaper.scaled(
                self.window.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation,
            )

            x = (self.window.width() - scaled.width()) // 2
            y = (self.window.height() - scaled.height()) // 2

            painter.drawPixmap(x, y, scaled)

        else:
            painter.fillRect(self.window.rect(), QColor("#081018"))

        # =================================================
        # DESKTOP ICONS
        # =================================================

        icon_x = 22
        icon_y = 34

        # ---------- Files ----------

        self.desktop_files_rect = (icon_x, icon_y, 68, 84)

        painter.setBrush(QColor(255, 255, 255, 10))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(icon_x, icon_y, 68, 68, 14, 14)

        painter.setBrush(QColor("#8FB8FF"))
        painter.drawRoundedRect(icon_x + 16, icon_y + 26, 36, 20, 6, 6)
        painter.drawRoundedRect(icon_x + 20, icon_y + 20, 14, 8, 3, 3)

        painter.setPen(QColor("#F5F7FB"))
        painter.setFont(QFont("Segoe UI", 8))
        painter.drawText(
            icon_x,
            icon_y + 70,
            68,
            12,
            Qt.AlignCenter,
            "Files",
        )

        # ---------- Recycle Bin ----------

        icon_y += 96

        self.recycle_rect = (icon_x, icon_y, 68, 84)

        painter.setBrush(QColor(255, 255, 255, 10))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(icon_x, icon_y, 68, 68, 14, 14)

        painter.setPen(QColor("#D6DCE5"))
        painter.setBrush(Qt.NoBrush)

        painter.drawLine(
            icon_x + 22,
            icon_y + 20,
            icon_x + 46,
            icon_y + 20,
        )

        painter.drawLine(
            icon_x + 28,
            icon_y + 16,
            icon_x + 40,
            icon_y + 16,
        )

        painter.drawRect(
            icon_x + 24,
            icon_y + 20,
            20,
            24,
        )

        painter.setPen(QColor("#F5F7FB"))
        painter.setFont(QFont("Segoe UI", 8))
        painter.drawText(
            icon_x - 4,
            icon_y + 70,
            76,
            12,
            Qt.AlignCenter,
            "Recycle Bin",
        )

        # =================================================
        # START MENU
        # =================================================

        if self.start_open:

            menu_w = 520
            menu_h = 590

            mx = 18
            my = self.window.height() - 68 - menu_h

            painter.setBrush(QColor(20, 24, 30, 245))
            painter.setPen(QColor(255, 255, 255, 18))
            painter.drawRoundedRect(mx, my, menu_w, menu_h, 24, 24)

            # Title

            painter.setPen(QColor("#F5F7FB"))
            painter.setFont(QFont("Segoe UI", 18, QFont.Bold))
            painter.drawText(mx + 24, my + 38, "LunaOS")

            painter.setPen(QColor("#B8C2CF"))
            painter.setFont(QFont("Segoe UI", 9))
            painter.drawText(mx + 24, my + 58, "Pinned")

            apps = [
                ("Files", "folder"),
                ("Settings", "gear"),
                ("Terminal", "terminal"),
                ("Calculator", "calc"),
                ("Notes", "note"),
                ("Browser", "web"),
            ]

            start_x = mx + 28
            start_y = my + 84

            for i, (name, icon) in enumerate(apps):

                cx = start_x + (i % 3) * 150
                cy = start_y + (i // 3) * 112

                rect = (cx, cy, 108, 86)

                if name == "Files":
                    self.files_start_rect = rect
                elif name == "Settings":
                    self.settings_start_rect = rect
                elif name == "Terminal":
                    self.terminal_start_rect = rect

                painter.setBrush(QColor(255, 255, 255, 12))
                painter.setPen(Qt.NoPen)
                painter.drawRoundedRect(cx, cy, 108, 86, 16, 16)

                # Folder
                if icon == "folder":
                    painter.setBrush(QColor("#8FB8FF"))
                    painter.drawRoundedRect(cx + 30, cy + 22, 46, 24, 6, 6)
                    painter.drawRoundedRect(cx + 36, cy + 16, 18, 8, 3, 3)

                # Gear
                elif icon == "gear":
                    painter.setPen(QColor("#D6DCE5"))
                    painter.setFont(QFont("Segoe UI Symbol", 20))
                    painter.drawText(cx, cy + 40, 108, 20, Qt.AlignCenter, "⚙")
                    painter.setPen(Qt.NoPen)

                # Terminal
                elif icon == "terminal":
                    painter.setBrush(QColor("#2B3440"))
                    painter.drawRoundedRect(cx + 30, cy + 18, 46, 30, 6, 6)

                    painter.setPen(QColor("#D6DCE5"))
                    painter.setFont(QFont("Consolas", 10))
                    painter.drawText(cx + 38, cy + 37, ">_")
                    painter.setPen(Qt.NoPen)

                # Calculator
                elif icon == "calc":
                    painter.setBrush(QColor("#D6DCE5"))
                    painter.drawRoundedRect(cx + 32, cy + 18, 42, 32, 6, 6)

                    painter.setBrush(QColor("#445162"))
                    for r in range(2):
                        for c in range(3):
                            painter.drawEllipse(
                                cx + 38 + c * 10,
                                cy + 28 + r * 8,
                                4,
                                4,
                            )

                # Notes
                elif icon == "note":
                    painter.setBrush(QColor("#E8EDF5"))
                    painter.drawRoundedRect(cx + 36, cy + 16, 36, 36, 5, 5)

                # Browser
                elif icon == "web":
                    painter.setPen(QColor("#8FB8FF"))
                    painter.setFont(QFont("Segoe UI Symbol", 20))
                    painter.drawText(cx, cy + 40, 108, 20, Qt.AlignCenter, "🌐")
                    painter.setPen(Qt.NoPen)

                painter.setPen(QColor("#F5F7FB"))
                painter.setFont(QFont("Segoe UI", 9))
                painter.drawText(
                    cx,
                    cy + 68,
                    108,
                    16,
                    Qt.AlignCenter,
                    name,
                )

            # =================================================
            # Bottom user section
            # =================================================

            painter.setPen(QColor(255, 255, 255, 18))
            painter.drawLine(
                mx + 20,
                my + menu_h - 74,
                mx + menu_w - 20,
                my + menu_h - 74,
            )

            avatar_x = mx + 24
            avatar_y = my + menu_h - 54

            # Avatar
            painter.setBrush(QColor("#223040"))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(avatar_x, avatar_y, 28, 28)

            painter.setPen(QColor("#D6DCE5"))
            painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
            painter.drawText(
                avatar_x,
                avatar_y + 20,
                28,
                10,
                Qt.AlignCenter,
                "L",
            )

            # User
            painter.setPen(QColor("#F5F7FB"))
            painter.setFont(QFont("Segoe UI", 9, QFont.DemiBold))
            painter.drawText(avatar_x + 40, avatar_y + 10, "User")

            painter.setPen(QColor("#9EA9B8"))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(avatar_x + 40, avatar_y + 22, "Local User")

            # =================================================
            # POWER BUTTON
            # =================================================

            pwr_x = mx + menu_w - 58
            pwr_y = avatar_y - 2

            self.power_start_rect = (pwr_x, pwr_y, 36, 34)

            painter.setBrush(QColor(255, 255, 255, 10))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(pwr_x, pwr_y, 36, 34, 10, 10)

            painter.setPen(QColor("#D6DCE5"))
            painter.setBrush(Qt.NoBrush)
            painter.drawArc(
                pwr_x + 9,
                pwr_y + 6,
                18,
                18,
                35 * 16,
                290 * 16,
            )
            painter.drawLine(
                pwr_x + 18,
                pwr_y + 5,
                pwr_x + 18,
                pwr_y + 15,
            )

            # =================================================
            # POWER POPUP
            # =================================================

            if self.power_open:

                pop_w = 160
                pop_h = 126

                pop_x = pwr_x - 118
                pop_y = pwr_y - pop_h - 8

                painter.setBrush(QColor(26, 30, 36, 248))
                painter.setPen(QColor(255, 255, 255, 18))
                painter.drawRoundedRect(
                    pop_x,
                    pop_y,
                    pop_w,
                    pop_h,
                    14,
                    14,
                )

                self.lock_rect = (pop_x + 8, pop_y + 8, 144, 32)
                self.reboot_rect = (pop_x + 8, pop_y + 46, 144, 32)
                self.shutdown_rect = (pop_x + 8, pop_y + 84, 144, 32)

                for text, rect in [
                    ("Lock", self.lock_rect),
                    ("Reboot", self.reboot_rect),
                    ("Shutdown", self.shutdown_rect),
                ]:
                    rx, ry, rw, rh = rect

                    painter.setBrush(QColor(255, 255, 255, 10))
                    painter.setPen(Qt.NoPen)
                    painter.drawRoundedRect(rx, ry, rw, rh, 8, 8)

                    painter.setPen(QColor("#F5F7FB"))
                    painter.setFont(QFont("Segoe UI", 9))
                    painter.drawText(rx + 12, ry + 20, text)
        # =================================================
        # SEARCH PANEL
        # =================================================

        if self.search_open:

            sw = 500
            sh = 430

            sx = self.window.width() // 2 - 250
            sy_panel = self.window.height() - 68 - sh

            painter.setBrush(QColor(20, 24, 30, 245))
            painter.setPen(QColor(255, 255, 255, 18))
            painter.drawRoundedRect(sx, sy_panel, sw, sh, 22, 22)

            # Search box
            painter.setBrush(QColor(255, 255, 255, 15))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(
                sx + 18,
                sy_panel + 18,
                sw - 36,
                42,
                18,
                18,
            )

            painter.setPen(QColor("#B8C2CF"))
            painter.setFont(QFont("Segoe UI", 10))
            painter.drawText(
                sx + 32,
                sy_panel + 44,
                "Search LunaOS",
            )

            painter.setPen(QColor("#F5F7FB"))
            painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
            painter.drawText(
                sx + 18,
                sy_panel + 88,
                "Best match",
            )

            results = ["Files", "Settings", "Terminal"]

            for i, item in enumerate(results):

                ry = sy_panel + 110 + i * 42

                rect = (sx + 18, ry, sw - 36, 34)

                if item == "Files":
                    self.search_files_rect = rect

                painter.setBrush(QColor(255, 255, 255, 10))
                painter.setPen(Qt.NoPen)
                painter.drawRoundedRect(
                    rect[0],
                    rect[1],
                    rect[2],
                    rect[3],
                    12,
                    12,
                )

                painter.setPen(QColor("#F5F7FB"))
                painter.setFont(QFont("Segoe UI", 9))
                painter.drawText(
                    rect[0] + 14,
                    rect[1] + 22,
                    item,
                )

        # =================================================
        # TASKBAR
        # =================================================

        h = 58

        grad = QLinearGradient(
            0,
            self.window.height() - h,
            0,
            self.window.height(),
        )

        grad.setColorAt(0, QColor(28, 30, 34, 220))
        grad.setColorAt(1, QColor(16, 18, 22, 230))

        painter.fillRect(
            0,
            self.window.height() - h,
            self.window.width(),
            h,
            grad,
        )

        sy = self.window.height() - 47

        # ---------- Start ----------

        sx = 12

        self.start_rect = (sx, sy, 36, 36)

        painter.setBrush(QColor(255, 255, 255, 18))
        painter.setPen(QColor(255, 255, 255, 22))
        painter.drawRoundedRect(sx, sy, 36, 36, 12, 12)

        painter.setBrush(QColor("#D6DCE5"))
        painter.setPen(Qt.NoPen)

        moon = QPainterPath()
        moon.addRoundedRect(sx + 10, sy + 6, 8, 22, 4, 4)

        foot = QPainterPath()
        foot.addRoundedRect(sx + 10, sy + 20, 18, 8, 4, 4)

        painter.drawPath(moon.united(foot))

        # =================================================
        # CENTERED APPS
        # =================================================

        center = self.window.width() // 2

        search_x = center - 84
        files_x = center - 28
        settings_x = center + 28
        terminal_x = center + 84

        # ---------- Search ----------

        self.search_rect = (search_x, sy, 36, 36)

        painter.setBrush(QColor(255, 255, 255, 16))
        painter.setPen(QColor(255, 255, 255, 22))
        painter.drawRoundedRect(search_x, sy, 36, 36, 12, 12)

        painter.setPen(QColor("#D6DCE5"))
        painter.drawEllipse(search_x + 9, sy + 9, 12, 12)
        painter.drawLine(search_x + 19, sy + 19, search_x + 25, sy + 25)

        # ---------- Files ----------

        self.files_rect = (files_x, sy, 36, 36)

        painter.setBrush(QColor(255, 255, 255, 16))
        painter.setPen(QColor(255, 255, 255, 22))
        painter.drawRoundedRect(files_x, sy, 36, 36, 12, 12)

        painter.setBrush(QColor("#8FB8FF"))
        painter.setPen(Qt.NoPen)

        painter.drawRoundedRect(files_x + 7, sy + 13, 22, 15, 5, 5)
        painter.drawRoundedRect(files_x + 9, sy + 9, 10, 6, 3, 3)

        if self.files.visible or self.files.minimized:
            painter.drawEllipse(files_x + 15, sy + 33, 6, 6)

        # ---------- Settings ----------

        self.settings_rect = (settings_x, sy, 36, 36)

        painter.setBrush(QColor(255, 255, 255, 16))
        painter.setPen(QColor(255, 255, 255, 22))
        painter.drawRoundedRect(settings_x, sy, 36, 36, 12, 12)

        painter.setPen(QColor("#D6DCE5"))
        painter.drawEllipse(settings_x + 11, sy + 11, 14, 14)
        painter.drawEllipse(settings_x + 15, sy + 15, 6, 6)

        # ---------- Terminal ----------

        self.terminal_rect = (terminal_x, sy, 36, 36)

        painter.setBrush(QColor(255, 255, 255, 16))
        painter.setPen(QColor(255, 255, 255, 22))
        painter.drawRoundedRect(terminal_x, sy, 36, 36, 12, 12)

        painter.setBrush(QColor("#D6DCE5"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(terminal_x + 7, sy + 9, 22, 18, 4, 4)

        painter.setPen(QColor("#14181E"))
        painter.setFont(QFont("Consolas", 8, QFont.Bold))
        painter.drawText(terminal_x + 11, sy + 21, ">")
        painter.drawLine(
            terminal_x + 17,
            sy + 21,
            terminal_x + 23,
            sy + 21,
        )

        # ---------------- Clock ----------------

        now = QDateTime.currentDateTime()

        painter.setPen(QColor("#F5F7FB"))
        painter.setFont(QFont("Segoe UI", 10))

        painter.drawText(
            self.window.width() - 82,
            self.window.height() - 36,
            70,
            14,
            Qt.AlignRight,
            now.toString("HH:mm"),
        )

        painter.setPen(QColor(210, 215, 225, 170))
        painter.setFont(QFont("Segoe UI", 7))

        painter.drawText(
            self.window.width() - 82,
            self.window.height() - 19,
            70,
            12,
            Qt.AlignRight,
            now.toString("dd MMMM"),
        )
        # =================================================
        # FILES WINDOW
        # =================================================

        self.files.draw(painter)