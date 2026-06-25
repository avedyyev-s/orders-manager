CREATE TABLE orders(
    id SERIAL PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    price INTEGER NOT NULL
);