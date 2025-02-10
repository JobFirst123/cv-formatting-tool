from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "CV Formatting Tool is Running!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
