from website import create_app

app=create_app()

if __name__=='__main__':#what this line ensures is if we import main.py it will start web server if we don't have this line it will only run server if we run main.py
    app.run(debug=True)

