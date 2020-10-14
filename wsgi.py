from app import create_app


app = create_app()


@app.route('/')
def root():
    """
    this is the root of our app
    """
    return "Hey there welcome to RMS"


if __name__ == "__main__":
    app.run()
