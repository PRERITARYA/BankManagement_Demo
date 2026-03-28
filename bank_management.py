"""
╔══════════════════════════════════════════════════════════════╗
║              BANK MANAGEMENT SYSTEM                          ║
║              Built with Python + MySQL                       ║
║              Class 12 | Computer Science Project             ║
║              Author: Prerit Arya                             ║
╚══════════════════════════════════════════════════════════════╝
"""

import mysql.connector as mysql


# ─────────────────────────────────────────────
#  DATABASE CONNECTION HELPER
# ─────────────────────────────────────────────

def get_connection():
    """Return a fresh MySQL connection."""
    return mysql.connect(
        host="localhost",
        user="root",
        passwd="1234",       # ← Change to your MySQL password
        database="bank_db"
    )


# ─────────────────────────────────────────────
#  UTILITY: PRINT DIVIDER
# ─────────────────────────────────────────────

def divider(char="-", length=60):
    print(char * length)


# ══════════════════════════════════════════════
#  ADMIN FUNCTIONS
# ══════════════════════════════════════════════

def write_data():
    """
    ADMIN | Create new customer records.
    Loops until the admin presses Q to quit.
    """
    connection = get_connection()
    cursor = connection.cursor(buffered=True)
    choice = 'o'

    while choice not in ('Q', 'q'):

        # ── Account Number ──
        str_accno = input("Enter account no: ")
        if not str_accno.isdigit():
            print("❌ Account number should be digits only.")
            connection.close()
            return 0
        acc_no = int(str_accno)

        # ── Customer Name ──
        customer_name = input("Enter name: ")

        # ── Account Type ──
        print("\n┌─────────────────────┐")
        print("│    Account Type     │")
        print("│  C : Current        │")
        print("│  S : Savings        │")
        print("└─────────────────────┘")
        choice = input("Enter your choice: ")

        if choice in ('c', 'C'):
            acc_type = "Current"
        elif choice in ('s', 'S'):
            acc_type = "Savings"
        else:
            print("❌ Invalid account type choice.")
            connection.close()
            return 0

        # ── Balance ──
        str_bal = input("Enter balance amount: ")
        if not str_bal.isdigit():
            print("❌ Amount should be digits only.")
            connection.close()
            return 0
        bal_amt = float(str_bal)

        # ── Address ──
        address = input("Enter address: ")

        # ── Phone Number ──
        str_phone = input("Enter phone number: ")
        if len(str_phone) != 10:
            print("❌ Phone number must be exactly 10 digits.")
            connection.close()
            return 0
        ph_no = int(str_phone)

        # ── Insert into bank_record ──
        query = """
            INSERT INTO bank_record
                (ACCOUNT_NO, CUSTOMER_NAME, BALANCE, ACCOUNT_TYPE, ADDRESS, PHONE_NO)
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
        """.format(acc_no, customer_name, bal_amt, acc_type, address, ph_no)
        cursor.execute(query)
        connection.commit()

        # ── Log transaction ──
        cursor.execute("SELECT * FROM bank_record")
        data = cursor.fetchall()
        sr = data[-1][0]
        cursor.execute(
            "INSERT INTO transaction (sr, trans_type, trns_date) VALUES ({}, 'Create', CURDATE())".format(sr)
        )
        connection.commit()

        print("\n✅ Account created successfully!\n")

        print("Press Q to QUIT  |  Press Enter to add another record")
        choice = input("Your choice: ")

    connection.close()
    return 1


# ──────────────────────────────────────────────

