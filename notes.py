from bottle import Bottle, route, run

app = Bottle()

@app.route('/')
def index():
    return 'hello'

if __name__ == '__main__':
    app.run()
