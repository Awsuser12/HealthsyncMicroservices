from flask import Flask, request, jsonify
from models import db, Patient
import os

app = Flask(__name__)

# Configuration for Redshift
REDHSHIFT_DB_URI = os.getenv(
    "REDSHIFT_DB_URI",
    "postgresql://username:password@redshift-cluster-endpoint:5439/database_name"
)
app.config['SQLALCHEMY_DATABASE_URI'] = REDHSHIFT_DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    try:
        new_patient = Patient(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            medical_history=data.get('medical_history', '')
        )
        db.session.add(new_patient)
        db.session.commit()
        return jsonify({"message": "Patient added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/patients', methods=['GET'])
def get_all_patients():
    patients = Patient.query.all()
    return jsonify([patient.to_dict() for patient in patients])

@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        return jsonify(patient.to_dict())
    return jsonify({"error": "Patient not found"}), 404

@app.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.get_json()
    patient = Patient.query.get(patient_id)
    if patient:
        patient.name = data.get('name', patient.name)
        patient.age = data.get('age', patient.age)
        patient.gender = data.get('gender', patient.gender)
        patient.medical_history = data.get('medical_history', patient.medical_history)
        db.session.commit()
        return jsonify({"message": "Patient updated successfully!"})
    return jsonify({"error": "Patient not found"}), 404

@app.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return jsonify({"message": "Patient deleted successfully!"})
    return jsonify({"error": "Patient not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
