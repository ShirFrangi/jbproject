CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY, 
    role_name VARCHAR(20) UNIQUE
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY, 
    first_name VARCHAR(20), 
    last_name VARCHAR(20), 
    email VARCHAR(40) UNIQUE NOT NULL, 
    password VARCHAR(20) NOT NULL, 
    role_id INT NOT NULL, 
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY, 
    country_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE vacations (
    vacation_id SERIAL PRIMARY KEY, 
    country_id INT NOT NULL,
    vacation_info VARCHAR(1000), 
    vacation_start_date DATE, 
    vacation_end_date DATE, 
    price INT NOT NULL, 
    photo_file_path VARCHAR(1000),
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

CREATE TABLE likes (
    like_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    vacation_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE, 
    FOREIGN KEY (vacation_id) REFERENCES vacations(vacation_id) ON DELETE CASCADE
);

INSERT INTO roles (role_name) VALUES 
    ('user'), 
    ('admin');

INSERT INTO users (first_name, last_name, email, password, role_id) VALUES 
    ('Shir', 'Frangi', 'shir@gmail.com', '1234', 2), 
    ('Test', 'Test', 'test@gmail.com', '1234', 1);

INSERT INTO countries (country_name) VALUES 
    ('France'), ('Spain'), ('United States'), ('China'), ('Italy'), 
    ('Thailand'), ('Germany'), ('United Kingdom'), ('Japan'), ('Austria'), 
    ('Greece'), ('Australia'), ('Portugal'), ('Netherlands');

INSERT INTO vacations (country_id, vacation_info, vacation_start_date, vacation_end_date, price, photo_file_path) VALUES 
    (1, 'A magical experience that offers a blend of rich culture, historical landmarks, exquisite food, and streets filled with romantic charm.', '2025-10-03', '2025-10-11', 3452, NULL),
    (2, 'A vacation in Madrid offers the perfect blend of culture, vibrant nightlife, excellent food, and a warm and inviting urban atmosphere.', '2025-10-25', '2025-10-30', 2530, NULL),
    (3, 'The United States offers a variety of experiences that include diverse cultures, dynamic cities, breathtaking natural landscapes, and attractions for every taste and interest.', '2025-11-04', '2025-11-18', 5436, NULL),
    (4, 'A stunning blend of ancient history, rich cultures, breathtaking natural landscapes, and rapidly developing modern cities.', '2025-09-12', '2025-09-25', 6790, NULL),
    (5, 'Rome offers a stunning blend of ancient history, amazing architecture, rich culture, and a magical atmosphere that makes you feel like you have stepped back in time.', '2025-09-15', '2025-09-21', 542, NULL),
    (6, 'Thailand offers the perfect blend of magical tropical beaches, rich culture, stunning temples, and delicious street food.', '2026-01-03', '2026-01-22', 5470, NULL),
    (7, 'Germany offers an experience that blends fascinating history, picturesque villages, vibrant cities with contemporary architecture, and magical natural landscapes.', '2025-12-04', '2025-12-10', 467, NULL),
    (8, 'A magical Christmas vacation in beautiful London offers a blend of sparkling lights, festive markets, and a holiday atmosphere that fills the city with charm and joy.', '2025-12-21', '2025-12-29', 5290, NULL),
    (9, 'Japan offers a stunning blend of ancient tradition and technological innovation, with breathtaking natural landscapes, traditional temples, advanced cities, and exceptional Japanese cuisine.', '2025-09-02', '2025-09-14', 4879, NULL),
    (10, 'Austria offers unforgettable experiences with stunning mountain landscapes, charming cities, rich culture, and classical music that has left its mark on history.', '2025-11-07', '2025-11-12', 468, NULL),
    (11, 'Greece offers the perfect blend of magical beaches, stunning archaeological sites, rich culture, and excellent traditional food.', '2025-08-28', '2025-09-03', 420, NULL),
    (12, 'Australia offers a unique blend of breathtaking nature, tropical beaches, vibrant cities, and a variety of local cultures.', '2025-11-06', '2025-11-18', 2690, NULL),
    (13, 'Portugal offers a unique experience with peaceful beaches, picturesque villages, stunning landscapes, and a relaxed atmosphere perfect for any type of vacation.', '2025-12-05', '2025-12-19', 1546, NULL);