def add_data():
    """
    CUSTOMER | Open a new bank account.
    """
    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    # ── Account Number ──
    str_accno = input("Enter account no: ")
    if not str_accno.isdigit():
        print("❌ Account number should be digits only.")
        connection.close()
        return 0
    acc_no = int(str_accno)

    # ── Customer Name ──
    customer_name = input("Enter name: ")

    # ── Account Type ──
    print("\n┌─────────────────────┐")
    print("│    Account Type     │")
    print("│  C : Current        │")
    print("│  S : Savings        │")
    print("└─────────────────────┘")
    choice = input("Enter your choice: ")

    if choice in ('c', 'C'):
        acc_type = "Current"
    elif choice in ('s', 'S'):
        acc_type = "Savings"
    else:
        print("❌ Invalid account type choice.")
        connection.close()
        return 0

    # ── Initial Deposit ──
    deposit = input("Do you want to deposit money? (Y/N): ")
    if deposit in ('y', 'Y'):
        bal_amt = float(input("Enter balance amount: "))
    else:
        bal_amt = 0.0

    # ── Address & Phone ──
    address = input("Enter address: ")
    ph_no = int(input("Enter phone number: "))

    # ── Insert into bank_record ──
    query = """
        INSERT INTO bank_record
            (ACCOUNT_NO, CUSTOMER_NAME, BALANCE, ACCOUNT_TYPE, ADDRESS, PHONE_NO)
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
    """.format(acc_no, customer_name, bal_amt, acc_type, address, ph_no)
    cursor.execute(query)
    connection.commit()

    # ── Log transaction ──
    cursor.execute("SELECT * FROM bank_record")
    data = cursor.fetchall()
    sr = data[-1][0]
    cursor.execute(
        "INSERT INTO transaction (sr, trans_type, trns_date) VALUES ({}, 'Create', CURDATE())".format(sr)
    )
    connection.commit()

    print("\n✅ Process completed.\n")
    connection.close()
    return 1


# ──────────────────────────────────────────────

def read_data():
    """
    ADMIN | Display all customer records in a formatted table.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM bank_record")
    bank_data = cursor.fetchall()

    print()
    print(" SR NO  ", "Customer Name".ljust(18), "Account Number".ljust(16),
          "Account Type".ljust(14), "Balance".ljust(17), "Contact".ljust(17), "Address")
    divider("-", 117)

    for row in bank_data:
        print("➤",
              str(row[0]).ljust(6),
              str(row[2]).ljust(18),
              str(row[1]).ljust(16),
              str(row[4]).ljust(14),
              str(row[3]).ljust(17),
              str(row[6]).ljust(17),
              row[5])
        print()

    connection.close()


# ──────────────────────────────────────────────

def search_data():
    """
    ADMIN & CUSTOMER | Search for a customer by account number.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM bank_record")
    bank_data = cursor.fetchall()

    str_accno = input("Enter account no: ")
    if not str_accno.isdigit():
        print("❌ Account number should be digits only.")
        connection.close()
        return 0
    acc_no = int(str_accno)

    for row in bank_data:
        if int(row[1]) == acc_no:
            print()
            divider()
            print("  SR No          :", row[0])
            print("  Account Number :", row[1])
            print("  Account Name   :", row[2])
            print("  Account Type   :", row[4])
            print("  Balance        :", row[3])
            print("  Address        :", row[5])
            print("  Contact Number :", row[6])
            divider()
            break
    else:
        print("❌ Account number not found.")

    connection.close()


# ──────────────────────────────────────────────

