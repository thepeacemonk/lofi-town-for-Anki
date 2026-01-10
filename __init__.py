from aqt import mw
from aqt.qt import QAction, QMenu, QKeySequence
from .main import LofiWindow
from .settings import LofiSettingsDialog
from .reload_utils import reload_modules

def show_lofi():
    if not hasattr(mw, "lofi_window"):
        mw.lofi_window = LofiWindow(mw)
    mw.lofi_window.show()
    mw.lofi_window.activateWindow()

def show_settings():
    d = LofiSettingsDialog(mw)
    d.exec()

# Setup the menu item in Tools
lofi_menu = QMenu("lofi.town", mw)
mw.form.menuTools.addMenu(lofi_menu)

action = QAction("Open lofi.town", mw)
action.setShortcut(QKeySequence("Shift+L"))
action.triggered.connect(show_lofi)
lofi_menu.addAction(action)

settings_action = QAction("Settings", mw)
settings_action.triggered.connect(show_settings)
lofi_menu.addAction(settings_action)

# Add separator and reload action for development
lofi_menu.addSeparator()
reload_action = QAction("Refresh Add-on", mw)
reload_action.triggered.connect(reload_modules)
lofi_menu.addAction(reload_action)

def show_instructions():
    from .instructions_dialog import InstructionsDialog
    if not hasattr(mw, "instructions_dialog") or not mw.instructions_dialog:
        mw.instructions_dialog = InstructionsDialog(mw)
    mw.instructions_dialog.show()
    mw.instructions_dialog.activateWindow()
    mw.instructions_dialog.raise_()

instr_action = QAction("Instructions", mw)
instr_action.triggered.connect(show_instructions)
lofi_menu.insertAction(settings_action, instr_action)

def check_welcome_screen():
    config = mw.addonManager.getConfig(__name__)
    if config is None:
        config = {}
    
    # Default true if not set
    if config.get("show_welcome", True):
        # We need to show the welcome screen
        # Use a timer to ensure main window is visible/ready
        from .welcome_dialog import WelcomeDialog
        if not hasattr(mw, "welcome_dialog") or not mw.welcome_dialog:
            mw.welcome_dialog = WelcomeDialog(mw)
        mw.welcome_dialog.show()
        mw.welcome_dialog.activateWindow()
        mw.welcome_dialog.raise_()

from aqt import gui_hooks
gui_hooks.profile_did_open.append(check_welcome_screen)

# Initialize deck browser widget
from .deck_widget import init_deck_widget
init_deck_widget()