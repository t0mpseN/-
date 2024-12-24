import sys
import time
from PIL import ImageGrab
manga_ocr_path = r'manga-ocr'
sys.path.append(manga_ocr_path)
from manga_ocr import MangaOcr
from ocr_gui import display_text_in_gui
import pystray
from pystray import MenuItem as item

# Global variable to track if the script is active
script_active = True
icon = None

# Instantiate the MangaOcr object
ocr = MangaOcr()

def get_clipboard_image():
    try:
        im = ImageGrab.grabclipboard()
        if isinstance(im, ImageGrab.Image.Image):
            return im
        else:
            print("No image in clipboard.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def ocr_image():
    try:
        # Get the image from the clipboard
        img = get_clipboard_image()
        
        if img:
            # Perform OCR on the image using manga-ocr
            text = ocr(img)
            return text
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def monitor_clipboard(root, dictionaries):
    global script_active
    last_image = None
    current_window = None  # Track the current window

    while True:
        if script_active:
            current_image = get_clipboard_image()
            if current_image and current_image != last_image:
                last_image = current_image
                current_text = ocr_image()
                if current_text:
                    with open("resources/ocr_result.txt", "w", encoding="utf-8") as f:
                        f.write(current_text)
                    
                    # Close the existing window if it exists
                    if current_window is not None:
                        current_window.destroy()
                    
                    # Schedule GUI update on the main thread and update the current window reference
                    root.after(0, lambda: update_window(current_text, dictionaries, current_window))
        time.sleep(0.5)

def update_window(text, dictionaries, current_window):
    # Close the existing window if it exists
    if current_window is not None:
        current_window.destroy()
    
    # Create a new window and update the reference
    current_window = display_text_in_gui(text, dictionaries)

def toggle_script(icon, item):
    global script_active
    script_active = not script_active
    update_menu(icon)

def update_menu(icon):
    icon.menu = pystray.Menu(
        item('Toggle Script', toggle_script, checked=lambda item: script_active),
        item('Quit', quit_app)
    )
    icon.update_menu()

def quit_app(icon, item):
    icon.stop()
    sys.exit()