def update_data():
    """
    ADMIN | Update customer details (name, balance, address, phone).
    """
    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute("SELECT * FROM bank_record")
    bank_data = cursor.fetchall()

    # ── Show all customers ──
    print("\n  CUSTOMER NAME".ljust(22), "ACCOUNT NO")
    divider("-", 40)
    for row in bank_data:
        print(" ", str(row[2]).ljust(20), row[1])
        divider("-", 40)

    acc_no = int(input("Enter account number to update: "))
    ch = 'Y'

    for row in bank_data:
        if int(row[1]) == acc_no:
            while ch not in ('n', 'N'):
                print("\n┌──────────────────────────────────────────┐")
                print("│         What do you want to update?      │")
                print("│  1 : Change customer name                │")
                print("│  2 : Change balance amount               │")
                print("│  3 : Change address                      │")
                print("│  4 : Change phone number                 │")
                print("└──────────────────────────────────────────┘")
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    new_name = input("Enter new customer name: ")
                    cursor.execute(
                        "UPDATE bank_record SET customer_name = '{}' WHERE account_no = {}".format(new_name, acc_no)
                    )
                    cursor.execute(
                        "INSERT INTO transaction (sr, trans_type, trns_date) VALUES ({}, 'Name Update', CURDATE())".format(row[0])
                    )
                    print("\n✅ Customer name updated successfully.")

                elif choice == 2:
                    bal_amt = float(input("Enter new balance: "))
                    cursor.execute(
                        "UPDATE bank_record SET balance = {} WHERE account_no = {}".format(bal_amt, acc_no)
                    )
                    cursor.execute(
                        "INSERT INTO transaction (sr, trans_type, trns_date) VALUES ({}, 'Balance Update', CURDATE())".format(row[0])
                    )
                    print("\n✅ Balance updated successfully.")

                elif choice == 3:
                    new_address = input("Enter new address: ")
                    cursor.execute(
                        "UPDATE bank_record SET ADDRESS = '{}' WHERE account_no = {}".format(new_address, acc_no)
                    )
                    cursor.execute(
                        "INSERT INTO transaction (sr, trans_type, trns_date) VALUES ({}, 'Address Update', CURDATE())".format(row[0])
                    )
                    print("\n✅ Address updated successfully.")

                elif choice == 4:
                    ph_no = input("Enter new phone number: ")
                    cursor.execute(
                        "UPDATE bank_record SET phone_no = '{}' WHERE account_no = {}".format(ph_no, acc_no)
                    )
                    cursor.execute(
                        "INSERT INTO transaction (sr, trans_type, trns_date) VALUES ({}, 'Phone Update', CURDATE())".format(row[0])
                    )
                    print("\n✅ Phone number updated successfully.")

                else:
                    print("❌ Invalid choice.")
                    connection.close()
                    return 0

                ch = input("Do you want to update more items? (Y/N): ")

            connection.commit()
            connection.close()
            return 1

    print("❌ Account number not found.")
    connection.close()
    return 0


# ──────────────────────────────────────────────

def del_data():
    """
    ADMIN | Delete a customer account.
    """
    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute("SELECT * FROM bank_record")
    bank_data = cursor.fetchall()

    # ── Show all customers ──
    print("\n  CUSTOMER NAME".ljust(22), "ACCOUNT NO")
    divider("-", 40)
    for row in bank_data:
        print(" ", str(row[2]).ljust(20), row[1])
        divider("-", 40)

    acc_no = int(input("Enter account number to delete: "))

    for row in bank_data:
        if int(row[1]) == acc_no:
            sr = row[0]
            cursor.execute(
                "DELETE FROM bank_record WHERE account_no = {}".format(acc_no)
            )
            cursor.execute(
                "INSERT INTO transaction (sr, trans_type, trns_date) VALUES ({}, 'Deleted', CURDATE())".format(sr)
            )
            connection.commit()
            print("\n🗑️  Account deleted successfully.")
            connection.close()
            return
    else:
        print("❌ Account number not found.")

    connection.close()


# ══════════════════════════════════════════════
#  CUSTOMER FUNCTIONS
# ══════════════════════════════════════════════

def deposite():
    """
    CUSTOMER | Deposit money into an account.
    """
    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute("SELECT * FROM bank_record")
    bank_data = cursor.fetchall()

    acc_no = input("Enter account no: ")
    if not acc_no.isdigit():
        print("❌ Account number should be digits only.")
        connection.close()
        return 0

    for row in bank_data:
        if int(acc_no) == int(row[1]):
            depo_amt = float(input("Enter deposit amount: "))
            updated_balance = row[3] + depo_amt

            cursor.execute(
                "UPDATE bank_record SET balance = {} WHERE account_no = {}".format(updated_balance, int(acc_no))
            )
            cursor.execute(
                "INSERT INTO transaction (sr, trans_type, amount, trns_date) VALUES ({}, 'Debit', {}, CURDATE())".format(row[0], depo_amt)
            )
            connection.commit()

            print("\n✅ Money deposited successfully.")
            print("   Updated balance: ₹", updated_balance)
            connection.close()
            return 1

    print("❌ Account number not found.")
    connection.close()
    return 0


# ──────────────────────────────────────────────

