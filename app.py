from flask import Flask, render_template
import pymysql

app = Flask(__name__)

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '+Dumitru01',
    'cursorclass': pymysql.cursors.DictCursor
}

def ensure_database():
    connection = pymysql.connect(**DATABASE_CONFIG)
    cursor = connection.cursor()
    
    cursor.execute('CREATE DATABASE IF NOT EXISTS ForeverHomeFinder')
    
    connection.close()

def get_db_connection():
    db_config = DATABASE_CONFIG.copy()
    db_config['database'] = 'ForeverHomeFinder'
    connection = pymysql.connect(**db_config)
    return connection

def ensure_table():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Animals (
            AnimalId INT AUTO_INCREMENT PRIMARY KEY,
            AnimalName VARCHAR(255),
            AnimalType VARCHAR(255),
            AnimalAge INT,
            AnimalBreed VARCHAR(255),
            AnimalImage VARCHAR(1024)
        )
    ''')
    
    connection.commit()
    connection.close()

def add_animal():
    connection = get_db_connection()
    cursor = connection.cursor()

    animal_data = {
        'AnimalId': 10,
        'AnimalName': 'Sili',
        'AnimalType': 'Cat',
        'AnimalAge': 9,
        'AnimalBreed': 'Orange Tabby',
        'AnimalImage': r'10.jpg'
    }

    query = '''
        INSERT INTO Animals (AnimalId, AnimalName, AnimalType, AnimalAge, AnimalBreed, AnimalImage)
        VALUES (%(AnimalId)s, %(AnimalName)s, %(AnimalType)s, %(AnimalAge)s, %(AnimalBreed)s, %(AnimalImage)s)
        ON DUPLICATE KEY UPDATE
        AnimalName = VALUES(AnimalName),
        AnimalType = VALUES(AnimalType),
        AnimalAge = VALUES(AnimalAge),
        AnimalBreed = VALUES(AnimalBreed),
        AnimalImage = VALUES(AnimalImage)
    '''
    
    cursor.execute(query, animal_data)
    connection.commit()
    connection.close()

ensure_database()
ensure_table()
add_animal()

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/animals')
def animals():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM `foreverhomefinder`.`animals`")
    animals = cursor.fetchall()

    print(animals)

    connection.close()
    
    return render_template('animals.html', animals=animals)

@app.route('/animal/<int:animal_id>')
def animaldescription(animal_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM `foreverhomefinder`.`animals` WHERE AnimalId=%s", (animal_id,))
    animal = cursor.fetchone()

    connection.close()
    
    if animal:
        return render_template('animaldescription.html', animal=animal)
    else:
        return "Animal not found", 404


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
