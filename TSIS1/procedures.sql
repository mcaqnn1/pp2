CREATE OR REPLACE PROCEDURE add_user(
    p_first_name varchar,
    p_last_name varchar,
    p_phone varchar,
    p_email varchar,
    p_birth date
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO users(first_name, last_name, phone_number, email, date_of_birth)
    VALUES (p_first_name, p_last_name, p_phone, p_email, p_birth);
END;
$$;