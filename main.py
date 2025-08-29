from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)

USER_ID = "arnavsharma"
EMAIL = "arnav06as@gmail.com"
ROLL_NUMBER = "22BCE2519"

def process_data(data_array):
    odd_numbers = []
    even_numbers = []
    alphabets = []
    special_characters = []
    numbers_sum = 0
    
    for item in data_array:
        if item.isdigit():
            num = int(item)
            numbers_sum += num
            if num % 2 == 0:
                even_numbers.append(item)
            else:
                odd_numbers.append(item)
        elif item.isalpha():
            alphabets.append(item.upper())
        else:
            special_characters.append(item)
    
    return {
        'odd_numbers': odd_numbers,
        'even_numbers': even_numbers,
        'alphabets': alphabets,
        'special_characters': special_characters,
        'numbers_sum': numbers_sum
    }

def create_concat_string(alphabets):
    if not alphabets:
        return ""
    
    reversed_alphabets = alphabets[::-1]
    
    concat_string = ""
    for i, char in enumerate(reversed_alphabets):
        if i % 2 == 0:
            concat_string += char.upper()
        else:
            concat_string += char.lower()
    
    return concat_string

@app.route('/bfhl', methods=['POST'])
def bfhl_endpoint():
    try:
        json_data = request.get_json()
        
        if not json_data or 'data' not in json_data:
            return jsonify({
                "is_success": False,
                "error": "Invalid input format. Expected 'data' field with array."
            }), 400
        
        data_array = json_data['data']
        
        if not isinstance(data_array, list):
            return jsonify({
                "is_success": False,
                "error": "Data field must be an array."
            }), 400
        
        result = process_data(data_array)
        
        original_alphabets = []
        for item in data_array:
            if item.isalpha():
                original_alphabets.append(item)
        
        concat_string = create_concat_string(original_alphabets)
        
        response = {
            "is_success": True,
            "user_id": USER_ID,
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": result['odd_numbers'],
            "even_numbers": result['even_numbers'],
            "alphabets": result['alphabets'],
            "special_characters": result['special_characters'],
            "sum": str(result['numbers_sum']),  
            "concat_string": concat_string
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            "is_success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/bfhl', methods=['GET'])
def bfhl_get():
    return jsonify({
        "operation_code": 1
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "is_success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "is_success": False,
        "error": "Method not allowed"
    }), 405

if __name__ == '__main__':
    # Use PORT environment variable if available, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)