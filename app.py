from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Claves de API
SERPAPI_KEY = "7ecd9462c7a387f5ff3d026465396000b3f7c700656012f5a7e8a805a7dba5ff"
DEEPAI_API_KEY = "03d85b95-bd4f-475c-9869-913de021cdd6"

SERPAPI_URL = "https://serpapi.com/search"
DEEPAI_URL = "https://api.deepai.org/api/text2img"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Busca imágenes de tatuajes en Google usando SerpAPI."""
    try:
        data = request.json
        query = data.get("query", "realistic tattoo design")

        params = {
            "q": query,
            "tbm": "isch",
            "api_key": SERPAPI_KEY
        }

        response = requests.get(SERPAPI_URL, params=params)
        
        if response.status_code != 200:
            return jsonify({"error": "Error en la búsqueda de imágenes"}), 500

        results = response.json()
        images = [img["original"] for img in results.get("images_results", [])[:8]]

        return jsonify({"images": images})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error de conexión con SerpAPI: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Excepción en búsqueda: {str(e)}"}), 500

@app.route('/generate', methods=['POST'])
def generate():
    """Genera un tatuaje realista basado en el diseño seleccionado."""
    try:
        data = request.json
        height = data.get("height", "")
        weight = data.get("weight", "")

        if not height or not weight:
            return jsonify({"error": "Faltan datos"}), 400

        # Prompt simplificado para evitar problemas con la API
        prompt = "Realistic black ink tattoo, inspired by Mayan warriors, detailed."

        headers = {"api-key": DEEPAI_API_KEY}
        response = requests.post(DEEPAI_URL, headers=headers, data={"text": prompt})

        print("Código de respuesta de DeepAI:", response.status_code)
        print("Respuesta de DeepAI:", response.json())

        if response.status_code == 200:
            json_response = response.json()
            if "output_url" in json_response:
                return jsonify({"image_url": json_response["output_url"]})
            else:
                return jsonify({"error": "DeepAI no devolvió una imagen válida."}), 500
        else:
            return jsonify({"error": f"Error en DeepAI: {response.text}"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error de conexión con DeepAI: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Excepción en generación: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
