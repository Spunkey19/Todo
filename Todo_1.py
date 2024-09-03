import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

# Files to store tasks
TASKS_FILE = "tasks.txt"
COMPLETED_FILE = "completed_tasks.txt"

# Initialize the main window
window = tk.Tk()
window.title("To-Do's")
window.geometry("500x600")
window.resizable(False, False)

tasks = []  # List to store task text and completion status
task_vars = []  # List to store IntVars for Checkbuttons

# Load the background image
try:
    bg_image = Image.open("messi.jpg")  # Replace with your image file name
    bg_image = bg_image.resize((500, 600), Image.LANCZOS)  # Resize the image to fit the window
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a label to hold the background image
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Error loading image: {e}")

def update_listbox():
    """Update the listbox with current tasks."""
    for widget in frame.winfo_children():
        widget.destroy()

    # Update existing task_vars and add new ones
    for i, (task, completed) in enumerate(tasks):
        if i >= len(task_vars):
            task_vars.append(tk.IntVar(value=completed))  # Create new IntVar for new tasks
        else:
            task_vars[i].set(completed)  # Update existing IntVar with task completion status
        
        checkbutton = tk.Checkbutton(frame, text=task, variable=task_vars[i], onvalue=1, offvalue=0, bg='white')
        checkbutton.pack(anchor='w')

def add_task():
    """Add a new task to the list."""
    task = entry.get().strip().lower()  # Convert to lowercase and trim extra spaces
    if task:
        if any(t.lower() == task for t, _ in tasks):
            messagebox.showwarning('Warning', 'This task already exists')
        else:
            tasks.append((task, 0))  # Add task with default completion status (0)
            task_vars.append(tk.IntVar())  # Create an IntVar for the new task
            update_listbox()  # Update listbox to include new task
            save_tasks()  # Save tasks to file
            entry.delete(0, tk.END)
    else:
        messagebox.showwarning('Warning', 'Please enter a task')

def delete_task():
    """Delete the selected task."""
    selected_indices = [i for i, var in enumerate(task_vars) if var.get() == 1]
    
    if selected_indices:
        # Write removed tasks to completed file with timestamp
        with open(COMPLETED_FILE, "a") as file:
            for index in sorted(selected_indices, reverse=True):
                if 0 <= index < len(tasks):  # Check if index is within range
                    task_text = tasks[index][0]
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    file.write(f"{task_text} - {timestamp}\n")
                    tasks.pop(index)
                    task_vars.pop(index)
        update_listbox()
        save_tasks()  # Save tasks to file
    else:
        messagebox.showwarning('Warning', 'You must select a task to delete')

def load_tasks():
    """Load tasks from a file."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    task = parts[0]
                    completed = int(parts[1])
                    tasks.append((task, completed))
                    task_vars.append(tk.IntVar(value=completed))  # Initialize with the saved status

def save_tasks():
    """Save tasks to a file."""
    with open(TASKS_FILE, "w") as file:
        for task, completed in tasks:
            file.write(f"{task}|{completed}\n")

# Create frame to contain checkbuttons for tasks
frame = tk.Frame(window, bg='white')
frame.pack(pady=10)

# Load existing tasks from the file and update the listbox
load_tasks()
update_listbox()

# Entry widget for entering tasks
entry = tk.Entry(window, width=30)
entry.pack(pady=10)

# Button to add tasks
add_button = tk.Button(window, text='Add', width=15, command=add_task)
add_button.pack(pady=5)

# Button to delete tasks
remove_button = tk.Button(window, text='Remove', width=15, command=delete_task)
remove_button.pack(pady=5)

# Start the main loop
window.mainloop()