def withdrawal():
    """
    CUSTOMER | Withdraw money from an account.
    """
    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute("SELECT * FROM bank_record")
    bank_data = cursor.fetchall()

    str_acc_no = input("Enter account no: ")
    if not str_acc_no.isdigit():
        print("❌ Account number should be digits only.")
        connection.close()
        return 0
    acc_no = int(str_acc_no)

    for row in bank_data:
        if row[1] == acc_no:
            widr_amt = float(input("Enter withdrawal amount: "))

            if widr_amt <= row[3]:
                updated_balance = row[3] - widr_amt
                cursor.execute(
                    "UPDATE bank_record SET balance = {} WHERE account_no = {}".format(updated_balance, acc_no)
                )
                cursor.execute(
                    "INSERT INTO transaction (sr, trans_type, amount, trns_date) VALUES ({}, 'Credit', {}, CURDATE())".format(row[0], widr_amt)
                )
                connection.commit()
                print("\n✅ Amount withdrawn successfully.")
                print("   Current balance: ₹", updated_balance)
                connection.close()
                return 1
            else:
                print("❌ Insufficient balance!")
                connection.close()
                return 0

    print("❌ Account number not found.")
    connection.close()
    return 0


# ──────────────────────────────────────────────

def transaction():
    """
    CUSTOMER | Transfer money between two accounts.
    """
    connection = get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute("SELECT * FROM bank_record")
    bank_data = cursor.fetchall()

    # ── Sender ──
    str_sender = input("Enter your account number: ")
    if not str_sender.isdigit():
        print("❌ Account number should be digits only.")
        connection.close()
        return 0
    sender_acc = int(str_sender)

    # ── Receiver ──
    str_receiver = input("Enter receiver account number: ")
    if not str_receiver.isdigit():
        print("❌ Account number should be digits only.")
        connection.close()
        return 0
    receiver_acc = int(str_receiver)

    # ── Find both accounts ──
    check = 0
    sender_idx = 0
    receiver_idx = 0

    for i in range(len(bank_data)):
        if sender_acc in bank_data[i]:
            check += 1
            sender_idx = i
        elif receiver_acc in bank_data[i]:
            check += 1
            receiver_idx = i
        if check == 2:
            break
    else:
        print("❌ One or both account numbers not found.")
        connection.close()
        return 0

    if check == 2:
        bal_amt = float(input("Enter amount to transfer: "))

        cursor.execute(
            "UPDATE bank_record SET balance = balance - {} WHERE account_no = {}".format(bal_amt, sender_acc)
        )
        cursor.execute(
            "UPDATE bank_record SET balance = balance + {} WHERE account_no = {}".format(bal_amt, receiver_acc)
        )
        sr_no = bank_data[sender_idx][0]
        cursor.execute(
            "INSERT INTO transaction (sr, trans_type, amount, trns_date) VALUES ({}, 'Transfer', {}, CURDATE())".format(sr_no, bal_amt)
        )
        connection.commit()

        print("\n✅ Transaction completed successfully.")
        print("   Your current balance: ₹", bank_data[sender_idx][3] - bal_amt)

    connection.close()
    return 1


# ══════════════════════════════════════════════
#  TRANSACTION VIEWER FUNCTIONS
# ══════════════════════════════════════════════

