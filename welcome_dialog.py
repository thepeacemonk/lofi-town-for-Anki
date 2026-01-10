from aqt import mw
from aqt.qt import *
import os
from . import font_utils

class WelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to lofi.town")
        # self.setFixedSize(500, 500)  # Removed fixed size to allow flexibility
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint) 
        
        # Load fonts
        self.title_font = font_utils.load_custom_font("Silkscreen-Regular.ttf")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Detect theme
        is_dark = mw.pm.night_mode() if hasattr(mw.pm, 'night_mode') else False
        
        # Color Palette
        if is_dark:
            bg_color = "#7D593A"
            text_color = "#F9F7E4"
            btn_bg = "#B48555"
            btn_text = "#FFFFFF"
            btn_hover = "#C49565"
        else:
            bg_color = "#F9F7E4"
            text_color = "#7D593A"
            btn_bg = "#DCE597"
            btn_text = "#7D593A"
            btn_hover = "#ECF5A7"

        # Stylesheet
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
            }}
            QPushButton {{
                background-color: {btn_bg};
                color: {btn_text};
                border: none;
                border-radius: 25px;
                padding: 12px 40px;
                font-size: 15px;
                font-weight: 700;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                min-height: 26px;
                max-height: 26px;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
            }}
            QPushButton:pressed {{
                background-color: #CCEB87;
            }}
            QPushButton:focus {{
                outline: none;
            }}
            QPushButton.secondary {{
                background-color: transparent;
                color: {text_color};
                border: 2px solid {btn_bg};
                border-radius: 20px;
                padding: 8px 30px;
                font-size: 13px;
                font-weight: 600;
                min-height: 20px;
                max-height: 20px;
            }}
            QPushButton.secondary:hover {{
                background-color: {btn_bg};
                color: {btn_text};
            }}
            QCheckBox {{
                color: {text_color};
                font-size: 13px;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid {btn_bg};
            }}
            QCheckBox::indicator:checked {{
                background-color: {btn_bg};
                border: 2px solid {btn_bg};
            }}
            QCheckBox::indicator:checked::after {{
                content: "✓";
                color: {btn_text};
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)
        
        layout.addStretch()
        
        # Logo Image
        addon_dir = os.path.dirname(__file__)
        img_path = os.path.join(addon_dir, "assets", "lofi_town_name.png") 
        if os.path.exists(img_path):
            img_label = QLabel()
            pixmap = QPixmap(img_path)
            pixel_ratio = self.devicePixelRatioF()
            # Increased width to be prominent and uncropped
            target_width = 280
            scaled_w = int(target_width * pixel_ratio)
            scaled_pixmap = pixmap.scaledToWidth(scaled_w, Qt.TransformationMode.SmoothTransformation)
            scaled_pixmap.setDevicePixelRatio(pixel_ratio)
            img_label.setPixmap(scaled_pixmap)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(img_label)
            
        layout.addStretch()
        
        # Buttons
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(15)
        
        start_btn = QPushButton("Log in / Sign up")
        start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        start_btn.clicked.connect(self.open_lofi)
        btn_layout.addWidget(start_btn)
        
        # Instructions button (smaller, secondary style)
        instructions_btn = QPushButton("Instructions")
        instructions_btn.setProperty("class", "secondary")
        instructions_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        instructions_btn.clicked.connect(self.open_instructions)
        btn_layout.addWidget(instructions_btn)

        layout.addLayout(btn_layout)
        
        layout.addSpacing(20)
        
        # Don't show again checkbox
        self.dont_show_again = QCheckBox("Don't show this again")
        self.dont_show_again.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.dont_show_again, 0, Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(10)
        
        self.setLayout(layout)
        
    def save_preference(self):
        """Save the 'don't show again' preference"""
        config = mw.addonManager.getConfig(__name__)
        if config is None: 
            config = {}
        config["show_welcome"] = not self.dont_show_again.isChecked()
        mw.addonManager.writeConfig(__name__, config)
    
    def open_lofi(self):
        # Save preference
        self.save_preference()
        
        # Open Main Window
        from . import show_lofi
        show_lofi()
        self.accept()
    
    def open_instructions(self):
        """Open the instructions dialog"""
        from .instructions_dialog import InstructionsDialog
        dialog = InstructionsDialog(self)
        dialog.exec()
    
    def closeEvent(self, event):
        """Save preference when dialog is closed"""
        self.save_preference()
        super().closeEvent(event)
