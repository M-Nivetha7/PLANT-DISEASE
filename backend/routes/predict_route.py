from flask import Blueprint, request, jsonify, render_template, current_app
import os
from config import UPLOAD_FOLDER
from ml.predict import predict_disease
from database.db import get_connection
import shutil

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    # Accept file under 'image' (frontend) or 'file' (older form)
    if "image" in request.files:
        file = request.files["image"]
    elif "file" in request.files:
        file = request.files["file"]
    else:
        return jsonify({"error": "No file part in request"}), 400

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Ensure upload folder exists
    if not os.path.isabs(UPLOAD_FOLDER):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        upload_folder = os.path.join(base_dir, "..", UPLOAD_FOLDER)
        upload_folder = os.path.normpath(upload_folder)
    else:
        upload_folder = UPLOAD_FOLDER

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    result = predict_disease(filepath)

    conn = get_connection()
    conn.execute(
        "INSERT INTO predictions (filename, disease, confidence, status) VALUES (?, ?, ?, ?)",
        (file.filename, result["disease"], result["confidence"], result["status"])
    )
    conn.commit()
    conn.close()

    # If client prefers HTML (browser form submit), render the template for user
    best = request.accept_mimetypes.best_match(["application/json", "text/html"])
    prefers_html = best == "text/html" and request.accept_mimetypes["text/html"] >= request.accept_mimetypes["application/json"]

    if prefers_html:
        # Ensure static/uploads exists and copy file there for template display
        static_uploads = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "uploads")
        static_uploads = os.path.normpath(static_uploads)
        os.makedirs(static_uploads, exist_ok=True)
        dest_path = os.path.join(static_uploads, file.filename)
        try:
            shutil.copy(filepath, dest_path)
        except Exception:
            # non-critical; continue to render even if copy fails
            dest_path = filepath

        return render_template(
            "index.html",
            prediction=result.get("disease") if result else None,
            confidence=result.get("confidence") if result else None,
            image_path=f"static/uploads/{file.filename}"
        )

    return jsonify(result)