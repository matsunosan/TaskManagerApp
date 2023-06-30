import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
import time


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("400x400")

        self.tasks = []
        self.deadlines = []
        self.priorities = []
        self.descriptions = []

        self.tasks_listbox = tk.Listbox(self.root, width=50)
        self.tasks_listbox.pack(pady=10)

        add_button = tk.Button(self.root, text="Add Task", command=self.add_task_window)
        add_button.pack(pady=5)

        view_button = tk.Button(self.root, text="View Details", command=self.view_task_details)
        view_button.pack(pady=5)

        edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        edit_button.pack(pady=5)

        delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        delete_button.pack(pady=5)

        self.load_tasks()
        self.update_task_list()
        self.check_deadlines()

    def add_task_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Task")

        task_label = tk.Label(add_window, text="Task:")
        task_label.pack()
        task_entry = tk.Entry(add_window, width=50)
        task_entry.pack()

        date_label = tk.Label(add_window, text="Date (YYYY-MM-DD):")
        date_label.pack()
        date_entry = DateEntry(add_window, width=12, background="white", foreground="black", date_pattern="yyyy-mm-dd")
        date_entry.pack()

        time_label = tk.Label(add_window, text="Time (HH:MM):")
        time_label.pack()
        time_combobox = ttk.Combobox(add_window, values=self.get_time_values(), state="readonly", width=12)
        time_combobox.pack()

        priority_label = tk.Label(add_window, text="Priority (1-5):")
        priority_label.pack()
        priority_entry = tk.Entry(add_window, width=50)
        priority_entry.pack()

        description_label = tk.Label(add_window, text="Description:")
        description_label.pack()
        description_entry = tk.Entry(add_window, width=50)
        description_entry.pack()

        save_button = tk.Button(add_window, text="Save", command=lambda: self.save_task(task_entry.get(),
                                                                                       date_entry.get(),
                                                                                       time_combobox.get(),
                                                                                       priority_entry.get(),
                                                                                       description_entry.get(),
                                                                                       add_window))
        save_button.pack(pady=5)

    def save_task(self, task, date, time, priority, description, add_window):
        if task and date and time and priority and description:
            if priority.isdigit() and 1 <= int(priority) <= 5:
                deadline = f"{date} {time}"
                current_datetime = datetime.datetime.now()
                input_datetime = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")

                if input_datetime >= current_datetime:
                    self.tasks.append(task)
                    self.deadlines.append(deadline)
                    self.priorities.append(priority)
                    self.descriptions.append(description)

                    self.update_task_list()
                    self.save_tasks()
                    add_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Please enter a future date and time.")
            else:
                messagebox.showwarning("Warning", "Please enter a valid priority (1-5).")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    def view_task_details(self):
        selected_task = self.tasks_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            task, deadline, priority, description = self.get_task_details(index)
            messagebox.showinfo("Task Details", f"Task: {task}\nDeadline: {deadline}\nPriority: {priority}\nDescription: {description}")
        else:
            messagebox.showwarning("Warning", "Please select a task.")

    def edit_task(self):
        selected_task = self.tasks_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            task, deadline, priority, description = self.get_task_details(index)

            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")

            task_label = tk.Label(edit_window, text="Task:")
            task_label.pack()
            task_entry = tk.Entry(edit_window, width=50)
            task_entry.insert(0, task)
            task_entry.pack()

            date_label = tk.Label(edit_window, text="Date (YYYY-MM-DD):")
            date_label.pack()
            date_entry = DateEntry(edit_window, width=12, background="white", foreground="black", date_pattern="yyyy-mm-dd")
            date_entry.set_date(datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M").date())
            date_entry.pack()

            time_label = tk.Label(edit_window, text="Time (HH:MM):")
            time_label.pack()
            time_combobox = ttk.Combobox(edit_window, values=self.get_time_values(), state="readonly", width=12)
            time_combobox.set(datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M").strftime("%H:%M"))
            time_combobox.pack()

            priority_label = tk.Label(edit_window, text="Priority (1-5):")
            priority_label.pack()
            priority_entry = tk.Entry(edit_window, width=50)
            priority_entry.insert(0, priority)
            priority_entry.pack()

            description_label = tk.Label(edit_window, text="Description:")
            description_label.pack()
            description_entry = tk.Entry(edit_window, width=50)
            description_entry.insert(0, description)
            description_entry.pack()

            save_button = tk.Button(edit_window, text="Save", command=lambda: self.update_task(task_entry.get(),
                                                                                               date_entry.get(),
                                                                                               time_combobox.get(),
                                                                                               priority_entry.get(),
                                                                                               description_entry.get(),
                                                                                               index,
                                                                                               edit_window))
            save_button.pack(pady=5)
        else:
            messagebox.showwarning("Warning", "Please select a task to edit.")

    def update_task(self, task, date, time, priority, description, index, edit_window):
        if task and date and time and priority and description:
            if priority.isdigit() and 1 <= int(priority) <= 5:
                deadline = f"{date} {time}"
                current_datetime = datetime.datetime.now()
                input_datetime = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")

                if input_datetime >= current_datetime:
                    self.tasks[index] = task
                    self.deadlines[index] = deadline
                    self.priorities[index] = priority
                    self.descriptions[index] = description

                    self.update_task_list()
                    self.save_tasks()
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Please enter a future date and time.")
            else:
                messagebox.showwarning("Warning", "Please enter a valid priority (1-5).")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    def delete_task(self):
        selected_task = self.tasks_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            task, _, _, _ = self.get_task_details(index)
            confirmed = messagebox.askyesno("Delete Task", f"Are you sure you want to delete the task: {task}?")
            if confirmed:
                del self.tasks[index]
                del self.deadlines[index]
                del self.priorities[index]
                del self.descriptions[index]
                self.update_task_list()
                self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def update_task_list(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, task)

    def get_task_details(self, index):
        task = self.tasks[index]
        deadline = self.deadlines[index]
        priority = self.priorities[index]
        description = self.descriptions[index]
        return task, deadline, priority, description

    def get_time_values(self):
        times = []
        for hour in range(0, 24):
            for minute in range(0, 60, 15):
                time = f"{hour:02d}:{minute:02d}"
                times.append(time)
        return times

    def check_deadlines(self):
        current_datetime = datetime.datetime.now()
        for i in range(len(self.deadlines)):
            deadline = datetime.datetime.strptime(self.deadlines[i], "%Y-%m-%d %H:%M")
            if current_datetime >= deadline:
                task = self.tasks[i]
                messagebox.showinfo("Task Reminder", f"The following task is past its deadline:\n\nTask: {task}")
                break

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for i in range(len(self.tasks)):
                file.write(f"{self.tasks[i]},{self.deadlines[i]},{self.priorities[i]},{self.descriptions[i]}\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    task, deadline, priority, description = line.strip().split(",")
                    self.tasks.append(task)
                    self.deadlines.append(deadline)
                    self.priorities.append(priority)
                    self.descriptions.append(description)
        except FileNotFoundError:
            pass


root = tk.Tk()
app = TaskManagerApp(root)
root.mainloop()
