from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import face_recognition
from datetime import datetime
from web3 import Web3
import json
import os
import web3

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Load contract details
with open('contract_details.json') as f:
    contract_details = json.load(f)

contract_address = contract_details['address']
contract_abi = contract_details['abi']
checksum_address = Web3.to_checksum_address(contract_address)
# Load contract
contract = w3.eth.contract(address=checksum_address, abi=contract_abi)

# Set up paths and load images
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

# Function to find encodings for known images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)

# Function to mark attendance on the blockchain
def markAttendance(name):
    # Call markAttendance function
    tx_hash = contract.functions.markAttendance(name, datetime.now().strftime('%H:%M:%S')).transact({
        'from': w3.eth.accounts[0]
    })

    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Transaction Receipt:", tx_receipt)

# Function to fetch attendance data from the blockchain
# Function to fetch attendance data from the blockchain
def get_attendance_data():
    attendance_data = []
    try:
        # Retrieve attendance count
        attendance_count = contract.functions.getAttendanceCount().call()

        # Retrieve attendance records
        for i in range(attendance_count):
            name, time = contract.functions.getAttendanceRecord(i).call()
            attendance_data.append({"name": name, "time": time})

    except Exception as e:
        # Handle any exceptions
        print("Error fetching attendance data:", e)

    return attendance_data

# API endpoint to start attendance marking
@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    try:
        # Get the image from the request
        img = request.files['image']
        
        # Convert image to numpy array
        img_np = np.frombuffer(img.read(), np.uint8)
        img_cv = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        # Convert image to RGB (face_recognition library uses RGB)
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

        # Find faces in the image
        face_locations = face_recognition.face_locations(img_rgb)
        face_encodings = face_recognition.face_encodings(img_rgb, face_locations)

        if len(face_locations) == 0:
            return jsonify({"error": "No faces detected"}), 400

        # Match faces with known faces
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
            face_distances = face_recognition.face_distance(encodeListKnown, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = classNames[best_match_index]
                markAttendance(name)

        return jsonify({"message": "Attendance saved"})
    
    except KeyError:
        return jsonify({"error": "No 'image' file provided"}), 400

# API endpoint to fetch and display attendance data
# API endpoint to fetch and display attendance data
# API endpoint to fetch and display attendance data
@app.route('/display_attendance', methods=['GET'])
def display_attendance():
    try:
        # Retrieve attendance data from the blockchain
        attendance_data = get_attendance_data()
        return jsonify(attendance_data)
    except web3.exceptions.ABIEventFunctionNotFound as e:
        # If the event is not found in the contract's ABI
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # If any other error occurs
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
