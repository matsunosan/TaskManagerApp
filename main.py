import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
import datetime

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.tasks = []
        self.deadlines = []
        self.priorities = []
        self.descriptions = []

        self.tasks_listbox = tk.Listbox(self.root, width=50)
        self.tasks_listbox.pack(pady=10)

        self.task_label = tk.Label(self.root, text="Task:")
        self.task_label.pack()
        self.task_entry = tk.Entry(self.root, width=50)
        self.task_entry.pack()

        self.date_label = tk.Label(self.root, text="Date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = DateEntry(self.root, width=12, background="white", foreground="black", date_pattern="yyyy-mm-dd")
        self.date_entry.pack()

        self.time_label = tk.Label(self.root, text="Time (HH:MM):")
        self.time_label.pack()
        self.time_combobox = ttk.Combobox(self.root, values=self.get_time_values(), state="readonly", width=12)
        self.time_combobox.pack()

        self.priority_label = tk.Label(self.root, text="Priority (1-5):")
        self.priority_label.pack()
        self.priority_entry = tk.Entry(self.root, width=50)
        self.priority_entry.pack()

        self.description_label = tk.Label(self.root, text="Description:")
        self.description_label.pack()
        self.description_entry = tk.Entry(self.root, width=50)
        self.description_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.view_button = tk.Button(self.root, text="View Details", command=self.view_task_details)
        self.view_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.load_tasks()

    def get_time_values(self):
        times = []
        for hour in range(24):
            for minute in range(0, 60, 15):
                time = f"{hour:02d}:{minute:02d}"
                times.append(time)
        return times

    def add_task(self):
        task = self.task_entry.get()
        date = self.date_entry.get()
        time = self.time_combobox.get()
        priority = self.priority_entry.get()
        description = self.description_entry.get()

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

                    self.tasks_listbox.insert(tk.END, task)

                    self.task_entry.delete(0, tk.END)
                    self.date_entry.delete(0, tk.END)
                    self.time_combobox.set("")
                    self.priority_entry.delete(0, tk.END)
                    self.description_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Warning", "Please enter a future date and time.")
            else:
                messagebox.showwarning("Warning", "Please enter a valid priority (1-5).")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    # Остальной код без изменений...



    def view_task_details(self):
        selected_task = self.tasks_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            task, deadline, priority, description = self.get_task_details(index)
            details_window = tk.Toplevel(self.root)
            details_window.title("Task Details")

            task_label = tk.Label(details_window, text=f"Task: {task}")
            task_label.pack()

            deadline_label = tk.Label(details_window, text=f"Deadline: {deadline}")
            deadline_label.pack()

            priority_label = tk.Label(details_window, text=f"Priority: {priority}")
            priority_label.pack()

            description_label = tk.Label(details_window, text=f"Description: {description}")
            description_label.pack()
        else:
            messagebox.showwarning("Warning", "Please select a task to view details.")
    
    def get_task_details(self, index):
        task = self.tasks[index]
        deadline = self.deadlines[index]
        priority = self.priorities[index]
        description = self.descriptions[index]
        return task, deadline, priority, description

    def delete_task(self):
        selected_task = self.tasks_listbox.curselection()
        if selected_task:
            index = selected_task[0]
            del self.tasks[index]
            del self.deadlines[index]
            del self.priorities[index]
            del self.descriptions[index]
            self.tasks_listbox.delete(selected_task)
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                lines = file.read().splitlines()
                for line in lines:
                    task, deadline, priority, description = line.split(" | ")
                    self.tasks.append(task)
                    self.deadlines.append(deadline)
                    self.priorities.append(priority)
                    self.descriptions.append(description)
                    self.tasks_listbox.insert(tk.END, task)
        except FileNotFoundError:
            pass

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for i in range(len(self.tasks)):
                task = self.tasks[i]
                deadline = self.deadlines[i]
                priority = self.priorities[i]
                description = self.descriptions[i]
                file.write(f"{task} | {deadline} | {priority} | {description}\n")

    def on_closing(self):
        self.save_tasks()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
