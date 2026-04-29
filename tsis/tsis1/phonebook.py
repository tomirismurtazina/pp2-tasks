import psycopg2
import csv
import json

query = """CREATE OR REPLACE PROCEDURE add_phone(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    IF p_type NOT IN ("home", "work", "mobile") THEN
        PAISE EXCEPTION "Invalid phone";
    END IF;

    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION "contact not found";
    END IF

    INSERT INTO phones(contact_id, phone, type) VALUES (v_contact_id, p_phone, p_type)
END;
$$;"""

query1 = """CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR, 
    p_group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
    v_contact_id INT;
BEGIN
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name) RETURNING id INTO v_group_id;
        RAISE NOTICE "Created new group: %", p_group_name;
    END IF;
    
    SELECT id INTO v_contact_id FROM contacts WHERE username = p_contact_name;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION "Contact % not found", p_contact_name;
    END IF;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;"""

query2 = """CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INT,
            username VARCHAR,
            email VARCHAR,
            birthday DATE,
            group_name VARCHAR,
            phone VARCHAR,
            phone_type VARCHAR)
LANGUAGE pl AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.id, c.username, c.email, c.birthday, g.name AS group_name, p.phone, p.type AS phone_type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE 
        c.username ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'
    ORDER BY c.username;
END;
$$;"""

query3 = """CREATE OR REPLACE FUNCTION pagination(lim INT, off INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone FROM contacts LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql"""

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

def alter():
    cur = conn.cursor()

    cur.execute("""CREATE TABLE groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
    );

    ALTER TABLE contacts
        ADD COLUMN email    VARCHAR(100),
        ADD COLUMN birthday DATE,
        ADD COLUMN group_id INTEGER REFERENCES groups(id);

    CREATE TABLE phones (
        id         SERIAL PRIMARY KEY,
        contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
        phone      VARCHAR(20)  NOT NULL,
        type       VARCHAR(10)  CHECK (type IN ('home', 'work', 'mobile'))
    );""")
    conn.commit()
    cur.close()

def insert_csv():
    cur=conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as f:
        data=csv.reader(f)
        next(data)
        for row in data:
            cur.execute("INSERT INTO contacts(name, phone, email, birthday, group_id) VALUES(%s, %s, %s, %s, %s)", row)

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

def execute(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def filter_by_group():
    with conn.cursor as cur:
        group = input("select group to show ")
        cur.execute("SELECT * FROM CONTACTS WHERE group_id=%s", (group))

        filtered=cur.fetchall
        if filtered:
            for row in filtered:
                print(row)

def search_by_email():
    with conn.cursor as cur:
        pattern = input()
        sort_by = input()
        pat=f"%{pattern}%"
        cur.execute(f"SELECT * FROM contacts WHERE email ILIKE %s ORDER BY {sort_by}", (pat))
        match = cur.fetchall
        if match:
            for row in match:
                print(row)

def view_paginated():
    limit  = int(input("Contacts per page(limit): ").strip())
    offset = int(input("Skip (offset): ").strip())
    
    while True:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
                rows = cur.fetchall()
        
            if not rows:
                print("No more contacts.")
                break
            
            print(f"\n--- Page {offset//limit + 1} ---")
            for row in rows:
                print(row)
        
            print("\nOptions: [n]ext, [p]rev, [q]uit")
            choice = input("Choice: ").strip().lower()
        
            if choice == 'n':
                offset += limit
            elif choice == 'p':
                offset = max(0, offset - limit)
            elif choice == 'q':
                break

def export():
    with conn.cursor as cur:
        cur.execute("SELECT * FROM contacts")
        all = cur.fetchall
        contacts = []
        for row in all:
            contact_id, username, email, birthday, group_name = row
                
            cur.execute("""
                SELECT phone, type FROM phones WHERE contact_id = %s
            """, (contact_id,))
            phones_rows = cur.fetchall()
                
            contact_data = {
                "username": username,
                "email": email,
                "birthday": str(birthday) if birthday else None,
                "group": group_name,
                "phones": [{'phone': p[0], 'type': p[1]} for p in phones_rows]
                }
            contacts.append(contact_data)
    
    with open("contacts.json", "w", encoding = "utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

def import_json():
    filename = input("Enter filename (e.g., contacts.json): ").strip()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return
    
    for contact in contacts:
        username = contact['username']
        email = contact.get('email')
        birthday = contact.get('birthday')
        group_name = contact.get('group', 'Other')
        phones = contact.get('phones', [])
        
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
            existing = cur.fetchone()
        
        if existing:
            action = input(f"Contact '{username}' exists. [s]kip or [o]verwrite? ").strip().lower()
            if action != 'o':
                continue
        
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s, %s, %s)", 
                (username, email, birthday, group_name))

        for phone_data in phones:
            with conn.cursor() as cur:
                cur.execute("CALL add_phone(%s, %s, %s)", 
                            (username, phone_data['phone'], phone_data['type']))

def main():
    create_table()
    alter()

    while True:
        print("\n--- PhoneBook ---")
        print("1. Insert contacts from CSV")
        print("2. search by email")
        print("3. Edit contact")
        print("4. Delete contact")
        print("5. Filter contacts")
        print("6. Exit")
        print("7. procedures and functions")
        print("8. import json")
        print("9 export json")
        print("0. filter by group")

        
        com=input("Choose the command: ")
        if com == "1":
            insert_csv()
        elif com == "2":
            search_by_email()
        elif com == "3":
            edit_contact()
        elif com == "4":
            delete()
        elif com == "5":
            filter()
        elif com == "6":
            break
        elif com == "7":
            execute(query)
            execute(query1)
            execute(query2)
            execute(query3)
            view_paginated()
        elif com == "8":
            import_json()
        elif com == "9":
            export()
        elif com == "0":
            filter_by_group()
        else:
            print("Invalid command")

    conn.close()

if __name__=="__main__":
    main()