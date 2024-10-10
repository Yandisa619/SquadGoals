import tkinter as tk
from tkinter import Listbox, Scrollbar, messagebox, simpledialog, ttk
import secrets
import string
import tkinter

class Event:
    def __init__(self, name, date, location, description, password=None):
        self.name = name
        self.date = date
        self.location = location
        self.description = description
        self.password = password or self.generate_password()

    def generate_password(self, length=12):
        alphabet = string.ascii_letters
        digits = string.digits
        symbols = string.punctuation
        all_characters = alphabet + digits + symbols

        password = [
            secrets.choice(alphabet),
            secrets.choice(digits),
            secrets.choice(symbols)
        ]
        password += [secrets.choice(all_characters) for _ in range(length - 3)]
        secrets.SystemRandom().shuffle(password)

        return ''.join(password)

    @staticmethod
    def save_event(event):
        with open("Event.txt", "a") as file:
            file.write(f'{event.name}, {event.date}, {event.location}, {event.description}, {event.password}\n')

    @staticmethod
    def load_events():
        events = []
        try:
            with open("Event.txt", "r") as file:
                for line in file:
                    name, date, location, description, password = line.strip().split(", ")
                    events.append(Event(name, date, location, description, password))
        except FileNotFoundError:
            pass
        return events

    @staticmethod
    def delete_event(name):
        events = Event.load_events()
        events = [event for event in events if event.name != name]

        with open("Event.txt", "w") as file:
            for event in events:
                file.write(f'{event.name}, {event.date}, {event.location}, {event.description}, {event.password}\n')


class EventApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Manager")
        self.root.geometry("600x400")
        self.root.config(bg="#ffffff")

        self.form_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        self.form_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create input fields
        self.label_title = tk.Label(self.form_frame, text="Create Event", font=("Arial", 18), bg="#ffffff")
        self.label_title.pack(pady=(0, 20))

        self.label_event_name = tk.Label(self.form_frame, text="Event Name:", bg="#ffffff")
        self.label_event_name.pack(anchor='w')
        self.entry_event_name = tk.Entry(self.form_frame, font=("Arial", 12), width=30)
        self.entry_event_name.pack(pady=(0, 10))

        self.label_event_date = tk.Label(self.form_frame, text="Date", bg="#ffffff")
        self.label_event_date.pack(anchor='w')
        self.entry_event_date = tk.Entry(self.form_frame, font=("Arial", 12), width=30)
        self.entry_event_date.pack(pady=(0, 10))
 

        # self.date_combobox = ttk.Combobox(self.form_frame, font=("Arial", 12), width=28)
        # self.date_combobox['values'] = ['2024/10/09', '2024/10/10', '2024/10/11']  # Example values
        # self.date_combobox.set('Select Date')  # Set default text
        # self.date_combobox.pack(pady=(0, 10))

#  DateEntry(parent, style='success.TCalendar')
        self.label_event_location = tk.Label(self.form_frame, text="Event Location:", bg="#ffffff")
        self.label_event_location.pack(anchor='w')
        self.entry_event_location = tk.Entry(self.form_frame, font=("Arial", 12), width=30)
        self.entry_event_location.pack(pady=(0, 10))

        self.label_event_description = tk.Label(self.form_frame, text="Event Description:", bg="#ffffff")
        self.label_event_description.pack(anchor='w')
        self.entry_event_description = tk.Entry(self.form_frame, font=("Arial", 12), width=30)
        self.entry_event_description.pack(pady=(0, 20))

        # Save button below input fields
        self.save_button = tk.Button(self.form_frame, text="Save Event", command=self.save_event, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.save_button.pack(pady=(10, 20))

        # Create Listbox with a scrollbar for events
        self.listbox_frame = tk.Frame(self.root, bg="#ffffff")
        self.listbox_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=(10,20))

        self.event_listbox = Listbox(self.listbox_frame, font=("Arial", 12), bg="#ffffff", selectbackground="#B2EBF2")
        self.event_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(10,20))

        self.scrollbar = Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.event_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.event_listbox.yview)

        # Buttons for Edit and Delete below the Listbox
        self.edit_button = tk.Button(self.listbox_frame, text="Edit Event", command=self.edit_event, bg="#FFC107", fg="black", font=("Arial", 12), padx=10, pady=5)
        self.edit_button.pack(side=tk.BOTTOM, pady=(5, 0))

        self.delete_button = tk.Button(self.listbox_frame, text="Delete Event", command=self.delete_event, bg="#F44336", fg="white", font=("Arial", 12), padx=10, pady=5)
        self.delete_button.pack(side=tk.BOTTOM, pady=(5, 20))

        # Load existing events
        self.load_events()

    def save_event(self):
        name = self.entry_event_name.get()
        date = self.entry_event_date.get()
        location = self.entry_event_location.get()
        description = self.entry_event_description.get()

        if name and date and location and description:
            event = Event(name, date, location, description)
            Event.save_event(event)
            self.clear_entries()
            self.load_events()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def load_events(self):
        self.event_listbox.delete(0, tk.END)
        events = Event.load_events()
        for event in events:
            self.event_listbox.insert(tk.END, event.name)

    def edit_event(self):
        selected_event_index = self.event_listbox.curselection()
        if selected_event_index:
            selected_event_name = self.event_listbox.get(selected_event_index)
            events = Event.load_events()
            selected_event = next((event for event in events if event.name == selected_event_name), None)

            new_name = simpledialog.askstring("Edit Event", "New Event Name:", initialvalue=selected_event.name)
            new_date = simpledialog.askstring("Edit Event", "New Date (YYYY-MM-DD):", initialvalue=selected_event.date)
            new_location = simpledialog.askstring("Edit Event", "New Location:", initialvalue=selected_event.location)
            new_description = simpledialog.askstring("Edit Event", "New Description:", initialvalue=selected_event.description)

            if new_name and new_date and new_location and new_description:
                Event.delete_event(selected_event.name)
                edited_event = Event(new_name, new_date, new_location, new_description)
                Event.save_event(edited_event)
                self.load_events()
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields.")
        else:
            messagebox.showwarning("Selection Error", "Please select an event to edit.")

    def delete_event(self):
        selected_event_index = self.event_listbox.curselection()
        if selected_event_index:
            selected_event_name = self.event_listbox.get(selected_event_index)
            Event.delete_event(selected_event_name)
            self.load_events()
        else:
            messagebox.showwarning("Selection Error", "Please select an event to delete.")

    def clear_entries(self):
        self.entry_event_name.delete(0, tk.END)
        self.entry_event_date.delete(0, tk.END)
        self.entry_event_location.delete(0, tk.END)
        self.entry_event_description.delete(0, tk.END)


# Main application
root = tk.Tk()
app = EventApp(root)
root.mainloop()
