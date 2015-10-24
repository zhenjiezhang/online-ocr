from bs4 import BeautifulSoup as bs


class ocr_element(object):

	def __init__(self, element):
		self.id=element.get('id')


		title=element.get('title').split()
		i=next(i for i in range(len(title)) if title[i]=='bbox')


		self.left=int(title[i+1])
		self.top=int(title[i+2])
		self.right=int(title[i+3])
		self.bottom=int(title[i+4].strip(';'))

	def __str__(self):
		return self.id

class ocr_page(ocr_element):
	def __init__(self, page):
		super(ocr_page, self).__init__(page)
		self.ppageno=page.get('ppageno')

class ocr_word(ocr_element):
	def __init__(self, word):
		super(ocr_word, self).__init__(word)
		self.text=word.text
		self.bold=bool(word.find('strong'))
		self.italic=bool(word.find('em'))

	def __str__(self):
		return self.text

class ocr_line(ocr_element):
	def __init__(self, line):
		super(ocr_line, self).__init__(line)
		self.words=[]
		for w in line.find_all(class_='ocrx_word'):
			self.words.append(ocr_word(w))






def readOCR(inFile):

	f=open(inFile)
	soup=bs(f,'lxml')
	pages=[]
	for p in soup.find_all(class_='ocr_page'):
		pages.append(ocr_page(p))

	areas=[]
	paragraphs=[]
	lines=[]
	words=[]

	for p in soup.find_all(class_='ocr_page'):
		# print 'page:', p.get('title')
		areas+=p.find_all(class_='ocr_carea')

	for a in areas:
		# print 'area:', a.get('title')
		paragraphs+=a.find_all(class_='ocr_par')
	for par in paragraphs:
		# print 'paragraph', par.get('title')
		for l in par.find_all(class_='ocr_line'):
			lines.append(ocr_line(l))

	for par in paragraphs:
		for l in par.find_all(class_='ocr_line'):
			# print 'line', l.get('title')
			for w in l.find_all(class_='ocrx_word'):
				words.append(ocr_word(w))
	# for w in words:
		# print 'word', w.get('title'), w.text
	return pages[0], lines, words





