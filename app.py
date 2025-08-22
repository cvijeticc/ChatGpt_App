from flask import Flask, jsonify
from gpt_client import GPTClient

app = Flask(__name__)
gpt = GPTClient()

@app.get("/ask/<path:question>")
def ask(question: str):
    try:
        answer = gpt.ask(question)
        return jsonify({
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
