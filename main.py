from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols= [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)
    password="".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def get_value():
    website_value=website_entry.get()
    email_value=email_entry.get()
    password_value=password_entry.get()
    new_data={
        website_value :{
            "email":email_value,
            "password":password_value
        }
    }
    is_okay=False
    if website_value=='' or email_value=='' or password_value=='':
        messagebox.showerror("Error","Please fill all the fields")
    else:
        is_okay=messagebox.askokcancel(title=f"{website_value}",message=f"This is the information that you give:\nEmail= {email_value}\n Password:{password_value}\n is this okay to save?")
    if is_okay==True:
        try:
            with open("data.json","r") as file:
                data = json.load(file)
                data.update(new_data)
        except (json.JSONDecodeError, FileNotFoundError):
            with open("./data.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            with open("./data.json", mode="w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ----------------------------FIND PASSWORD------------------------------- #
def get_password():
    website_value=website_entry.get()
    with open("data.json","r") as file:
        data = json.load(file)
        try:
            data_value=data[website_value]
            password_value=data_value["password"]
            email_value=data_value["email"]
            messagebox.showinfo(title=f"{website_value}",message=f"Email/Username: {email_value} \n Password: {password_value}")
        except json.JSONDecodeError:
            messagebox.showinfo(title="error",message="Error, Your database is empty")
        except FileNotFoundError:
            messagebox.showinfo(title="error",message="Error, No such file")
        except KeyError as err:
            messagebox.showinfo(title="error", message=f"No details for {err} exists")
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)


canvas = Canvas(width=200, height=200)
lock_image=PhotoImage(file="logo.png")
canvas.create_image(100, 100,image=lock_image)
canvas.grid(column=1, row=0)

website_label=Label(text="Website:")
website_label.grid(column=0, row=1)
website_entry=Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()

search_button=Button(text="Search",width=12,command=get_password)
search_button.grid(column=2, row=1)

email_label=Label(text="Email/Username:")
email_label.grid(column=0, row=2)
email_entry=Entry(width=37)
email_entry.grid(column=1, row=2,columnspan=2)
email_entry.insert(0,"YOUR EMAIL")

password_label=Label(text="Password:")
password_label.grid(column=0, row=3)
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)
password_button=Button(text="Generate Password",command=generate_password,width=12)
password_button.grid(column=2, row=3)

add_button=Button(text="Add",width=35,command=get_value)
add_button.grid(column=1, row=4,columnspan=2)

window.mainloop()