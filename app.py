from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------------------------------
# PLANT DATABASE
# --------------------------------------------------

PLANTS = {

    "tomato": {
        "name": "Tomato",
        "scientific": "Solanum lycopersicum",
        "icon": "🍅",
        "description":
            "Tomato is an important vegetable crop commonly grown in home gardens and farms.",
        "soil":
            "Well-drained, fertile soil with good organic matter. Slightly acidic to neutral soil is generally suitable.",
        "water":
            "Keep soil consistently moist but avoid waterlogging.",
        "sun":
            "Needs good sunlight for healthy growth.",
        "medical":
            "Tomato is primarily a food crop and contains nutrients such as lycopene and vitamin C.",
        "diseases": [
            "Early Blight",
            "Late Blight",
            "Leaf Spot",
            "Bacterial Spot"
        ],
        "link":
            "https://powo.science.kew.org/results?q=Solanum%20lycopersicum"
    },

    "potato": {
        "name": "Potato",
        "scientific": "Solanum tuberosum",
        "icon": "🥔",
        "description":
            "Potato is a major food crop cultivated in many parts of the world.",
        "soil":
            "Loose, fertile and well-drained soil is preferred.",
        "water":
            "Provide regular moisture without prolonged waterlogging.",
        "sun":
            "Requires adequate sunlight.",
        "medical":
            "Potato is mainly a food crop and provides carbohydrates, potassium and other nutrients.",
        "diseases": [
            "Late Blight",
            "Early Blight",
            "Black Scurf",
            "Common Scab"
        ],
        "link":
            "https://powo.science.kew.org/results?q=Solanum%20tuberosum"
    },

    "rice": {
        "name": "Rice",
        "scientific": "Oryza sativa",
        "icon": "🌾",
        "description":
            "Rice is one of the world's major cereal crops and is widely cultivated in Asia.",
        "soil":
            "Clayey to loamy soil with good water-holding capacity can be suitable depending on the production system.",
        "water":
            "Water requirements depend strongly on cultivation method and growth stage.",
        "sun":
            "Requires good sunlight.",
        "medical":
            "Rice is primarily a food crop and is an important source of dietary energy.",
        "diseases": [
            "Rice Blast",
            "Brown Spot",
            "Bacterial Leaf Blight",
            "Sheath Blight"
        ],
        "link":
            "https://powo.science.kew.org/results?q=Oryza%20sativa"
    },

    "mango": {
        "name": "Mango",
        "scientific": "Mangifera indica",
        "icon": "🥭",
        "description":
            "Mango is a tropical fruit tree widely cultivated in India and other warm regions.",
        "soil":
            "Well-drained loamy soil is generally suitable.",
        "water":
            "Young trees need regular irrigation; mature trees have different water requirements depending on climate and soil.",
        "sun":
            "Requires full sunlight.",
        "medical":
            "Mango is mainly a food crop. The fruit provides vitamins and other nutrients.",
        "diseases": [
            "Powdery Mildew",
            "Anthracnose",
            "Dieback",
            "Bacterial Black Spot"
        ],
        "link":
            "https://powo.science.kew.org/results?q=Mangifera%20indica"
    },

    "chilli": {
        "name": "Chilli",
        "scientific": "Capsicum annuum",
        "icon": "🌶️",
        "description":
            "Chilli is an important spice and vegetable crop.",
        "soil":
            "Fertile, well-drained soil with good organic matter is preferred.",
        "water":
            "Water regularly but avoid standing water.",
        "sun":
            "Requires good sunlight.",
        "medical":
            "Chilli is primarily a food/spice crop. Capsaicin is the compound responsible for its pungency.",
        "diseases": [
            "Leaf Curl",
            "Anthracnose",
            "Powdery Mildew",
            "Bacterial Leaf Spot"
        ],
        "link":
            "https://powo.science.kew.org/results?q=Capsicum%20annuum"
    },

    "neem": {
        "name": "Neem",
        "scientific": "Azadirachta indica",
        "icon": "🌳",
        "description":
            "Neem is a well-known tree native to the Indian subcontinent.",
        "soil":
            "Neem can tolerate a range of soils but prefers well-drained conditions.",
        "water":
            "Established trees generally tolerate dry conditions.",
        "sun":
            "Prefers strong sunlight.",
        "medical":
            "Neem has a long history of traditional uses. Such traditional use should not be treated as proof of a medical treatment.",
        "diseases": [
            "Leaf Spot",
            "Powdery Mildew",
            "Sooty Mold"
        ],
        "link":
            "https://powo.science.kew.org/results?q=Azadirachta%20indica"
    },

    "tulsi": {
        "name": "Tulsi",
        "scientific": "Ocimum tenuiflorum",
        "icon": "🌿",
        "description":
            "Tulsi, also called holy basil, is a fragrant plant widely grown in South Asia.",
        "soil":
            "Well-drained soil with organic matter is suitable.",
        "water":
            "Water when the upper soil begins to dry.",
        "sun":
            "Needs good sunlight.",
        "medical":
            "Tulsi has a history of traditional use. Traditional use does not guarantee medical effectiveness or safety.",
        "diseases": [
            "Leaf Spot",
            "Downy Mildew",
            "Root Rot"
        ],
        "link":
            "https://powo.science.kew.org/results?q=Ocimum%20tenuiflorum"
    },

    "rose": {
        "name": "Rose",
        "scientific": "Rosa",
        "icon": "🌹",
        "description":
            "Rose plants are popular ornamental plants with many cultivated varieties.",
        "soil":
            "Rich, well-drained soil with organic matter is generally preferred.",
        "water":
            "Water at the root zone and avoid continuously wet foliage.",
        "sun":
            "Requires several hours of sunlight.",
        "medical":
            "Rose is mainly ornamental, although various rose products have traditional and culinary uses.",
        "diseases": [
            "Black Spot",
            "Powdery Mildew",
            "Rust",
            "Downy Mildew"
        ],
        "link":
            "https://powo.science.kew.org/results?q=Rosa"
    }
}


