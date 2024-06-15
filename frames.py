import customtkinter
import pandas as pd
from tkinter import filedialog, messagebox
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os

from helpers import get_current_fg_color


def create_home_frame(root):
    home_frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
    home_frame.grid_columnconfigure(0, weight=1)
    home_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

    welcome_label = customtkinter.CTkLabel(home_frame, text="Welcome!", font=customtkinter.CTkFont(size=72),
                                           text_color=("black", "white"))
    welcome_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

    home_frame_label = customtkinter.CTkLabel(home_frame,
                                              text="This is a sample GUI created using customTkinter just for demonstration purposes.",
                                              text_color=("black", "white"))
    home_frame_label.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    developed_by_label = customtkinter.CTkLabel(home_frame, text="Developed by Ladybug",
                                                font=customtkinter.CTkFont(size=15), text_color=("black", "white"))
    developed_by_label.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    return home_frame


def create_frame(root, name):
    frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
    frame.grid_columnconfigure(0, weight=1)
    label = customtkinter.CTkLabel(frame, text=name, text_color=("black", "white"))
    label.grid(row=0, column=0, padx=20, pady=10)
    return frame


def sort_and_clean_excel(file_path, categories, sorted_output_path, cleaned_output_path):
    # Load the Excel file
    excel_data = pd.ExcelFile(file_path)

    # Load the data from the first sheet
    data = pd.read_excel(file_path, sheet_name=excel_data.sheet_names[0])

    # Create a dictionary to hold the data for each category
    category_data = {category: data[data['Category'].str.contains(category, case=False, na=False)] for category in
                     categories}

    # Create a new Excel writer object
    with pd.ExcelWriter(sorted_output_path, engine='xlsxwriter') as writer:
        # Write each category data to a separate sheet
        for category, df in category_data.items():
            df.to_excel(writer, sheet_name=category, index=False)

    # Load the sorted data workbook
    sorted_excel_data = pd.ExcelFile(sorted_output_path)

    # Process each sheet to remove columns with all null values
    cleaned_data = {}
    for sheet_name in sorted_excel_data.sheet_names:
        df = pd.read_excel(sorted_output_path, sheet_name=sheet_name)
        cleaned_df = df.dropna(axis=1, how='all')
        cleaned_data[sheet_name] = cleaned_df

    # Create a new Excel writer object for the cleaned data
    with pd.ExcelWriter(cleaned_output_path, engine='xlsxwriter') as writer:
        # Write each cleaned category data to a separate sheet
        for sheet_name, df in cleaned_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Sorted data has been saved to {sorted_output_path}")
    print(f"Cleaned data has been saved to {cleaned_output_path}")


def create_split_data_frame(root):
    split_data_frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
    split_data_frame.grid_columnconfigure(0, weight=1)
    split_data_frame.grid_rowconfigure(6, weight=1)  # Ensure the last row stretches to push buttons to the bottom

    input_file_var = customtkinter.StringVar()
    output_folder_var = customtkinter.StringVar()

    def select_input_file():
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            input_file_var.set(file_path)
            input_file_label.configure(text=f"Selected file: {os.path.basename(file_path)}")

    def select_output_path():
        folder_path = filedialog.askdirectory()
        if folder_path:
            output_folder_var.set(folder_path)
            output_folder_label.configure(text=f"Selected folder: {os.path.basename(folder_path)}")

    def sort_and_clean():
        input_file = input_file_var.get()
        output_folder = output_folder_var.get()

        if not input_file or not output_folder:
            messagebox.showerror("Error", "Please select both input file and output folder")
            return

        try:
            sorted_output_path = os.path.join(output_folder, "Sorted_Data.xlsx")
            cleaned_output_path = os.path.join(output_folder, "Cleaned_Sorted_Data.xlsx")

            # Define the categories to filter
            categories = ['Doors', 'Walls', 'Ceiling', 'Structural Columns', 'Structural Framing', 'Floor', 'Stairs']

            # Call the sort_and_clean_excel function
            sort_and_clean_excel(input_file, categories, sorted_output_path, cleaned_output_path)

            messagebox.showinfo("Success",
                                f"Sorted data has been saved to {sorted_output_path}\nCleaned data has been saved to {cleaned_output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Input file selection
    customtkinter.CTkLabel(split_data_frame, text="Select input Excel file:").grid(row=0, column=0, padx=20,
                                                                                   pady=(20, 5), sticky="ew")
    input_file_button = customtkinter.CTkButton(split_data_frame, text="Browse...", command=select_input_file,
                                                width=100)
    input_file_button.grid(row=1, column=0, padx=20, pady=5, sticky="w")
    input_file_label = customtkinter.CTkLabel(split_data_frame, text="No file selected",
                                              text_color=("gray50", "gray50"), wraplength=400)
    input_file_label.grid(row=1, column=1, padx=20, pady=5, sticky="w")

    # Output folder selection
    customtkinter.CTkLabel(split_data_frame, text="Select output folder:").grid(row=2, column=0, padx=20, pady=(20, 5),
                                                                                sticky="ew")
    output_folder_button = customtkinter.CTkButton(split_data_frame, text="Browse...", command=select_output_path,
                                                   width=100)
    output_folder_button.grid(row=3, column=0, padx=20, pady=5, sticky="w")
    output_folder_label = customtkinter.CTkLabel(split_data_frame, text="No folder selected",
                                                 text_color=("gray50", "gray50"), wraplength=400)
    output_folder_label.grid(row=3, column=1, padx=20, pady=5, sticky="w")

    # Generate button
    generate_button = customtkinter.CTkButton(split_data_frame, text="Sort and Clean", command=sort_and_clean,
                                              width=150)
    generate_button.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="sew")

    return split_data_frame


def select_frame(frame_name, frames, buttons):
    for frame in frames.values():
        frame.grid_forget()
    frames[frame_name].grid(row=0, column=1, sticky="nsew")
    for button_name, button in buttons.items():
        button.configure(fg_color=("gray75", "gray25") if button_name == frame_name else "transparent")


def toggle_theme(frames, theme_toggle_switch):
    current_mode = customtkinter.get_appearance_mode()
    new_mode = "Dark" if current_mode == "Light" else "Light"
    customtkinter.set_appearance_mode(new_mode)

    # Update the background color of the frames
    new_bg_color = get_current_fg_color()
    for frame in frames.values():
        frame.configure(fg_color=new_bg_color)

    # Update the theme toggle switch state
    theme_toggle_switch.select() if new_mode == "Dark" else theme_toggle_switch.deselect()
