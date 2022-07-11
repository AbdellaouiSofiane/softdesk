# softdesk
> Api for an issue tracking system app.

## Requirements

* python3

## Installation

Navigate to the desired folder using your command prompt and type:

`git clone https://github.com/AbdellaouiSofiane/softdesk.git`

Create your virtual enviroment (replace \<PATH\> with the desired location):

`python -m venv <PATH>`

Activate your virtual enviroment (see [python documentation](https://docs.python.org/fr/3/library/venv.html#creating-virtual-environments) for any trouble):

* POSIX: `source <PATH>/bin/activate`

* Windows: `C:\<PATH>\Scripts\activate.bat`

Navigate to the project directory and type :

`pip install -r requirements.txt`

## Usage

To launch the website, type:

`python manage.py runserver`

Migrate the database 

`python manage.py migrate`

Go to your browser and go to 

`http://127.0.0.1:8000/`
