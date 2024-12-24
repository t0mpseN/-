import sys
import os
import threading
import tkinter as tk
from pynput import keyboard
from ocr_gui import display_text_in_gui
from tray_icon import create_tray_icon
from clipboard_monitor import monitor_clipboard, toggle_script, script_active
from dictionary_manager import load_dictionaries

def main():
    global dictionaries, root, listener
    dictionary_files = ['resources/jmdict-examples.json']  # List all your dictionary files here

    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Load the dictionaries
    dictionaries = load_dictionaries(dictionary_files)
    if not dictionaries:
        print("Failed to load dictionaries.")
        return

    # Start a thread to monitor the clipboard, passing dictionaries as an argument
    clipboard_thread = threading.Thread(target=monitor_clipboard, args=(root, dictionaries))
    clipboard_thread.daemon = True
    clipboard_thread.start()

    # Run create_tray_icon in a separate thread
    tray_thread = threading.Thread(target=create_tray_icon)
    tray_thread.daemon = True
    tray_thread.start()

    # Close the hidden root window
    root.destroy()

    # Start the Tkinter main loop
    root.mainloop()

def on_press(key):
    try:
        if key == keyboard.Key.f10:
            toggle_script(None, None)
    except AttributeError:
        pass

if __name__ == "__main__":
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()

    # Start the pynput listener for global key events
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    main()