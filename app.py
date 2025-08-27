from flask import Flask, jsonify, request, send_from_directory
#Flask je klasa u falask frameworku a jsonify 
#je funkcija koja konvertuje podatke u JSON format
from gpt_client import GPTClient
from werkzeug.utils import secure_filename
import os

app = Flask(__name__) #kreira instancu Flask aplikacije
gpt = GPTClient() #kreira instancu GPTClient klase

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=False)

@app.get("/ask/<path:question>") #definiše rutu koja prima GET zahteve sa dinamičkim delom u URL-u
def ask(question: str):
    try:
        answer = gpt.ask(question) #poziva metodu ask iz GPTClient klase
        return jsonify({
            "question": question,
            "answer": answer
        }), 200
    except Exception as e:
        return jsonify({
            "error": "GPT call failed",
            "details": str(e)
        }), 500

@app.get("/ask_with_prompt/<path:prompt>/<path:question>")
def ask_with_prompt(prompt: str, question: str):
    try:
        answer = gpt.ask_with_prompt(question, prompt)
        return jsonify({
            "prompt": prompt,
            "question": question,
            "answer": answer
        }), 200
    except Exception as e:
        return jsonify({
            "error": "GPT call failed",
            "details": str(e)
        }), 500

@app.post("/vision")
def vision():
    try:
        if "image" not in request.files:
            return jsonify({"error": "Nisi poslao fajl. Pošalji 'image' u multipart/form-data."}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "Prazno ime fajla."}), 400

        # Sačuvaj fajl u uploads/ sa bezbednim imenom
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_DIR, filename)
        file.save(save_path)

        # Napravi PUNI URL do tog fajla
        # npr. http://127.0.0.1:5000/uploads/SlikaZaTest.jpg
        base = os.getenv("PUBLIC_BASE_URL") or request.host_url.rstrip("/")
  # http://127.0.0.1:5000
        image_url = f"{base}/uploads/{filename}"

        prompt = request.form.get("prompt", "Šta je na ovoj slici?")

        # Pozovi vision preko URL-a (STRING!)
        answer = gpt.describe_image_url(image_url, prompt)

        return jsonify({
            "prompt": prompt,
            "image_url": image_url,
            "answer": answer
        }), 200

    except Exception as e:
        return jsonify({"error": "Vision call failed", "details": str(e)}), 500

# from flask import Flask, jsonify, request  # <- već imaš

@app.post("/vision_json")
def vision_json():
    try:
        data = request.get_json(silent=True)  # Body: raw JSON
        if not data:
            return jsonify({"error": "Pošalji JSON u body-ju."}), 400

        image_url = data.get("image_url")
        prompt = data.get("prompt", "Šta je na ovoj slici?")

        if not image_url:
            return jsonify({"error": "Nedostaje 'image_url' u JSON-u."}), 400

        # Važno: mora biti JAVNI, DIREKTAN URL slike (npr. .jpg / .png), ne Google search stranica
        answer = gpt.describe_image_url(image_url, prompt)

        return jsonify({
            # "image_url": image_url,
            "prompt": prompt,
            "answer": answer
        }), 200

    except Exception as e:
        return jsonify({"error": "Vision call failed", "details": str(e)}), 500


if __name__ == "__main__":
    # # probni poziv vision metode sa javnim URL-om
    # test_answer = gpt.describe_image_url(
    #     "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nqlLiEAuxdgfpJILCS_hgcdy7P3G7t5bE2FvIdf-4sYkS7sa7ZTMk0hsjJ3oQ15y4bMsPVZbAajy0ovKpNVszpfwzbpSs72IdjOuiymVNkAKzk6ijC1gaD5Ei-8Ydr_bd9yNrqU=s1360-w1360-h1020-rw",
    #     "Objasni mi detaljno šta je na slici"
    # )
    # print(">>> Vision odgovor:", test_answer)

    app.run(host="127.0.0.1", port=5000, debug=True)

