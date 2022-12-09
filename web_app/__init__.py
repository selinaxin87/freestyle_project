from flask import Flask, render_template

from web_app.routes.project_routes import home_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_routes)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)