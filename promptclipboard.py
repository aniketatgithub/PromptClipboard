import tkinter as tk
import pyperclip
import pyautogui
import time
import threading
import sys  

# Predefined texts
texts = {
    "Skills": "Using the extracted keywords from the job description, refine my 'Skills' section to:\n1. Remove irrelevant technologies.\n2. Add all relevant ones mentioned in the job description, along with related tools and frameworks.\n3. Keep the section concise, impactful, and professional.\nReturn the updated 'Skills' section in LaTeX format.",
    "Experience": "Refine the 'Experience' section for my role at all the companies. Ensure:\n1. Four points for this role, 2 line each. each with 40+ words.\n2. Include relevant keywords and quantifiable results from the job description.\n3. Create believable, impactful achievements tied to the company’s domain (e.g., Viasat could include scalable systems or secure communications).\n4. Avoid repeating action verbs, make sure to change the designation according to the role that i am applying to but keep internship as intern and full time as full time but change the role accordingly.",
    "Exp 2": "Each point should be 30+ words, believable, has all the ATS keywords you extracted, according to industry change the points and do not leave any open-ended question by providing enough context and believable impacts. Do not overuse the same action verbs.",
    "Projects": "Create two new projects for my 'Projects' section based on the job description. Follow these guidelines:\n1. Each project should align with technologies and keywords in the job description.\n2. Use a timeline that fits within my master’s program.\n3. Each project should have 3 points, 2 LINES EACH 30+ words each, with quantifiable results.\n4. Avoid repeating action verbs which you have already used in this as well as experience section\nReturn the updated 'Projects' section in LaTeX format."
}

# Global variables
stop_watcher = False
pasting = False
window = None  


def copy_and_paste(key):
    """Copy text to clipboard and paste it."""
    global stop_watcher, pasting
    pyperclip.copy(texts[key])  
    status_label.config(text="✅ Copied!", fg="green")
    stop_watcher = False
    pasting = True

    thread = threading.Thread(target=watch_for_focus_and_paste, args=(key,))
    thread.daemon = True  
    thread.start()


def watch_for_focus_and_paste(key):
    """Wait and paste once focused."""
    global stop_watcher, pasting
    time.sleep(1)  
    while pasting and not stop_watcher:
        pyautogui.hotkey('ctrl', 'v')  
        pasting = False
        stop_watcher = True
        if key == "Projects":  
            exit_application()


def open_edit_menu():
    """Open a dropdown menu to edit prompts."""
    menu = tk.Toplevel(window)
    menu.title("Edit Prompts")
    menu.geometry("200x180")
    menu.configure(bg="#222222")
    menu.attributes("-topmost", True)  

    for key in texts:
        btn = tk.Button(
            menu,
            text=f"Edit {key}",
            command=lambda key=key: edit_prompt(key, menu),
            font=("Arial", 9),
            bg="#333333",
            fg="white",
            relief="flat",
            activebackground="#555555",
            activeforeground="white",
            bd=0
        )
        btn.pack(fill=tk.X, pady=2, padx=8)

    close_menu_btn = tk.Button(
        menu,
        text="Close",
        command=menu.destroy,
        font=("Arial", 9, "bold"),
        bg="#FF5555",
        fg="white",
        relief="flat"
    )
    close_menu_btn.pack(pady=5)


def edit_prompt(key, menu):
    """Open a text editor to modify a prompt."""
    menu.destroy()  

    edit_window = tk.Toplevel(window)
    edit_window.title(f"Edit {key}")
    edit_window.geometry("350x200")
    edit_window.configure(bg="#222222")
    edit_window.attributes("-topmost", True)

    text_editor = tk.Text(edit_window, wrap="word", font=("Arial", 9), bg="#333333", fg="white", height=8)
    text_editor.pack(expand=True, fill="both", padx=8, pady=8)
    text_editor.insert("1.0", texts[key])  

    def save_changes():
        texts[key] = text_editor.get("1.0", tk.END).strip()  # **Fixed: Updates texts dictionary**
        edit_window.destroy()
        status_label.config(text=f"✅ {key} Updated!", fg="yellow")  # Feedback message

    save_button = tk.Button(
        edit_window,
        text="Save",
        command=save_changes,
        font=("Arial", 9, "bold"),
        bg="#4CAF50",
        fg="white",
        relief="flat"
    )
    save_button.pack(pady=5)


def exit_application():
    """Exit the entire application."""
    global stop_watcher
    stop_watcher = True
    if window:
        window.destroy()
    sys.exit()


def create_window():
    """Create a small floating UI with a hamburger menu for editing."""
    global status_label, window
    window = tk.Tk()
    window.title("Quick Paste")
    window.overrideredirect(True)  
    window.attributes("-topmost", True)  
    window.attributes("-alpha", 0.85)  
    window.configure(bg="#222222")  

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    mouse_x, mouse_y = pyautogui.position()
    window_width, window_height = 220, 160  
    safe_x = max(0, min(mouse_x, screen_width - window_width))
    safe_y = max(0, min(mouse_y, screen_height - window_height))
    window.geometry(f"{window_width}x{window_height}+{safe_x}+{safe_y}")

    # Topbar Frame
    topbar = tk.Frame(window, bg="#222222")
    topbar.pack(fill=tk.X)

    # Close Button (Smaller)
    close_button = tk.Button(
        topbar,
        text="✖",
        command=exit_application,
        font=("Arial", 8, "bold"),
        bg="#FF5555",
        fg="white",
        relief="flat",
        width=2
    )
    close_button.pack(side=tk.RIGHT, padx=2, pady=2)

    # Hamburger Menu Button (Smaller)
    menu_button = tk.Button(
        topbar,
        text="☰",  
        command=open_edit_menu,
        font=("Arial", 8, "bold"),
        bg="#444444",
        fg="white",
        relief="flat",
        width=2
    )
    menu_button.pack(side=tk.LEFT, padx=2, pady=2)

    # Button Style
    button_style = {
        "font": ("Arial", 9),
        "bg": "#333333",
        "fg": "white",
        "relief": "flat",
        "activebackground": "#555555",
        "activeforeground": "white",
        "bd": 0
    }

    for key in texts:
        btn = tk.Button(
            window,
            text=key,
            command=lambda key=key: copy_and_paste(key),  # Now fetches updated text
            **button_style
        )
        btn.pack(fill=tk.X, pady=2, padx=8)

    status_label = tk.Label(window, text="Select a prompt to copy.", font=("Arial", 9), bg="#222222", fg="white")
    status_label.pack(pady=5)

    window.mainloop()


if __name__ == "__main__":
    create_window()
