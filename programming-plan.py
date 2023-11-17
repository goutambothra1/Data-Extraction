import tkinter as tk
from tkinter import filedialog
from main import main
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
project_path=None
def browse_files():
    global project_path 
    project_path = filedialog.askdirectory()
    if project_path:
        # Do something with the selected file path (e.g., display it in a label)
        selected_file_label.config(text="Selected Project path: " + project_path)

def submit():
    # project_path = entry1.get()
    global project_path
    reviewer_sdtmc_sdtme= entry2.get()
    programmer_sdtm_domain  = entry3.get()
    reviewer_sdtm_domain= entry4.get()
    
    # Check if any of the text entry fields is empty
    if not all([reviewer_sdtmc_sdtme, programmer_sdtm_domain, reviewer_sdtm_domain]):
        error_label.config(text="Please fill in all required fields", fg="red")
    elif project_path is None:
        error_label.config(text="Please select a project folder", fg="red")
    else:
        error_label.config(text="")  # Clear any previous error messages

        # Call the main function with the provided values
        message = main(project_path, reviewer_sdtmc_sdtme, programmer_sdtm_domain, reviewer_sdtm_domain)
        #  Create a new window for the message
        global message_window
        message_window = tk.Toplevel(root)
        message_window.geometry('900x200')
        message_window.title("Message")
        message_label = tk.Label(message_window, text=message)
        message_label.pack(padx=40, pady=20)
        message_window.protocol("WM_DELETE_WINDOW", exit_message_window)

   
    # Do something with the input values
def reset():
    # entry1.delete(0, tk.END)
    global project_path
    project_path=None
    selected_file_label.config(text="")
    error_label.config(text="") 
    entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)
    entry4.delete(0, tk.END)

def exit_app():
    root.destroy()
def exit_message_window():
    global message_window
    if message_window:
        message_window.destroy()  
# Create the main window
root = tk.Tk()
root.title("Automated-X")
root.geometry("500x450")  # Set window size

# Create labels and entry fields
label1_frame = tk.Frame(root)
label1_frame.pack(padx=5, pady=5, anchor="w")

# Create label1
label1 = tk.Label(label1_frame, text="Select project folder path", anchor="w")
label1.pack(side=tk.LEFT, padx=5, pady=5)

# Create browse_button
browse_button = tk.Button(label1_frame, text="Browse Files", command=browse_files)
browse_button.pack(side=tk.LEFT, padx=10)

# Create a label for the selected file path (centered)
selected_file_label = tk.Label(root, text="", justify="center")
selected_file_label.pack(pady=1)

# entry1 = tk.Entry(root, width=40)
# entry1.pack(anchor="w", padx=5,pady=5)

label2 = tk.Label(root, text="reviewer for sdtmc and sdtme files", anchor="w")
label2.pack(anchor="w", padx=5,pady=5)
entry2 = tk.Entry(root, width=40)
entry2.pack(anchor="w", padx=5,pady=5)

label3 = tk.Label(root, text="programmer/initreviewer for SDTM Domain and other deliverables", anchor="w")
label3.pack(anchor="w", padx=5,pady=5)
entry3 = tk.Entry(root, width=40)
entry3.pack(anchor="w", padx=5,pady=5)

label4 = tk.Label(root, text="reviewer for SDTM domain and other deliverables", anchor="w")
label4.pack(anchor="w")
entry4 = tk.Entry(root, width=40)
entry4.pack(anchor="w", padx=5,pady=5)

error_label = tk.Label(root, text="", justify="center")
error_label.pack(pady=10)
# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(anchor="w", padx=15,pady=15)

# Create a submit button
submit_button = tk.Button(button_frame, text="Submit", command=submit)
submit_button.pack(side=tk.LEFT, padx=15,pady=15)

# Create a reset button
reset_button = tk.Button(button_frame, text="Reset", command=reset)
reset_button.pack(side=tk.LEFT, padx=15,pady=15)

# Create an exit button
exit_button = tk.Button(button_frame, text="Exit", command=exit_app)
exit_button.pack(side=tk.LEFT, padx=15,pady=15)

# Start the GUI event loop
root.mainloop()