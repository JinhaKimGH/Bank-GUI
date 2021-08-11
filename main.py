import random
import datetime
import tkinter as tk
import tkinter.font


class Bank:
    accounts = []

    # initializes each account
    def __init__(self, f_name, l_name, password, email, balance=0):
        self.f_name = f_name
        self.l_name = l_name
        self.account_num = self.account_num_creation()
        self.password = password
        self.email = email
        self.balance = balance
        self.transactions = []
        Bank.add_account(self)

    # Adds each initialized account to a list
    @classmethod
    def add_account(cls, self):
        cls.accounts.append(self)

    # Creates a unique account number
    def account_num_creation(self):
        while True:
            account_num = random.randint(1000, 9999)

            if Bank.dup_account_num_check(account_num):
                continue

            else:
                break

        return account_num

    # Checks whether the account number is unique
    @classmethod
    def dup_account_num_check(cls, account_num):
        for account in cls.accounts:
            if account.account_num == account_num:
                return True

        else:
            return False

    # Withdraws Balance (Returns True for a successful withdrawl, returns False for an unsuccessful withdrawl)
    def withdraw(self, amount):
        if amount > self.balance:
            return False

        else:
            self.balance -= amount
            self.do_transactions("Withdrew", self.email, amount)
            return True

    # Deposits into their bank account
    def deposit(self, amount):
        self.balance += amount
        self.do_transactions("Deposited", self.email, amount)
        return

    # Creates a .txt statment of all the transactions made through this account
    def bank_statement(self):
        file = open("{} {}'s Bank Statement.txt".format(self.f_name, self.l_name), "w")

        for transaction in self.transactions:
            file.write(transaction + "\n")

        file.close()

        return

    # Transfers money through email (Returns True for a success, and False for a failure)
    def transfer(self, email, amount):
        if amount > self.balance:
            return 0

        transfer_to = None
        for account in Bank.accounts:
            if account.email == email:
                transfer_to = account
                break

        if transfer_to is None:
            return 2

        else:
            transfer_to.balance += amount

            self.balance -= amount

            self.do_transactions("Transfer", email, amount)

            transfer_to.do_transactions("Received", self.email, amount)
            return True

    # Appends each transaction into a list of transactions
    def do_transactions(self, action, target, amount):
        now = datetime.datetime.now()
        if action == "Transfer":
            self.transactions.append(
                "{}red ${} to {} on {}.".format(action, amount, target, now.strftime("%Y-%m-%d %H:%M:%S")))

        elif action == "Received":
            self.transactions.append(
                "{} ${} from {} on {}.".format(action, amount, target, now.strftime("%Y-%m-%d %H:%M:%S")))

        elif action == "Deposited":
            self.transactions.append("{} ${} on {}.".format(action, amount, now.strftime("%Y-%m-%d %H:%M:%S")))

        elif action == "Withdrew":
            self.transactions.append("{} ${} on {}.".format(action, amount, now.strftime("%Y-%m-%d %H:%M:%S")))

    @classmethod
    def login_confirm(cls, user, password):
        for account in cls.accounts:
            if account.account_num == user and account.password == password:
                return account

        return None


#The login screen of the application
def home():
    global account_number_entry1, password_entry1

    clear_widgets()

    title = tk.Label(text="Online Banking")
    title.pack(padx=5, pady=20)

    user = tk.Label(text="Account Number")
    user.config(font=("Avenir", 15))
    user.pack()

    account_number_entry1 = tk.Entry(window, justify='center', selectborderwidth=10)
    account_number_entry1.pack()

    passw = tk.Label(text="Password")
    passw.config(font=("Avenir", 15))
    passw.pack()
    password_entry1 = tk.Entry(window, justify='center', show="*")
    password_entry1.pack(pady=5)

    login_b = tk.Button(window, text="Login", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                        width=15, height=2, command=login)

    login_b.pack(pady=10, padx=5)

    register_b = tk.Button(window, text="Register", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                           width=15, height=2, command=register)

    register_b.pack(pady=10, padx=5)


