from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
import os

class ToggleSwitch(QCheckBox):
    """Custom animated toggle switch widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(44, 24)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Animation state
        self._position = 0.0
        self._animation = QVariantAnimation(self)
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._animation.valueChanged.connect(self._handle_animation_value)
        
    def _handle_animation_value(self, value):
        self._position = value
        self.update()
        
    def setChecked(self, checked):
        super().setChecked(checked)
        # Snap to target state if not validating interaction
        target = 1.0 if checked else 0.0
        if self._animation.state() == QAbstractAnimation.State.Stopped:
             self._position = target
             self.update()

    def mousePressEvent(self, event):
        # Toggle and animate
        new_state = not self.isChecked()
        super().setChecked(new_state)
        
        self._animation.stop()
        self._animation.setStartValue(self._position)
        self._animation.setEndValue(1.0 if new_state else 0.0)
        self._animation.start()
        event.accept()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Detect theme
        is_dark = mw.pm.night_mode() if hasattr(mw.pm, 'night_mode') else False
        
        # Define base colors
        if is_dark:
            off_color = QColor("#3A3A3A")
        else:
            off_color = QColor("#E5D09D") # Using secondary color for off state
        on_color = QColor("#DCE597") # Accent
        
        # Interpolate color based on position
        t = self._position
        
        r = off_color.red() + (on_color.red() - off_color.red()) * t
        g = off_color.green() + (on_color.green() - off_color.green()) * t
        b = off_color.blue() + (on_color.blue() - off_color.blue()) * t
        track_color = QColor(int(r), int(g), int(b))
        
        # Draw track
        track_rect = QRectF(0, 0, 44, 24)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(track_color)
        painter.drawRoundedRect(track_rect, 12, 12)
        
        # Draw thumb
        thumb_range = 44 - 20 - 4 # width - thumb_size - padding*2
        thumb_x = 2 + (thumb_range * t)
        thumb_rect = QRectF(thumb_x, 2, 20, 20)
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(thumb_rect)

class LofiSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("lofi.town Settings")
        self.setMinimumSize(500, 300)
        
        # Load custom font
        self.load_custom_font()
        
        self.setup_ui()
        self.load_settings()

    def load_custom_font(self):
        """Load the Silkscreen-Regular font"""
        addon_dir = os.path.dirname(__file__)
        self.font_path = os.path.join(addon_dir, "assets", "Silkscreen-Regular.ttf")
        
        if os.path.exists(self.font_path):
            font_id = QFontDatabase.addApplicationFont(self.font_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                self.custom_font_family = families[0] if families else "Arial"
            else:
                self.custom_font_family = "Arial"
        else:
            self.custom_font_family = "Arial"

    def setup_ui(self):
        # Detect theme
        is_dark = mw.pm.night_mode() if hasattr(mw.pm, 'night_mode') else False
        
        # Color scheme
        bg_color = "#7D593A" if is_dark else "#F9F7E4"
        text_color = "#F9F7E4" if is_dark else "#7D593A"
        accent_color = "#DCE597"
        btn_bg = "#B48555" # Secondary button bg
        
        # Get font name
        font_family = self.custom_font_family
        
        # Modern Stylesheet
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
            }}
            QLabel {{
                font-size: 14px;
                color: {text_color};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QLabel.section-title {{
                font-size: 16px;
                font-weight: 600;
                color: {text_color};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                padding: 4px 0px;
            }}
            QPushButton {{
                background-color: {btn_bg};
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QPushButton:hover {{
                background-color: #C49565;
            }}
            QPushButton:pressed {{
                background-color: #A47545;
            }}
            QPushButton#reportBtn {{
                background-color: #E5D09D;
                color: #7D593A;
                border-radius: 18px;
                padding: 0px 16px;
                font-size: 13px;
                font-weight: 600;
                min-height: 36px;
                max-height: 36px;
            }}
            QPushButton#reportBtn:hover {{
                background-color: #F5E0AD;
            }}
            QPushButton#donateBtn {{
                background-color: {accent_color};
                color: #7D593A;
                border: none;
                border-radius: 18px;
                padding: 0px 16px;
                font-size: 13px;
                font-weight: 600;
                min-height: 36px;
                max-height: 36px;
            }}
            QPushButton#donateBtn:hover {{
                background-color: #ECF5A7;
            }}
            QPushButton#saveBtn {{
                background-color: {accent_color};
                color: #7D593A;
            }}
            QPushButton#saveBtn:hover {{
                background-color: #ECF5A7;
            }}
            QPushButton#saveBtn:pressed {{
                background-color: #CCEB87;
            }}
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(32, 32, 32, 32)
        # Header Layout
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        header_layout.addStretch()  # Add stretch to center

        # Report Bug Button (Keeping generic or user can update later)
        report_btn = QPushButton("Report Bug")
        report_btn.setObjectName("reportBtn")
        report_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        report_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/thepeacemonk/lofi-town-for-Anki"))) # Assuming repo change or redirect
        report_btn.setFixedSize(120, 36)
        header_layout.addWidget(report_btn)

        # Logo (Centered)
        logo_label = QLabel()
        addon_dir = os.path.dirname(__file__)
        logo_path = os.path.join(addon_dir, "assets", "lofi_town_name.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            
            # High DPI Scaling Logic
            pixel_ratio = self.devicePixelRatioF()
            target_height = 40 # Slightly larger for text logo
            
            # Scale to (target_height * pixel_ratio)
            scaled_h = int(target_height * pixel_ratio)
            scaled_pixmap = pixmap.scaledToHeight(scaled_h, Qt.TransformationMode.SmoothTransformation)
            
            # Set device pixel ratio
            scaled_pixmap.setDevicePixelRatio(pixel_ratio)
            
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)

        # Donate Button
        donate_btn = QPushButton("Donate")
        donate_btn.setObjectName("donateBtn")
        donate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        donate_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://studio.buymeacoffee.com/dashboard")))
        donate_btn.setFixedSize(100, 36)
        header_layout.addWidget(donate_btn)
        
        header_layout.addStretch()  # Add stretch to center

        main_layout.addLayout(header_layout)
        main_layout.addSpacing(20)

        # Main Title
        title = QLabel("Configuration")
        title_font = QFont(self.custom_font_family, 22, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {text_color}; padding-bottom: 0px; font-family: '{self.custom_font_family}';")
        title.setMinimumHeight(35)  # Prevent clipping
        main_layout.addWidget(title)
        
        main_layout.addSpacing(8)  # Small space after title

        # Always on Top Section
        always_on_top_layout = QHBoxLayout()
        always_on_top_layout.setSpacing(12)
        
        always_on_top_label = QLabel("Always on Top")
        always_on_top_label.setProperty("class", "section-title")
        always_on_top_label.setMinimumHeight(28)  # Prevent clipping
        
        self.always_on_top_toggle = ToggleSwitch()
        self.always_on_top_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        
        always_on_top_layout.addWidget(always_on_top_label)
        always_on_top_layout.addStretch()
        always_on_top_layout.addWidget(self.always_on_top_toggle)
        
        main_layout.addLayout(always_on_top_layout)
        
        # Hide Widget Section
        hide_widget_layout = QHBoxLayout()
        hide_widget_layout.setSpacing(12)
        
        hide_widget_label = QLabel("Hide Widget")
        hide_widget_label.setProperty("class", "section-title")
        hide_widget_label.setMinimumHeight(28)  # Prevent clipping
        
        self.hide_widget_toggle = ToggleSwitch()
        self.hide_widget_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        
        hide_widget_layout.addWidget(hide_widget_label)
        hide_widget_layout.addStretch()
        hide_widget_layout.addWidget(self.hide_widget_toggle)
        
        main_layout.addLayout(hide_widget_layout)
        
        # Spacer to push buttons to bottom
        main_layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setMinimumHeight(40)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_settings)
        self.save_btn.setMinimumHeight(40)

        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def load_settings(self):
        config = mw.addonManager.getConfig(__name__)
        if config:
            self.always_on_top_toggle.setChecked(config.get("always_on_top", False))
            self.hide_widget_toggle.setChecked(config.get("hide_widget", False))

    def save_settings(self):
        config = mw.addonManager.getConfig(__name__)
        if config is None:
            config = {}
        
        config["always_on_top"] = self.always_on_top_toggle.isChecked()
        config["hide_widget"] = self.hide_widget_toggle.isChecked()
        mw.addonManager.writeConfig(__name__, config)
        
        # If the window is open, update it
        if hasattr(mw, "lofi_window") and mw.lofi_window.isVisible():
             # We need to restart the window to apply window flags
             mw.lofi_window.close()
             # Optionally trigger show_lofi again if we want to immediately reopen
             # from . import show_lofi
             # show_lofi()
             pass
        
        # Refresh deck browser to apply widget visibility changes
        if hasattr(mw, "deckBrowser") and mw.state == "deckBrowser":
            mw.deckBrowser.refresh()
             
        self.accept()
