from flask_api import status
from flask import render_template
from jinja2.exceptions import TemplateNotFound
from indigo.exceptions.validators import JSONValidatorException

from indigo import create_app

app = create_app(config_obj='indigo.config.ProductionConfig')

@app.errorhandler(TemplateNotFound)
def not_found(error):
    return {'error': 'Page not found'}, status.HTTP_404_NOT_FOUND

@app.route('/ping/')
def ping():
    return 'Pong'

# INFO: Code snippet: http://flask.pocoo.org/snippets/57/
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', False))
