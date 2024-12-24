import sys
from PIL import Image
import pystray
from pystray import MenuItem as item
from clipboard_monitor import script_active, toggle_script, update_menu, quit_app

def create_tray_icon():
    global icon
    icon_image = Image.open("resources/icon.png")  # Path to your tray icon image
    menu = pystray.Menu(
        item('Toggle Script (F10)', toggle_script, checked=lambda item: script_active),
        item('Quit', quit_app)
    )
    icon = pystray.Icon("PrtScJisho", icon_image, "PrtScJisho", menu)
    icon.run()