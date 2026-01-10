from aqt import mw
from aqt.qt import *
import os
from . import font_utils
from .main import LofiWindow

class InstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent or mw)
        self.setWindowTitle("lofi.town Instructions")
        self.setMinimumWidth(550)
        self.setMinimumHeight(400)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        
        # Load font
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
            section_bg = "#68482E"
            link_color = "#DCE597"
        else:
            bg_color = "#F9F7E4"
            text_color = "#7D593A"
            btn_bg = "#DCE597"
            btn_text = "#7D593A"
            btn_hover = "#ECF5A7"
            section_bg = "#FFFFFF"
            link_color = "#B48555"

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
            }}
            QLabel {{
                color: {text_color};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                line-height: 1.5;
            }}
            QLabel.h1 {{
                font-family: '{self.title_font}', monospace;
                font-size: 20px;
                color: {text_color};
                margin-bottom: 15px;
            }}
            QLabel.h2 {{
                font-family: '{self.title_font}', monospace;
                font-size: 16px;
                color: {text_color};
                margin-top: 0px;
                margin-bottom: 8px;
            }}
            QLabel.body {{
                font-size: 14px;
                color: {text_color};
            }}
            QFrame.section {{
                background-color: {section_bg};
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 10px;
            }}
            QPushButton {{
                background-color: {btn_bg};
                color: {btn_text};
                border: 1px solid {btn_bg};
                border-radius: 20px; /* Pill shape */
                padding: 0px 24px;
                font-size: 14px;
                font-weight: 700;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                min-height: 40px;
                max-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
                border-color: {btn_hover};
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QWidget#scrollContent {{
                background-color: transparent;
            }}
        """)
        
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        content_widget.setObjectName("scrollContent")
        scroll_layout = QVBoxLayout(content_widget)
        scroll_layout.setContentsMargins(30, 30, 30, 30)
        scroll_layout.setSpacing(20)
        
        # Title
        title = QLabel("Instructions")
        title.setProperty("class", "h1")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(title)
        
        # 1. First Steps
        first_steps_frame = QFrame()
        first_steps_frame.setProperty("class", "section")
        fs_layout = QVBoxLayout(first_steps_frame)
        
        fs_title = QLabel("Getting Started")
        fs_title.setProperty("class", "h2")
        fs_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fs_layout.addWidget(fs_title)
        
        fs_text = QLabel()
        fs_text.setProperty("class", "body")
        fs_text.setWordWrap(True)
        fs_text.setTextFormat(Qt.TextFormat.RichText)
        fs_text.setText(f"""
        <p><b>Login Process:</b><br>
        Simply log in on <a href="lofi:login" style="color: {link_color}; text-decoration: underline;">app.lofi.town</a>.
        </p>
        """)
        fs_text.linkActivated.connect(self.handle_link)
        fs_layout.addWidget(fs_text)
        
        scroll_layout.addWidget(first_steps_frame)
        
        # 2. Shortcuts
        sc_frame = QFrame()
        sc_frame.setProperty("class", "section")
        sc_layout = QVBoxLayout(sc_frame)
        
        sc_title = QLabel("Shortcut")
        sc_title.setProperty("class", "h2")
        sc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sc_layout.addWidget(sc_title)
        
        sc_text = QLabel()
        sc_text.setProperty("class", "body")
        sc_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sc_text.setWordWrap(True)
        sc_text.setText(f"""
        <b>Open lofi.town: Shift + L</b>
        """)
        sc_layout.addWidget(sc_text)
        
        scroll_layout.addWidget(sc_frame)
        
        # 3. Functions
        funcs_frame = QFrame()
        funcs_frame.setProperty("class", "section")
        f_layout = QVBoxLayout(funcs_frame)
        
        f_title = QLabel("Menu Functions")
        f_title.setProperty("class", "h2")
        f_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_layout.addWidget(f_title)
        
        f_text = QLabel("""
        <ul>
        <li><b>Open lofi.town:</b> Open the main window.</li>
        <li><b>Refresh:</b> Reload the add-on if you encounter visual glitches.</li>
        <li><b>Instruction:</b> Open this guide again.</li>
        </ul>
        """)
        f_text.setProperty("class", "body")
        f_text.setWordWrap(True)
        f_layout.addWidget(f_text)
        
        scroll_layout.addWidget(funcs_frame)
        
        scroll_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Close button at bottom
        bottom_bar = QWidget()
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(20, 10, 20, 20)
        
        close_btn = QPushButton("Close")
        close_btn.setObjectName("actionBtn") # Reuse style
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(close_btn)
        bottom_layout.addStretch()
        
        main_layout.addWidget(bottom_bar)
        
        self.setLayout(main_layout)

    def handle_link(self, url):
        if url == "lofi:login":
            self.open_browser("https://app.lofi.town/")
        else:
            QDesktopServices.openUrl(QUrl(url))

    def open_browser(self, target_url):
        # Open in add-on browser window
        if not hasattr(mw, "lofi_window"):
            mw.lofi_window = LofiWindow(mw)
        
        mw.lofi_window.show()
        mw.lofi_window.activateWindow()
        
        # Navigate to URL
        if hasattr(mw.lofi_window, "browser"):
            mw.lofi_window.browser.setUrl(QUrl(target_url))
