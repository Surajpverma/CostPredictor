import os
import customtkinter
from PIL import Image
from helpers import get_current_fg_color

def setup_images():
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
    logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(30, 30))
    return logo_image

def create_nav_button(parent, text, command):
    button = customtkinter.CTkButton(parent, corner_radius=6, height=40, border_spacing=10, text=text,
                                     fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=command)
    button.grid(sticky="ew")
    return button

def create_navigation_frame(root, logo_image, toggle_theme, select_frame):
    navigation_frame = customtkinter.CTkFrame(root, corner_radius=0, width=200, fg_color=("#D4D4D4","#323232"))
    navigation_frame.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)

    navigation_frame_label = customtkinter.CTkLabel(navigation_frame, text="   Ladybug", image=logo_image,
                                                    compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
    navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

    home_button = create_nav_button(navigation_frame, "Home", lambda: select_frame("home"))
    sort_button = create_nav_button(navigation_frame, "Sort", lambda: select_frame("sort"))
    split_data_button = create_nav_button(navigation_frame, "Split Data", lambda: select_frame("split_data"))

    home_button.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
    sort_button.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
    split_data_button.grid(row=3, column=0, sticky="ew", padx=20, pady=5)

    # Add a spacer row with high weight to push other elements up
    navigation_frame.grid_rowconfigure(97, weight=1)

    def quit_app():
        root.quit()

    quit_button = customtkinter.CTkButton(navigation_frame, text="Quit", command=quit_app, fg_color="#BA0B13", hover_color="#94070D")
    quit_button.grid(row=99, column=0, padx=20, pady=(10,30), sticky="ew")

    theme_toggle_switch = customtkinter.CTkSwitch(navigation_frame, text="Dark Mode", command=toggle_theme)
    theme_toggle_switch.grid(row=98, column=0, padx=20, pady=10, sticky="sew")

    return home_button, sort_button, split_data_button

def select_frame(frame_name):
    for frame in frames.values():
        frame.grid_forget()
    frames[frame_name].grid(row=0, column=1, sticky="nsew")  # Make sure content frames stretch
    for button_name, button in buttons.items():
        button.configure(fg_color=("gray75", "gray25") if button_name == frame_name else "transparent")

def toggle_theme():
    current_mode = customtkinter.get_appearance_mode()
    new_mode = "Dark" if current_mode == "Light" else "Light"
    customtkinter.set_appearance_mode(new_mode)

    # Update the background color of the frames
    new_bg_color = get_current_fg_color()
    for frame in frames.values():
        frame.configure(fg_color=new_bg_color)