def show_tran():
    """
    ADMIN | Show all transactions across all accounts.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM transaction")
    bank_data = cursor.fetchall()

    print()
    print("  ID".ljust(8), "SR NO".ljust(11), "Transaction Type".ljust(23),
          "Amount".ljust(13), "Transaction Date")
    divider("-", 72)

    for row in bank_data:
        print("➤",
              str(row[0]).ljust(6),
              str(row[1]).ljust(11),
              str(row[2]).ljust(23),
              str(row[3]).ljust(13),
              str(row[4]))
        print()

    connection.close()


# ──────────────────────────────────────────────

def show_custran():
    """
    CUSTOMER | Show transaction history for a specific account.
    """
    str_accno = input("Enter account no: ")
    if not str_accno.isdigit():
        print("❌ Account number should be digits only.")
        return 0
    acc_no = int(str_accno)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM bank_record")
    bank_data = cursor.fetchall()

    sr_no = 0
    for data in bank_data:
        if data[1] == acc_no:
            sr_no = data[0]
            break
    else:
        print("❌ Account number not found.")
        connection.close()
        return 0

    cursor.execute("SELECT * FROM transaction WHERE sr = {}".format(sr_no))
    cust_data = cursor.fetchall()

    print()
    print("  ID".ljust(8), "SR NO".ljust(11), "Transaction Type".ljust(23),
          "Amount".ljust(13), "Transaction Date")
    divider("-", 72)

    for row in cust_data:
        print("➤",
              str(row[0]).ljust(6),
              str(row[1]).ljust(11),
              str(row[2]).ljust(23),
              str(row[3]).ljust(13),
              str(row[4]))
    print()

    connection.close()


# ══════════════════════════════════════════════
#  MENUS
# ══════════════════════════════════════════════

def admin_menu():
    """Display and handle the Admin menu."""
    choice = -1
    while choice != 0:
        print("\n" + "═" * 72)
        print("  " + " " * 20 + "W E L C O M E,  A D M I N")
        print("═" * 72)
        print("  1 : Create new customer record")
        print("  2 : Display all records")
        print("  3 : Search a customer record")
        print("  4 : Update a customer record")
        print("  5 : Delete a customer record")
        print("  6 : View all transactions")
        print("  0 : Exit")
        print("═" * 72)

        choice = int(input("  Enter your choice: "))

        if choice == 0:
            break
        elif choice == 1:
            y = 9
            while y != 1:
                y = write_data()
        elif choice == 2:
            read_data()
        elif choice == 3:
            search_data()
        elif choice == 4:
            c = 9
            while c != 1:
                c = update_data()
        elif choice == 5:
            del_data()
        elif choice == 6:
            show_tran()
        else:
            print("❌ Invalid choice. Please try again.")

        input("\n  Press Enter to continue...")


def customer_menu():
    """Display and handle the Customer menu."""
    choice = -1
    while choice != 0:
        print("\n" + "═" * 72)
        print("  " + " " * 18 + "W E L C O M E,  C U S T O M E R")
        print("═" * 72)
        print("  1 : View my account details")
        print("  2 : Open a new account")
        print("  3 : Deposit money")
        print("  4 : Withdraw money")
        print("  5 : Transfer money")
        print("  6 : View my transaction history")
        print("  0 : Exit")
        print("═" * 72)

        choice = int(input("  Enter your choice: "))

        if choice == 0:
            break
        elif choice == 1:
            search_data()
        elif choice == 2:
            y = 9
            while y != 1:
                y = add_data()
        elif choice == 3:
            deposite()
        elif choice == 4:
            withdrawal()
        elif choice == 5:
            y = 9
            while y != 1:
                y = transaction()
        elif choice == 6:
            show_custran()
        else:
            print("❌ Invalid choice. Please try again.")

        input("\n  Press Enter to continue...")


# ══════════════════════════════════════════════
#  MAIN ENTRY POINT
# ══════════════════════════════════════════════

def main():
    print("\n" + "═" * 40)
    print("  ●  BANK MANAGEMENT SYSTEM  ●")
    print("  A : Admin")
    print("  C : Customer")
    print("═" * 40)

    person = input("  Press A / C: ").strip()

    # ── ADMIN ──
    if person in ('A', 'a'):
        MAX_ATTEMPTS = 3
        count = 0

        while count < MAX_ATTEMPTS:
            password = input("\n  Enter admin password: ")
            if password == "****":       # ← Change to your admin password
                admin_menu()
                break
            else:
                count += 1
                remaining = MAX_ATTEMPTS - count
                if remaining > 0:
                    print(f"  ❌ Incorrect password. {remaining} attempt(s) remaining.")
                else:
                    print("  🔒 Too many failed attempts. Access denied.")

    # ── CUSTOMER ──
    elif person in ('C', 'c'):
        customer_menu()

    else:
        print("  ❌ Invalid option. Please choose A or C.")

    # ── EXIT ──
    print("\n" + " " * 18 + "─────────────")
    print(" " * 18 + "│  THANK YOU  │")
    print(" " * 18 + "─────────────\n")


if __name__ == "__main__":
    main()
