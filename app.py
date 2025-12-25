from flask import Flask, render_template, jsonify, request
from models import db, Survey, Response, Question, ContactMessage
import os

app = Flask(__name__)

# Veritabanı dosyasının tam yolunu belirle (Absolute Path)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'surveys.db')

# Instance klasörünün var olduğundan emin ol
if not os.path.exists(os.path.join(basedir, 'instance')):
    os.makedirs(os.path.join(basedir, 'instance'))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + db_path
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"Veritabanı yolu: {db_path}")

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('adminpaneli.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin-dashboard.html')

@app.route('/anket')
def anket():
    return render_template('anketformusayfasi.html')

@app.route('/pasta-grafik')
def pasta_grafik():
    return render_template('pastagrafiksayfasi.html')

@app.route('/survey-init')
def survey_init():
    return render_template('surveyforminit.html')

@app.route('/tesekkur')
def tesekkur():
    return render_template('tesekkur.html')

@app.route('/analytic')
def analytic_page():
    return render_template('analytic-page.html')

# API Routes
@app.route('/api/health')
def api_health():
    return jsonify({"status": "ok"})

@app.route('/api/surveys', methods=['GET'])
def get_surveys():
    surveys = Survey.query.all()
    return jsonify([s.to_dict() for s in surveys])

@app.route('/api/surveys', methods=['POST'])
def create_survey():
    data = request.json
    new_survey = Survey(
        title=data.get('title'),
        description=data.get('description'),
        status=data.get('status', 'active')
    )
    db.session.add(new_survey)
    db.session.flush() # Get ID

    questions_data = data.get('questions', [])
    for i, q_data in enumerate(questions_data):
        question = Question(
            survey_id=new_survey.id,
            text=q_data.get('text'),
            type=q_data.get('type', 'text'),
            options=q_data.get('options'),
            order=i
        )
        db.session.add(question)

    db.session.commit()
    return jsonify(new_survey.to_dict()), 201

@app.route('/api/surveys/<int:survey_id>', methods=['GET'])
def get_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    return jsonify(survey.to_dict())

@app.route('/api/surveys/<int:survey_id>', methods=['PUT'])
def update_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    data = request.json
    if 'title' in data:
        survey.title = data['title']
    if 'description' in data:
        survey.description = data['description']
    if 'status' in data:
        survey.status = data['status']
    
    if 'questions' in data:
        # Remove existing questions
        Question.query.filter_by(survey_id=survey_id).delete()
        
        # Add new questions
        questions_data = data.get('questions', [])
        for i, q_data in enumerate(questions_data):
            question = Question(
                survey_id=survey.id,
                text=q_data.get('text'),
                type=q_data.get('type', 'text'),
                options=q_data.get('options'),
                order=i
            )
            db.session.add(question)

    db.session.commit()
    return jsonify(survey.to_dict())

@app.route('/api/surveys/<int:survey_id>', methods=['DELETE'])
def delete_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    db.session.delete(survey)
    db.session.commit()
    return jsonify({"message": "Deleted"})

@app.route('/api/surveys/<int:survey_id>/responses', methods=['GET'])
def get_survey_responses(survey_id):
    responses = Response.query.filter_by(survey_id=survey_id).all()
    return jsonify([r.to_dict() for r in responses])

@app.route('/api/surveys/<int:survey_id>/responses', methods=['POST'])
def submit_survey_response(survey_id):
    data = request.json
    survey = Survey.query.get_or_404(survey_id)
    
    participant_id = data.get('participant_id', 'anonymous')
    participant_name = data.get('participant_name', 'Anonymous')
    participant_email = data.get('participant_email', '')
    answers = data.get('answers', [])

    for ans in answers:
        response = Response(
            survey_id=survey.id,
            participant_id=participant_id,
            participant_name=participant_name,
            participant_email=participant_email,
            question_text=ans.get('question_text'),
            response_value=ans.get('value'),
            response_type=ans.get('type', 'text')
        )
        db.session.add(response)
    
    db.session.commit()
    return jsonify({"message": "Responses saved"}), 201

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.json
    new_message = ContactMessage(
        name=data.get('name'),
        email=data.get('email'),
        message=data.get('message')
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Message received"}), 201

@app.route('/api/contact-messages', methods=['GET'])
def get_contact_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify([m.to_dict() for m in messages])

def seed_data():
    if Survey.query.first() is None:
        s1 = Survey(title="Müşteri Memnuniyeti Anketi", description="Genel müşteri memnuniyetini ölçmek için.", status="active")
        s2 = Survey(title="Ürün Geri Bildirimi", description="Yeni ürün hakkında geri bildirim.", status="paused")
        db.session.add_all([s1, s2])
        db.session.commit()
        
        # Add some dummy responses
        for i in range(1, 21):
            r = Response(
                survey_id=s1.id,
                participant_id=str(i % 5 + 1),
                participant_name=f"Participant {i % 5 + 1}",
                participant_email=f"user{i % 5 + 1}@example.com",
                question_text="Hizmetten memnun kaldınız mı?",
                response_value="Evet" if i % 2 == 0 else "Hayır",
                response_type="text"
            )
            db.session.add(r)
        db.session.commit()
        print("Database seeded!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # seed_data() # Commented out to prevent re-seeding after deletion
    app.run(debug=True)
