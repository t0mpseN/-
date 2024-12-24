import tkinter as tk
from customtkinter import *
from PIL import Image
from dictionary_manager import fetch_readings_and_definitions

last_selected_text = ""
gui_open = False

# CustomTkinter Floating Window class
class CTkFloatingWindow(CTkToplevel):
    
    def __init__(self,
                 master=None,
                 alpha=0.99,
                 width=800,
                 height=600,
                 x=None,
                 y=None,
                 corner_radius=25,
                 border_width=1,
                 cancel_button=True,
                 **kwargs):
        
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
            self.button_close = CTkButton(self.frame, corner_radius=10, width=0, height=0, hover=False,
                                          text_color=self.frame._border_color, text="✕", fg_color="transparent",
                                          command=lambda: self.destroy())
            self.button_close.pack(side="top", anchor="ne", padx=7+self.border, pady=7+self.border)
            self.button_close.configure(cursor="arrow")
            
        self.resizable(width=False, height=False)
        self.transient(self.master_window)
         
        self.update_idletasks()
        
        if self.master_window is None:
            self.x = int((self.winfo_screenwidth() - self.width) / 2) if x is None else x
            self.y = int((self.winfo_screenheight() - self.height) / 2) if y is None else y
        else:
            self.x = int(self.master_window.winfo_width() * 0.5 + self.master_window.winfo_x() - 0.5 * self.width + 7) if x is None else x
            self.y = int(self.master_window.winfo_height() * 0.5 + self.master_window.winfo_y() - 0.5 * self.height + 20) if y is None else y
    
        self._iconify()
        self.attributes('-alpha', alpha)
        
    def popup(self, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self._iconify()

    def _iconify(self):
        self.deiconify()
        self.focus()
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))

    def configure(self, **kwargs):
        if "width" in kwargs:
            self.width = kwargs.pop("width")
        if "height" in kwargs:
            self.height = kwargs.pop("height")
        if "alpha" in kwargs:
            self.attributes('-alpha', kwargs.pop("alpha"))
        if "x" in kwargs:
            self.x = kwargs.pop("x")
        if "y" in kwargs:
            self.y = kwargs.pop("y")
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
        # Get the selected text
        selected_text = text_widget.get("sel.first", "sel.last")

        # Prevent multiple updates for the same selection
        if selected_text == last_selected_text:
            return
        last_selected_text = selected_text

        # Fetch the readings and definitions from the dictionary
        readings, definitions, examples = fetch_readings_and_definitions(selected_text, dictionaries)

        # If no readings found, use the selected text as the reading
        if not readings:
            readings = [selected_text]

        # Initialize results lists
        results = []

        # Add readings to results
        results.append("Readings:")
        results.append(", ".join(readings) + "\n")

        if definitions:
            results.append("Meanings:")
            results.extend(definitions)

        if examples:
            results.append("")
            results.append("Examples:")
            results.extend(examples)

        # Display the results
        definition_text_widget.configure(state="normal")
        definition_text_widget.delete("1.0", "end")
        
        # Insert results with appropriate tags for styling
        bold_lines = ["Readings:", "Meanings:", "Examples:"]
        for line in results:
            if line in bold_lines:
                definition_text_widget.insert("insert", line + "\n", "bold")
            else:
                definition_text_widget.insert("insert", line + "\n")
        
        definition_text_widget.configure(state="disabled")
    except tk.TclError:
        pass  # No text selected

def display_text_in_gui(text, dictionaries):
    global text_widget, definition_text_widget, last_selected_text, gui_open
    last_selected_text = ""
    gui_open = True

    # Create the floating window
    root = CTkFloatingWindow(width=800, height=600)
    root.title("PrtScJisho")

    # Load the custom font with different sizes for the textboxes
    custom_font_ocr = CTkFont(family="JetBrains Mono", size=18)  # Increased font size for OCR text
    custom_font_definitions = CTkFont(family="JetBrains Mono", size=14)

    # Create a scrolled text widget to display the OCR result with a larger font size
    text_widget = CTkTextbox(root.frame, wrap="word", width=70, font=custom_font_ocr, fg_color="#1f1f1f", text_color="white", corner_radius=15)
    text_widget.pack(pady=10, padx=20, fill="both", expand=True)

    # Insert the text into the scrolled text widget
    text_widget.insert("1.0", text)
    text_widget.configure(state="normal")

    # Adjust the height of text_widget based on the number of lines in the OCR text
    num_lines = text.count('\n') + 1
    text_widget.configure(height=min(num_lines, 20))

    # Bind the selection event
    text_widget.bind("<<Selection>>", lambda event: display_definitions(event, dictionaries))

    # Create a frame to hold the definitions textbox with rounded corners
    definition_frame = CTkFrame(root.frame, fg_color="#1f1f1f", corner_radius=15, width=800, height=200)
    definition_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Create another scrolled text widget to display the definitions with a smaller font size
    definition_text_widget = tk.Text(definition_frame, wrap="word", height=20, font=("JetBrains Mono", 14), bg="#1f1f1f", fg="white", bd=0, highlightthickness=0)
    definition_text_widget.pack(pady=10, padx=20, fill="both", expand=True)
    definition_text_widget.configure(state="disabled")

    # Create a tag for bold text using tk.Text
    definition_text_widget.tag_configure("bold", font=("JetBrains Mono", 14, "bold"))

    # Run the application
    root.mainloop()
    gui_open = False