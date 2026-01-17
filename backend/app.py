from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__, template_folder='../frontend')

# Mock AI disease detection
def detect_disease(image_data):
    # Default detection for demo
    return 'Leaf Blight'

# Mock recommendations
def get_recommendations(disease):
    recommendations = {
        'Healthy': 'No treatment needed. Continue good farming practices.',
        'Leaf Blight': 'Apply copper-based fungicide. Improve air circulation.',
        'Powdery Mildew': 'Use sulfur-based fungicide. Avoid overhead watering.',
        'Rust': 'Remove infected leaves. Apply fungicide containing triazole.',
        'Fusarium Wilt': 'Remove infected plants. Use resistant varieties next season.'
    }
    return recommendations.get(disease, 'Consult a local agricultural expert.')

# Mock weather data
def get_weather_data():
    return {
        'temperature': random.randint(15, 35),
        'humidity': random.randint(40, 90),
        'rainfall': random.randint(0, 20)
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        response = jsonify({'error': 'No image file provided'})
        response.status_code = 400
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    image = request.files['image']
    if image.filename == '':
        response = jsonify({'error': 'No image selected'})
        response.status_code = 400
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    # Mock processing
    disease = detect_disease(image.read())
    recommendations = get_recommendations(disease)

    response = jsonify({
        'disease': disease,
        'recommendations': recommendations
    })
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/recommend', methods=['GET'])
def recommend():
    disease = request.args.get('disease', 'Unknown')
    recommendations = get_recommendations(disease)
    return jsonify({'recommendations': recommendations})

@app.route('/climate', methods=['GET'])
def climate():
    weather = get_weather_data()
    return jsonify(weather)

@app.route('/results')
def results():
    disease = request.args.get('disease', 'Unknown')
    recommendations = request.args.get('recommendations', 'No recommendations available.')
    return render_template('results.html', disease=disease, recommendations=recommendations)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
