from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from email.utils import parseaddr
import re
import os
import bcrypt
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import threading
from tkinter import ttk
from tkinter import Tk, Label, Toplevel, Frame, Button, Entry, messagebox 

RESET_COOLDOWN = 15 * 60  
TOKEN_EXPIRATION_TIME = 3600  


# Function to send registration email
def send_registration_email(client_email, password):
    sender_email = "Yandisa.Ndubela@Capaciti.org.za"
    sender_password = "981008Yn#" 

    subject = "Registration Successful"
    body = (f"Welcome {client_email}!\n\n"
            f"Your account has been created successfully.\n"
            f"Your password is: {password}\n\n"
            "Best regards,\nEventPlannify Team")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = client_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.set_debuglevel(1)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Registration email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error Sending Email", f"Error sending registration email")

# Function to send reset email with token
def send_reset_email(client_email, token):
    sender_email = "Yandisa.Ndubela@Capaciti.org.za"
    sender_password = "981008Yn#"

    subject = "Password Reset Request"
    reset_link = f"http://localhost/reset_password?token={token}&email={client_email}"
    body = f"Click the link to reset your password: {reset_link}. Tokens will expire after an hour."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = client_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.set_debuglevel(1)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Reset email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error Sending Email", f"Error sending reset email")

# Function to create entry widgets with placeholders
def create_entry(frame, placeholder, y_position):
    entry = Entry(frame, width = 25, fg = '#800080', border = 0, bg = 'black', font = ('Microsoft YaHei UI Light', 11))
    entry.place(x = 30, y= y_position)
    entry.insert(0, placeholder)

    entry.bind("<FocusIn>", lambda event: on_focus_in(event, entry, placeholder))
    entry.bind("<FocusOut>", lambda event: on_focus_out(event, entry, placeholder))

    Frame(frame, width = 295, height = 2, bg = 'purple').place(x = 25, y=y_position + 27)
    
    return entry
    
def on_focus_in(event, entry_widget, placeholder):
        if  entry_widget.get() == placeholder:
            entry_widget.delete(0, 'end')
            entry_widget.config(fg='white')

def on_focus_out(event, entry_widget, placeholder):
        if entry_widget.get() == '':
            entry_widget.insert(0, placeholder)
            entry_widget.config(fg='#800080')

def is_valid_email(email):
    return '@' in parseaddr(email)[1]
    
class SplashScreen:
  def __init__(self, master):
        self.master = master 
        self.master.title("Welcome")
        self.master.geometry('1400x800')
        self.master.resizable(True, True)

        img_path = r'C:\Users\Yandisa\OneDrive - Cape IT Initiative\Documents\GitHub\SquadGoals\sign up\free-photo-of-thrilling-amusement-park-ride-at-twilight.jpeg'
        if os.path.exists(img_path):
                    print("Image found.")
        img = Image.open(img_path)
        img_resized = img.resize((1400, 800), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img_resized)
        background_label = Label(master, image=self.tk_img)
        background_label.place(x=0, y=0, relwidth=1)

        self.canvas = Canvas(master, width = 1400, height = 800, bg = "white", highlightthickness=0)
        self.canvas.place(x = 0, y = 0 , relwidth = 1, relheight = 1)

        self.canvas.create_image(0,0, anchor = 'nw', image = self.tk_img)
        self.canvas.create_text(700, 300, text = "Welcome to EventPlannify", fill = "#000000", font = ('Microsoft YaHei UI Light',48, 'bold'), anchor = 'center')
      

        
        self.canvas.create_text(700, 400, text = "Crafting Experiences 1 Event At A Time", fill = "white", font = ('Microsoft YaHei UI Light', 18, 'italic'), anchor = 'center')

        style = ttk.Style()
        style.theme_use('default')
        style.configure("custom.Horizontal.TProgressbar", thickness = 15, troughcolor = '#444444', background = '#800080', relief = 'flat')
        self.progress_bar = ttk.Progressbar(master, orient = "horizontal", length = 400, mode = 'indeterminate', style = "custom.Horizontal.TProgressbar")
        self.progress_bar.place(relx =0.5, rely = 0.65, anchor = 'center')
        self.progress_bar.start()

        self.master.after(6000, self.hide_splash)
  def create_text_with_shadow(self, x, y, text, shadow_color, text_color, font_size, font_weight):
        """Creates text with a shadow effect."""
        # Create shadow text (slightly offset)
        self.canvas.create_text(x + 2, y + 2, text=text, fill=shadow_color, font=('Microsoft YaHei UI Light', font_size, font_weight), anchor='center')
        # Create main text
        self.canvas.create_text(x, y, text=text, fill=text_color, font=('Microsoft YaHei UI Light', font_size, font_weight), anchor='center')
  def hide_splash(self):
    self.progress_bar.stop()
    self.master.destroy()
    root = Tk()
    app = App(root)
    root.mainloop()
      



