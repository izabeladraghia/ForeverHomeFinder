from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from database import get_db_connection
import datetime

app = Flask(__name__)

# configuring mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'foreverhomefinder2023@gmail.com'
app.config['MAIL_PASSWORD'] = 'gccioxnkdhqunamy'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/animals')
def animals():
    connection = get_db_connection()
    cursor = connection.cursor()

    # getting all the animals
    cursor.execute("SELECT * FROM `foreverhomefinder`.`animals`")
    animals = cursor.fetchall()
    connection.close()

    return render_template('animals.html', animals=animals)

@app.route('/animal/<int:animal_id>', methods=['GET', 'POST'])
def animaldescription(animal_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # deleting visits from the past
    start_of_today = datetime.datetime.combine(datetime.date.today(), datetime.time())
    delete_query = "DELETE FROM Schedule WHERE VisitDateTime < %s"
    cursor.execute(delete_query, (start_of_today,))
    connection.commit()

    # adding schedule visit to the db
    if request.method == 'POST':
        selected_time = request.form.get('selected-time')
        cursor.execute("INSERT INTO Schedule (AnimalId, VisitDateTime) VALUES (%s, %s)", (animal_id, selected_time))
        connection.commit()

        # sending the email for new visit
        cursor.execute("SELECT * FROM `foreverhomefinder`.`animals` WHERE AnimalId=%s", (animal_id,))
        animal = cursor.fetchone()
        msg = Message('New Visit Scheduled', sender='youremail@gmail.com', recipients=['foreverhomefinder2023@gmail.com'])
        msg.body = f"A visit has been scheduled for {animal['AnimalName']} on {selected_time}"
        mail.send(msg)

    # getting anibal details
    cursor.execute("SELECT * FROM `foreverhomefinder`.`animals` WHERE AnimalId=%s", (animal_id,))
    animal = cursor.fetchone()

    # getting the available times for the visit dropdown
    available_times = get_available_times(animal_id)

    connection.close()
    
    # return animal or display error
    if animal:
        return render_template('animaldescription.html', animal=animal, available_times=available_times)
    else:
        return "Animal not found", 404

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add-animal', methods=['GET'])
def add_animal_page():
    return render_template('animaladd.html')

@app.route('/insert-animal', methods=['POST'])
def insert_animal():
    # getting info
    animalName = request.form.get('animalName')
    animalType = request.form.get('animalType')
    animalAge = request.form.get('animalAge')
    animalBreed = request.form.get('animalBreed')
    
    # handling the image
    image = request.files.get('animalImage')
    fileName = image.filename
    animalImage = fileName

    # inserting animal into database
    connection = get_db_connection()
    cursor = connection.cursor()

    animal_data = {
        'AnimalName': animalName,
        'AnimalType': animalType,
        'AnimalAge': animalAge,
        'AnimalBreed': animalBreed,
        'AnimalImage': animalImage
    }

    # inserting animal into db
    query = '''
        INSERT INTO Animals (AnimalName, AnimalType, AnimalAge, AnimalBreed, AnimalImage)
        VALUES (%(AnimalName)s, %(AnimalType)s, %(AnimalAge)s, %(AnimalBreed)s, %(AnimalImage)s)
    '''
    
    cursor.execute(query, animal_data)
    connection.commit()
    connection.close()

    return redirect(url_for('animals'))

@app.route('/animal/<int:animal_id>/delete', methods=['POST'])
def delete_animal(animal_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # deleting animal from db
    cursor.execute("DELETE FROM `foreverhomefinder`.`animals` WHERE AnimalId=%s", (animal_id,))
    
    connection.commit()
    connection.close()
    
    return redirect(url_for('animals'))

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    # getting data from form
    full_name = request.form.get('name')
    email = request.form.get('email')
    message_content = request.form.get('message')

    # sending email
    msg = Message('New Contact Message', sender=email, recipients=['foreverhomefinder2023@gmail.com'])
    msg.body = f"From: {full_name} ({email})\n\n{message_content}"
    mail.send(msg)
    
    return redirect(url_for('contact', message='sent'))

def get_available_times(animal_id):

    # getting the weekdays
    today = datetime.date.today()
    next_week = today + datetime.timedelta(weeks=1)
    weekdays = [today + datetime.timedelta(days=i) for i in range((next_week-today).days) if (today + datetime.timedelta(days=i)).weekday() < 5]
    
    # getting the hours
    available_times = []
    for day in weekdays:
        for hour in range(9, 17):
            available_times.append(datetime.datetime.combine(day, datetime.time(hour, 0)))
    
    connection = get_db_connection()
    cursor = connection.cursor()

    # getting already booked hours
    cursor.execute("SELECT VisitDateTime FROM Schedule WHERE AnimalId=%s", (animal_id,))
    booked_times = [item['VisitDateTime'] for item in cursor.fetchall()]

    # removing already booked hours
    for booked in booked_times:
        if booked in available_times:
            available_times.remove(booked)
    
    connection.close()

    return available_times

if __name__ == "__main__":
    app.run(debug=True)
