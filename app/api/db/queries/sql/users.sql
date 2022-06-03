
-- name: create-new-user<!
INSERT INTO users (username, email, password, token_api)
VALUES (:username, :email, :password, :token_api)
RETURNING
    id, created_at, updated_at;

-- name: select-user-by-teacher-code
SELECT * FROM users WHERE email = :email
