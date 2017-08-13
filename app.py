from flask_script import Manager
from web_im.app import create_app
from web_im.exts import db


app = create_app()
manager = Manager(app)


@manager.command
def create():
    """Create database tables
    """
    db.create_all()


if __name__ == '__main__':
    manager.run()
