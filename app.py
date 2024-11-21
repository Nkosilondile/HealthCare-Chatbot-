from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load mock healthcare facilities data
with open('healthcare_facilities.json', 'r') as f:
    healthcare_data = json.load(f)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()

    # Greeting and initial options
    greetings = ["hey", "hello", "hi", "good morning", "good afternoon", "good evening"]
    if any(greet in user_message for greet in greetings):
        return jsonify({
            "response": "Hello! How can I assist you today?",
            "buttons": [
                {"text": "Find a Hospital", "value": "find a hospital"},
                {"text": "Find a Clinic", "value": "find a clinic"},
                {"text": "Get Medical Tips", "value": "medical information"},
                {"text": "Get Health Tips", "value": "get health tips"},
                {"text": "I'm feeling sick", "value": "feeling sick"}
            ],
            "options": [
                {"text": "1. Find a Hospital", "value": "find a hospital"},
                {"text": "2. Find a Clinic", "value": "find a clinic"},
                {"text": "3. Get Medical Tips", "value": "medical information"},
                {"text": "4. Get Health Tips", "value": "get health tips"},
                {"text": "5. I'm feeling sick", "value": "feeling sick"}
            ]
        })

    # Check if user input is a number corresponding to options
    if user_message in ["1", "2", "3", "4", "5"]:
        option_mapping = {
            "1": "find a hospital",
            "2": "find a clinic",
            "3": "get medical tips",
            "4": "get health tips",
            "5": "feeling sick"
        }
        selected_option = option_mapping[user_message]
        return handle_option(selected_option)

    # Asking for location if user wants to find a hospital or clinic
    if "find a hospital" in user_message or "find a clinic" in user_message:
        return jsonify({
            "response": "Please specify your location (Harare, Chitungwiza, or Chinhoyi)."
        })

    # Provide hospitals or clinics based on location
    if user_message in ["harare", "chitungwiza", "chinhoyi"]:
        location = user_message
        response = ""

        if "find a hospital" in request.json.get('previous_message', '').lower():
            response = f"Here are some hospitals in {location}:\n"
            for facility in healthcare_data:
                if facility["type"] == "Hospital" and facility["location"].lower() == location:
                    response += f"{facility['name']} - {facility['address']}\n"
            return jsonify({"response": response.strip()})

        elif "find a clinic" in request.json.get('previous_message', '').lower():
            response = f"Here are some clinics in {location}:\n"
            for facility in healthcare_data:
                if facility["type"] == "Clinic" and facility["location"].lower() == location:
                    response += f"{facility['name']} - {facility['address']}\n"
            return jsonify({"response": response.strip()})

    elif "get health tips" in user_message:
        response = "Here are some health tips:\n1. Stay hydrated.\n2. Eat a balanced diet.\n3. Exercise regularly."
        return jsonify({"response": response.strip()})
    
    elif "medical information" in user_message:
        response = "Please specify your symptom (e.g., fever, cough)."
        return jsonify({"response": response.strip()})

    elif "feeling sick" in user_message:
        response = "I'm sorry to hear that. Please tell me your symptoms."
        return jsonify({"response": response.strip()})

    # Provide medical advice based on symptoms
    symptom = user_message
    advice_response = ""
    
    for facility in healthcare_data:
        medical_info = facility.get("medical_info", {})
        
        if isinstance(medical_info, dict):
            symptoms = medical_info.get("symptoms", [])
            medications = medical_info.get("medications", {})
            
            if symptom in symptoms:
                advice_response += f"For {symptom}, {facility['name']} advises: {medical_info['advice']}\n"
                if symptom in medications:
                    advice_response += f"Recommended medications: {', '.join(medications[symptom])}\n"

    if advice_response:
        return jsonify({"response": advice_response.strip()})

    else:
        response = "I'm sorry, I can help you find hospitals and clinics or provide health tips. Please ask about them."

    return jsonify({"response": response})

def handle_option(option):
    """Handle the selected option and provide the corresponding response."""
    if option == "find a hospital":
        return jsonify({"response": "Please specify your location (Harare, Chitungwiza, or Chinhoyi)."})
    elif option == "find a clinic":
        return jsonify({"response": "Please specify your location (Harare, Chitungwiza, or Chinhoyi)."})
    elif option == "get medical tips":
        return jsonify({"response": "Please specify your symptom (e.g., fever, cough)."})
    elif option == "get health tips":
        response = "Here are some health tips:\n1. Stay hydrated.\n2. Eat a balanced diet.\n3. Exercise regularly."
        return jsonify({"response": response.strip()})
    elif option == "feeling sick":
        return jsonify({"response": "I'm sorry to hear that. Please tell me your symptoms."})

if __name__ == '__main__':
    app.run(debug=True)