CREATE OR REPLACE PROCEDURE insert_by_name(new_name VARCHAR, new_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = new_name) THEN
        UPDDATE contacts SET phone = new_phone WHERE name = new_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES (new-name, new_phone);
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