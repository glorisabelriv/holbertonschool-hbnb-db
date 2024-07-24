import sqlite3
import json
import uuid

connect = sqlite3.connect('instance/development.db')
cursor = connect.cursor()

with open('countries.json', 'r') as file:
    countries = json.load(file)

for country in countries:
    cursor.execute("SELECT * FROM country WHERE code=?", (country['code'],))
    data = cursor.fetchone()
    if data is None:
        countries_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO country (id, name, code) VALUES (?, ?, ?);",
            (countries_id, country['name'], country['code'])
        )

connect.commit()
cursor.close()
connect.close()
