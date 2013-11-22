import bottle

@bottle.route('/')
def index():
    return 'hello'

if __name__ == '__main__':
    bottle.run()
