from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)     #this 'debug' will mean that the web server will automatically update whenever a change is made