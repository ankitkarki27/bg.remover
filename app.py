from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return "No file uploaded", 400

    file = request.files["image"]
    if file.filename == "":
        return "No file selected", 400

    input_image = Image.open(file.stream).convert("RGBA")

    # Process image
    output_image = remove(input_image)

    # Save result in memory
    img_io = io.BytesIO()
    output_image.save(img_io, "PNG")
    img_io.seek(0)

    # Option A: Direct Download
    return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="image.png")

    # Option B: Save on server and display in UI
    # output_path = os.path.join(UPLOAD_FOLDER, "output.png")
    # output_image.save(output_path, "PNG")
    # return render_template("index.html", result_image=output_path)

if __name__ == "__main__":
    app.run(debug=True)
