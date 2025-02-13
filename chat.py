import google.generativeai as genai
import json

# Load the JSON dataset
with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Configure Gemini API
genai.configure(api_key="AIzaSyAAl6Y1Ea6oA-sWzQt8sXYYcGHf6_4qIqM")

# Function to find response from dataset
def search_dataset(user_input):
    user_input_lower = user_input.lower()
    
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            pattern_lower = pattern.lower()
            if user_input_lower in pattern_lower or pattern_lower in user_input_lower:
                print(f"🔍 Found match in dataset: {pattern}")  # Debugging
                return intent["responses"][0]  # Return the first matching response
    
    print("❌ No match found in dataset, using Gemini API")  # Debugging
    return None  # Return None if no match is found

# Function to get response from Gemini API
def get_gemini_response(user_input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_input)
    return response.text.strip()

# Function to get the final chatbot response
def get_response(user_input):
    dataset_response = search_dataset(user_input)
    if dataset_response:
        return dataset_response  # Return dataset response if found
    else:
        return get_gemini_response(user_input)  # Use Gemini API if no match
