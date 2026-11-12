from flask import Flask, render_template, request, jsonify
import json
import random
import os

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'pantun_data.json')

# --- 1. Load Data ---
def load_dataset():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# --- 2. Save Data ---
def save_dataset(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

PANTUN_DB = load_dataset()

# --- 3. Configuration ---
EMOTION_KEYWORDS = {
    'joy': [
        'happy', 'glad', 'joy', 'excited', 'good',
        'gembira', 'riang', 'seronok', 'teruja', 'ceria', 'bahagia', 
        'suka', 'senang', 'manis', 'gelak', 'ketawa'
    ],
    'sadness': [
        'sad', 'cry', 'bad', 'depressed', 'down',
        'sedih', 'pilu', 'sayu', 'duka', 'hiba', 'muram', 
        'kecewa', 'nangis', 'sunyi', 'hampa', 'merana'
    ],
    'anger': [
        'angry', 'mad', 'furious', 'hate',
        'marah', 'geram', 'berang', 'murka', 'naik angin', 'bengang', 
        'benci', 'panas hati', 'mengamuk', 'dendam'
    ],
    'fear': [
        'scared', 'afraid', 'fear', 'nervous', 'panicked',
        'takut', 'gentar', 'cemas', 'seram', 'ngeri', 'kecut perut', 
        'risau', 'bimbang', 'gementar'
    ],
    'love': [
        'love', 'adore', 'miss',
        'cinta', 'kasih', 'sayang', 'rindu', 'jodoh', 'kekasih'
    ],
    'neutral': [
        'neutral', 'okay', 'fine', 'normal',
        'biasa', 'tenang', 'berkecuali', 'mendatar', 'tidak beremosi', 
        'nasihat', 'ok', 'relaks'
    ]
}

TOXIC_KEYWORDS = ['bodoh', 'sial', 'babi', 'anjing', 'gila', 'sundal', 'bangang', 'stupid', 'idiot', 'damn', 'celaka']

PANTUN_ADAB = {
    "title": "Teguran Santun",
    "body": "Yang kurik itu kundi,\nYang merah itu saga,\nYang baik itu budi,\nYang indah itu bahasa.",
    "meaning": "Peringatan: Tutur kata yang kesat tidak mencerminkan budaya kita. Sila gunakan bahasa yang sopan."
}

# --- 4. Logic Functions ---

def adab_check(text):
    text = text.lower()
    for word in TOXIC_KEYWORDS:
        if word in text:
            return False 
    return True 

def predict_complex_emotion(text):
    """Detects top 2 emotions for mixed feelings"""
    text = text.lower()
    scores = {emotion: 0 for emotion in EMOTION_KEYWORDS}
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for word in keywords:
            if word in text:
                scores[emotion] += 1
    
    # Sort emotions by score
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_emotion, top_score = sorted_scores[0]
    
    if top_score == 0:
        return None, None # No emotion found
        
    second_emotion, second_score = sorted_scores[1]
    
    # Return both emotions if the second one exists (score > 0)
    if second_score > 0:
        return top_emotion, second_emotion
        
    return top_emotion, None

# --- 5. Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    user_text = data.get('text', '')

    # 1. Adab Check
    if not adab_check(user_text):
        return jsonify({
            'status': 'violation',
            'emotion': 'Cultural Violation',
            'results': [PANTUN_ADAB]
        })

    # 2. Detect Emotions (Primary & Secondary)
    primary, secondary = predict_complex_emotion(user_text)
    
    if primary is None:
        return jsonify({
            'status': 'no_emotion',
            'message': 'Emotion required only'
        })
    
    # 3. Build Pantun List
    # Fetch primary emotion list (copy it)
    pantun_list = list(PANTUN_DB.get(primary, PANTUN_DB['neutral']))
    
    emotion_label = primary
    is_mixed = False

    # If secondary emotion exists, merge lists!
    if secondary:
        is_mixed = True
        emotion_label = f"{primary} & {secondary}" # Label becomes "Joy & Sadness"
        secondary_list = PANTUN_DB.get(secondary, [])
        pantun_list.extend(secondary_list) # Combine both lists
    
    # Shuffle so user gets a mix of both themes when clicking "Next"
    random.shuffle(pantun_list)
    # Sort slightly by weight so 'learned' pantuns still appear often, but mixed
    pantun_list.sort(key=lambda x: x['weight'], reverse=True)
    
    response = {
        'status': 'success',
        'emotion': emotion_label,
        'is_mixed': is_mixed,
        'results': pantun_list
    }
    
    return jsonify(response)

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    pantun_id = data.get('id')
    # Note: For mixed emotions, we just need to find the ID in the DB to update it
    # We search all categories since we don't know exactly which category the ID belongs to in a mixed list
    
    found = False
    if pantun_id:
        for category in PANTUN_DB:
            for p in PANTUN_DB[category]:
                if p['id'] == pantun_id:
                    p['weight'] += 1
                    found = True
                    break
            if found: break
    
    if found:
        save_dataset(PANTUN_DB)
        return jsonify({'status': 'learned'})
    
    return jsonify({'status': 'error'}), 400

if __name__ == '__main__':
    app.run(debug=True)