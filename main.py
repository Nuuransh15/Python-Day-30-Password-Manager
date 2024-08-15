from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- CONSTANTS ------------------------------- #
WINDOW_HEIGHT = 370
WINDOW_WIDTH = 480
CANVAS_HEIGHT = 200
CANVAS_WIDTH = 200
IMAGE_PATH = "logo.png"
SAVE_FILE_PATH = "data.json"
EMAIL_KEY = "email"
PASSWORD_KEY = "password"
NUM_INDENTS = 4
X_PAD = 50
Y_PAD = 50


# ---------------------------- GET ACCOUNT DETAILS ------------------------------- #
def get_details():
    """
    Gets the account details (email and password) from the website entered within the text entry field if it exists
    within data.json and shows the details to the user in a pop-up dialog box.
    :return: None
    """

    # Get string within text entry field
    website = website_entry.get().strip()
    if len(website) == 0:
        messagebox.showerror(title="Empty Field(s)", message="Error! \nThe Website field cannot be empty "
                                                             "or filled with whitespaces!")
        return

    try:
        with open(SAVE_FILE_PATH, "r") as data_file:
            data = json.load(data_file)
            account_details = data[website]

    except FileNotFoundError:
        messagebox.showerror(title="Non-existent data file", message="Error! \nNo data file exists, please save "
                                                                     "details for an account and try again!")
    except KeyError:
        messagebox.showerror(title="Website not found!", message=f"Error! \nNo saved details exist for the "
                                                                 f"following website: {website}")
    else:
        saved_email = account_details[EMAIL_KEY]
        saved_password = account_details[PASSWORD_KEY]
        messagebox.showinfo(title=website, message=f"Email: {saved_email} \nPassword: {saved_password}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """
    This function generates a random password within the 'Password' text entry field and copies this generated
    password to their system's clipboard.
    :return: None
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """
    Function to save the website, email and password details entered by the user into a datapoint within the JSON.
    :return: None
    """
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    data_dict = {
        website: {
            "email": email,
            "password": password
        }
    }

    # ensure no empty fields
    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showerror(title="Empty Field(s)", message="Error! \nThe Website, Email and Password fields "
                                                             "cannot be empty or filled with whitespaces!")
        return

    # confirmation pop-up
    is_okay = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: "
                                                            f"{email} \nPassword: {password} \nIs it okay to save?")
    if is_okay:
        try:
            with open(SAVE_FILE_PATH, "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open(SAVE_FILE_PATH, "w") as data_file:
                json.dump(data_dict, data_file, indent=NUM_INDENTS)

        else:
            data.update(data_dict)
            with open(SAVE_FILE_PATH, "w") as data_file:
                json.dump(data, data_file, indent=NUM_INDENTS)

            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=X_PAD, pady=Y_PAD)
window.minsize(height=WINDOW_HEIGHT, width=WINDOW_WIDTH)

# Lock logo image
lock_img = PhotoImage(file=IMAGE_PATH)
canvas = Canvas(height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
canvas.create_image(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, image=lock_img)
canvas.pack()
canvas.grid(column=1, row=0)

# -------------------------- LABELS -------------------------- #
# Website label
website_lbl = Label(text="Website:")
website_lbl.grid(column=0, row=1)

# Email label
email_lbl = Label(text="Email/Username:")
email_lbl.grid(column=0, row=2)

# Password label
password_lbl = Label(text="Password:")
password_lbl.grid(column=0, row=3)

# ------------------------ TEXT FIELDS ------------------------ #
# Website text field
website_entry = Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()

# Email text field
email_entry = Entry(width=50)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(index=0, string="example@email.com")

# Password text field
password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)

# -------------------------- BUTTONS -------------------------- #
# Generate password button
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3)

# Add button
add_button = Button(text="Add", width=42, command=save)
add_button.grid(column=1, row=4, columnspan=2)

# Search button
search_button = Button(text="Search", width=13, command=get_details)
search_button.grid(column=2, row=1)


window.mainloop()
