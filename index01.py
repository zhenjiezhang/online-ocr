import os
from flask import Flask
from ocr import process_image
app = Flask(__name__)



@app.route('/')
def hello():
    return process_image('http://www.nhc.noaa.gov/gifs/WindSpeedProbText2_sm.gif')

    # return "Hello from Python!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
