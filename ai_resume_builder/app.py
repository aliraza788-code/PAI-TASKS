from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
import openai
import pdfkit
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Set your OpenAI API Key
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def generate_ai_content(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",  # Fast and good model
            messages=[
                {"role": "system", "content": "You are an expert AI content writer. Write professionally, clearly and shortly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenRouter API error:", e)
        return "Content could not be generated. Please try again later."
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Form Data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        skills = request.form['skills']
        skills_list = [skill.strip() for skill in skills.split(',')]
        education = request.form['education']
        experience = request.form['experience']
        template_choice = request.form['template']

        # Image Upload
        image_file = request.files['photo']
        image_filename = None
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_filename = filename

        # NLP Clean Text
        combined_text = clean_text(f"{skills} {education} {experience}")

        # Generate AI Sections
        resume_content = generate_ai_content(f"Write a professional resume content based on: {combined_text}")
        about_me = generate_ai_content(f"Write a short 'About Me' section for resume based on: {skills} and {experience}")
        cover_letter = generate_ai_content(f"Write a professional cover letter for a candidate with skills: {skills} and experience: {experience}")

        return render_template(f"resume{template_choice}.html",
                                name=name,
                                email=email,
                                phone=phone,
                                skills_list=skills_list,
                                education=education,
                                experience=experience,
                                photo=image_filename,
                                resume_content=resume_content,
                                about_me=about_me,
                                cover_letter=cover_letter)
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_pdf():
    rendered_html = request.form['html']
    output_pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], 'resume.pdf')
    pdfkit.from_string(rendered_html, output_pdf_path)
    return send_file(output_pdf_path, as_attachment=True)
@app.route("/cover-letter", methods=['GET','POST'])
def cover_letter():
    # Sirf important fields user se aayi hongi
    user_name = "Ali Raza"
    user_email = "ali@example.com"
    user_phone = "+92-300-1234567"
    company_name = "Tech Solutions"
    position_name = "Web Developer"
    hiring_manager_name = "Mr. Ahmed"

    return render_template("cover_letter.html",
        name=user_name,
        address="Not Provided",  # Default value
        city_state_zip="Lahore, Punjab, 54000",  # Default value
        email=user_email,
        phone=user_phone,
        date="April 27, 2025",  # Default value (or generate dynamically)
        hiring_manager_name=hiring_manager_name,
        company_name=company_name,
        company_address="Not Provided",  # Default value
        company_city_state_zip="Lahore, Punjab, 54000",  # Default value
        position_name=position_name,
        job_listing_source="LinkedIn"  # Default value
    )

if __name__ == "__main__":
    app.run(debug=True)
