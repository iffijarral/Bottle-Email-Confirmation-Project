PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS users;
 
CREATE TABLE users(
    user_pk                 TEXT,
    user_name               TEXT,    
    user_email              TEXT UNIQUE,
    user_password           TEXT,
    user_verification_key   TEXT,
    is_verified             INTEGER,
    user_created_at         INTEGER,
    user_updated_at         TEXT, 
    PRIMARY KEY(user_pk)
) WITHOUT ROWID;

SELECT * FROM users;