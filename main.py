# from flask import Flask, render_template, request
# import google.generativeai as genai

# app = Flask(__name__)
# genai.configure(api_key="AIzaSyBOgxan8GWoy78Ry2Ev2JnVY9PNkX_ljbs")  # Replace with your API key

# mymodel = genai.GenerativeModel("gemini-1.5-flash")
# chat = mymodel.start_chat()

# @app.route('/')
# def home():
#     return render_template('job_chat.html')  # Updated HTML filename

# @app.route('/send', methods=['POST', 'GET'])
# def submit():
#     uinput = request.form.get('user_input')
#     response = chat.send_message(f"Suggest job roles for skills: {uinput}")
#     return render_template('job_chat.html', user_input=uinput, message=response.text)

# if __name__ == "__main__":
#     app.run(debug=True)








from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key="AIzaSyAzOTxpzYqxx1f4cpy-duUcqdughHlktAQ")  # Replace with your actual API key

mymodel = genai.GenerativeModel("gemini-1.5-flash")
chat = mymodel.start_chat()

# Predefined domains and subdomains
domains = {
    "Full-Stack Development": ["Front-End", "Back-End","MERN Stack", "MEAN Stack", "DevOps"],
    "Data Science": ["Data Analysis", "Machine Learning", "Big Data"],
    "Graphic Design": ["Illustration", "Logo Design", "UI Design"],
    "Cyber Security": ["Network Security", "Ethical Hacking", "Cryptography", "SIEM Tools", "Penetration Testing"],
    "Networking": ["CCNA", "CCNP", "Network Security", "Wireless Networking", "Network Troubleshooting"],
    "System Administration": ["Linux Administration", "Windows Server", "VMware", "Cloud Systems"],
    "Embedded Systems": ["Arduino", "Raspberry Pi", "FPGA Programming", "Microcontrollers", "C Programming"],
    "IoT": ["IoT Protocols", "IoT Security", "IoT Development Tools", "Smart Devices"],
    "Design/Animation": ["Graphic Design","UI/UX Design","Product Design","Animation"],
    "Something Else": ["Marketing","Content Writing","HR","Sales"],
}

skills = {
    "Front-End": ["HTML/CSS", "JavaScript", "React", "Vue.js", " Angular","Responsive Design, Bootstrap","Version Control (Git)"],
    "Back-End": ["Node.js", "Django", "Flask", "Spring Boot","Ruby on Rails"],
    "DevOps": ["Docker, Kubernetes", "CI/CD Tools (Jenkins, Travis CI)", "Cloud Platforms (AWS, Azure, Google Cloud)", "Infrastructure as Code (Terraform, Ansible)"],
    "Data Analysis": ["Python", "R", "SQL", "TensorFlow", "Pandas", "Scikit-Learn"],
    "Graphic Design": ["Adobe Photoshop", "Illustrator", "CorelDRAW", "Canva"],
    "UI/UX Design": ["Figma", "Sketch", "Adobe XD", "Prototyping Tools", "Wireframing"],
    "Product Design": ["3D Modeling", "SolidWorks", "AutoCAD", "3D Printing"],
    "Animation": ["Blender", "Maya", "After Effects", "2D Animation", "3D Animation"],
    "Marketing": ["Digital Marketing", "SEO", "Social Media Marketing", "Google Ads"],
    "Content Writing": ["Blog Writing", "Technical Writing", "Creative Writing", "Copywriting"],
    "HR": ["Recruitment", "Payroll Management", "Employee Engagement", "Conflict Resolution"],
    "Sales": ["B2B Sales", "B2C Sales", "CRM Tools", "Cold Calling"]
}

@app.route('/')
def welcome():
    return render_template('Welcome.html')

@app.route('/start')
def start():
    return render_template('job_chat.html', domains=domains.keys())

@app.route('/domain', methods=['POST'])
def get_subdomains():
    user_domain = request.form.get('domain')
    subdomains = domains.get(user_domain, [])
    return render_template('job_chat.html', user_domain=user_domain, subdomains=subdomains)

@app.route('/subdomain', methods=['POST'])
def get_skills():
    user_domain = request.form.get('user_domain')
    user_subdomain = request.form.get('subdomain')
    skill_options = skills.get(user_subdomain, [])
    return render_template('job_chat.html', user_domain=user_domain, user_subdomain=user_subdomain, skills=skill_options)

@app.route('/recommend', methods=['POST'])
def recommend_jobs():
    user_domain = request.form.get('user_domain')
    user_subdomain = request.form.get('user_subdomain')
    user_skills = request.form.getlist('skills')

    # Generate tailored recommendations
    prompt = (
        f"The user is interested in {user_domain}, specifically {user_subdomain}. "
        f"They are skilled in {', '.join(user_skills)}. "
        "Generate 3 job recommendations tailored to these skills. Suggest additional skills and resources for upskilling."
    )
    response = chat.send_message(prompt)

    # Clean and format the response for better readability
    recommendations = response.text.split("\n")
    recommendations = [line.strip() for line in recommendations if line.strip()]

    # Pass structured recommendations to the template
    return render_template(
        'job_chat.html',
        user_domain=user_domain,
        user_subdomain=user_subdomain,
        user_skills=user_skills,
        message=recommendations
    )



if __name__ == "__main__":
    app.run(debug=True)


