# ==========================================================
# 🌸 Suganya P | PM Portfolio Website
# Author: Suganya P
# Purpose: Flask backend for personal portfolio website (Render Ready)
# ==========================================================

from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
import os, json

# ==========================================================
# ⚙️ APP INITIALIZATION
# ==========================================================
app = Flask(__name__, static_folder='assets', static_url_path='/static')
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")  # Required for session handling

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
# 🏠 MAIN ROUTES
# ==========================================================
@app.route('/')
def home():
    visits = update_visits()
    return render_template('index.html', visits=visits)

@app.route('/projects')
def projects():
    visits = get_visits()
    return render_template('projects.html', visits=visits)

@app.route('/education')
def education():
    visits = get_visits()
    return render_template('education.html', visits=visits)

@app.route('/governance')
def governance():
    visits = get_visits()
    return render_template('governance.html', visits=visits)

# ==========================================================
# 📂 PDF SERVING ROUTES
# ==========================================================
@app.route('/pdfs/<path:filename>')
def serve_pdf(filename):
    pdf_dir = os.path.join(app.root_path, 'assets', 'pdfs')
    return send_from_directory(pdf_dir, filename)

@app.route('/pdfs/governance/<path:filename>')
def serve_governance_pdf(filename):
    pdf_dir = os.path.join(app.root_path, 'assets', 'pdfs', 'governance')
    return send_from_directory(pdf_dir, filename)

@app.route('/view_resume')
def view_resume():
    pdf_dir = os.path.join(app.root_path, 'assets', 'pdfs')
    return send_from_directory(pdf_dir, 'resume.pdf')

# ==========================================================
# 💬 FEEDBACK SYSTEM (LOCAL STORAGE ONLY)
# ==========================================================
FEEDBACK_FILE = os.path.join(app.root_path, 'assets', 'data', 'feedback.json')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """Handles feedback submission and saves locally."""
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)

    # Load existing feedback data
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

    # Save locally
    feedback_data.append(new_entry)
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_data, f, indent=2)

    print("✅ Feedback saved locally.")
    return redirect(url_for('thank_you'))

# ==========================================================
# 🙏 THANK YOU PAGE
# ==========================================================
@app.route('/thankyou')
def thank_you():
    """Renders a Thank You page after feedback submission."""
    return render_template('thankyou.html')

# ==========================================================
# 🔒 ADMIN LOGIN & FEEDBACK VIEWER
# ==========================================================
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """Secure login for admin to view feedback."""
    ADMIN_KEY = os.environ.get('ADMIN_KEY', 'MuruganBlessMeAlways')
    print("🔍 Loaded ADMIN_KEY:", ADMIN_KEY)

    if request.method == 'POST':
        password = request.form.get('password').strip()
        print("🧩 Entered Password:", password)  # log what came from form
        if password == ADMIN_KEY:
            session['admin'] = True
            return redirect(url_for('view_feedback'))
        else:
            return "<h3 style='color:red; text-align:center;'>⚠️ Wrong password! Try again.</h3>"

    return '''
        <div style="text-align:center; margin-top:80px; font-family:Poppins; color:#fff; 
                    background:linear-gradient(160deg, #0A1930 0%, #1E3A8A 100%);
                    padding:40px; border-radius:12px; width:60%; margin:auto; box-shadow:0 0 15px rgba(130,207,255,0.3);">
            <h2>🔐 Admin Login</h2>
            <form method="POST" action="/admin-login">
                <input type="password" name="password" placeholder="Enter Admin Key"
                style="padding:8px; border-radius:6px; border:none; margin-top:10px; width:60%;
                       background:rgba(255,255,255,0.15); color:#fff; text-align:center;" required>
                <br><br>
                <button type="submit"
                style="padding:8px 16px; border-radius:8px; background:linear-gradient(135deg,#1e4fff,#537cff);
                       color:white; border:none; cursor:pointer;">Login</button>
            </form>
        </div>
    '''


@app.route('/view_feedback')
def view_feedback():
    """Displays feedback entries only if admin is logged in."""
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if not os.path.exists(FEEDBACK_FILE):
        return "<h3 style='color:#fff; text-align:center;'>No feedback found yet 🌸</h3>"

    with open(FEEDBACK_FILE, 'r') as f:
        feedback_data = json.load(f)

    # 🌸 Styled feedback dashboard
    feedback_html = """
    <div style="font-family:Poppins; background:linear-gradient(180deg,#061A3A,#0B2B5C);
                color:#fff; padding:40px; border-radius:12px; width:80%; margin:auto; 
                box-shadow:0 0 25px rgba(130,207,255,0.3);">
        <h2 style='text-align:center; color:#82cfff;'>💬 Collected Feedback</h2>
        <hr style='border-color:#537cff;'>
    """
    for entry in feedback_data:
        feedback_html += f"""
        <div style="background:rgba(255,255,255,0.08); margin:15px 0; padding:15px; border-radius:10px;
                    box-shadow:0 2px 10px rgba(66,133,244,0.2); transition:transform 0.3s;">
            <p><strong>{entry['name']}</strong> ({entry['email']})</p>
            <p style='color:#d9e7ff;'>🌸 {entry['feedback']}</p>
        </div>
        """
    feedback_html += """
        <hr style='border-color:#537cff;'>
        <div style='text-align:center;'>
            <a href='/' style='color:#82cfff; text-decoration:none;'>⬅ Back to Home</a> |
            <a href='/logout' style='color:#ffb6d6; text-decoration:none;'>Logout 🔒</a>
        </div>
    </div>
    """
    return feedback_html

@app.route('/logout')
def logout():
    """Clears admin session."""
    session.pop('admin', None)
    return redirect(url_for('home'))

# ==========================================================
# 🚀 RUN FLASK SERVER (LOCAL / RENDER)
# ==========================================================
if __name__ == '__main__':
    app.run(debug=True)
