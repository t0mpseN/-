import tkinter as tk
from customtkinter import *
from PIL import Image
from dictionary_manager import fetch_readings_and_definitions
from screeninfo import get_monitors

# Keep track of the current window
current_window = None

# CustomTkinter Floating Window class
class CTkFloatingWindow(CTkToplevel):
    def __init__(self, master=None, alpha=0.99, width=800, height=600, corner_radius=25, border_width=1, cancel_button=True, **kwargs):
        super().__init__(takefocus=1)
        self.focus()
        self.master_window = master
        self.width = width
        self.height = height
        self.attributes('-alpha', 0)
        self.corner = corner_radius
        self.border = border_width
        if sys.platform.startswith("win"):
            self.after(100, lambda: self.overrideredirect(True))
            self.transparent_color = self._apply_appearance_mode(self._fg_color)
            self.attributes("-transparentcolor", self.transparent_color)
        elif sys.platform.startswith("darwin"):
            self.overrideredirect(True)
            self.transparent_color = 'systemTransparent'
            self.attributes("-transparent", True)
        else:
            self.attributes("-type", "splash")
            self.transparent_color = '#000001'
            self.corner = 0
            self.withdraw()
        self.frame = CTkFrame(self, bg_color=self.transparent_color, corner_radius=self.corner, border_width=self.border, **kwargs)
        self.frame.pack(expand=True, fill="both")
        self.frame.bind("<B1-Motion>", self.move_window)
        self.frame.bind("<ButtonPress-1>", self.oldxyset)
        if cancel_button:
            self.button_close = CTkButton(self.frame, corner_radius=10, width=0, height=0, hover=False, text_color=self.frame._border_color, text="✕", fg_color="transparent", command=lambda: self.destroy())
            self.button_close.pack(side="top", anchor="ne", padx=7+self.border, pady=7+self.border)
            self.button_close.configure(cursor="arrow")
        self.resizable(width=False, height=False)
        self.transient(self.master_window)
        self.update_idletasks()
        self.attributes('-alpha', alpha)

    def popup(self):
        self.deiconify()
        self.focus()

    def configure(self, **kwargs):
        if "width" in kwargs:
            self.width = kwargs.pop("width")
        if "height" in kwargs:
            self.height = kwargs.pop("height")
        if "alpha" in kwargs:
            self.attributes('-alpha', kwargs.pop("alpha"))
        self.frame.configure(**kwargs)

    def oldxyset(self, event):
        self.oldx = event.x
        self.oldy = event.y

    def move_window(self, event):
        self.y = event.y_root - self.oldy
        self.x = event.x_root - self.oldx
        self.geometry(f'+{self.x}+{self.y}')

def display_definitions(event, dictionaries):
    global last_selected_text
    try:
        selected_text = text_widget.get("sel.first", "sel.last")
        if selected_text == last_selected_text:
            return
        last_selected_text = selected_text
        readings, definitions, examples = fetch_readings_and_definitions(selected_text, dictionaries)
        if not readings:
            readings = [selected_text]
        results = []
        results.append("Readings:")
        results.append(", ".join(readings) + "\n")
        if definitions:
            results.append("Meanings:")
            results.extend(definitions)
        if examples:
            results.append("")
            results.append("Examples:")
            results.extend(examples)
        definition_text_widget.configure(state="normal")
        definition_text_widget.delete("1.0", "end")
        bold_lines = ["Readings:", "Meanings:", "Examples:"]
        for line in results:
            if line in bold_lines:
                definition_text_widget.insert("insert", line + "\n", "bold")
            else:
                definition_text_widget.insert("insert", line + "\n")
        definition_text_widget.configure(state="disabled")
    except tk.TclError:
        pass

def display_text_in_gui(text, dictionaries):
    global text_widget, definition_text_widget, last_selected_text, current_window
    last_selected_text = ""
    if current_window is not None:
        current_window.destroy()
    
    # Get the screen dimensions of the primary monitor
    monitors = get_monitors()
    primary_monitor = monitors[0]
    screen_width = primary_monitor.width
    screen_height = primary_monitor.height
    x_position = int((screen_width - 800) / 2)
    y_position = int((screen_height - 600) / 2)
    
    current_window = CTkFloatingWindow(width=800, height=600)
    current_window.title("PrtScJisho")
    
    # Set the window to be always on top
    current_window.attributes("-topmost", True)
    
    # Move the window to the center position
    current_window.geometry(f"+{x_position}+{y_position}")
    
    custom_font_ocr = CTkFont(family="JetBrains Mono", size=18)
    custom_font_definitions = CTkFont(family="JetBrains Mono", size=14)
    
    # Adjust the corner_radius to make the corners less rounded
    text_widget = CTkTextbox(current_window.frame, wrap="word", width=70, font=custom_font_ocr, fg_color="#1f1f1f", text_color="white", corner_radius=5)
    text_widget.pack(pady=10, padx=20, fill="both", expand=True)
    text_widget.insert("1.0", text)
    text_widget.configure(state="normal")
    num_lines = text.count('\n') + 1
    text_widget.configure(height=min(num_lines, 20))
    text_widget.bind("<<Selection>>", lambda event: display_definitions(event, dictionaries))
    
    # Adjust the corner_radius to make the corners less rounded
    definition_frame = CTkFrame(current_window.frame, fg_color="#1f1f1f", corner_radius=5, width=800, height=200)
    definition_frame.pack(pady=10, padx=20, fill="both", expand=True)
    definition_text_widget = tk.Text(definition_frame, wrap="word", height=20, font=("JetBrains Mono", 14), bg="#1f1f1f", fg="white", bd=0, highlightthickness=0)
    definition_text_widget.pack(pady=10, padx=20, fill="both", expand=True)
    definition_text_widget.configure(state="disabled")
    definition_text_widget.tag_configure("bold", font=("JetBrains Mono", 14, "bold"))
    current_window.mainloop()
    return current_window  # Return the window object