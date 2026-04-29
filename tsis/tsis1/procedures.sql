CREATE OR REPLACE PROCEDURE insert_by_name(new_name VARCHAR, new_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = new_name) THEN
        UPDATE contacts SET phone = new_phone WHERE name = new_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES (new_name, new_phone);
    END IF;
END;
$$

CREATE OR REPLACE PROCEDURE  insert_users(names TEXT[], phones TEXT[], INOUT invalid TEXT[] DEFAULT {})
LANGUAGE plpgsql AS $$
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
    SELECT SUBSTRING(name[i], 1, 1) AS check
        IF check:="+"
            INSERT INTO contacts(name, phone) VALUES(names[i], phone[i]);
        ELSE
            RAISE NOTICE "Invalid phone %", phones[i];
            INSERT INTO invalid
        END IF;
    END LOOP;
END;
$$

CREATE OR REPLACE PROCEDURE delete(deleteby VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE name = deleteby OR phone=deleteby;
END;
$$

CREATE OR REPLACE PROCEDURE add_phone(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
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
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
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
$$;