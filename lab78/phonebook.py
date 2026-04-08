import psycopg2
import csv

conn = psycopg2.connect("host='localhost' dbname='postgres' user='postgres' password='1234' port=5432")
def create_table():
    cur=conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(20) NOT NULL
            )""")

    conn.commit()
    cur.close()

def insert_csv():
    cur=conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as f:
        data=csv.reader(f)
        next(data)
        for row in data:
            cur.execute("INSERT INTO contacts(name, phone) VALUES(%s, %s)", row)

    conn.commit()
    cur.close()

    print("Contacts inserted from contacts.csv")
    
def insert_terminal():
    cur=conn.cursor()
    name=input("Name: ")
    phone=input("Number: ")
    cur.execute("INSERT INTO contacts(name, phone) VALUES(%s, %s)", (name, phone))

    conn.commit()
    cur.close()

    print(f"Added {name}'s contact")

def edit_contact():
    cur=conn.cursor()
    com=input("type 1 to select by name, 2 to select by phone: ")

    if com == "1":
        name=input("Type the name of the contact to edit: ")
        newphone=input("Type new phone: ")
        cur.execute("UPDATE contacts SET phone=%s WHERE name=%s", (newphone, name))

        conn.commit()
        cur.close()

        print("Updated contact")
    
    elif com == "2":
        phone=input("Type the phone of the contact to edit: ")
        newname=input("Type the new name for the contact: ")
        cur.execute("UPDATE contacts SET name=%s WHERE phone=%s", (newname, phone))

        conn.commit()
        cur.close()

        print("Updated contact")
    
    else:
        print("Invalid command")


def delete():
    cur=conn.cursor()

    com=input("Type 1 to delete by name, type 2 to delete by phone: ")
    if com == "1":
        name=input("Type name of the contact: ")
        cur.execute("DELETE FROM contacts WHERE name=%s", (name,))
        print(f"Deleted {name} contact")

    elif com == "2":
        phone=input("Type phone to delete: ")
        cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))
        print(f"Deleted {phone} contact")

    else:
        print("Invalid command")
    
    conn.commit()
    cur.close()

def filter():
    pattern=input("Type the pattern to filter by: ")
    pat=f"%{pattern}%"
    cur=conn.cursor()
    cur.execute("SELECT * FROM contacts WHERE name ILIKE %s OR phone ILIKE %s", (pat, pat))

    filtered=cur.fetchall()
    if filtered:
        for row in filtered:
            print(row[0], row[1], row[2])
    
    cur.close()

def main():
    create_table()

    while True:
        print("\n--- PhoneBook ---")
        print("1. Insert contacts from CSV")
        print("2. Insert contacts from terminal")
        print("3. Edit contact")
        print("4. Delete contact")
        print("5. Filter contacts")
        print("6. Exit")
        
        com=input("Choose the command: ")
        if com == "1":
            insert_csv()
        elif com == "2":
            insert_terminal()
        elif com == "3":
            edit_contact()
        elif com == "4":
            delete()
        elif com == "5":
            filter()
        elif com == "6":
            break
        else:
            print("Invalid command")

    conn.close()

if __name__=="__main__":
    main()