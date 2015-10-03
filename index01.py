import os
from flask import Flask
# from ocr import process_image
app = Flask(__name__)

@app.route('/')
def hello_world():
    # return process_image('http://www.nhc.noaa.gov/gifs/WindSpeedProbText2_sm.gif')
    return "hello ginger"

if __name__ == '__main__':
	port=int(os.environ.get("PORT", 5000))
	
    app.run(host='0.0.0.0',port=port)