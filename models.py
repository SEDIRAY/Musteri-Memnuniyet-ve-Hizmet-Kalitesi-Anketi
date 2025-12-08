from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship('Question', backref='survey', lazy=True, cascade="all, delete-orphan")
    responses = db.relationship('Response', backref='survey', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "questions": [q.to_dict() for q in self.questions],
            "participant_count": len(set(r.participant_id for r in self.responses)), # Unique participants
            "response_count": len(self.responses)
        }

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), default='text') # text, rating, multiple_choice
    options = db.Column(db.Text, nullable=True) # JSON string or comma separated for multiple choice
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "survey_id": self.survey_id,
            "text": self.text,
            "type": self.type,
            "options": self.options,
            "order": self.order
        }

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    participant_id = db.Column(db.String(50), nullable=True) # Can be session ID or user ID
    participant_name = db.Column(db.String(100), nullable=True)
    participant_email = db.Column(db.String(100), nullable=True)
    question_text = db.Column(db.String(200), nullable=False)
    response_value = db.Column(db.Text, nullable=False)
    response_type = db.Column(db.String(20), default='text')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "survey_id": self.survey_id,
            "participant_id": self.participant_id,
            "participant_name": self.participant_name,
            "participant_email": self.participant_email,
            "question_text": self.question_text,
            "response_value": self.response_value,
            "response_type": self.response_type,
            "created_at": self.created_at.isoformat()
        }

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "created_at": self.created_at.isoformat()
        }
