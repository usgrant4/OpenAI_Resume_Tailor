# Resume Tailoring with OpenAI

This project automates the process of **tailoring a resume** to specific job descriptions using the OpenAI API.  
It converts resumes from **Markdown** (or PDF) into a recruiter-friendly Markdown format, optimized with keywords and skills relevant to a provided job description.

---

## 📂 Project Structure

```

resume-tailor/
├── resume/
│   ├── Ulysses\_Grant.md          # Original resume in Markdown
│   ├── job\_description.md        # Target job description in Markdown
│   └── Ulysses\_Grant\_Tailored.md # Auto-generated tailored resume
├── tailor\_resume.py              # Main script for tailoring
├── convert\_pdf\_to\_md\_resume.py   # Optional: Convert PDF → Markdown + tailor
├── .gitignore
└── README.md

````

---

## 🚀 Features
- Supports **Markdown resumes** directly.  
- Can extract text from **PDF resumes** using `pdfplumber`.  
- Uses **OpenAI GPT-5** (default `gpt-5-turbo`) to rewrite and tailor resumes.  
- Emphasizes **relevant skills, experience, and achievements** based on the job description.  
- Outputs a clean **Markdown resume** ready for recruiters or further formatting.  

---

## ⚙️ Requirements

Install dependencies:
```bash
pip install pdfplumber python-dotenv openai
````

Create a `.env` file in the project root with your API key:

```env
OPENAI_API_KEY=sk-yourkeyhere
```

---

## 📝 Usage

### Tailor an existing Markdown resume

```bash
python tailor_resume.py \
  --resume-md ./resume/Ulysses_Grant.md \
  --jd ./resume/job_description.md \
  --out ./resume/Ulysses_Grant_Tailored.md
```

### Tailor a PDF resume (text will be extracted automatically)

```bash
python tailor_resume.py \
  --resume-pdf ./resume/Ulysses_S_Grant_IV.pdf \
  --jd ./resume/job_description.md \
  --out ./resume/Ulysses_Grant_Tailored.md
```

### Options

* `--model` → OpenAI model (default: `gpt-5-turbo`)
* `--temperature` → Creativity of output (default: `0.25`)
* `--out` → Output Markdown file path

---

## 📖 Example Workflow

1. Save your resume as `resume/Ulysses_Grant.md`.
2. Copy a job description into `resume/job_description.md`.
3. Run the script to generate a tailored resume.
4. Check the tailored output in `resume/Ulysses_Grant_Tailored.md`.

---

## 🔒 Notes

* `.env` is ignored by Git for security.
* Never commit your OpenAI API key.
* Markdown output can be further converted to **PDF** or **Word** using tools like Pandoc.

---

## 📌 Roadmap

* [ ] Add export to PDF/DOCX.
* [ ] Create GitHub Action for one-click tailoring.
* [ ] Add support for multiple job descriptions in batch mode.

---

## 🧑‍💻 Author

**Ulysses Grant, IV**

* [LinkedIn](https://www.linkedin.com/in/usgrant4/)
* [GitHub](https://github.com/usgrnt4)

```
