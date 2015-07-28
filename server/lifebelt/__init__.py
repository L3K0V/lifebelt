from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET'])
def index():
    return "<h1 style='color:blue'>Hello There!</h1>"
