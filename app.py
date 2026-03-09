from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

queue = []
token = 1
current_patient = None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add_patient', methods=['POST'])
def add_patient():
    global token
    data = request.json
    name = data.get("name")

    patient = {
        "token": token,
        "name": name
    }

    queue.append(patient)
    token += 1

    return jsonify({
        "message": f"{name} added with Token {patient['token']}"
    })

@app.route('/next_patient', methods=['GET'])
def next_patient():
    global current_patient

    if queue:
        current_patient = queue.pop(0)
        return jsonify({"next_patient": current_patient})
    else:
        return jsonify({"message": "No patients in queue"})

@app.route('/queue', methods=['GET'])
def show_queue():
    return jsonify({"queue": queue})

@app.route('/reset_queue', methods=['POST'])
def reset_queue():
    global queue, token
    queue = []
    token = 1
    return jsonify({"message": "Queue reset successfully"})

@app.route('/display_board', methods=['GET'])
def display_board():

    waiting = len(queue)

    if current_patient:
        serving = f"Token {current_patient['token']} - {current_patient['name']}"
    else:
        serving = "No patient being served"

    wait_time = waiting * 3

    return jsonify({
        "now_serving": serving,
        "patients_waiting": waiting,
        "estimated_wait": wait_time
    })

    

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=10000)