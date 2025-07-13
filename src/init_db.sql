CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY, 
    role_name VARCHAR(20) UNIQUE
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY, 
    first_name VARCHAR(20), 
    last_name VARCHAR(20), 
    email VARCHAR(40) UNIQUE NOT NULL, 
    hashed_password VARCHAR(255) NOT NULL, 
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

INSERT INTO users (first_name, last_name, email, hashed_password, role_id) VALUES 
    ('admin', 'admin', 'admin@gmail.com', 'pbkdf2:sha256:1000000$LuQuSLWArUV5KcIV$f72f7b6f3e5ca84886f5ee1f671ea2574e5d9ad10b2159f3381e21537df2f07f', 2),
    ('customer', 'customer', 'customer@gmail.com', 'pbkdf2:sha256:1000000$LuQuSLWArUV5KcIV$f72f7b6f3e5ca84886f5ee1f671ea2574e5d9ad10b2159f3381e21537df2f07f', 1);

INSERT INTO countries (country_name) VALUES 
    ('צרפת'), ('ספרד'), ('ארצות הברית'), ('סין'), ('איטליה'), 
    ('תאילנד'), ('גרמניה'), ('בריטניה'), ('יפן'), ('אוסטריה'), 
    ('יוון'), ('אוסטרליה'), ('פורטוגל'), ('הולנד');

INSERT INTO vacations (country_id, vacation_info, vacation_start_date, vacation_end_date, price, photo_file_path) VALUES 
    (1, 'רומנטיקה, יין ונופים עוצרי נשימה בלב צרפת', '2025-10-03', '2025-10-11', 3452, 'france.jpg'),
    (2, 'קסם ספרדי עם שמש, טאפס וחוויות בלתי נשכחות', '2025-10-25', '2025-10-30', 2530, 'spain.jpg'),
    (3, 'הרפתקה אמריקאית עם ערים נוצצות ונופים עוצרי נשימה', '2025-11-04', '2025-11-18', 5436, 'usa.jpg'),
    (4, 'מסע קסום בסין עם תרבות, טבע ואוכל אותנטי', '2025-09-12', '2025-09-25', 6790, 'china.jpg'),
    (5, 'סמטאות רומנטיות, פסטה ונופים קסומים', '2025-09-15', '2025-09-21', 1542, 'italy.jpg'),
    (6, 'חופים לבנים, תרבות צבעונית והרפתקאות טרופיות', '2026-01-03', '2026-01-22', 5470, 'thailand.jpg'),
    (7, 'היסטוריה מרתקת, ערים מודרניות ונופים ירוקים', '2025-12-04', '2025-12-10', 1467, 'germany.jpg'),
    (8, 'היסטוריה עשירה, ערים תוססות וטבע עוצר נשימה', '2025-12-21', '2025-12-29', 5290, 'united_kingdom.jpg'),
    (9, 'מסע קסום בין מסורות עתיקות לטכנולוגיה מודרנית', '2025-09-02', '2025-09-14', 4879, 'japan.jpg'),
    (10, 'נופים עוצרי נשימה, הרים ירוקים ותרבות אירופית מקסימה', '2025-11-07', '2025-11-12', 1468, 'austria.jpg'),
    (11, 'חופים כחולים, הרים מרהיבים, וטעמים יווניים אותנטיים', '2025-08-28', '2025-09-03', 1420, 'greece.jpg'),
    (12, 'מסעות טבע מרתקים והרפתקאות קסומות לאורך חופים יפהפיים', '2025-11-06', '2025-11-18', 2690, 'australia.jpg'),
    (13, 'חופים זהובים, ערים צבעוניות ותרבות עשירה בלב ים התיכון', '2025-12-05', '2025-12-19', 1546, 'portugal.jpg');