from flask import Flask, render_template

from bp_api.views import api_blueprint
from bp_posts.views import post_blueprint
from exceptions.data_exceptions import DataSourceError
from config_logger import config_log


def create_and_config_app(config_path):
    app = Flask(__name__)
    app.register_blueprint(post_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.config.from_pyfile(config_path)
    config_log(app)

    return app


app = create_and_config_app("config.py")


@app.errorhandler(404)
def page_error_404(error):
    return f"Такой страницы нет {error}", 404


@app.errorhandler(500)
def page_error_500(error):
    return f"На сервере произошла ошибка - {error}", 500


@app.errorhandler(DataSourceError)
def page_error_data_source_error(error):
    return f"Ошибка, поломались данные {error}", 500


if __name__ == '__main__':
    app.run()
