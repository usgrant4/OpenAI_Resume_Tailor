# Resume Tailoring with OpenAI

This project automates the process of **tailoring a resume** to a specific job description using the OpenAI API. It reads your resume from a Markdown, PDF, or DOCX file, and leverages a Large Language Model to optimize it with keywords and skills relevant to the provided job description. The output is a clean, recruiter-friendly document available in multiple formats.

-----

## 🚀 Features

  * **Multi-Format Input**: Supports resumes in **Markdown**, **PDF**, and **DOCX** formats.
  * **AI-Powered Tailoring**: Uses the OpenAI API (defaulting to `gpt-4o`) to rewrite and tailor your resume.
  * **Real-Time Output**: **Streams the response** from the API, so you can see the results instantly.
  * **Flexible Export Options**: Outputs the tailored resume in **Markdown**, and can also export to **PDF** or **DOCX** using Pandoc.
  * **Manual GitHub Action**: Run the entire process from your browser with a one-click manual GitHub Action workflow.
  * **Safe Dry-Run Mode**: A `--dry-run` flag lets you preview the exact prompt that will be sent to the API without incurring costs.
  * **Secure Configuration**: Uses a `.env` file to keep your API key safe and out of the source code.

-----

## 📂 Project Structure

```
resume-tailor/
├── .github/
│   └── workflows/
│       └── manual_tailor.yml     # GitHub Action workflow file
├── resume/
│   ├── Ulysses_Grant.md          # Example resume
│   └── job_description.md        # Example job description
├── .env                          # For storing your API key (local only)
├── .gitignore
├── requirements.txt              # Project dependencies
├── tailor_resume.py              # Main Python script
└── README.md
```

-----

## ⚙️ Setup & Configuration

Follow these steps to set up the project on your local machine.

1.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
2.  **Install Dependencies**
    Create a `requirements.txt` file with the content below and run `pip install -r requirements.txt`.
    ```text
    # requirements.txt
    openai
    python-dotenv
    pdfplumber
    python-docx
    pypandoc-binary
    ```
3.  **Set Up API Key**
    Create a `.env` file in the project root and add your OpenAI API key.
    ```env
    OPENAI_API_KEY="sk-YourSecretApiKeyHere"
    ```
4.  **Install LaTeX for PDF Export (Optional) ⚠️**
    To export files to PDF, Pandoc requires a system-level LaTeX distribution. This is a one-time, external installation.
      * **Windows**: Install [MiKTeX](https://miktex.org/)
      * **macOS**: Install [MacTeX](https://www.tug.org/mactex/)
      * **Linux**: Install TeX Live (e.g., `sudo apt-get install texlive-full`)

-----

## 📝 Usage (Command Line)

Here are some examples of how to run the script from your terminal.

  * **Basic Run (using default files)**
    This command uses the fallback files defined in the script's `CONFIG`.
    ```bash
    python tailor_resume.py
    ```
  * **Specify PDF Resume & Export to DOCX**
    ```bash
    python tailor_resume.py --resume-pdf "./resume/my_resume.pdf" --jd "./resume/jd.txt" --export-format docx
    ```
  * **Specify DOCX Resume & Export to PDF**
    ```bash
    python tailor_resume.py --resume-docx "MyResume.docx" --jd "JobDesc.txt" --out "Tailored.md" --export-format pdf
    ```
  * **Dry Run to Test the Prompt**
    This will print the prompt to the console without calling the API.
    ```bash
    python tailor_resume.py --resume-md "resume.md" --jd "jd.txt" --dry-run
    ```

-----

## 🤖 Usage (GitHub Action)

You can run the script directly from your GitHub repository's "Actions" tab.

1.  **Add Repository Secret**
      * In your GitHub repo, go to **Settings** \> **Secrets and variables** \> **Actions**.
      * Create a **New repository secret** named `OPENAI_API_KEY` and paste your API key.
2.  **Run the Workflow**
      * Go to the **Actions** tab.
      * Select the **Manual Resume Tailor** workflow.
      * Click the **Run workflow** button.
      * Fill in the input fields for your file paths and export options, then run the workflow.
      * 
      * The generated files will be available as downloadable **artifacts** on the workflow summary page.

-----

## 📌 Roadmap

  * [ ] Add support for batch processing multiple job descriptions.
  * [ ] Integrate a web scraper to pull job descriptions directly from URLs.
  * [ ] Develop an interactive mode for CLI execution.

-----

## 🧑‍💻 Author

**Ulysses Grant, IV**

  * [LinkedIn](https://www.linkedin.com/in/usgrant4/)
  * [GitHub](https://www.google.com/search?q=https://github.com/usgrant4)