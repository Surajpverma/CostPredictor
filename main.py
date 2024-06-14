import customtkinter
import os
from PIL import Image
from frames import create_home_frame, create_split_data_frame, get_current_fg_color

def setup_images():
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
    logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(30, 30))
    return logo_image

def create_nav_button(parent, text, command):
    button = customtkinter.CTkButton(parent, corner_radius=0, height=40, border_spacing=10, text=text,
                                     fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=command)
    button.grid(sticky="ew")
    return button

def create_navigation_frame(root, logo_image, change_appearance_mode):
    navigation_frame = customtkinter.CTkFrame(root, corner_radius=0)
    navigation_frame.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    navigation_frame_label = customtkinter.CTkLabel(navigation_frame, text="   Ladybug", image=logo_image,
                                                    compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
    navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

    home_button = create_nav_button(navigation_frame, "Home", lambda: select_frame("home"))
    split_data_button = create_nav_button(navigation_frame, "Split Data", lambda: select_frame("split_data"))

    toggle_switch = customtkinter.CTkSwitch(navigation_frame, text="Dark Mode", command=change_appearance_mode)
    toggle_switch.grid(row=15, column=0, padx=20, pady=20, sticky="s")

    quit_button = customtkinter.CTkButton(navigation_frame, text="Quit", command=root.quit, width=150)
    quit_button.grid(row=16, column=0, padx=20, pady=10, sticky="s")

    return home_button, split_data_button

def select_frame(frame_name):
    global current_frame
    frames = {"home": home_frame, "split_data": split_data_frame}
    if current_frame is not None:
        current_frame.grid_forget()
    current_frame = frames[frame_name]
    current_frame.grid(row=0, column=1, sticky="nsew")

def change_appearance_mode():
    customtkinter.set_appearance_mode("dark" if toggle_switch.get() else "light")
    home_frame.configure(fg_color=get_current_fg_color())
    split_data_frame.configure(fg_color=get_current_fg_color())

if __name__ == "__main__":
    root = customtkinter.CTk()
    root.title("Cost Predictor and Smart Decision App")
    root.geometry("900x650")
    root.resizable(False, False)

    current_frame = None

    logo_image = setup_images()

    home_button, split_data_button = create_navigation_frame(root, logo_image, change_appearance_mode)

    home_frame = create_home_frame(root)
    split_data_frame = create_split_data_frame(root)

    select_frame("home")

    root.mainloop()
