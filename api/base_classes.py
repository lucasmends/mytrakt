from mongoengine import *

class ID(DynamicEmbeddedDocument):
	trakt = IntField(required=True)
	imdb = StringField()

class BaseDocumentIntern(Document):
	number = IntField(required=True)
	ids = EmbeddedDocumentField(ID)
	rating = FloatField()
	votes = IntField()
	overview = StringField()
	image = StringField(required=True)

	#para checar se precisa atualizar
	__date_update = DateTimeField(required=True)

	meta = {'allow_inheritance': True}

class BaseDocumment(Document):
	title = StringField(required=True)
	year = IntField()
	ids = EmbeddedDocumentField(ID)
	overview = StringField()
	rating = FloatField()
	votes = IntField()	
	images = DictField()
	__date_update = DateTimeField(required=True)
		
	meta = {'allow_inheritance': True}
