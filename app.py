# ==========================================================
# 🌸 Suganya P | PM Portfolio Website
# Author: Suganya P
# Purpose: Flask backend for personal portfolio website
# ==========================================================

from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os, json, requests  # Added 'requests' for Google Sheets API call

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
GOOGLE_SHEET_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbzC0N9tH--UiUPiIN7aeDdMisOB3JCCpsvV4LKQyTvSdyGsQ8IMYQ_MCLfGCRbCAHWn/exec"

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """Handles feedback submission from the floating widget,
    saves locally, and also sends data to Google Sheets via Apps Script."""
    
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)

    # Load existing feedback from JSON
    feedback_data = []
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            feedback_data = json.load(f)

    # Extract form fields
    name = request.form.get('name', 'Anonymous')
    email = request.form.get('email', '')
    feedback_message = request.form.get('feedback', '')

    # Create feedback entry
    new_entry = {
        "name": name,
        "email": email,
        "feedback": feedback_message
    }

    # Save locally (backup)
    feedback_data.append(new_entry)
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_data, f, indent=2)

    # Send data to Google Sheet via Apps Script Web App
    try:
        response = requests.post(GOOGLE_SHEET_WEBAPP_URL, data=new_entry, timeout=5)
        if response.status_code == 200:
            print("✅ Feedback successfully sent to Google Sheets.")
        else:
            print(f"⚠️ Google Sheet logging failed. Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error sending feedback to Google Sheets: {e}")

    # Redirect to thank-you page
    return redirect(url_for('thank_you'))

# ==========================================================
# 🙏 THANK YOU PAGE
# ==========================================================
@app.route('/thankyou')
def thank_you():
    """Renders a Thank You page after feedback submission."""
    return render_template('thankyou.html')

# ==========================================================
# 📄 RESUME VIEW ROUTE (Opens in Browser)
# ==========================================================
@app.route('/view_resume')
def view_resume():
    """Opens the resume PDF directly in a new browser tab instead of downloading."""
    pdf_dir = os.path.join(app.root_path, 'assets', 'pdfs')
    return send_from_directory(pdf_dir, 'resume.pdf')

# ==========================================================
# 🚀 RUN FLASK SERVER
# ==========================================================
if __name__ == '__main__':
    app.run(debug=True)
