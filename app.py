# ==========================================================
# 🌸 Suganya P | PM Portfolio Website
# Author: Suganya P
# Purpose: Flask backend for personal portfolio website
# ==========================================================

from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os, json

# ==========================================================
# ⚙️ APP INITIALIZATION
# ==========================================================
app = Flask(__name__, static_folder='assets', static_url_path='/static')

# ==========================================================
# 📊 VISITOR COUNTER
# ==========================================================
VISIT_FILE = os.path.join(app.root_path, 'assets', 'data', 'visits.json')

def get_visits():
    """Reads total visit count from JSON file."""
    if not os.path.exists(VISIT_FILE):
        os.makedirs(os.path.dirname(VISIT_FILE), exist_ok=True)
        with open(VISIT_FILE, 'w') as f:
            json.dump({"count": 0}, f)
    with open(VISIT_FILE, 'r') as f:
        return json.load(f).get("count", 0)

def update_visits():
    """Increments visit count and updates the JSON file."""
    count = get_visits() + 1
    with open(VISIT_FILE, 'w') as f:
        json.dump({"count": count}, f)
    return count

# ==========================================================
# 🏠 HOMEPAGE
# ==========================================================
@app.route('/')
def home():
    visits = update_visits()
    return render_template('index.html', visits=visits)

# ==========================================================
# 💼 PROJECTS PAGE
# ==========================================================
@app.route('/projects')
def projects():
    visits = get_visits()
    return render_template('projects.html', visits=visits)

# ==========================================================
# 🎓 EDUCATION PAGE
# ==========================================================
@app.route('/education')
def education():
    visits = get_visits()
    return render_template('education.html', visits=visits)

# ==========================================================
# 🧭 GOVERNANCE PAGE
# ==========================================================
@app.route('/governance')
def governance():
    visits = get_visits()
    return render_template('governance.html', visits=visits)

# ==========================================================
# 📂 SERVE PROJECT PDFS
# ==========================================================
@app.route('/pdfs/<path:filename>')
def serve_pdf(filename):
    pdf_dir = os.path.join(app.root_path, 'assets', 'pdfs')
    return send_from_directory(pdf_dir, filename)

# ==========================================================
# 🧾 GOVERNANCE PDF VIEWER
# ==========================================================
@app.route('/pdfs/governance/<path:filename>')
def serve_governance_pdf(filename):
    pdf_dir = os.path.join(app.root_path, 'assets', 'pdfs', 'governance')
    return send_from_directory(pdf_dir, filename)

# ==========================================================
# 💬 FEEDBACK SUBMISSION (Floating Widget)
# ==========================================================
FEEDBACK_FILE = os.path.join(app.root_path, 'assets', 'data', 'feedback.json')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """Handles feedback submission from floating widget and saves to JSON."""
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)

    # Load existing feedback
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            feedback_data = json.load(f)
    else:
        feedback_data = []

    # Extract fields from form (correct names from HTML)
    name = request.form.get('name', 'Anonymous')
    email = request.form.get('email', '')
    feedback_message = request.form.get('feedback', '')

    new_entry = {
        "name": name,
        "email": email,
        "feedback": feedback_message
    }

    feedback_data.append(new_entry)

    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_data, f, indent=2)

    # Redirect to thank you page
    return redirect(url_for('thank_you'))
# ==========================================================
# 🙏 THANK YOU PAGE
# ==========================================================
@app.route('/thankyou')
def thank_you():
    """Renders a Thank You page after feedback submission."""
    return render_template('thankyou.html')

# ==========================================================
# 🚀 RUN FLASK SERVER
# ==========================================================
if __name__ == '__main__':
    app.run(debug=True)
