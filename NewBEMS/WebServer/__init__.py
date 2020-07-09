from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    # from . import discovery
    # app.register_blueprint(discovery.bp)

    from . import active_devices
    app.register_blueprint(active_devices.bp)

    @app.route('/')
    def index():
        return "hello"

    return app
