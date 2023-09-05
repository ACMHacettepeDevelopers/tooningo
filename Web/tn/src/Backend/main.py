from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/endpoint', methods=['POST'])
def process_user_input():
    data = request.get_json()
    user_input = data.get('userInput')

    # Now, you can use the 'userInput' in your Python app as needed

    # Example response
    response_data = {'message': 'Received user input successfully'}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
