CREATE TABLE IF NOT EXISTS chatbot_sessions (
    user_id INT PRIMARY KEY,
    has_visited_dashboard TINYINT(1) NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chatbot_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_created (user_id, created_at)
);

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

ALTER TABLE chatbot_sessions
ADD CONSTRAINT fk_chatbot_sessions_user
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE chatbot_messages
ADD CONSTRAINT fk_chatbot_messages_user
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE user_preferences
ADD CONSTRAINT fk_user_preferences_user
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE
ON UPDATE CASCADE;
