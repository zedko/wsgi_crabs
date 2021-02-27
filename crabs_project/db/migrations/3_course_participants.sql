CREATE TABLE IF NOT EXISTS course_participants
(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
user_id INTEGER REFERENCES users(id),
course_id INTEGER REFERENCES courses(id)
);