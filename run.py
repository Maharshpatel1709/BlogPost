import subprocess
subprocess.call("pip freeze > requirements.txt")
subprocess.call("pip install -r requirements.txt")
subprocess.call("python manage.py runserver")