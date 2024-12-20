from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database
appointments = []

@app.route('/appointments', methods=['POST'])
def book_appointment():
    """Book an appointment."""
    data = request.json
    appointments.append(data)
    return jsonify({"message": "Appointment booked successfully"}), 201

@app.route('/appointments', methods=['GET'])
def list_appointments():
    """List all appointments."""
    return jsonify(appointments), 200

@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def cancel_appointment(appointment_id):
    """Cancel an appointment."""
    global appointments
    appointments = [appt for appt in appointments if appt.get("id") != appointment_id]
    return jsonify({"message": "Appointment cancelled"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
