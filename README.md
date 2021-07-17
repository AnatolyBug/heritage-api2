## Heritage Backend

This is the backend of the Heritage web app.

### Installation

```command
    git clone https://github.com/AnatolyBug/heritage-api2.git
    pip3 install -r requirements.txt
```

### Create DB

```command
    python3 manaage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser
```

### Run

```command
    python3 manage.py runserver
```