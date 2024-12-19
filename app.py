from flask import Flask, jsonify, request, render_template
from mamdani import mamdani

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/generate-price", methods=["POST"])
def gerneratePrice():
    if request.method == "POST":
        data = request.get_json()

        luas = data["luas"]
        jarak = data["jarak"]
        fasilitas = data["fasilitas"]

        hasil = mamdani(luas=luas, jarak=jarak, fasilitas=fasilitas)

        response = {"message": "success", "result": f"{hasil:.0f}"}

        return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
