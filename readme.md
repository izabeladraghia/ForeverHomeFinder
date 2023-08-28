# Forever Home Finder 🐕🏠

Forever Home Finder is a web application designed to help animals find their loving owners and have a forever home.

## Features 🌟

- **Animal Listings**: Browse through a list of animals with details and images;
- **Schedule Visits**: Users can request a visit for the animal they desire, based on availability, and an email will be sent to the owner of the website alerting him of this;
- **Add or Remove Animals**: Animals can be added or removed based on need;
- **Contact**: Users can fill a contact form and an email will be sent to the owner of the website;

## Getting Started 🚀

Follow these steps to get the web application running on your local machine:

### Prerequisites 📋

- Python (latest version recommended)
- Flask framework
- Flask-Mail for email functionalities
- MySQL Database

### Installation 🔧

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/izabeladraghia/ForeverHomeFinder.git
    cd foreverhomefinder

2. **Install Dependencies**:
    ```bash
    pip install Flask
    pip install Flask-Mail
    pip install pymysql
    pip install python-dotenv
    ```

3. **Add Credentials**:

   Set up the necessary credentials, for example:
   - `MAIL_USERNAME`: Email Address
   - `MAIL_PASSWORD`: Email Password
   - `DB_HOST`: Database Host
   - `DB_USER`: Database User
   - `DB_PASSWORD`: Database Password

4. **Create the database**:
    ```bash
    python database.py
    ```

5. **Run the Application**:
    ```bash
    python app.py
    ```

   The application should now be running at `http://127.0.0.1:5000/index`.
