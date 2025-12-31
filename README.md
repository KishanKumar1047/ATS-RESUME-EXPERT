# 📄 ATS Resume Scoring System (Gemini AI)

An AI-powered **ATS (Applicant Tracking System) Resume Analyzer** built using **Streamlit** and **Google Gemini**.  
It evaluates resumes against a job description, calculates an ATS-style score, identifies missing keywords, and provides a concise profile summary.

---

## 🚀 Features

- 📊 **ATS Resume Score (/100)**
- 🎯 **JD Match Percentage**
- 🧩 **Missing Keywords Detection**
- 📝 **AI-Generated Profile Summary**
- 📎 **PDF Resume Upload**
- 🔐 **Secure API Key Handling (.env)**
- 🧠 **Robust JSON Parsing (Production-Safe)**

---

## 🛠️ Tech Stack

- **Python 3.10**
- **Streamlit**
- **Google Gemini (google-generativeai)**
- **PyPDF2**
- **dotenv**
- **Regex-based JSON extraction**

---

## 📂 Project Structure

```

ATS-Resume-Scorer/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

````

---

## 🔑 Environment Setup

### 1️⃣ Create `.env` file
```env
GOOGLE_API_KEY=your_gemini_api_key_here
````

> ⚠️ Never commit `.env` to GitHub.
> `.env` is already added to `.gitignore`.

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run the App

```bash
streamlit run app.py
```

---

## 📈 Resume Scoring Logic

```
Resume Score = JD Match %
Penalty = min(Missing Keywords × 2, 20)
Final Score = max(JD Match − Penalty, 0)
```

This mimics how real ATS systems penalize missing skills while keeping scores fair.

---

## 🧪 Example Output

* **JD Match:** 85%
* **Resume Score:** 81 / 100
* **Missing Keywords:** Docker, AWS, System Design
* **Profile Summary:** AI-generated professional summary

---

## 🔒 Security Best Practices

* `.env` is excluded via `.gitignore`
* `.env.example` is included for reference
* API keys are accessed using `os.getenv()`
* Keys should be rotated immediately if exposed

---

## 🚀 Future Enhancements

* Skill-wise scoring (Python, ML, SQL, etc.)
* Resume auto-improvement suggestions
* PDF export of ATS report
* Multi-resume comparison
* Role-based scoring (Fresher / Senior)

---

## 👤 Author

**Kishan Kumar**
GitHub: [kishankumar1047](https://github.com/kishankumar1047)

---

## 📜 License

This project is for **educational and portfolio purposes**.
You are free to modify and extend it.

---

⭐ If you found this project helpful, consider starring the repository!

```

---

If you want, I can also:
- Write a **GitHub project description**
- Add **badges** (Python, Streamlit, Gemini)
- Create a **portfolio-ready README version**
- Add **deployment steps (Streamlit Cloud)**

Just tell me 🚀
```
