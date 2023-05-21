--CREATE A TABLE IF IT DOESN'T EXIST
CREATE TABLE IF NOT EXISTS cars (
         id SERIAL PRIMARY KEY,
        name TEXT,
        price TEXT,
        year TEXT,
        mileage TEXT,
        engine_size TEXT,
         fuel_type TEXT
    );

