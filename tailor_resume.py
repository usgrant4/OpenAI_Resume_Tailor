import argparse
import os
import sys
from typing import Optional

# --- Environment ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import openai  # pip install openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("openai_api_key")
if not OPENAI_API_KEY:
    sys.stderr.write("[warn] OPENAI_API_KEY not set; set it in env or .env\n")
openai.api_key = OPENAI_API_KEY

# --- Optional inline content (keeps parity with your original snippet) ---
# These can be set either to the literal Markdown text OR a path to a file
# If the value points to an existing file the script will read it; otherwise
# the value will be treated as the inline content.
md_resume: Optional[str] = "resume/Ulysses_Grant.md"   # Paste your Markdown resume here or set to a path like "resume/Ulysses_Grant.md"
job_description: Optional[str] = "resume/job_description.md"  # Paste JD here or set to a path like "job_description.md"

# --- Helpers ---
def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_pdf_text(pdf_path: str) -> str:
    try:
        import pdfplumber
    except ImportError as e:
        raise RuntimeError("Missing pdfplumber. Install with: pip install pdfplumber") from e

    parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            parts.append(p.extract_text() or "")
    text = "\n".join(parts).strip()
    if not text:
        raise RuntimeError("No text extracted from PDF (it may be image-based).")
    return text

def build_prompt(resume_md: str, jd: str) -> str:
    return f"""
I have a resume formatted in Markdown and a job description.
Please adapt my resume to better align with the job requirements while maintaining a professional tone.
Tailor my skills, experiences, and achievements to highlight the most relevant points for the position.
Use keywords and phrases from the job description where appropriate (no keyword stuffing).
Keep the resume concise, scannable, and metrics-oriented.
Return ONLY the updated resume in Markdown format.

### Here is my resume in Markdown:
{resume_md}

### Here is the job description:
{jd}
""".strip()

def call_openai(prompt: str, model: str = "gpt-5", temperature: float = 0.25) -> str:
    resp = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a meticulous resume editor who writes concise, professional Markdown tailored to the target role."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    return resp.choices[0].message.content

def resolve_inputs(args) -> tuple[str, str]:
    # Resolve resume Markdown
    resume_md = None
    if args.resume_md:
        resume_md = read_text(args.resume_md)
    elif args.resume_pdf:
        resume_md = extract_pdf_text(args.resume_pdf)
    elif md_resume:
        # If the module-level md_resume points to a file, read it; else treat it as content
        if os.path.isfile(md_resume):
            resume_md = read_text(md_resume)
        else:
            resume_md = md_resume
    else:
        sys.exit("[error] Provide --resume-md or --resume-pdf, or set md_resume variable in code.")

    # Resolve JD
    jd_text = None
    if args.jd:
        jd_text = read_text(args.jd)
    elif job_description:
        # If the module-level job_description points to a file, read it; else treat it as content
        if os.path.isfile(job_description):
            jd_text = read_text(job_description)
        else:
            jd_text = job_description
    else:
        sys.exit("[error] Provide --jd path or set job_description variable in code.")

    # Basic validation: ensure we didn't end up with empty content (e.g., an empty file)
    if not resume_md or not resume_md.strip():
        sys.exit("[error] Resolved resume content is empty. Provide a non-empty resume via --resume-md/--resume-pdf or set md_resume to valid content/file path.")

    if not jd_text or not jd_text.strip():
        sys.exit("[error] Resolved job description is empty. Provide a non-empty JD via --jd or set job_description to valid content/file path.")

    return resume_md, jd_text

def main():
    parser = argparse.ArgumentParser(description="Tailor a Markdown (or PDF) resume to a job description via OpenAI.")
    parser.add_argument("--resume-md", help="Path to a Markdown resume file.")
    parser.add_argument("--resume-pdf", help="Path to a PDF resume file (text-extracted to Markdown-like text).")
    parser.add_argument("--jd", help="Path to a text/Markdown file containing the job description.")
    parser.add_argument("--out", default="./Tailored_Resume.md", help="Output Markdown file.")
    parser.add_argument("--model", default="gpt-5", help="OpenAI model (default: gpt-5-turbo).")
    parser.add_argument("--temperature", type=float, default=1, help="Sampling temperature (default: 1).")
    args = parser.parse_args()

    if not OPENAI_API_KEY:
        sys.exit("[error] OPENAI_API_KEY is not set. Add it to env or .env.")

    try:
        resume_md, jd_text = resolve_inputs(args)
        prompt = build_prompt(resume_md, jd_text)
        tailored_md = call_openai(prompt, model=args.model, temperature=args.temperature)
    except Exception as e:
        sys.exit(f"[error] {e}")

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(tailored_md.strip() + "\n")

    print(f"[ok] Wrote tailored Markdown resume → {args.out}")

if __name__ == "__main__":
    main()