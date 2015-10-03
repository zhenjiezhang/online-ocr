import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO


def process_image(url):
    image = _get_image(url)
    image=image.convert('RGB')
    # image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)


def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))

if __name__=="__main__":
	url=raw_input('provide the image url: \n')
	img=process_image(url)
	print img