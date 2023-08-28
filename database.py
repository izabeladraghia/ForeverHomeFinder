import pymysql

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '+Dumitru01',
    'cursorclass': pymysql.cursors.DictCursor
}

def ensure_database():
    connection = pymysql.connect(**DATABASE_CONFIG)
    cursor = connection.cursor()
    
    # creating database if it doesn't exist
    cursor.execute('CREATE DATABASE IF NOT EXISTS ForeverHomeFinder')
    connection.close()

def get_db_connection():
    db_config = DATABASE_CONFIG.copy()
    db_config['database'] = 'ForeverHomeFinder'
    connection = pymysql.connect(**db_config)
    return connection

def ensure_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    # creating Animals and Shcedule table if they don't already exist
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Schedule (
            ScheduleId INT AUTO_INCREMENT PRIMARY KEY,
            AnimalId INT,
            VisitDateTime DATETIME,
            FOREIGN KEY (AnimalId) REFERENCES Animals(AnimalId)
        )
    ''')
    
    connection.commit()
    connection.close()

if __name__ == "__main__":
    ensure_database()
    ensure_tables()
