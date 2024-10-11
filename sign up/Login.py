from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import os
import bcrypt
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

RESET_COOLDOWN = 15 * 60  # 15 minutes in seconds
TOKEN_EXPIRATION_TIME = 3600  # 1 hour in seconds


def send_registration_email(client_email):
    sender_email = "yandisa.ndubela@capaciti.org.za"
    sender_password = "981008Yn#"

    subject = "Registration Successful"
    body = f"Welcome {client_email}!\n\nYour account has been created successfully.\n\nBest regards,\nSquad Goals"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = client_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def send_reset_email(client_email, token):
    sender_email = "yandisa.ndubela@capaciti.org.za"
    sender_password = "981008Yn#"

    subject = "Password Reset Request"
    reset_link = f"http://localhost/reset_password?token={token}&email={client_email}"
    body = f"Click the link to reset your password: {reset_link}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = client_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Reset email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def create_entry(frame, placeholder, y_position):
    def on_focus_in(event, entry_widget):
        if entry_widget.get() == placeholder:
            entry_widget.delete(0, 'end')
            entry_widget.config(fg='white')

    def on_focus_out(event, entry_widget):
        if entry_widget.get() == '':
            entry_widget.insert(0, placeholder)
            entry_widget.config(fg='#800080')

    entry = Entry(frame, width=25, fg='#800080', border=0, bg='black', font=('Microsoft YaHei UI Light', 11))
    entry.place(x=30, y=y_position)
    entry.insert(0, placeholder)

    entry.bind("<FocusIn>", lambda event: on_focus_in(event, entry))
    entry.bind("<FocusOut>", lambda event: on_focus_out(event, entry))

    Frame(frame, width=295, height=2, bg='purple').place(x=25, y=y_position + 27)

    return entry


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Sign Up")
        self.master.geometry('940x515+315+215')
        self.master.resizable(False, False)

        try:
            img = Image.open(r'C:\Users\Yandisa\OneDrive - Cape IT Initiative\Documents\Github\SquadGoals\sign up\pexels-photo-1190297.png')
            img_resized = img.resize((940, 515), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img_resized)
            self.master.tk_img = tk_img
        except Exception as e:
            print(f"Error loading image: {e}")
            tk_img = None

        if tk_img:
            background_label = Label(master, image=tk_img)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame = Frame(master, width=350, height=450, bg='#000000')
        self.frame.place(x=480, y=50)

        self.signup_window()

    def signup_window(self):
        self.clear_frame()

        heading = Label(self.frame, text='REGISTER', fg='#800080', bg='black', font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        self.email = create_entry(self.frame, 'Email Address', 80)
        self.password = create_entry(self.frame, 'Password', 150)
        self.confirm_password = create_entry(self.frame, 'Confirm Password', 220)

        Button(self.frame, width=39, pady=7, text='Sign Up', bg='#800080', fg='white', border=0, command=self.signup).place(x=35, y=350)

        label = Label(self.frame, text='Have an account?', fg='purple', bg='black', font=('Microsoft YaHei UI Light', 9))
        label.place(x=90, y=400)
        signin_button = Button(self.frame, width=6, text='Sign In', border=0, bg='black', cursor='hand2', fg='#800080', command=self.signin_window)
        signin_button.place(x=200, y=400)

    def signin_window(self):
        self.clear_frame()

        heading = Label(self.frame, text='LOG IN', fg='#800080', bg='black', font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        self.email = create_entry(self.frame, 'Email Address', 80)
        self.password = create_entry(self.frame, 'Password', 150)

        Button(self.frame, width=39, pady=7, text='Sign In', bg='#800080', fg='white', border=0, command=self.signin).place(x=35, y=220)

        label = Label(self.frame, text="Don't Have An Account?", fg='purple', bg='black', font=('Microsoft YaHei UI Light', 8))
        label.place(x=75, y=280)
        signup_button = Button(self.frame, width=6, text='Sign Up', border=0, bg='black', cursor='hand2', fg='#800080', command=self.signup_window)
        signup_button.place(x=200, y=280)

        forgot_password_button = Button(self.frame, text='Forgot Password?', border=0, bg='black', cursor='hand2', fg='purple', command=self.forgot_password_window)
        forgot_password_button.place(x=120, y=320)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def signup(self):
        email_value = self.email.get()
        password = self.password.get()
        confirm_password_value = self.confirm_password.get()

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email_value):
            messagebox.showerror('Invalid', 'Please enter a valid email address')
            return

        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messagebox.showerror('Invalid', 'Password must be at least 8 characters long, contain upper and lowercase letters, a number, and a special character')
            return

        if password != confirm_password_value:
            messagebox.showerror('Invalid', 'Both passwords must match')
            return

        user_data = {}
        data_file = 'datasheet.txt'

        if os.path.exists(data_file):
            with open(data_file, 'r') as file:
                for line in file:
                    if ',' in line:
                        email, hashed_password = line.strip().split(',', 1)
                        user_data[email] = hashed_password

        if email_value in user_data:
            messagebox.showerror('Error', 'Email already registered')
            return

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data[email_value] = hashed.decode('utf-8')

        with open(data_file, 'w') as file:
            for email, hashed_password in user_data.items():
                file.write(f"{email},{hashed_password}\n")

        send_registration_email(email_value)

        messagebox.showinfo('Signup', 'Successfully signed up')

    def signin(self):
        email_value = self.email.get()
        password = self.password.get()

        try:
            user_data = {}
            data_file = 'datasheet.txt'
            if os.path.exists(data_file):
                with open(data_file, 'r') as file:
                    for line in file:
                        email, hashed_password = line.strip().split(',')
                        user_data[email] = hashed_password

            if email_value in user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[email_value].encode('utf-8')):
                messagebox.showinfo('Sign In', 'Successfully logged in!')
            else:
                messagebox.showerror('Error', 'Incorrect email or password')
        except Exception as e:
            print(f"Error during sign-in: {e}")
            messagebox.showerror('Error', 'An error occurred during sign-in')

    def forgot_password_window(self):
        self.clear_frame()

        heading = Label(self.frame, text='RESET PASSWORD', fg='#800080', bg='black', font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=40, y=5)

        self.email = create_entry(self.frame, 'Email Address', 80)

        Button(self.frame, width=39, pady=7, text='Submit', bg='#800080', fg='white', border=0, command=self.forgot_password).place(x=35, y=200)
        
        label = Label(self.frame, text = 'Remembered your password?', fg = 'purple', bg ='black', font = ('Microsoft YaHei UI Light', 9))
        label.place(x = 50, y = 250)

        signin_button = Button(self.frame, width = 6, text = 'Log In', border = 0, bg = 'black', cursor = 'hand2', fg = '#800080', command = self.signin_window)
        signin_button.place(x = 220, y = 250)
    def forgot_password(self):
        email_value = self.email.get()

        # Email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email_value):
            messagebox.showerror('Invalid', 'Please enter a valid email address')
            return

        # Check if the email exists in the user data
        user_data = {}
        data_file = 'datasheet.txt'
        last_reset_file = 'last_reset.txt'  # file to store last reset timestamps

        if os.path.exists(data_file):
            with open(data_file, 'r') as file:
                for line in file:
                    email, hashed_password = line.strip().split(',')
                    user_data[email] = hashed_password

        if email_value not in user_data:
            messagebox.showerror('Error', 'Email address not registered')
            return

        # Check reset frequency from 'last_reset.txt'
        if os.path.exists(last_reset_file):
            with open(last_reset_file, 'r') as file:
                for line in file:
                    registered_email, last_reset_time = line.strip().split(',')
                    if email_value == registered_email:
                        last_reset_time = float(last_reset_time)
                        current_time = time.time()

                        # Check if cooldown period has passed
                        if current_time - last_reset_time < RESET_COOLDOWN:
                            messagebox.showerror('Error', f'Reset request too soon. Please wait {int((RESET_COOLDOWN - (current_time - last_reset_time)) // 60)} minutes.')
                            return

        # Generate a reset token
        reset_token = str(uuid.uuid4())

        # Update the last reset time
        with open(last_reset_file, 'a') as file:
            file.write(f"{email_value},{time.time()}\n")

        # Store the reset token securely
        self.store_reset_token(email_value, reset_token)

        # Send the reset email
        send_reset_email(email_value, reset_token)

        messagebox.showinfo('Forgot Password', 'Password reset email sent!')

    def store_reset_token(self, email, token):
        reset_token_file = 'reset_tokens.txt'

        with open(reset_token_file, 'a') as file:
            file.write(f"{email},{token},{time.time()}\n")

    def validate_reset_token(self, email, token):
        reset_token_file = 'reset_tokens.txt'
        if not os.path.exists(reset_token_file):
            return False  # Token not found

        with open(reset_token_file, 'r') as file:
            valid_tokens = []
            for line in file:
                stored_email, stored_token, token_time = line.strip().split(',')
                token_time = float(token_time)

                # Check if token is expired
                if email == stored_email and token == stored_token:
                    if time.time() - token_time < TOKEN_EXPIRATION_TIME:
                        return True
                    else:
                        messagebox.showerror('Error', 'Token has expired.')
                        return False
                else:
                    valid_tokens.append(line)

        # Clean up expired tokens
        with open(reset_token_file, 'w') as file:
            file.writelines(valid_tokens)

        return False  # Token is invalid


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()
