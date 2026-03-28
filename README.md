<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,50:16213e,100:0f3460&height=200&section=header&text=Bank%20Management%20System&fontSize=42&fontColor=e94560&fontAlignY=38&desc=Python%20%2B%20MySQL%20%C2%B7%20Class%2012%20Project%20%C2%B7%20Terminal-Based&descAlignY=58&descSize=16&descColor=ffffff" width="100%"/>

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/>
  <img src="https://img.shields.io/badge/mysql--connector-Python-00758F?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Project-Class%2012%20CSE-e94560?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Interface-Terminal-333333?style=for-the-badge&logo=windowsterminal&logoColor=white"/>
</p>

<br/>

> *My first real project — built in Class 12 as part of my Computer Science coursework.*
> *It taught me how databases actually work, how to connect Python to MySQL,*
> *and how to think about real-world systems like banking.*

</div>

---

## 💡 About This Project

This is a **terminal-based Bank Management System** built using **Python and MySQL**, developed during my Class 12 Computer Science project. It simulates a real banking environment where both **Admins** and **Customers** can log in and perform their respective operations — all powered by a live MySQL database running in the background.

No fancy UI. No frameworks. Just pure Python logic, SQL queries, and a lot of learning. 🚀

---

## 👥 Two-Role System

The system supports two types of users — each with their own menu and set of operations:

### 🔐 Admin Panel *(Password Protected)*
| # | Operation |
|---|---|
| 1 | Create new customer records (with loop to add multiple) |
| 2 | Display all customer records in a formatted table |
| 3 | Search a specific customer by account number |
| 4 | Update customer details (name, balance, address, phone) |
| 5 | Delete a customer account |
| 6 | View all transactions across all accounts |

### 👤 Customer Panel
| # | Operation |
|---|---|
| 1 | View personal account details |
| 2 | Open a new bank account |
| 3 | Deposit money |
| 4 | Withdraw money |
| 5 | Transfer money to another account |
| 6 | View personal transaction history |

---

## ✨ Features

- **Dual Role Login** — Admin (password protected) and Customer modes
- **Admin brute-force protection** — locks out after 3 wrong password attempts
- **Full CRUD operations** on bank records via MySQL
- **Live transaction logging** — every deposit, withdrawal, transfer, creation, and deletion is recorded with date
- **Money Transfer** between two accounts with real-time balance update
- **Input validation** — account numbers, phone numbers, and amounts are all validated before processing
- **Formatted terminal tables** for displaying records and transactions
- **Account types** — supports both Current and Savings accounts

---

## 🗄️ Database Schema

Two tables power this entire system:

```sql
-- Stores all customer/account information
CREATE TABLE bank_record (
    SR_NO        INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    ACCOUNT_NO   BIGINT,
    CUSTOMER_NAME VARCHAR(20),
    BALANCE      REAL,
    ACCOUNT_TYPE VARCHAR(10),
    ADDRESS      VARCHAR(50),
    PHONE_NO     VARCHAR(10)
);

-- Logs every transaction with a foreign key to bank_record
CREATE TABLE transaction (
    ID         INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    SR         INT,
    TRANS_TYPE VARCHAR(35),
    AMOUNT     INT,
    TRANS_DATE DATE,
    FOREIGN KEY (SR) REFERENCES bank_record(SR_NO)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

---

## 🏗️ How It Works

```
Program Starts
      │
      ▼
 ┌────────────┐
 │ ADMIN / C  │  ← User selects role
 └────────────┘
      │
      ├──── ADMIN ──── Password Check (3 attempts max)
      │                     │
      │              ┌──────▼──────────────────┐
      │              │  Admin Menu (6 options)  │
      │              │  Create / Read / Search  │
      │              │  Update / Delete / Txns  │
      │              └─────────────────────────-┘
      │
      └──── CUSTOMER ──── No password needed
                               │
                        ┌──────▼──────────────────────┐
                        │  Customer Menu (6 options)   │
                        │  View / Open / Deposit /     │
                        │  Withdraw / Transfer / Txns  │
                        └─────────────────────────────-┘

All operations → MySQL (bank_db) → Commits & Closes connection
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.x installed
- MySQL Server installed and running
- `mysql-connector-python` library

### 1. Install the required library
```bash
pip install mysql-connector-python
```

### 2. Set up the MySQL database
Open MySQL and run:
```sql
CREATE DATABASE bank_db;
USE bank_db;

CREATE TABLE bank_record (
    SR_NO INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    ACCOUNT_NO BIGINT,
    CUSTOMER_NAME VARCHAR(20),
    BALANCE REAL,
    ACCOUNT_TYPE VARCHAR(10),
    ADDRESS VARCHAR(50),
    PHONE_NO VARCHAR(10)
);

CREATE TABLE transaction (
    ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    SR INT,
    TRANS_TYPE VARCHAR(35),
    AMOUNT INT,
    TRANS_DATE DATE,
    FOREIGN KEY (SR) REFERENCES bank_record(SR_NO)
    ON DELETE CASCADE ON UPDATE CASCADE
);
```

### 3. Update your MySQL credentials
Open `bank_management.py` and update these lines with your MySQL username and password:
```python
connection = mysql.connect(
    host="localhost",
    user="root",       # ← your MySQL username
    passwd="****",     # ← your MySQL password
    database="bank_db"
)
```

### 4. Run the program
```bash
python bank_management.py
```

---

## 🖥️ Sample Terminal Output

```
===============================
|| ● Are you ADMIN/CUSTOMER ● ||
|| press A:for ADMIN           ||
|| press C:for CUSTOMER        ||
===============================
Press A/C:- A

Enter your password: ****

# # # # # # # # # # # # # # # #
#         'WELCOME'            #
# ● Press 1: Create record     #
# ● Press 2: Display all       #
# ● Press 3: Search record     #
# ● Press 4: Update record     #
# ● Press 5: Delete record     #
# ● Press 6: All transactions  #
# ● Press 0: Exit              #
# # # # # # # # # # # # # # # #
```

---

## 🧠 What I Learned

This project was my first real hands-on experience with:

- Connecting **Python to a live MySQL database** using `mysql-connector`
- Writing **raw SQL queries** (INSERT, SELECT, UPDATE, DELETE) from Python
- Designing a **relational database** with foreign keys and cascading rules
- Building **input validation** and **error handling** from scratch
- Thinking about **real-world systems** — roles, permissions, transaction logs
- Structuring a large Python program with **multiple functions**

---

## 📁 Project Structure

```
Bank-Management-System/
│
├── bank_management.py     # 🐍 Main Python file — all logic lives here
└── README.md
```

---

## ⚠️ Note

> This project was built for **educational purposes** as a Class 12 CS project.
> The admin password is hardcoded for simplicity — in a real-world system,
> passwords would be hashed and stored securely in a database.

---

## 👨‍💻 Author

<div align="center">

**Prerit Arya**
B.Tech Computer Science & Engineering

*This project was built when I was in Class 12 — one of my first steps into the world of real programming. It may not be perfect, but it started everything.* 🙌

[![GitHub](https://img.shields.io/badge/GitHub-PRERITARYA-181717?style=for-the-badge&logo=github)](https://github.com/PRERITARYA)

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f3460,50:16213e,100:1a1a2e&height=120&section=footer" width="100%"/>

**⭐ If this helped you understand Python + MySQL projects, drop a star!**

*Built with curiosity, Stack Overflow, and a lot of trial & error. 😄*

</div>
