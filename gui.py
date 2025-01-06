import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import list_generator

# function to open a file dialog and insert the selected file path into the given entry
def open_file_dialog(entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

# function to generate the attendee list
def generate_list():
    input_path = path_entry_input.get()
    output_path = path_entry_output.get()

    # validate input and output paths
    error_message = ""
    if not input_path:
        error_message = "Please select an input file."
    elif not output_path:
        error_message = "Please select an output file."
    elif not input_path.endswith(".csv"):
        error_message = "The input file must be a CSV file."
    elif not output_path.endswith(".csv"):    
        error_message = "The output file must be a CSV file."

    if error_message:
        messagebox.showerror("Error", error_message)
        return

    # no error, generate the list
    list_generator.generate_list(input_path, output_path)

# create the main window
root = tk.Tk()
root.title("Lawdays Attendee List Generator")
title_font = ("Helvetica", 25, "bold")
font = ("Helvetica", 15)

# set window size
#root.geometry("640x300")
#root.resizable(False, False)

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
settings_button = tk.Button(root, text="Settings", font=font)
settings_button.grid(row=6, column=0, pady=10)

# doc Button
documentation_button = tk.Button(root, text="Documentation", font=font, 
                                 command=lambda: webbrowser.open("https://github.com/DemianFlury/Lawdays/blob/main/README.md"))
documentation_button.grid(row=6, column=1, pady=10)

# close Button
close_button = tk.Button(root, text="Close", command=root.quit, font=font)
close_button.grid(row=6, column=2, pady=10)

# run the application
root.mainloop()