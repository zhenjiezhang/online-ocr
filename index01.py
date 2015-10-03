from flask import Flask
from ocr import process_image
app = Flask(__name__)

@app.route('/')
def hello_world():
    return process_image('http://www.nhc.noaa.gov/gifs/WindSpeedProbText2_sm.gif')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)