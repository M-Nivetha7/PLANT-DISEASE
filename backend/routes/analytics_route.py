from flask import Blueprint, jsonify, render_template, request
from database.db import get_connection

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics", methods=["GET"])
def analytics():
    conn = get_connection()
    data = conn.execute("SELECT disease, COUNT(*) as count FROM predictions GROUP BY disease").fetchall()
    conn.close()

    rows = [dict(row) for row in data]

    # Content negotiation: if browser requests HTML, render the template
    best = request.accept_mimetypes.best_match(["application/json", "text/html"])
    prefers_html = best == "text/html" and request.accept_mimetypes["text/html"] >= request.accept_mimetypes["application/json"]

    if prefers_html:
        # Render the backend template (static-ish dashboard)
        # Provide simple aggregate data to template
        total = sum(r.get("count", 0) for r in rows)
        healthy = sum(r.get("count", 0) for r in rows if "Healthy" in r.get("disease", ""))
        diseased = total - healthy
        return render_template("analytics.html", total=total, healthy=healthy, diseased=diseased, rows=rows)

    return jsonify(rows)