class App:



    def __init__(self, master):
        self.master = master
        self.loading_lable = None
        self.master.title("Sign Up")
        self.master.geometry('1400x800')
        self.master.resizable(True, True)
        self.frame = Frame(master, width = 350, height = 450, bg = '#000000')
        self.frame.place(x = 480, y = 50)
        self.spinner_label = None

        self.email = create_entry(self.frame, 'Email Address', 80)

   
    
        try:
            img_path = r'C:\Users\Yandisa\OneDrive - Cape IT Initiative\Documents\GitHub\SquadGoals\sign up\pexels-photo-1190297.png'
            if os.path.exists(img_path):
                    print("Image found.")
            img = Image.open(img_path)
            img_resized = img.resize((1400, 800), Image.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img_resized)
            background_label = Label(master, image=self.tk_img)
            background_label.place(x=0, y=0, relwidth=1)
        
        except Exception as e:
            print(f"Error loading image: {e}")
           

        self.frame = Frame(master, width=350, height=450, bg='#000000')
        self.frame.place(x=480, y=50)

        self.current_frame = 'signup'
        self.signup_window()
    
    class Tooltip:
     def __init__(self, widget, text):
        self.widget = widget
        self.text = text 
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window is not None:
            return 
        
        x, y, _, _, = self.widgetbbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.window.wm_geometry(f"+ {x}={y}")
        
        label = Label(self.tooltip_window, text = self.text, bg = "lightyellow", relief = "solid", borderwidth= 1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def show_loading_spinner(self):
        self.loading_label = Label(self.frame, text = "Processing ...", fg = 'white', bg = 'black')
        self.loading_label.place(x = 150, y = 200)
        self.master.update_idletasks()

    def hide_loading_spinner(self):
        if self.loading_label:
            self.loading_label.destroy()
            self.loading_label = None

    def normalize_email(self, email):
        if '@' not in email or email.count('@') !=1:
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return None
            
        
        local_part, domain_part = email.split ('@')
        local_part = local_part.replace('.','')
        domain_part = domain_part.lower()
        return f"{local_part}@{domain_part}"
    
    # Method to handle frame transitions
    def signup_window(self):
        self.transition_frame('signup')

    def signin_window(self):
        self.transition_frame('signin')

    def forgot_password_window(self):
        self.transition_frame('forgot_password')

    def transition_frame(self, frame_type):
        self.clear_frame()
        if frame_type == 'signup':
            self.create_signup_frame()
        elif frame_type == 'signin':
            self.create_signin_frame()
        elif frame_type == 'forgot_password':
            self.create_forgot_password_frame()
        self.current_frame = frame_type

    # Signup frame creation
    def create_signup_frame(self):
        self.frame.config(width = 400, height =560)
        heading = Label(self.frame, text='REGISTER', fg='#800080', bg='black', font=('Microsoft YaHei UI Light', 30, 'bold'))
        heading.place(relx=0.5, y=20, anchor='n')

        self.email = create_entry(self.frame, 'Email Address', 100)
        self.password = create_entry(self.frame, 'Password', 180)
        self.confirm_password = create_entry(self.frame, 'Confirm Password', 260)
        self.strength_label = Label(self.frame, text="", fg='white', bg='black', font=('Microsoft YaHei UI Light', 20))
        self.strength_label.place(x=30, y=220)

        self.password_entry = self.password 
        self.password_entry.bind("<KeyRelease>", self.check_password_strength)

        Button(self.frame, width=50, pady=10, text='Sign Up', bg='#800080', fg='white', border=0, command=self.signup).place(relx=0.5, y=400, anchor = 'n')

        label = Label(self.frame, text='Have an account?', fg='purple', bg='black', font=('Microsoft YaHei UI Light', 12))
        label.place(relx=0.5, y=450, anchor = 'n')
        signin_button = Button(self.frame, width=10, text='Sign In', border=0, bg='black', cursor='hand2', fg='#800080', font = ('Microsoft YaHei UI Light', 9, ), command=self.signin_window)
        signin_button.place(relx=0.5, y=480, anchor= 'n')
        self.add_hover_effects(signin_button)

    # Sign-in frame creation
    def create_signin_frame(self):
        heading = Label(self.frame, text='LOG IN', fg='#800080', bg='black', font=('Microsoft YaHei UI Light', 30, 'bold'))
        heading.place(relx = 0.5, y = 20, anchor = 'n')

        self.email = create_entry(self.frame, 'Email Address', 100)
        self.password = create_entry(self.frame, 'Password', 180)

        Button(self.frame, width=50, pady=10, text='Sign In', bg='#800080', fg='white', border=0, command=self.signin).place(relx=0.5, y=300, anchor= 'n')

        label = Label(self.frame, text="Don't Have An Account?", fg='purple', bg='black', font=('Microsoft YaHei UI Light', 12))
        label.place(relx=0.5, y=360, anchor = 'n')
        signup_button = Button(self.frame, width=10, text='Sign Up', border=0, bg='black', cursor='hand2', fg='#800080', font = ('Microsoft YaHei UI Light', 9, 'italic'), command=self.signup_window)
        signup_button.place(relx=0.5, y=400, anchor = 'n')
        self.add_hover_effects(signup_button)

        forgot_password_button = Button(self.frame, text='Forgot Password?', border=0, bg='black', cursor='hand2', fg='purple', font = ('Microsoft YaHei UI Light', 9, ), command=self.forgot_password_window)
        forgot_password_button.place(relx=0.5, y=440, anchor = 'n')
        self.add_hover_effects(forgot_password_button)

    # Forgot password frame creation
    def create_forgot_password_frame(self):
        heading = Label(self.frame, text='RESET PASSWORD', fg='#800080', bg='black', font=('Microsoft YaHei UI Light', 30, 'bold'))
        heading.place(relx=0.5, y=20, anchor = 'n')

        self.reset_email = create_entry(self.frame, 'Registered Email', 100)

        Button(self.frame, width=50, pady=10, text='Send Reset Token', bg='#800080', fg='white', border=0, command=self.send_reset_token).place(relx=0.5, y=200, anchor = 'n')

        back_button = Button(self.frame, text='Remembered your password?', border=0, bg='black', cursor='hand2', fg='purple', font = ('Microsoft YaHei UI Light', 9), command=self.signin_window)
        back_button.place(relx=0.5, y=260, anchor = 'n')
        self.add_hover_effects(back_button)

    # Clear frame content
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
    

    def start_main_app(self):
        self.master.deiconify()
        self.master.mainloop()



    # Password strength checker
    def check_password_strength(self, event):
        password = self.password_entry.get()
        strength, color  = self.evaluate_password_strength(password)
        self.strength_label.config(text=strength, fg = color)
        self.set_password_entry_text_color(strength)

    def set_password_entry_text_color(self, strength):
        if strength.startswith("Weak"):
            self.password_entry.config(fg='red')
        else: 
             self.password_entry.config(fg = 'green')
    
    
    def evaluate_password_strength(self, password):
        criteria = []
        if len(password) < 8:
            criteria.append("min 8 characters")
        if not re.search(r"[A-Z]", password):
            criteria.append ("1 uppercase letter")
        if not re.search(r"[0-9]", password):
            criteria.append ("1 number")
        if not re.search(r"[@$!%*?&#]", password):
            criteria.append("1 special character")
        
        if criteria:
            return f"Weak Password: {';'.join(criteria)}",'red'
        return  "Strong Password", "green"  

    # Button hover effects
    def add_hover_effects(self, button):
        def on_enter(event):
            button.config(fg='white', bg='purple')
        def on_leave(event):
            button.config(fg='#800080', bg='black')

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    def disable_buttons(self):
        for button in self.frame.winfo_children():
            if isinstance(button, Button):
                button.config(state = DISABLED)

    def enable_buttons(self):
        for button in self.frame.winfo_children():
            if isinstance(button, Button):
                button.config(state = NORMAL)

    # Signup function
    def signup(self):
        self.disable_buttons()
        self.show_loading_spinner()
        email = self.email.get()
        password = self.password.get()
        confirm_password = self.confirm_password.get()
        normalized_email = self.normalize_email(email)
        
        if normalized_email is None:
           self.hide_loading_spinner()
           self.enable_buttons()
           return

        if not email or '@' not in email:
            messagebox.showerror("Error", "Please enter a valid email address!")
            self.hide_loading_spinner()
            self.enable_buttons()
            return
        
        normalized_email = self.normalize_email(email)
        self.hide_loading_spinner()
        self.enable_buttons()

        if not email or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are requried!")
            return
 

        if self.email_registered(normalized_email):
            messagebox.showerror("Error", "Email already registered!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        strength, color = self.evaluate_password_strength(password)
        if strength.startswith("Weak"):
            messagebox.showerror("Error", "Password is not strong enough!")

            return 
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.save_user_data(email, hashed_password)
        self.progress_and_email(email, "registration", password = password)
    
    def email_registered(self, email):
     with open('C:\\Users\\Yandisa\\OneDrive - Cape IT Initiative\\Documents\\GitHub\\SquadGoals\\sign up\\datasheet.txt', 'r') as file:
        users = file.readlines()
        for user in users:
            user = user.strip()  
            if user:  # Check if the line is not empty
                try:
                    saved_email, _ = user.split(',')  
                    if saved_email == email:
                        return True
                except ValueError:
                    print(f"Skipping invalid line: {user}")  
     return False
    # Save user data
    def save_user_data(self,normalized_email, hashed_password):
        with open('C:\\Users\\Yandisa\\OneDrive - Cape IT Initiative\\Documents\\GitHub\\SquadGoals\\sign up\\datasheet.txt', 'a') as file:
            file.write(f"{normalized_email},{hashed_password.decode('utf-8')}\n")
    
    
    # Signin function
    def signin(self):
     email = self.email.get()
     password = self.password.get()


    # Check if the email is registered
     if not self.email_registered(email):
        messagebox.showerror("Error", "Email not registered! Please sign up.")
        return

    # Ensure password field is not empty
     if not password:
        messagebox.showerror("Error", "Missing Fields")
        return

    # Open and read the stored user data
     with open('C:\\Users\\Yandisa\\OneDrive - Cape IT Initiative\\Documents\\GitHub\\SquadGoals\\sign up\\datasheet.txt', 'r') as file:
        users = file.readlines()
        for user in users:
            # Each line should contain email and hashed password separated by a comma
            try:
                saved_email, saved_hashed_password = user.strip().split(',')
                
                # Check if the email matches
                if saved_email == email:
                    # Validate the password using bcrypt
                    if bcrypt.checkpw(password.encode('utf-8'), saved_hashed_password.encode('utf-8')):
                        messagebox.showinfo("Success", "Login successful!")
                        return
                    else:
                        messagebox.showerror("Error", "Incorrect Password! Please try again.")
                        return
            except ValueError:
                print(f"Error processing line: {user}")

    # If no matching email is found
    messagebox.showerror("Error", "Invalid credentials!")

   
    # Forgot password
    def send_reset_token(self):
        email = self.reset_email.get()

        if not self.email_registered(email):
            messagebox.showerror("Error", "Email not registered!")
            return

        token = str(uuid.uuid4())
        self.save_token(email, token)
        self.progress_and_email(email, "reset", token)

    # Token management
    def save_token(self, email, token):
        with open('C:\\Users\\Yandisa\\OneDrive - Cape IT Initiative\\Documents\\GitHub\\SquadGoals\\sign up\\tokens.txt', 'a') as file:
            file.write(f"{email},{token},{time.time()}\n")


    def is_token_valid(self, email, token):
        with open('C:\\Users\\Yandisa\\OneDrive - Cape IT Initiative\\Documents\\Github\\SquadGoals\\sign up\\tokens.txt', 'r') as file:
            tokens = file.readlines()
            for t in tokens:
             saved_email, saved_token, timestamp = t.strip().split(',')
             if saved_email == email and saved_token == token:
              if time.time() - float(timestamp) < TOKEN_EXPIRATION_TIME:
                 return True
            return False  
    # Progress bar simulation
    def progress_and_email(self, email, email_type, token=None, password = None):
        progress_window = Toplevel(self.master)
        progress_window.title("Verifying Email")
        progress_window.geometry("300x100")

        label = Label(progress_window, text="Email verification in process please wait")
        label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, orient=HORIZONTAL, length=200, mode='determinate')
        progress_bar.pack(pady=10)
        progress_bar.start()

        def send_email_simulation():
            time.sleep(5)
            progress_bar.stop()
            progress_window.destroy()

            if email_type == "registration":
                send_registration_email(email, password)
                messagebox.showinfo("Success", "Registered successfully!")
                self.signin_window()
            elif email_type == "reset":
                send_reset_email(email, token)
                messagebox.showinfo("Success", "Reset token sent to your email!")
                self.signin_window()

        threading.Thread(target=send_email_simulation).start()

if __name__ == "__main__":
   root = Tk()
   splash = SplashScreen(root)
   root.mainloop()
