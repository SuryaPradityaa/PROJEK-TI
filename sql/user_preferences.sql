CREATE TABLE IF NOT EXISTS user_preferences (
    user_id INT PRIMARY KEY,
    age_range VARCHAR(50) NULL,
    hobbies TEXT NULL,
    mood_preferences TEXT NULL,
    budget_level VARCHAR(30) NULL,
    trip_type VARCHAR(30) NULL,
    mobility_level VARCHAR(30) NULL,
    preferred_locations TEXT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

ALTER TABLE user_preferences
ADD CONSTRAINT fk_user_preferences_user
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE
ON UPDATE CASCADE;
