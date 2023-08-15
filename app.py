from flask import Flask, render_template
import pymysql

app = Flask(__name__)

def get_db_connection():
    connection = pymysql.connect(host='your_host',
                                 user='your_user',
                                 password='your_password',
                                 database='your_database',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

@app.route('/animals')
def animals():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetching all animals from the Animals table
    cursor.execute("SELECT * FROM Animals")
    animals = cursor.fetchall()

    connection.close()
    
    return render_template('animals.html', animals=animals)

if __name__ == "__main__":
    app.run(debug=True)