def login():
    e_user = tk.Entry.get(account_number_entry1)

    try:
        e_user = int(e_user)

    except ValueError:
        entry_error = tk.Label(text="The account number must only consist of numbers.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    e_pass = tk.Entry.get(password_entry1)

    account = Bank.login_confirm(e_user, e_pass)

    if account is None:
        login_error = tk.Label(text="This account number or password is invalid.", font=("Avenir", 10),
                               fg="#FF0000")
        login_error.pack()
        return

    else:
        account_home(account)


def all_children():
    _list = window.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    return _list


def clear_widgets():
    widget_list = all_children()
    for item in widget_list:
        item.pack_forget()


def account_home(account):
    clear_widgets()

    welcome_lbl = tk.Label(text="Welcome {} {}!".format(account.f_name, account.l_name), font=("Avenir", 25))
    welcome_lbl.pack(pady=20)

    account_info_btn = tk.Button(window, text="Account Info", font=("Avenir", 15), bg="#FF2D00",
                                 activebackground="#D42A06", width=15, height=2, command=lambda: account_info(account))

    account_info_btn.pack(pady=10)

    deposit_btn = tk.Button(window, text="Deposit", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                            width=15, height=2, command=lambda: deposit(account))

    deposit_btn.pack(pady=10, padx=5)

    withdraw_btn = tk.Button(window, text="Withdraw", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                             width=15, height=2, command=lambda: withdraw(account))

    withdraw_btn.pack(pady=10, padx=5)

    transfer_btn = tk.Button(window, text="Transfer", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                             width=15, height=2, command=lambda: transfer(account))

    transfer_btn.pack(pady=10, padx=5)

    view_bank_statement_btn = tk.Button(window, text="View Statement", font=("Avenir", 15), bg="#FF2D00",
                                        activebackground="#D42A06", width=15, height=2,
                                        command=lambda: view_bank_statement(account))

    view_bank_statement_btn.pack(pady=10, padx=5)

    logout_btn = tk.Button(window, text="Logout", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                           width=15, height=2, command=home)

    logout_btn.pack(pady=15, padx=5)


# Opens the deposit screen
def deposit(account):
    clear_widgets()

    title = tk.Label(text="Deposit Money")
    title.pack(padx=5, pady=20)

    d_amount = tk.Label(text="Amount")
    d_amount.config(font=("Avenir", 15))
    d_amount.pack()

    d_amount_entry = tk.Entry(window, justify='center', selectborderwidth=10)
    d_amount_entry.pack()

    deposit_b = tk.Button(window, text="Deposit", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                          width=15, height=2, command=lambda: deposit_action(d_amount_entry, account))

    deposit_b.pack(pady=10, padx=5)

    back_btn = tk.Button(window, text="Back", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                         width=15, height=2, command=lambda: account_home(account))

    back_btn.pack()


# Checks and inputs the amount of money
def deposit_action(d_amount, account):
    d = tk.Entry.get(d_amount)

    try:
        to_deposit = int(d)

    except ValueError:
        entry_error = tk.Label(text="The deposit amount must consist of numbers.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    if to_deposit <= 0:
        entry_error = tk.Label(text="The deposit amount must be greater than 0.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    else:
        account.deposit(to_deposit)
        account_home(account)


def withdraw(account):
    clear_widgets()

    title = tk.Label(text="Withdraw Money")
    title.pack(padx=5, pady=20)

    w_amount = tk.Label(text="Amount")
    w_amount.config(font=("Avenir", 15))
    w_amount.pack()

    w_amount_entry = tk.Entry(window, justify='center', selectborderwidth=10)
    w_amount_entry.pack()

    withdraw_b = tk.Button(window, text="Withdraw", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                           width=15, height=2, command=lambda: withdraw_action(w_amount_entry, account))

    withdraw_b.pack(pady=10, padx=5)

    back_btn = tk.Button(window, text="Back", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                         width=15, height=2, command=lambda: account_home(account))

    back_btn.pack()


def withdraw_action(w_amount_entry, account):
    w = tk.Entry.get(w_amount_entry)

    try:
        to_withdraw = int(w)

    except ValueError:
        entry_error = tk.Label(text="The withdraw amount must consist of numbers.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    if to_withdraw <= 0:
        entry_error = tk.Label(text="The withdraw amount must be greater than 0.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    elif to_withdraw > account.balance:
        entry_error = tk.Label(text="The withdraw amount must be less than your account balance.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    else:
        account.withdraw(to_withdraw)
        account_home(account)


def transfer(account):
    clear_widgets()

    title = tk.Label(text="Transfer Money")
    title.pack(padx=5, pady=20)

    t_amount = tk.Label(text="Amount")
    t_amount.config(font=("Avenir", 15))
    t_amount.pack()

    t_amount_entry = tk.Entry(window, justify='center', selectborderwidth=10)
    t_amount_entry.pack()

    t_account = tk.Label(text="Email of account")
    t_account.config(font=("Avenir", 15))
    t_account.pack()

    t_account_entry = tk.Entry(window, justify='center', selectborderwidth=10)
    t_account_entry.pack()

    transfer_b = tk.Button(window, text="Transfer", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                           width=15, height=2, command=lambda: transfer_action(t_amount_entry, account, t_account_entry))

    transfer_b.pack(pady=10, padx=5)

    back_btn = tk.Button(window, text="Back", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                         width=15, height=2, command=lambda: account_home(account))

    back_btn.pack()


def transfer_action(amount_entry, account, account_two_entry):
    amount = tk.Entry.get(amount_entry)
    account_two_email = tk.Entry.get(account_two_entry)

    try:
        to_transfer = int(amount)

    except ValueError:
        entry_error = tk.Label(text="The transfer amount must consist of numbers.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    if to_transfer <= 0:
        entry_error = tk.Label(text="The transfer amount must be greater than 0.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    elif account_two_email == account.email:
        entry_error = tk.Label(text="You must enter an email other than your own.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    elif account_two_email == "":
        entry_error = tk.Label(text="You must enter an email.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    result = account.transfer(account_two_email, to_transfer)

    if result == 0:
        entry_error = tk.Label(text="The transfer amount must not be greater than your balance.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    elif result == 2:
        entry_error = tk.Label(text="This email doesn't exist in our database.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()
        return

    elif result is True:
        account_home(account)


def account_info(account):
    clear_widgets()

    title = tk.Label(text="Account Information")
    title.pack(padx=5, pady=10)

    fname = tk.Label(text="First Name: {}".format(account.f_name), font=("Avenir", 15))
    fname.pack(padx=5, pady=10)

    lname = tk.Label(text="Last Name: {}".format(account.l_name), font=("Avenir", 15))
    lname.pack(padx=5, pady=10)

    pswrd_label = tk.Label(text="Password: {}".format(account.password), font=("Avenir", 15))
    pswrd_label.pack(padx=5, pady=10)

    account_num_label = tk.Label(text="Account Number: {}".format(account.account_num), font=("Avenir", 15))
    account_num_label.pack(padx=5, pady=10)

    email_label = tk.Label(text="Email: {}".format(account.email), font=("Avenir", 15))
    email_label.pack(padx=5, pady=10)

    balance_label = tk.Label(text="Balance: ${}".format(account.balance), font=("Avenir", 15))
    balance_label.pack(padx=5, pady=10)

    back_btn = tk.Button(window, text="Back", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                         width=15, height=2, command=lambda: account_home(account))

    back_btn.pack()


def view_bank_statement(account):
    clear_widgets()

    title = tk.Label(text="{}'s Bank Statement".format(account.f_name))
    title.pack(padx=5, pady=10)

    for transaction in account.transactions:
        transaction_lbl = tk.Label(text=transaction, font=("Avenir", 15))
        transaction_lbl.pack(pady=2)

    download_btn = tk.Button(window, text="Download Statement", font=("Avenir", 15), bg="#FF2D00",
                             activebackground="#D42A06", width=20, height=2, command=account.bank_statement)

    download_btn.pack(pady=10)

    back_btn = tk.Button(window, text="Back", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                         width=15, height=2, command=lambda: account_home(account))

    back_btn.pack()


def register():
    clear_widgets()
    global registration_info

    registration_info = []

    registration_script = tk.Label(text="Please enter information to create your online banking account.")
    registration_script.config(font=("Avenir", 15))
    registration_script.pack(pady=15)

    # firstname, lastname, password, re-enter password, email

    firstname = tk.Label(text="First Name")
    firstname.config(font=("Avenir", 10))
    firstname.pack()
    firstname_entry = tk.Entry(window, justify='center', font=("Avenir", 20))
    firstname_entry.pack(pady=5)

    registration_info.append(firstname_entry)

    lastname = tk.Label(text="Last Name")
    lastname.config(font=("Avenir", 10))
    lastname.pack()
    lastname_entry = tk.Entry(window, justify='center', font=("Avenir", 20))
    lastname_entry.pack(pady=5)

    registration_info.append(lastname_entry)

    password2 = tk.Label(text="Password")
    password2.config(font=("Avenir", 10))
    password2.pack()
    password_entry2 = tk.Entry(window, justify='center', show="*", font=("Avenir", 20))
    password_entry2.pack(pady=5)

    registration_info.append(password_entry2)

    password_two = tk.Label(text="Re-enter your password")
    password_two.config(font=("Avenir", 10))
    password_two.pack()
    password_two_entry = tk.Entry(window, justify='center', show="*", font=("Avenir", 20))
    password_two_entry.pack(pady=5)

    registration_info.append(password_two_entry)

    email = tk.Label(text="Email")
    email.config(font=("Avenir", 10))
    email.pack()
    email_entry = tk.Entry(window, justify='center', font=("Avenir", 20))
    email_entry.pack(pady=5)

    registration_info.append(email_entry)

    register_b = tk.Button(window, text="Register", font=("Avenir", 10), bg="#FF2D00", activebackground="#D42A06",
                           width=10, height=2, command=check_registration_info)

    register_b.pack(pady=5)

    back_btn = tk.Button(window, text="Back", font=("Avenir", 10), bg="#FF2D00", activebackground="#D42A06",
                         width=10, height=2, command=home)

    back_btn.pack()


def check_registration_info():
    registration_entries = []

    for info in registration_info:
        registration_entries.append(tk.Entry.get(info))

    if "" in registration_entries:
        entry_error = tk.Label(text="Please enter information in all boxes.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()

    elif registration_entries[2] != registration_entries[3]:
        entry_error = tk.Label(text="Please make sure the entered passwords are matching.", font=("Avenir", 10),
                               fg="#FF0000")
        entry_error.pack()

    else:
        account = Bank(registration_entries[0], registration_entries[1], registration_entries[2],
                       registration_entries[4])

        clear_widgets()

        account_num_label = tk.Label(text="Your account number is {}.".format(account.account_num), font=("Avenir", 30),
                                     fg="#55E33E")

        account_num_label.pack(pady=100)

        next_btn = tk.Button(window, text="Next", font=("Avenir", 15), bg="#FF2D00", activebackground="#D42A06",
                             width=15, height=2, command=home)

        next_btn.pack(pady=5, padx=5)


def main():
    global window
    window = tk.Tk()
    window.title("Bank Account Application")
    default_font = tkinter.font.Font(family="Avenir", size=36)

    window.option_add('*Font', default_font)
    window.geometry("640x512")

    home()

    window.mainloop()


main()
