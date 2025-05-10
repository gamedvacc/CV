import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="CV Generator", layout="centered")

st.title("📄 CV Generator (Urdu + English)")
language = st.radio("Select Language / زبان منتخب کریں", ("English", "اردو"))

# Translations (simple toggle)
def _(en, ur):
    return ur if language == "اردو" else en

st.markdown(_(
    "Please fill the form below to generate your professional CV.",
    "براہ کرم نیچے فارم پُر کریں تاکہ آپ کا پروفیشنل سی وی تیار ہو سکے۔"
))

with st.form("cv_form"):
    name = st.text_input(_("Full Name", "پورا نام"))
    job_title = st.text_input(_("Job Title", "عہدہ"))
    email = st.text_input(_("Email", "ای میل"))
    phone = st.text_input(_("Phone Number", "فون نمبر"))
    linkedin = st.text_input(_("LinkedIn URL", "لنکڈ اِن لنک"))
    experience_years = st.number_input(_("Total Experience (Years)", "کل تجربہ (سال)"), 0, 50)
    education = st.text_input(_("Highest Education", "اعلیٰ تعلیم"))
    current_company = st.text_input(_("Current Company", "موجودہ کمپنی"))
    skills = st.text_area(_("Skills (comma separated)", "مہارتیں (کاما لگا کر لکھیں)"))
    achievements = st.text_area(_("Key Achievements (one per line)", "اہم کامیابیاں (ہر سطر میں ایک)"))
    summary = st.text_area(_("Profile Summary (Optional)", "پروفائل خلاصہ (اختیاری)"))

    submitted = st.form_submit_button(_("Generate CV", "سی وی تیار کریں"))

def generate_summary(name, title, years, company):
    if language == "اردو":
        return f"میرا نام {name} ہے۔ میں ایک {title} ہوں اور مجھے {years} سال کا تجربہ ہے۔ میں اس وقت {company} میں کام کر رہا ہوں۔ میں محنتی ہوں، ٹیم کے ساتھ اچھا کام کرتا ہوں، اور ہمیشہ بہتر نتائج دینے کی کوشش کرتا ہوں۔"
    else:
        return f"My name is {name}. I am a {title} with over {years} years of experience. Currently, I work at {company}. I am skilled, work well with others, and always try to deliver my best."

# --- PDF Generation ---
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, name, ln=True, align="C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, title, ln=True, fill=True)

    def chapter_body(self, body):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, body)
        self.ln()

    def add_section(self, title, body):
        self.chapter_title(title)
        self.chapter_body(body)

if submitted:
    cv_summary = summary if summary else generate_summary(name, job_title, experience_years, current_company)

    st.subheader(_("📄 Your CV Preview:", "📄 آپ کا سی وی پیش نظارہ:"))
    st.markdown(f"**{_('Name','نام')}:** {name}")
    st.markdown(f"**{_('Job Title','عہدہ')}:** {job_title}")
    st.markdown(f"**{_('Email','ای میل')}:** {email} | **{_('Phone','فون')}:** {phone}")
    st.markdown(f"**LinkedIn:** {linkedin}")
    st.markdown(f"### {_('Profile Summary','پروفائل خلاصہ')}")
    st.write(cv_summary)
    st.markdown(f"### {_('Skills','مہارتیں')}")
    st.write(", ".join([s.strip() for s in skills.split(",")]))
    st.markdown(f"### {_('Key Achievements','اہم کامیابیاں')}")
    st.write(achievements)
    st.markdown(f"### {_('Education','تعلیم')}")
    st.write(education)
    st.markdown(f"### {_('Current Company','موجودہ کمپنی')}")
    st.write(current_company)
    st.markdown(f"### {_('Experience','تجربہ')}")
    st.write(f"{experience_years} {_('Years','سال')}")

    pdf = PDF()
    pdf.add_page()
    pdf.add_section(_("Profile Summary", "پروفائل خلاصہ"), cv_summary)
    pdf.add_section(_("Skills", "مہارتیں"), ", ".join([s.strip() for s in skills.split(",")]))
    pdf.add_section(_("Key Achievements", "اہم کامیابیاں"), achievements)
    pdf.add_section(_("Education", "تعلیم"), education)
    pdf.add_section(_("Current Company", "موجودہ کمپنی"), current_company)
    pdf.add_section(_("Experience", "تجربہ"), f"{experience_years} {_('Years','سال')}")
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, f"{_('Generated on','تاریخ')}: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True)

    pdf_file = "generated_cv.pdf"
    pdf.output(pdf_file)

    with open(pdf_file, "rb") as f:
        st.download_button(_("📥 Download CV as PDF", "📥 سی وی PDF میں ڈاؤن لوڈ کریں"), f, file_name="My_CV.pdf", mime="application/pdf")
