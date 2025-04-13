import streamlit as st
import json
import google.generativeai as genai
import urllib.parse
import zlib
import random
import matplotlib.pyplot as plt

# ✅ Gemini API Setup
GEMINI_API_KEY = "AIzaSyCEs0-0RsygY8XgP-xDB6NXwEqZuU3uefc"
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Career Roadmap Generation
def generate_career_roadmap(profile_data):
    prompt = f"""
You are a friendly career guide assistant.

Generate a roadmap in friendly and structured format for the following user:

👤 Name: {profile_data['name']}
🎓 Education: {profile_data['education']}
🛠️ Skills: {', '.join(profile_data['skills'])}
📍 Experience: {profile_data['experience']}

📚 Courses Completed:
"""
    for course in profile_data['courses']:
        prompt += f"- {course['course_name']} (Marks: {course['marks']}, Date: {course['date']})\n"

    prompt += """

Now, do the following:

1. Greet the user.
2. Describe their education & give a positive/neutral assessment of it.
3. Analyze their skills and tell if they are sufficient, average, or need improvement.
4. Discuss the work experience, and optionally provide real-life quotes/examples where such experience is valued.
5. Analyze completed courses and recommend 2–3 more relevant courses they can take.
6. Suggest a personalized career path: job roles they can target, required skills/certifications, and industries.
7. Give an approximate 6-month action plan with timelines.
8. End with a motivational note.
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# ✅ PlantUML Helpers
def deflate_and_encode(plantuml_text):
    zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return encode64(compressed_string)

def encode64(data):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    encoded = ""
    b = 0
    bits = 0
    for byte in data:
        b = (b << 8) | byte
        bits += 8
        while bits >= 6:
            bits -= 6
            encoded += alphabet[(b >> bits) & 0x3F]
    if bits > 0:
        encoded += alphabet[(b << (6 - bits)) & 0x3F]
    return encoded

# ✅ Motivational Quotes
quotes = [
    "Believe in yourself – you are capable of amazing things.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Your journey is unique. Embrace it with pride!",
    "Dream big, start small, act now.",
    "Every expert was once a beginner."
]

# ✅ Streamlit Layout
st.set_page_config(page_title="Career Roadmap Generator", layout="wide")
st.sidebar.title("📂 Options")
st.sidebar.markdown("Use the options below to interact:")

show_roadmap = st.sidebar.checkbox("📌 Show Roadmap", value=True)
show_chart = st.sidebar.checkbox("📊 Show Skill/Course Chart", value=True)
show_uml = st.sidebar.checkbox("🌐 Show Career Diagram", value=True)
show_quote = st.sidebar.checkbox("💡 Quote of the Day", value=True)

# ✅ Load Profile
profile_path = "user_profile.json"
with open(profile_path, 'r') as f:
    profile_data = json.load(f)

st.title("🚀 Personalized Career Roadmap Generator")
st.success(f"Profile loaded for **{profile_data['name']}** from `{profile_path}`")

# ✅ Roadmap Text
if show_roadmap:
    with st.spinner("Generating your personalized roadmap..."):
        roadmap_text = generate_career_roadmap(profile_data)

    st.markdown("## 🎯 Your Career Roadmap")
    st.markdown(roadmap_text)

    file_name = f"career_roadmap_for_{profile_data['name'].replace(' ', '_')}.txt"
    st.download_button("📄 Download Roadmap", roadmap_text, file_name, mime="text/plain")

# ✅ Chart: Skills vs Courses
if show_chart:
    st.subheader("📈 Skills vs Courses Distribution")

    skill_labels = profile_data["skills"]
    course_labels = [c["course_name"] for c in profile_data["courses"]]

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    ax[0].pie([1]*len(skill_labels), labels=skill_labels, startangle=140, autopct='%1.1f%%')
    ax[0].set_title("Skills")

    ax[1].pie([1]*len(course_labels), labels=course_labels, startangle=140, autopct='%1.1f%%')
    ax[1].set_title("Courses")

    st.pyplot(fig)

# ✅ UML Diagram
if show_uml:
    plantuml_code = """
    @startuml
    skinparam backgroundColor #FFFFFF
    skinparam defaultFontSize 14
    skinparam node {
        BackgroundColor white
        BorderColor black
        FontSize 14
    }
    skinparam ArrowColor #4B8BBE

    title Career Roadmap - Month-wise 🎯

    start

    :🎓 Jan: Education Completed\nBA Sociology;

    note right
    "You are here"
    end note

    :🛠️ Feb: Skill Analysis\nCommunication\nCustomer Service;

    :📚 Mar: Completed Courses\nDigital Literacy, Customer Support;

    :📦 Apr: Mini Projects\nCustomer Support Simulation;

    :🤝 May: Volunteering\nNGO Work (2 years);

    :💼 Jun: Internship\nRemote Support Internship;

    :🌐 Jul: Build Online Presence\nLinkedIn, Resume, Portfolio;

    :🧠 Aug: Learn Additional Skills\nCRM, Email Tools;

    split
        :🚀 Path 1:\nSocial Media Manager\n(Sept - Apply);
    split again
        :🤝 Path 2:\nCommunity Engagement Specialist\n(Sept - Apply);
    split again
        :📊 Path 3:\nResearch Assistant\n(Sept - Apply);
    split again
        :📞 Path 4:\nCustomer Success Specialist\n(Sept - Apply);
    endsplit

    :📝 Oct: Final Prep\nMock Interviews, Resume Boost;

    :🎉 Nov-Dec: Job Applications + Networking Events;

    stop
    @enduml
    """
    encoded = deflate_and_encode(plantuml_code)
    plantuml_url = f"http://www.plantuml.com/plantuml/png/{encoded}"

    st.subheader("🌐 Visual Career Map (PlantUML)")
    st.image(plantuml_url, caption="Branched Career Journey Diagram")

# ✅ Quote of the Day
if show_quote:
    st.sidebar.markdown("---")
    st.sidebar.subheader("💬 Quote of the Day")
    st.sidebar.info(random.choice(quotes))



