from mongoengine import Document, StringField, ListField, ReferenceField


class Authors(Document):
    fullname = StringField(max_length=100)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=50)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, required=True)
    quote = StringField()
    meta = {'allow_inheritance': True}
