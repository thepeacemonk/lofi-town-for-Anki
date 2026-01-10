from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo

try:
    from aqt.qt import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
except ImportError:
    # Fallback for older Anki versions or specific builds
    QWebEngineView = None
    QWebEngineProfile = None
    QWebEnginePage = None
    QWebEngineSettings = None

import os
import shutil

class LofiWindow(QMainWindow):
    def cleanup_cache(self, path):
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                print(f"Failed to clean cache: {e}")

    def __init__(self, parent=None):
        super(LofiWindow, self).__init__(parent)
        self.setWindowTitle("lofi.town")
        self.resize(1100, 750)

        # Ensure the window stays on top if desired
        addon_id = mw.addonManager.addonFromModule(__name__)
        config = mw.addonManager.getConfig(addon_id)
        if config and config.get("always_on_top", False):
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        if QWebEngineView is None:
            showInfo("QWebEngineView is not supported on this Anki version.")
            return

        self.browser = QWebEngineView()
        
        # Enable persistent cookies/storage so you stay logged in
        addon_dir = os.path.dirname(__file__)
        storage_path = os.path.join(addon_dir, "user_data")
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

        profile = QWebEngineProfile("LofiTownProfile", self.browser)
        # Set User Agent to Chrome to ensure standard browser behavior
        profile.setHttpUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        profile.setPersistentStoragePath(storage_path)

        # Separate cache path so we can clean it independently from cookies/storage
        cache_path = os.path.join(addon_dir, "cache_trash")
        self.cleanup_cache(cache_path)
        
        # Clean up legacy cache folders from previous versions if they exist in user_data
        for legacy_folder in ["GPUCache", "DawnCache", "VideoDecodeStats", "ShaderCache", "Code Cache"]:
            self.cleanup_cache(os.path.join(storage_path, legacy_folder))

        profile.setCachePath(cache_path)
        
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)

        page = QWebEnginePage(profile, self.browser)
        self.browser.setPage(page)
        
        # Configure web engine settings to isolate from Anki's styles
        if QWebEngineSettings:
            settings = page.settings()
            
            # Enable essential web features
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.XSSAuditingEnabled, True)
            
            # Ensure proper rendering without Anki interference
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
            
            # Enable modern web features for proper display
            settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
            
            # Prevent any style inheritance issues
            settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
        
        # Set a clean stylesheet for the browser widget itself to prevent Qt style leakage
        self.browser.setStyleSheet("")
        
        # Load lofi.town App
        self.browser.setUrl(QUrl("https://app.lofi.town/"))
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def closeEvent(self, event):
        # Unload the page to stop music/video
        if self.browser:
            self.browser.setUrl(QUrl("about:blank"))

        # Just hide the window instead of destroying it for faster reopening
        event.ignore()
        self.hide()

    def showEvent(self, event):
        # Reload if we are on blank page
        if self.browser and self.browser.url().toString() == "about:blank":
            self.browser.setUrl(QUrl("https://app.lofi.town/"))
        super().showEvent(event)

    def refresh(self):
        """Reload the current page."""
        if self.browser:
            self.browser.reload()