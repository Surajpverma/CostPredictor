import tkinter as tk
import customtkinter
from images import setup_images
from navigation import create_navigation_frame
from frames import create_home_frame, create_frame, create_split_data_frame, select_frame, toggle_theme

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cost Predictor and Smart Decision App")
    root.geometry("900x650")
    root.resizable(False, False)

    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    logo_image = setup_images()

    frames = {
        "home": create_home_frame(root),
        "sort": create_frame(root, "Sort"),
        "split_data": create_split_data_frame(root),
    }

    home_button, sort_button, split_data_button, theme_toggle_switch = create_navigation_frame(
        root, logo_image, lambda: toggle_theme(frames, theme_toggle_switch), lambda name: select_frame(name, frames, buttons)
    )

    buttons = {
        "home": home_button,
        "sort": sort_button,
        "split_data": split_data_button,
    }

    select_frame("home", frames, buttons)

    # Set initial state of theme toggle switch based on current theme
    current_mode = customtkinter.get_appearance_mode()
    theme_toggle_switch.select() if current_mode == "Dark" else theme_toggle_switch.deselect()

    root.mainloop()