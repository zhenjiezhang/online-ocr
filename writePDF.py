from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth 

from PIL import ImageFont
from hocrReader import readOCR


def ocr2PDF(ocrFile):

	zoomRatio=10

	p, lines, words=readOCR(ocrFile)

	c=canvas.Canvas('static/test.pdf', bottomup=0,pagesize=(p.right/zoomRatio,p.bottom/zoomRatio))

	# font=ImageFont.truetype('TimesNewRoman', size=10)
	# font=ImageFont.load('Helvetica')


	for l in lines:

		for w in l.words:
			textWidth = stringWidth(w.text, 'Helvetica', 10)
			print w.text
			if textWidth==0:
				continue
			fontSize=round(10.0*(w.right-w.left)/zoomRatio/textWidth)
			c.setFont('Helvetica',fontSize)

			c.drawString(w.left/zoomRatio,l.bottom/zoomRatio, w.text)

	c.save()