# --------------------------------------------------
# DISEASE DATABASE
# --------------------------------------------------

DISEASES = {

    "early blight": {
        "name": "Early Blight",
        "symptoms":
            "Dark circular or target-like spots may develop on older leaves.",
        "causes":
            "Commonly associated with fungal infection and favorable moisture conditions.",
        "care":
            "Remove badly affected leaves, improve air circulation and avoid unnecessary leaf wetness.",
        "prevention":
            "Use clean planting material, crop rotation and good garden sanitation."
    },

    "late blight": {
        "name": "Late Blight",
        "symptoms":
            "Dark water-soaked-looking lesions can expand rapidly under favorable conditions.",
        "causes":
            "Caused by a pathogen that spreads rapidly in cool, wet conditions.",
        "care":
            "Remove severely affected plant material and improve ventilation. Follow local agricultural guidance for approved treatments.",
        "prevention":
            "Avoid prolonged leaf wetness and maintain good plant spacing."
    },

    "powdery mildew": {
        "name": "Powdery Mildew",
        "symptoms":
            "White powder-like growth can appear on leaves and stems.",
        "causes":
            "Several fungi can cause powdery mildew.",
        "care":
            "Remove heavily affected leaves and improve airflow around plants.",
        "prevention":
            "Avoid overcrowding and maintain good ventilation."
    },

    "leaf spot": {
        "name": "Leaf Spot",
        "symptoms":
            "Small brown, black or yellowish spots can appear on leaves.",
        "causes":
            "Leaf spots can be caused by different fungi or bacteria depending on the crop.",
        "care":
            "Remove heavily affected leaves and avoid overhead irrigation.",
        "prevention":
            "Use clean tools and keep foliage dry where practical."
    },

    "anthracnose": {
        "name": "Anthracnose",
        "symptoms":
            "Dark lesions can occur on leaves, stems or fruits.",
        "causes":
            "A group of fungal diseases affecting many crops.",
        "care":
            "Remove infected material and improve air circulation.",
        "prevention":
            "Maintain sanitation and avoid unnecessary leaf wetness."
    },

    "root rot": {
        "name": "Root Rot",
        "symptoms":
            "Plants may wilt, show yellowing or have weak growth even when soil is moist.",
        "causes":
            "Often associated with excessive soil moisture and poor drainage.",
        "care":
            "Improve drainage and avoid excessive watering.",
        "prevention":
            "Use well-drained soil and suitable irrigation."
    }
}


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def analyse_plant(plant, soil, disease):
    score = 82

    if soil == "poor":
        score -= 12
    elif soil == "dry":
        score -= 7
    elif soil == "wet":
        score -= 10
    elif soil == "good":
        score += 5

    if disease and disease.lower() != "none":
        score -= 12

    score = max(35, min(98, score))

    plant_data = PLANTS.get(
        plant,
        PLANTS["tomato"]
    )

    disease_key = disease.lower().strip()

    if disease_key in DISEASES:
        disease_data = DISEASES[disease_key]
    else:
        disease_data = {
            "name": disease if disease else "No disease selected",
            "symptoms": "No disease symptoms selected.",
            "causes": "No disease information selected.",
            "care": "Continue regular monitoring.",
            "prevention": "Maintain good sanitation, watering and airflow."
        }

    suggestions = []

    if soil == "dry":
        suggestions.append(
            "Check soil moisture and provide appropriate irrigation."
        )

    elif soil == "wet":
        suggestions.append(
            "Reduce excessive watering and improve drainage."
        )

    elif soil == "poor":
        suggestions.append(
            "Consider adding suitable organic matter based on a soil test."
        )

    else:
        suggestions.append(
            "Continue maintaining balanced soil moisture."
        )

    suggestions.append(
        "Inspect both sides of leaves regularly for insects or disease symptoms."
    )

    suggestions.append(
        "Remove severely damaged plant material where appropriate."
    )

    suggestions.append(
        "Avoid unnecessary pesticide use and follow local agricultural recommendations."
    )

    return {
        "health_score": score,
        "plant": plant_data,
        "disease": disease_data,
        "suggestions": suggestions
    }


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return render_template(
        "index.html",
        plants=PLANTS,
        diseases=DISEASES
    )


