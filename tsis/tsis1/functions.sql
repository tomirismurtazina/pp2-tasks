CREATE OR REPLACE FUNCTION filter(pat text)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT contact.name, contact.phone FROM contacts contact
        WHERE contact.name ILIKE "%" || pat || "%" OR contact.phone ilike "%" || p || "%";
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION pagination(lim INT, off INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone FROM contacts LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
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
$$;