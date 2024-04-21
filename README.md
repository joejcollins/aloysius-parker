# flask-forge
> Flask API training project, based on **[this Udemy course.](https://www.udemy.com/course/rest-api-flask-and-python/)** and the **[official documentation site](https://flask.palletsprojects.com/en/3.0.x/quickstart/)**

## Setup
In Codespaces:
- Build the virtual environment with `make venv`
- Verify the environment is setup correctly by doing `make test`

To see other options, run `make`

## Running Flask API
By default:
1. Flask API looks for a file called `app.py` or `wsgi.py` in the directory it is ran in. The command to run the Flask API is `flask run`
2. Flask API runs on **port 5000**, so your bare bones application will be accessible via `http://127.0.0.1:5000/`
    - This can be changed using the `--port` argument variable, or the `PORT` environment variable.



### Customizing the filename
If you wish to run Flask API under a different filename (assuming **main.py**) you may:
 - Pass the argument `--app=main.py` to the `flask run` command, like so: `flask --app 'main.py' run`
 - Use the `FLASK_APP` environment variable and assign the filename,
    - On Linux:   `export FLASK_APP=main.py`
    - On Windows: `set FLASK_APP=main.py`

## Common issues
- **OSError: [Errno 98]** or **OSError: [WinError 10013]**
  - This means that the port you selected (5000 by default) is already in use. You can either [find the program that is using the port](https://flask.palletsprojects.com/en/3.0.x/server/#address-already-in-use) and terminate it (which can be another instance of Flask API), or for a quick fix you can select a different port using the `--port` argument.
