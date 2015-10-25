import os
from flask import Flask, render_template, request, jsonify
from ocr import process_web_image, process_file_image, refine_process
from myForm import picForm
import imghdr
from random import random
from writePDF import ocr2PDF

app = Flask(__name__)
app.config.from_object('config')


defaultTemplate='index.html'
postExtractionTemplate='refineExtraction.html'
workImage='/static/workImage.png'




@app.route('/', methods=['GET', 'POST'])
def extract(): 
    text=''
    image=''
    lang='eng'
    template=defaultTemplate
    pdfGenerated=False

    if request.method=='POST':
        imageString=workImage+'?random='+str(random())
        lang=request.form.get('lang')


        if 'PDF' in request.form:
            ocr2PDF('static/output.html')
            pdfGenerated=True
            text='PDF file generated'
            image=imageString
            template=postExtractionTemplate

            
        elif 'refine' in request.form:
            text=refine_process()
            image=imageString
            template=postExtractionTemplate

        elif 'submitFile' in request.form:

            
            f=request.files['file']
            
            text=process_file_image(f, lang=lang)
            image=imageString
            template=postExtractionTemplate


        elif 'suubmitURL' in request.form:
            url=request.form.get('webAddr')
            text=process_web_image(url, lang=lang)
            image=imageString
            template=postExtractionTemplate


        else:
            text= "Wrong form submitted"

        if not text:
            text= "No text in the request"
            

    return render_template(template, resp=text, image=image, lang=lang, pdf=pdfGenerated)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
