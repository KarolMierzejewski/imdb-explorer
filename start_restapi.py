from flask import Flask
from configparser import ConfigParser
from restapi.views import views
from restapi.models import db

def read_database_config(filename='database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)
    
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Not found section {0} in {1} file'.format(section, filename))
    
        return db

def prepare_app():
    app = Flask(__name__)
    
    params = read_database_config()
    db.init(params['database'],
            host=params['host'],
            user=params['user'],
            password=params['password']
    )

    db.connect()

    app.register_blueprint(views)

    @app.route('/')
    def index():
        return "Welcome in IMDB REST API!"

    return app

if __name__ == '__main__':
    app = prepare_app()
    app.run(debug=True)