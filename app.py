from flask import Flask, jsonify #Flask je klasa u falask frameworku a jsonify 
                                #je funkcija koja konvertuje podatke u JSON format
from gpt_client import GPTClient
 
app = Flask(__name__) #kreira instancu Flask aplikacije
gpt = GPTClient() #kreira instancu GPTClient klase

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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
