import argparse
import logging
import os
import sys
from typing import Optional

# --- Environment & Configuration ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

CONFIG = {
    "default_model": "gpt-4o",
    "default_temp": 0.25,
    "default_output_file": "Tailored_Resume.md",
    "fallback_resume": "resume/Ulysses_Grant.md",
    "fallback_jd": "resume/job_description.md",
}

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# --- API Initialization ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.warning("OPENAI_API_KEY not set; set it in your environment or a .env file.")

try:
    import openai
    client = openai.OpenAI()
except ImportError:
    logging.error("The 'openai' library is not installed. Please install it with: pip install openai")
    sys.exit(1)

# --- File Readers ---
def read_text(path: str) -> str:
    """Reads a text file and returns its stripped content."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_pdf_text(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    try:
        import pdfplumber
    except ImportError as e:
        raise RuntimeError("Missing pdfplumber. Install with: pip install pdfplumber") from e

    parts = []
    with pdfplumber.open(pdf_path) as pdf:
        if not pdf.pages:
            raise RuntimeError(f"No pages found in PDF: {pdf_path}")
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    
    text = "\n".join(parts).strip()
    if not text:
        raise RuntimeError("No text extracted from PDF (it may be image-based).")
    return text

def extract_docx_text(docx_path: str) -> str:
    """Extracts text from a DOCX file."""
    try:
        import docx
    except ImportError as e:
        raise RuntimeError("Missing python-docx. Install with: pip install python-docx") from e

    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

# --- Core Logic ---
def build_prompt(resume_content: str, jd_content: str) -> str:
    """Builds the prompt to be sent to the OpenAI API."""
    return f"""
You are an expert resume editor who writes concise, professional Markdown tailored to the target role. I have a resume and a job description. Please adapt my resume to better align with the job requirements while maintaining a professional and concise tone.

Tailor my skills, experiences, and achievements to highlight the most relevant points for this specific position. Where appropriate, integrate keywords and phrases from the job description naturally (no keyword stuffing). The final resume must be metrics-oriented and easily scannable.

IMPORTANT: Ensure all headings, lists, and paragraphs are separated by proper line breaks to maintain a valid and clean Markdown structure.

Return ONLY the updated resume in Markdown format.

### My Resume:
{resume_content}

