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