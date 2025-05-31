from mongoengine import Document, StringField, ListField, DateTimeField, FloatField, ReferenceField
import datetime

class SymptomInput(Document):
    symptoms = ListField(StringField())
    submitted_at = DateTimeField(default=datetime.datetime.utcnow)

class PredictionResult(Document):
    input = ReferenceField(SymptomInput)
    predicted_disease = StringField(max_length=100)
    probability = FloatField()
    predicted_at = DateTimeField(default=datetime.datetime.utcnow)
