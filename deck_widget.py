from aqt import mw
from aqt.qt import *
import os

def get_widget_html():
    """Generate the HTML for the deck browser widget."""
    import base64
    
    # Get the image as base64
    addon_dir = os.path.dirname(__file__)
    image_path = os.path.join(addon_dir, "assets", "bunny_lofi_town.png")
    
    with open(image_path, "rb") as img_file:
        image_data = base64.b64encode(img_file.read()).decode('utf-8')
    
    image_url = f"data:image/png;base64,{image_data}"
    
    # Read the SVG content directly
    gear_path = os.path.join(addon_dir, "assets", "gear.svg")
    with open(gear_path, "r", encoding="utf-8") as gear_file:
        gear_svg = gear_file.read()
    
    # Process gear SVG to add styling capabilities
    # We remove any existing fill and add width/height/transition
    gear_svg = gear_svg.replace('<svg ', '<svg style="width: 20px; height: 20px; fill: #8B9556; transition: fill 0.3s;" id="gear-icon" ')
    
    refresh_path = os.path.join(addon_dir, "assets", "refresh.svg")
    with open(refresh_path, "r", encoding="utf-8") as refresh_file:
        refresh_svg = refresh_file.read()
        
    # Process refresh SVG
    refresh_svg = refresh_svg.replace('<svg ', '<svg style="width: 20px; height: 20px; fill: #8B9556; transition: fill 0.3s;" id="refresh-icon" ')
    
    carrot_path = os.path.join(addon_dir, "assets", "carrot.svg")
    with open(carrot_path, "r", encoding="utf-8") as carrot_file:
        carrot_svg = carrot_file.read()
        
    # Process carrot SVG
    carrot_svg = carrot_svg.replace('<svg ', '<svg style="width: 20px; height: 20px; fill: #8B9556; transition: fill 0.3s;" id="carrot-icon" ')
    
    html = f"""
    <div id="lofi-widget" style="
        width: 200px;
        height: 200px;
        background-color: #DCE597;
        border-radius: 25px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 15px;
        box-sizing: border-box;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        position: relative;
    ">
        <!-- Icon buttons in top right -->
        <div style="
            position: absolute;
            top: 10px;
            right: 10px;
            display: flex;
            flex-direction: column;
            gap: 0px;
        ">
            <!-- Gear icon button -->
            <div role="button" onclick="pycmd('lofi:settings')" style="
                background-color: transparent;
                cursor: pointer;
                padding: 2px;
                width: 28px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
            " onmouseover="document.getElementById('gear-icon').style.fill='#372411'" 
               onmouseout="document.getElementById('gear-icon').style.fill='#8B9556'">
                {gear_svg}
            </div>
            
            <!-- Refresh icon button -->
            <div role="button" onclick="pycmd('lofi:refresh')" style="
                background-color: transparent;
                cursor: pointer;
                padding: 2px;
                width: 28px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
            " onmouseover="document.getElementById('refresh-icon').style.fill='#372411'" 
               onmouseout="document.getElementById('refresh-icon').style.fill='#8B9556'">
                {refresh_svg}
            </div>
            
            <!-- Carrot icon button -->
            <div role="button" onclick="pycmd('lofi:main')" style="
                background-color: transparent;
                cursor: pointer;
                padding: 2px;
                width: 28px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
            " onmouseover="document.getElementById('carrot-icon').style.fill='#372411'" 
               onmouseout="document.getElementById('carrot-icon').style.fill='#8B9556'">
                {carrot_svg}
            </div>
        </div>
        
        <img src="{image_url}" style="
            width: 100px;
            height: 100px;
            object-fit: contain;
            margin-bottom: 15px;
        " alt="Lofi Town Bunny">
        
        <button onclick="pycmd('lofi:open')" style="
            background-color: #8B9556;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s, color 0.3s;
        " onmouseover="this._bg=this.style.backgroundColor; this._c=this.style.color; this.style.backgroundColor=this._c; this.style.color=this._bg" 
           onmouseout="this.style.backgroundColor=this._bg; this.style.color=this._c">
            Open lofi.town
        </button>
    </div>
    """
    return html

def on_deck_browser_will_render_content(deck_browser, content):
    """Hook to add widget to deck browser."""
    # Check if widget should be hidden
    config = mw.addonManager.getConfig(__name__)
    if config and config.get("hide_widget", False):
        return  # Don't add widget if hidden
    
    widget_html = get_widget_html()
    
    # Add the widget to the deck browser content
    # Insert it at the top of the page
    content.stats += widget_html

def on_widget_command(handled, cmd, context):
    """Handle commands from the widget."""
    if cmd == "lofi:open":
        from . import show_lofi
        show_lofi()
        return True, None
    elif cmd == "lofi:settings":
        from . import show_settings
        show_settings()
        return True, None
    elif cmd == "lofi:main":
        from . import show_lofi
        show_lofi()
        return True, None
    elif cmd == "lofi:refresh":
        from .reload_utils import reload_modules
        reload_modules()
        return True, None
    return handled

def init_deck_widget():
    """Initialize the deck browser widget."""
    from aqt import gui_hooks
    
    # Add widget to deck browser
    gui_hooks.deck_browser_will_render_content.append(on_deck_browser_will_render_content)
    
    # Handle widget commands
    gui_hooks.webview_did_receive_js_message.append(on_widget_command)
