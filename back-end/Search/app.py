from flask import Flask
from api.authors_api import *
from api.authors_data_api import *
from api.books_api import *
from api.publishers_api import *
from api.search import *
from api.translator_data_api import *
from api.translators_api import *
import os

app = Flask(__name__)
app.register_blueprint(searchAPI, url_prefix='/api/v1/search')
app.register_blueprint(authorsAPI, url_prefix='/api/v1/authors')
app.register_blueprint(authorsDataAPI, url_prefix='/api/v1/authors-data')
app.register_blueprint(BooksAPI, url_prefix='/api/v1/books')
app.register_blueprint(PublishersAPI, url_prefix='/api/v1/publishers')
app.register_blueprint(translatorsDataAPI, url_prefix='/api/v1/translators-data')
app.register_blueprint(TranslatorsApi, url_prefix='/api/v1/translators')


if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 6001)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)

