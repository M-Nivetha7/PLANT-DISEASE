import os
from flask import Flask, render_template
from flask_cors import CORS
from config import UPLOAD_FOLDER
from werkzeug.utils import secure_filename

# -------------------- APP SETUP --------------------

app = Flask(__name__)

# Use UPLOAD_FOLDER from config if present; fall back to static/uploads
if not os.path.isabs(UPLOAD_FOLDER):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    upload_folder_resolved = os.path.join(BASE_DIR, UPLOAD_FOLDER)
else:
    upload_folder_resolved = UPLOAD_FOLDER

app.config["UPLOAD_FOLDER"] = upload_folder_resolved

# Create uploads folder if not exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Enable CORS so frontend can call API
CORS(app)

# Register API blueprints (predict and analytics)
from routes.predict_route import predict_bp
from routes.analytics_route import analytics_bp
from database.models import create_table

app.register_blueprint(predict_bp)
app.register_blueprint(analytics_bp)

# Ensure database tables exist
create_table()


@app.route("/")
def home():
    return render_template("index.html")


# -------------------- RUN APP --------------------

if __name__ == "__main__":
    app.run(debug=True)