# --------------------------------------------------
# UPLOAD + ANALYSIS API
# --------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    if "plant_image" not in request.files:
        return jsonify({
            "success": False,
            "message": "Please upload a plant or leaf image."
        }), 400

    file = request.files["plant_image"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Please select an image."
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "message": "Only JPG, JPEG, PNG and WEBP images are allowed."
        }), 400

    plant = request.form.get("plant", "tomato")
    soil = request.form.get("soil", "good")
    disease = request.form.get("disease", "none")

    original_name = secure_filename(file.filename)

    extension = original_name.rsplit(".", 1)[1].lower()

    unique_name = (
        str(uuid.uuid4()) + "." + extension
    )

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_name
    )

    file.save(file_path)

    result = analyse_plant(
        plant,
        soil,
        disease
    )

    result["image_url"] = "/uploads/" + unique_name
    result["filename"] = original_name
    result["time"] = datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    result["success"] = True

    return jsonify(result)


# --------------------------------------------------
# SERVE UPLOADED IMAGES
# --------------------------------------------------

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# --------------------------------------------------
# PLANT INFORMATION API
# --------------------------------------------------

@app.route("/api/plant/<plant_id>")
def plant_info(plant_id):

    plant = PLANTS.get(plant_id)

    if not plant:
        return jsonify({
            "success": False,
            "message": "Plant not found."
        }), 404

    return jsonify({
        "success": True,
        "plant": plant
    })


# --------------------------------------------------
# AI ASSISTANT
# --------------------------------------------------

@app.route("/api/ask", methods=["POST"])
def ask_ai():

    data = request.get_json()

    question = data.get(
        "question",
        ""
    ).lower().strip()

    plant_id = data.get(
        "plant",
        "tomato"
    )

    plant = PLANTS.get(
        plant_id,
        PLANTS["tomato"]
    )

    if not question:
        return jsonify({
            "answer":
                "Please ask something about the plant, soil or disease."
        })

    if "soil" in question:

        answer = (
            f"For {plant['name']}, start with well-drained soil "
            f"and maintain suitable moisture. "
            f"{plant['soil']}"
        )

    elif "water" in question:

        answer = (
            f"Watering advice for {plant['name']}: "
            f"{plant['water']}"
        )

    elif (
        "medicine" in question
        or "medical" in question
        or "health" in question
    ):

        answer = (
            f"{plant['name']} information: "
            f"{plant['medical']} "
            "Traditional or recorded plant use should not be treated "
            "as a diagnosis or substitute for professional medical advice."
        )

    elif "disease" in question:

        answer = (
            f"Commonly listed diseases/issues for {plant['name']} "
            f"include: {', '.join(plant['diseases'])}. "
            "A photograph alone cannot reliably confirm every disease."
        )

    elif "sun" in question:

        answer = (
            f"Sunlight information: {plant['sun']}"
        )

    elif (
        "care" in question
        or "cure" in question
        or "treatment" in question
    ):

        answer = (
            f"Basic care for {plant['name']}: "
            "monitor soil moisture, provide suitable light, "
            "remove severely affected plant material and improve "
            "air circulation. For serious crop disease, consult "
            "a local agricultural expert."
        )

    else:

        answer = (
            f"{plant['name']} ({plant['scientific']}) — "
            f"{plant['description']} "
            f"Common issues include {', '.join(plant['diseases'])}. "
            "You can also open the Plant Information section for "
            "soil, water and recorded-use information."
        )

    return jsonify({
        "answer": answer
    })


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

if __name__ == "__main__":
    print("")
    print("======================================")
    print("       SMART PLANT AI")
    print("======================================")
    print("Server starting...")
    print("Open: http://127.0.0.1:5000")
    print("======================================")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )