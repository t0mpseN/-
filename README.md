# **PrtSc辞書**

A print screen clipboard OCR app with a dictionary interface (*no network connection needed*).

![gif1](https://github.com/user-attachments/assets/61908e56-75d5-43da-a003-9d0187cb3436)

![gif2](https://github.com/user-attachments/assets/a278be3d-a355-4767-a445-f35ae9ee524d)

## **Description**

PrtScJisho is a Python application that allows users to capture text from their screen using OCR (Optical Character Recognition) and automatically translate or define the text using pre-loaded dictionaries. The application runs entirely client-side and does not require an internet connection. **You can also edit the Clipboard text and even include new text inside the interface**.

## **Features**

- OCR for screen captures (usable on non-selectable text from images)
- Dictionary integration for translations and examples (in some cases)
- Runs entirely client-side
- Editable text on User Interface

## **Installation**

### **Dependencies**

The application depends on several Python libraries and tools. 
    
#### **Windows**
1. Make sure you have Python and `pip` installed.
2. Clone the repository:
    
    ```
    git clone https://github.com/t0mpseN/PrtScJisho.git
    ```
    

3. Navigate to the repository:
    
    ```
    cd PrtScJisho
    ```
    

4. Run the installation script:
    
    ```
    install_dependencies.bat
    ```

5. **(OPTIONAL)** Add PrtScJisho to startup apps:

    a. Press the `Windows key + R` to open the **Run command**;
   
    b. Type `shell:startup`;
   
    c. Create or paste a shortcut to start.vbs in the folder that opened after `b)` (*C:\Users\[USER]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup*);
   
    d. The next time you restart your computer, the app should automatically start.
   

## Usage

### Running the Application

- On Windows, run `start.vbs` to start the application without showing a terminal window (use `start_terminal.bat` if you want a terminal window).

### Enabling/Disabling

- You can press `F10` or manually right-click the icon on the System Tray and then select **"Toggle Script"**. Please note that when **Toggled ON**, every*ng you print that goes to your clipboard will be considered for the program execution, so if you don't want to have the dictionary interface always opening when you print something, please **Toggle it OFF**.

### Text Selection and User Interface

- You can use the `Win + Shift + S` key combination to target a portion of your screen where the text is at. **Please note that the program doesn't work well with large texts. For this you should manually type or paste the text on the upper textbox inside the user interface**.
- Sometimes the OCR can detect some parts of the text wrong. In this cases you can manually edit the text.
  
# **Credits**

[Manga OCR](https://github.com/kha-white/manga-ocr) by kha-white

[JMdict simplified](https://github.com/scriptin/jmdict-simplified) by scriptin

GUI Font - [JetBrains Mono](https://www.jetbrains.com/)

[GUI Template](https://www.akascape.com/coding/rounded-corner-window-in-python-tkinter)

[Sun Valley GUI Theme](https://github.com/rdbende/Sun-Valley-ttk-theme) by rdbende 

System Tray Icon - <a href="https://www.flaticon.com/free-icons/hiragana" title="hiragana icons">Hiragana icons created by riajulislam - Flaticon</a>
