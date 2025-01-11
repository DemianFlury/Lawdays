import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import list_generator
import os

# function to open a file dialog and insert the selected file path into the given entry
def open_file_dialog(entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

# function to open the settings window
def open_settings():
    def save_settings():

        if not stands_entry.get():
            messagebox.showerror("Error", "Please enter the stands.")
            return
        if not timeslots_entry.get():
            messagebox.showerror("Error", "Please enter the number of timeslots.")
            return
        if not stand_capacity_entry.get():
            messagebox.showerror("Error", "Please enter the stand capacity.")
            return
        if not num_priorities_entry.get():
            messagebox.showerror("Error", "Please enter the number of priorities.")
            return
        
        settings.stands = stands_entry.get().split(',')
        settings.timeslots = int(timeslots_entry.get())
        settings.stand_capacity = int(stand_capacity_entry.get())
        settings.num_priorities = int(num_priorities_entry.get())
        
        settings_window.destroy()

    # Create new window
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.resizable(False, False)

    # Create labels and entries for each setting
    tk.Label(settings_window, text="Stands (comma separated):", font=font).grid(row=0, column=0, padx=10, pady=5)
    stands_entry = tk.Entry(settings_window, width=50, font=font)
    stands_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(settings_window, text="Timeslots:", font=font).grid(row=1, column=0, padx=10, pady=5)
    timeslots_entry = tk.Entry(settings_window, width=50, font=font)
    timeslots_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(settings_window, text="Stand Capacity:", font=font).grid(row=2, column=0, padx=10, pady=5)
    stand_capacity_entry = tk.Entry(settings_window, width=50, font=font)
    stand_capacity_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(settings_window, text="Number of Priorities:", font=font).grid(row=5, column=0, padx=10, pady=5)
    num_priorities_entry = tk.Entry(settings_window, width=50, font=font)
    num_priorities_entry.grid(row=5, column=1, padx=10, pady=5)

    if(settings.timeslots):
        timeslots_entry.insert(0, settings.timeslots)
    if(settings.stand_capacity):
        stand_capacity_entry.insert(0, settings.stand_capacity)
    if(settings.num_priorities):
        num_priorities_entry.insert(0, settings.num_priorities)
    if(settings.stands):
        stands_entry.insert(0, ",".join(settings.stands))

    # Save button
    tk.Button(settings_window, text="Save", command=save_settings, font=font).grid(row=6, column=0, columnspan=3, pady=10)


# function to generate the attendee list
def generate_list():
    settings.input_path=path_entry_input.get()
    settings.output_path=path_entry_output.get()

    # validate input and output paths
    error_message = ""
    if not settings.input_path:
        error_message = "Please select an input file."
    elif not settings.output_path:
        error_message = "Please select an output file."
    elif not os.path.exists(settings.input_path):
        error_message = "The input file does not exist."
    elif not settings.input_path.endswith(".csv"):
        error_message = "The input file must be a CSV file."
    elif not settings.output_path.endswith(".csv"):    
        error_message = "The output file must be a CSV file."
    

    if error_message:
        messagebox.showerror("Error", error_message)
        return

    # no error, generate the list
    code = list_generator.generate_list(settings)

    if code == 0:
        messagebox.showinfo("Success", "Attendee list generated successfully.")
    elif code == 1:
        messagebox.showerror("Error", "Too many attendees, increase stand capacity or amount of timeslots.")
    elif code == 2:
        messagebox.showerror("Error", "The input file is not formatted correctly. Check documentation for more information.")
    else:
        messagebox.showerror("Error", "An error occurred while generating the attendee list.")

settings = list_generator.Settings([], 0, 0, "", "", 0)

# create the main window
root = tk.Tk()
root.title("Lawdays Attendee List Generator")
title_font = ("Helvetica", 25, "bold")
font = ("Helvetica", 15)
root.resizable(False, False)

# title
title = tk.Label(root, text="Lawdays Attendee List Generator", font=title_font)
title.grid(row=0, column=0, columnspan=3, pady=10)

# input Label
path_label_input = tk.Label(root, text="Input File:", font=font)
path_label_input.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# input Path Entry
path_entry_input = tk.Entry(root, width=50, font=font)
path_entry_input.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# input File Button
file_button_input = tk.Button(root, text="Browse", command=lambda: open_file_dialog(path_entry_input), font=font)
file_button_input.grid(row=2, column=2,  padx=10, pady=5)

# output Label
path_label_output = tk.Label(root, text="Output File:", font=font)
path_label_output.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# output Path Entry
path_entry_output = tk.Entry(root, width=50, font=font)
path_entry_output.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# output File Button
file_button_output = tk.Button(root, text="Browse", command=lambda: open_file_dialog(path_entry_output), font=font)
file_button_output.grid(row=4, column=2, padx=10, pady=5)

# Generate List Button
generate_button = tk.Button(root, text="Generate ->", font=font,
                            command=generate_list)
generate_button.grid(row=5, column=0, columnspan=3, pady=10)

# settings Button
settings_button = tk.Button(root, text="Settings", font=font, command=open_settings)
settings_button.grid(row=6, column=0, pady=10)

# doc Button
documentation_button = tk.Button(root, text="Documentation & Instructions", font=font, 
                                 command=lambda: webbrowser.open("https://github.com/DemianFlury/Lawdays/blob/main/README.md"))
documentation_button.grid(row=6, column=1, pady=10)

# close Button
close_button = tk.Button(root, text="Close", command=root.quit, font=font)
close_button.grid(row=6, column=2, pady=10)

# run the application
root.mainloop()