### Job Description:
{jd_content}
""".strip()

def call_openai(prompt: str, model: str, temperature: float):
    """Calls the OpenAI API and yields the response content."""
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a meticulous resume editor who writes concise, professional Markdown tailored to the target role."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            stream=True,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except openai.APIError as e:
        logging.error(f"OpenAI API error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred during the API call: {e}")
        sys.exit(1)

def export_document(markdown_content: str, output_path: str, export_format: str):
    """Exports Markdown content to PDF or DOCX using Pandoc, applying custom styles."""
    try:
        import pypandoc
    except ImportError as e:
        raise RuntimeError("Missing pypandoc. Install with: pip install pypandoc-binary") from e
    
    logging.info(f"Exporting to {export_format.upper()} format at -> {output_path}")
    
    extra_args = ['--from=markdown']
    
    # --- Apply styling based on the export format ---
    if export_format == 'pdf':
        style_path = 'styling/style.css'
        extra_args.append('--pdf-engine=weasyprint')
        if os.path.exists(style_path):
            extra_args.append(f'--css={style_path}')
            logging.info(f"Applying CSS style from: {style_path}")
        else:
            logging.warning(f"CSS style file not found at {style_path}. Using default styling.")

    elif export_format == 'docx':
        style_path = 'styling/reference.docx'
        if os.path.exists(style_path):
            extra_args.append(f'--reference-doc={style_path}')
            logging.info(f"Applying DOCX styles from: {style_path}")
        else:
            logging.warning(f"Reference DOCX not found at {style_path}. Using default styling.")

    try:
        pypandoc.convert_text(
            markdown_content,
            to=export_format,
            format='md',
            outputfile=output_path,
            extra_args=extra_args
        )
        logging.info(f"Successfully exported {output_path}")
    except Exception as e:
        logging.error(f"Failed to export to {export_format.upper()}. Error: {e}")
        sys.exit(1)

def _get_content_from_source(source_path: Optional[str], fallback_path: str) -> str:
    """Reads content from a source path if provided, otherwise from a fallback path."""
    path_to_read = None
    content_to_use = None
    
    if source_path and os.path.isfile(source_path):
        path_to_read = source_path
    elif not source_path and os.path.isfile(fallback_path):
        path_to_read = fallback_path
    elif not source_path:
        content_to_use = fallback_path

    if path_to_read:
        return read_text(path_to_read)
    if content_to_use:
        return content_to_use
    
    return ""

def resolve_inputs(args) -> tuple[str, str]:
    """Resolves and validates resume and job description content from arguments or fallbacks."""
    resume_content = ""
    if args.resume_md:
        resume_content = read_text(args.resume_md)
    elif args.resume_pdf:
        resume_content = extract_pdf_text(args.resume_pdf)
    elif args.resume_docx:
        resume_content = extract_docx_text(args.resume_docx)
    else:
        resume_content = _get_content_from_source(None, CONFIG["fallback_resume"])

    jd_content = _get_content_from_source(args.jd, CONFIG["fallback_jd"])

    if not resume_content.strip():
        logging.error("Resume content is empty. Please provide a valid resume source.")
        sys.exit(1)
    if not jd_content.strip():
        logging.error("Job description content is empty. Please provide a valid JD source.")
        sys.exit(1)

    return resume_content, jd_content

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Tailor a resume to a job description via OpenAI.")
    
    resume_group = parser.add_mutually_exclusive_group(required=False)
    resume_group.add_argument("--resume-md", help="Path to a Markdown resume file.")
    resume_group.add_argument("--resume-pdf", help="Path to a PDF resume file.")
    resume_group.add_argument("--resume-docx", help="Path to a DOCX resume file.")
    
    parser.add_argument("--jd", help="Path to a text file with the job description.")
    parser.add_argument("--out", default=CONFIG["default_output_file"], help="Output Markdown file.")
    parser.add_argument("--model", default=CONFIG["default_model"], help=f"OpenAI model to use (default: {CONFIG['default_model']}).")
    parser.add_argument("--temperature", type=float, default=CONFIG["default_temp"], help=f"Sampling temperature (default: {CONFIG['default_temp']}).")
    parser.add_argument("--dry-run", action="store_true", help="Print the prompt and exit without calling the API.")
    parser.add_argument("--export-format", choices=['pdf', 'docx'], help="Export the final resume to PDF or DOCX format.")

    args = parser.parse_args()

    if not OPENAI_API_KEY:
        sys.exit()

    try:
        resume, jd = resolve_inputs(args)
        prompt = build_prompt(resume, jd)

        if args.dry_run:
            logging.info("--- DRY RUN: PROMPT ---")
            print(prompt)
            sys.exit(0)

        logging.info(f"Sending request to '{args.model}'...")
        
        full_response = []
        print("--- Tailored Resume ---")
        for content_chunk in call_openai(prompt, model=args.model, temperature=args.temperature):
            print(content_chunk, end="", flush=True)
            full_response.append(content_chunk)
        print("\n-----------------------")

        tailored_md = "".join(full_response)

        with open(args.out, "w", encoding="utf-8") as f:
            f.write(tailored_md.strip() + "\n")
        logging.info(f"Successfully wrote tailored resume to → {args.out}")

        if args.export_format:
            base_output_path = os.path.splitext(args.out)[0]
            export_path = f"{base_output_path}.{args.export_format}"
            export_document(tailored_md, export_path, args.export_format)

    except Exception as e:
        logging.error(f"An unexpected error occurred in the main process: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()