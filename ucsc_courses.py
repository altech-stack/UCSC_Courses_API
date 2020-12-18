from flask import Flask

# references:
# - restful api - https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
# - auth - http://flask-httpauth.readthedocs.io/en/latest/

app = Flask('ucsc_courses')
from src.endpoints import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = '5000', debug=True, use_reloader=True)
