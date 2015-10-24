from flask.ext.wtf import Form
from wtforms import StringField

class picForm(Form):
	webAddr=StringField('Web Address')
