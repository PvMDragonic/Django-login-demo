<div align="center">
   <h1 align="center">Django login system</h1>
   <p>This is a somewhat simple login system made entirely with Django on both front- and back-ends.</p>
   <img src="https://github.com/user-attachments/assets/b7388fda-5d69-4b57-acdc-daf3e431859f" alt="Django-login-demo landing page" height="420"/>
</div>

## Key Features
* Minimalistic visual theme;
* User creation;
* User email validation;
* User password change;
* User login;
* Login validation;
* Logged-in dashboard;
* Account logoff;
* Account "deletion" (invalidation)

## Installation

### Dependencies
* Download and install Python;
* Install the following dependencies:
    * `pip install django django-compressor python-decouple`
* Download and install Dart-sass
    * Windows
        * Extract and move it to `C:/Program Files/SASS`;
        * Add it to PATH:
            * Open the Start Menu;
            * Search for `Environment Variables`;
            * Select `Edit the system environment variables`;
            * In the System Properties window, click `Environment Variables...`;
            * Under `System variables`, click `New...`
            * Under `Variable name`, name it "SASS" (or whatever);
            * Under `Variable value`, add the file path;
            * Click `OK`.
    * Linux
        * Extract and move it to `/usr/local/bin`;
        * Open `~/.bashrc` using vim or nano;
        * Add `export PATH="/usr/local/bin/dart-sass:$PATH"`;
        * Save and close your editor;
        * Still in the terminal, run `source ~/.bashrc`;
    * Validate the install with `sass --version` in a command prompt/terminal.

### Setup 
* Clone the repository;
* Navigate inside the "logindemo" folder;
* Creade a `.env` file;
    * Add the following lines to it as is and save:
        * `SECRET_KEY = supermegasecretkey123`
        * `DEBUG = True`
    * If you wish to generate a proper secure key, open a command promp/terminal window and execute:
        * `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
* Create the database with `python manage.py migrate`;
* Create an admin user with `python manage.py createsuperuser` (optional);
* Run the project with `python manage.py runserver`;

## Credits
This project was built with:
* [Python](https://www.python.org/) (3.11.5);
* [Django](https://www.djangoproject.com/) (5.2);
* [Django-compressor](https://pypi.org/project/django-compressor/) (4.5.1);
* [Dart-sass](https://sass-lang.com/dart-sass/) (1.89.1)

## License
MPL 2.0
