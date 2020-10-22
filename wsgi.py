from flask import redirect, url_for
from app import create_app


app = create_app()


@app.route('/')
def root():
    """
    this is the root of our app
    """
    return redirect(url_for('rms.load_welcome_ui'))


if __name__ == "__main__":
    app.run()
