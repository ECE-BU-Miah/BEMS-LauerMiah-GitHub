from flask import Flask, render_template, request, redirect, abort, url_for

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    from . import active_devices
    app.register_blueprint(active_devices.bp)

    from . import settingsViews
    app.register_blueprint(settingsViews.bp)

    from . import applications
    app.register_blueprint(applications.bp)

    from . import notifications
    app.register_blueprint(notifications.bp)

    @app.route('/')
    def index():
        return redirect(url_for('home'))

    @app.route('/home')
    def home():
        return render_template('home.html')

    return app
