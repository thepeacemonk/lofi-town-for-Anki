"""
Deck Browser Widget for Lofi Town Add-on
Displays a 200px by 200px widget with Lofi Town stats on the deck browser.
"""

from aqt import mw, gui_hooks
import aqt.deckbrowser
import os
import base64

# Cache for the widget HTML
cached_html = None

def generate_css():
    """Generate CSS for the Lofi Town widget."""
    
    # Custom colors for Lofi Town
    bg_color = "#DCE597"
    button_color = "#8B9556"
    button_hover_color = "#372411"
    
    return f"""
        #lofi-widget-container {{
            position: relative;
            display: inline-block;
            margin-top: 20px;
            margin-bottom: 20px;
            margin-left: 6.875px;
            margin-right: 6.875px;
            
        }}
        
        #lofi-widget {{
            width: 200px;
            height: 200px;
            border-radius: 25px;
            background: {bg_color};
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 15px;
            box-sizing: border-box;
            position: relative;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}

        #lofi-widget .top-buttons {{
            position: absolute;
            top: 10px;
            right: 10px;
            display: flex;
            flex-direction: column;
            gap: 0px;
            z-index: 10;
        }}

        #lofi-widget .icon-btn {{
            width: 28px;
            height: 24px;
            cursor: pointer;
            background-color: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2px;
        }}

        #lofi-widget .icon-btn svg {{
            width: 20px; 
            height: 20px; 
            fill: {button_color}; 
            transition: fill 0.3s;
        }}

        #lofi-widget .icon-btn:hover svg {{
            fill: {button_hover_color};
        }}
        
        #lofi-widget .main-image {{
            width: 100px;
            height: 100px;
            object-fit: contain;
            margin-bottom: 15px;
        }}
        
        #lofi-widget .action-btn {{
            background-color: {button_color};
            color: white;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s, color 0.3s;
        }}
        
        #lofi-widget .action-btn:hover {{
            background-color: white;
            color: {button_color};
        }}
    """

def get_svg_content(filename):
    """Read SVG content from assets folder."""
    addon_dir = os.path.dirname(__file__)
    path = os.path.join(addon_dir, "assets", filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Strip potential <?xml ... ?> and DOCTYPE headers for cleaner embedding
            # Also remove existing fill attributes or style tags if we want CSS to control it rigidly,
            # but our CSS selectors targeting 'svg' fill should override attributes.
            # To be safe, we can remove the <svg ...> tag and wrapper logic if we want, or just return raw.
            # The reference code returned raw.
            return content
    return ""

def get_image_base64(filename):
    """Read image and return base64 string."""
    addon_dir = os.path.dirname(__file__)
    path = os.path.join(addon_dir, "assets", filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return ""

def generate_html():
    """Generate HTML for the Lofi Town widget."""
    
    # Top Buttons
    gear_svg = get_svg_content("gear.svg")
    refresh_svg = get_svg_content("refresh.svg")
    carrot_svg = get_svg_content("carrot.svg")
    
    buttons_html = f"""
        <div class="top-buttons">
            <div class="icon-btn" onclick="pycmd('lofi:settings')" title="Settings">
                {gear_svg}
            </div>
            <div class="icon-btn" onclick="pycmd('lofi:refresh')" title="Refresh">
                {refresh_svg}
            </div>
            <div class="icon-btn" onclick="pycmd('lofi:main')" title="Open Web App">
                {carrot_svg}
            </div>
        </div>
    """

    # Main Image
    img_b64 = get_image_base64("bunny_lofi_town.png")
    img_html = ""
    if img_b64:
        img_html = f'<img class="main-image" src="data:image/png;base64,{img_b64}" alt="Lofi Town Bunny">'

    # Main Button
    action_btn = f'''
        <button class="action-btn" onclick="pycmd('lofi:open')">
            Open lofi.town
        </button>
    '''
    
    return f"""
        <div id="lofi-widget">
            {buttons_html}
            {img_html}
            {action_btn}
        </div>
    """

def handle_lofi_commands(handled, message, context):
    """Handle JS messages from the widget."""
    if message == "lofi:settings":
        from . import show_settings
        show_settings()
        reset_cache()
        mw.deckBrowser.refresh()
        return (True, None)
    elif message == "lofi:open":
        from . import show_lofi
        show_lofi()
        return (True, None)
    elif message == "lofi:main":
        from . import show_lofi
        show_lofi()
        return (True, None)
    elif message == "lofi:refresh":
        from .reload_utils import reload_modules
        reload_modules()
        return (True, None)
    return handled

def add_widget_to_deck_browser(deck_browser: aqt.deckbrowser.DeckBrowser, 
                                content: aqt.deckbrowser.DeckBrowserContent):
    """Appends the Lofi widget to the deck browser's stats area."""
    global cached_html
    
    # Check if widget should be hidden
    addon_id = mw.addonManager.addonFromModule(__name__)
    config = mw.addonManager.getConfig(addon_id)
    if config and config.get("hide_widget", False):
        return

    # Prevent adding the widget multiple times in the same render
    if "<div id='lofi-widget-container'>" in content.stats:
        return
    
    if cached_html is None:
        css = generate_css()
        html_content = generate_html()
        cached_html = f"<div id='lofi-widget-container'><style>{css}</style>{html_content}</div>"
    
    content.stats += cached_html

def reset_cache(*args, **kwargs):
    """Clears the cached HTML, forcing a refresh on next view."""
    global cached_html
    cached_html = None

def on_theme_change():
    """Reset cache and refresh deck browser when theme changes."""
    reset_cache()
    if mw.state == "deckBrowser":
        mw.deckBrowser.refresh()

def init_deck_widget():
    """Initialize the deck browser widget."""
    # Register hooks
    # We should ensure we don't register hooks multiple times on reload
    # A simple way to avoid duplicates if this module is reloaded is tricky in this context, 
    # but for now we follow the pattern provided.
    gui_hooks.deck_browser_will_render_content.append(add_widget_to_deck_browser)
    gui_hooks.reviewer_will_end.append(reset_cache)
    gui_hooks.sync_did_finish.append(reset_cache)
    gui_hooks.theme_did_change.append(on_theme_change)
    
    # Register command handler if not already done
    if not hasattr(mw, "_lofi_widget_initialized"):
        gui_hooks.webview_did_receive_js_message.append(handle_lofi_commands)
        mw._lofi_widget_initialized = True

