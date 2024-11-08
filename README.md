# Web Hosting Service Application

This is a web application that allows users to purchase hosting services for their websites and applications. The project is built using Python and Flask and provides functionalities for user management, service management, and transaction processing.

## Features

- User registration and login
- Viewing and purchasing hosting plans
- Managing purchased services
- Processing payments and generating invoices
- Developer console for managing class instances

## Technologies Used

- Python
- Flask
- SQLAlchemy (ORM)
- SQLite (for development)
- HTML/CSS for frontend

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- sudo apt-get install pkg-config libmysqlclient-dev

### Clone the Repository

```bash
git clone https://github.com/JoanWaithira/SiteSwift.git
cd SiteSwift
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Database Setup

### Initialize the Database

Run the following commands to initialize the database:

```bash
flask db init
flask db migrate
flask db upgrade
```

## Running the Application
gunicorn -b 127.0.0.1:5001 web_dynamic.app:app
gunicorn -b 127.0.0.1:5001 api.v1.app:app

### Start the Development Server

```bash
flask run
```

Open your web browser and go to `http://127.0.0.1:5000/` to see the application running.

## Developer Console

A developer console is provided to manage class instances interactively. You can create, update, delete, and search for instances of the `User` class.

### Running the Developer Console

```bash
python console.py
```

### Console Commands

- `create User username email`: Create a new User instance.
- `update User id attribute=value`: Update an attribute of a User instance.
- `destroy User id`: Delete a User instance.
- `search User`: List all User instances.
- `search_id User id`: Search for a User instance by ID.
- `show_all`: Show all instances of all classes.
- `exit`: Exit the developer console.

## Project Structure

```
SiteSwift/
│
├── app.py                  # Main application file
├── dev_console.py          # Developer console script
├── models                  # Database models
├── requirements.txt        # Project dependencies
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── migrations/             # Database migration files
├── README.md               # Project README
└── config.py               # Configuration file
```

## Contribution

Contributions are welcome! Please create an issue or submit a pull request for any improvements or new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Flask for the web framework
- SQLAlchemy for ORM
- Bootstrap for the frontend framework
```
