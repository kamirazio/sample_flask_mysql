from flask import Flask

print('app start')
app = Flask(__name__)

@app.route('/')
def main():
    return 'hello flask :)'

if __name__ == "__main__":
    app.run( host='0.0.0.0', port = 5000, debug = True )
