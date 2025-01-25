import tkinter as tk
import pyperclip
import pyautogui
import time
import threading
import sys  # For exiting the application

# Predefined texts
texts = {
    "Skills": "Using the extracted keywords from the job description, refine my 'Skills' section to:\n1. Remove irrelevant technologies.\n2. Add all relevant ones mentioned in the job description, along with related tools and frameworks.\n3. Keep the section concise, impactful, and professional.\nReturn the updated 'Skills' section in LaTeX format.",
    "Experience": "Refine the 'Experience' section for my role at all the companies. Ensure:\n1. Four points for this role, 2 line each. each with 40+ words.\n2. Include relevant keywords and quantifiable results from the job description.\n3. Create believable, impactful achievements tied to the company’s domain (e.g., Viasat could include scalable systems or secure communications).\n4. Avoid repeating action verbs",
    "Exp 2": "Each point should be 30+ words, believable, has all the ATS keywords you extracted, according to industry change the points and do not leave any open-ended question by providing enough context and believable impacts. Do not overuse the same action verbs.",
    "Projects": "Create two new projects for my 'Projects' section based on the job description. Follow these guidelines:\n1. Each project should align with technologies and keywords in the job description.\n2. Use a timeline that fits within my master’s program.\n3. Each project should have 3 points, 2 LINES EACH 30+ words each, with quantifiable results.\n4. Avoid repeating action verbs which you have already used in this as well as experience section\nReturn the updated 'Projects' section in LaTeX format."
}

# Flags for controlling paste behavior
stop_watcher = False
pasting = False
window = None  # Declare globally for use in threads


def copy_and_paste(text, key):
    """Copy the text to the clipboard and watch for paste trigger."""
    global stop_watcher, pasting, window
    pyperclip.copy(text)
    status_label.config(text="✅", fg="green")
    stop_watcher = False
    pasting = True

    # Start a new thread to watch for focus and paste
    thread = threading.Thread(target=watch_for_focus_and_paste, args=(key,))
    thread.daemon = True  # Mark thread as daemon
    thread.start()


def watch_for_focus_and_paste(key):
    """Wait for user to focus on the desired window and perform a single paste."""
    global stop_watcher, pasting, window
    time.sleep(1)  # Allow time for focus switching
    while pasting and not stop_watcher:
        pyautogui.hotkey('ctrl', 'v')  # Simulate CTRL+V to paste
        pasting = False
        stop_watcher = True
        if key == "Projects":  # Exit application after pasting "Projects"
            exit_application()


def close_window():
    """Close the window only (not the application)."""
    global window
    if window:
        window.destroy()


def exit_application():
    """Exit the entire application."""
    global stop_watcher, window
    stop_watcher = True
    if window:
        window.destroy()
    sys.exit()  # Exit the entire application


def create_window():
    """Create a small, transparent, dark-mode GUI near the mouse cursor."""
    global status_label, window
    window = tk.Tk()
    window.title("Quick Paste")
    window.overrideredirect(True)  # No title bar
    window.attributes("-topmost", True)  # Always on top
    window.attributes("-alpha", 0.85)  # Semi-transparent window
    window.configure(bg="#222222")  # Dark mode background

    # Calculate safe position to ensure the window doesn't go out of screen bounds
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    mouse_x, mouse_y = pyautogui.position()
    window_width, window_height = 250, 200  # Adjusted size to fit all buttons
    safe_x = max(0, min(mouse_x, screen_width - window_width))
    safe_y = max(0, min(mouse_y, screen_height - window_height))
    window.geometry(f"{window_width}x{window_height}+{safe_x}+{safe_y}")

    # Add a close button on top
    close_button = tk.Button(
        window,
        text="X",  # Close button text
        command=exit_application,  # Close the application
        font=("Arial", 10, "bold"),
        bg="#FF5555",  # Red background for close button
        fg="white",  # White text
        relief="flat",
        activebackground="#FF7777",
        activeforeground="white",
        bd=0
    )
    close_button.pack(side=tk.TOP, anchor="ne", padx=5, pady=5)  # Pack it to the top-right corner

    # Button style for predefined texts
    button_style = {
        "font": ("Arial", 12),
        "bg": "#333333",
        "fg": "white",
        "relief": "flat",
        "activebackground": "#555555",
        "activeforeground": "white",
        "bd": 0
    }

    # Add buttons for predefined texts
    for key, value in texts.items():
        btn = tk.Button(
            window,
            text=key,
            command=lambda value=value, key=key: copy_and_paste(value, key),
            **button_style
        )
        btn.pack(fill=tk.X, pady=5, padx=10)

    # Status label for confirmation
    status_label = tk.Label(window, text="Select a prompt to copy.", font=("Arial", 10), bg="#222222", fg="white")
    status_label.pack(pady=10)

    window.mainloop()


if __name__ == "__main__":
    create_window()
