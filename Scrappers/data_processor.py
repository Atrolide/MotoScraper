def preprocess_data(ad_data):
    data = []

    for item in ad_data:
        if all(value is not None for value in item):
            brand = item[0]
            model = item[1]
            year = item[2]
            mileage = item[3]
            engine_size = item[4]
            fuel_type = item[5]
            horse_power = item[6]
            data.append((brand, model, year, mileage, engine_size, fuel_type, horse_power))

    return data