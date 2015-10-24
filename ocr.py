import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter, ImageEnhance
import imghdr
from StringIO import StringIO
import numpy as np
import subprocess as sp
from flask import jsonify
from hocrReader import readOCR

inputFile='static/current.png'
workFile='static/workImage.png'
outputFile='static/output'
zoomRatio=10


def pre_process(image):
    w,h=image.size[0], image.size[1]
    n=w*h
    maxN=1024*1024*2
    scale=(1.0*maxN/n)**0.5
    maxW, maxH=int(w*scale), int(h*scale)

    # image=image.convert('L')
    image=image.resize((maxW,maxH),Image.ANTIALIAS)



    # newSize=(image.size[0]*zoomRatio, image.size[1]*zoomRatio)
    # image=image.resize(newSize,Image.ANTIALIAS)

    # image=image.convert('L').resize(newSize,Image.ANTIALIAS)

    # image=image.point(lambda i: i>180 and 255)
    return image

def crude_process(lang='eng'):

    command = ['tesseract', workFile, outputFile, '-l', lang, 'hocr']

    proc = sp.Popen(command, stderr=sp.PIPE)
    proc.wait()



def process_image(image, lang='eng'):
    image.save(inputFile)

    image=pre_process(image).convert('RGB')
    image.filter(ImageFilter.SMOOTH)

    image.save(workFile)

    crude_process(lang=lang)

    pages, lines, words=readOCR(outputFile+'.html')

    resp=''
    for l in lines:
        # resp+='<p>'
        for w in l.words:
            resp+=w.text+' '
        # resp+='</p>'
        resp+='\n'
    return resp


    return resp

    # f=open(outputFile+'.html')
    # resp = jsonify( {
    #             u'status': 200,
    #             u'ocr':{k:v.decode('utf-8') for k,v in enumerate(f.read().splitlines())}
    #         } )
    # resp.status_code = 200

    # return resp

    # return pytesseract.image_to_string(image, lang='eng')

def refine_process():
    lang='eng'

    image=Image.open(workFile)

    pages, lines, words=readOCR(outputFile+'.html')

    resp=''
    for n in xrange(len(lines)):
        l=lines[n]
        tmpImage='static/tmp/lineImage'+str(n)+'.png'
        tmpXML='static/tmp/lineImage'+str(n)

        lineImage=image.crop((l.left, l.top, l.right, l.bottom)).convert('RGB')
        w=l.right-l.left
        h=l.bottom-l.top

        scale=1

        lineImage=lineImage.resize((int(w*scale), int(h*scale)), Image.ANTIALIAS)
        lineImage.filter(ImageFilter.SMOOTH).filter(ImageFilter.BLUR)

        
        ImageEnhance.Contrast(lineImage)


        margin=500
        boxImage=Image.new('L', (lineImage.size[0]+margin, lineImage.size[1]+margin), 'white')
        boxImage.paste(lineImage, (margin/2, margin/2))
        # boxImage=boxImage.convert('L')
        # boxImage=boxImage.point(lambda i: i>180 and 255)


        # boxImage=boxImage.resize((boxImage.size[0],boxImage.size[1]), Image.ANTIALIAS)

        # boxImage=boxImage.filter(ImageFilter.SHARPEN)

        


        boxImage.save(tmpImage)
        command = ['tesseract', tmpImage, tmpXML, '-l', lang, 'hocr']

        proc = sp.Popen(command, stderr=sp.PIPE)
        proc.wait()

        linePage, lineLines, lineWords=readOCR(tmpXML+'.html')
        for ll in lineLines:
            for w in ll.words:
                resp+=w.text+' '
            resp+='\n'
    return resp


def process_file_image(f, lang='eng'):
    if not imghdr.what(f):
        return "Not image file"
    image=Image.open(f)

    return process_image(image, lang=lang)

def process_web_image(url, lang='eng'):
    f=StringIO(requests.get(url).content)

    return process_file_image(f, lang=lang)



if __name__=="__main__":
	url=raw_input('provide the image url: \n')
	img=process_image(url)
	print img