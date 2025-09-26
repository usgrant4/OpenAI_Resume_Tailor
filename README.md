
-----

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
  * **Secure Configuration**: Uses a `.env` file to keep your API key safe and out of the source code for local testing only.

-----

## \#\# How It Works ⚙️

The script follows a simple, powerful sequence to transform your resume:

1.  **Parses Instructions**: It first reads the command-line arguments (like file paths and export format). If none are given, it uses the default files in the `resume` folder.
2.  **Extracts Text**: It reads the content from your resume (handling `.md`, `.pdf`, and `.docx` files) and the job description.
3.  **Builds an AI Prompt**: It combines the texts into a detailed prompt, instructing the AI to act as a resume editor and tailor the resume to the job description.
4.  **Streams the AI Response**: It sends the prompt to the OpenAI API and streams the response back, printing the tailored resume to your screen in real-time.
5.  **Saves the Markdown File**: After the stream is complete, it saves the full text as a new `.md` file.
6.  **Exports the Final Document (Optional)**: If you requested an export, it uses Pandoc to convert the new Markdown file into a polished `.pdf` or `.docx` document.

-----

## \#\# File & Folder Structure 📂

For the script to work correctly, your project should have the following files and folders.

  * **`resume/` folder**: This folder is used for the default, no-argument run.
      * **Your Resume**: Place your resume file here. It must be in one of three formats:
          * Markdown (`.md`)
          * PDF (`.pdf`)
          * Word Document (`.docx`)
      * **The Job Description**: Place the job description here. This should be a plain text file, like `.md` or `.txt`.
  * **Root Folder Files**: These two files are essential and must be in the main project directory.
      * **`.env`**: Stores your `OPENAI_API_KEY`.
      * **`requirements.txt`**: Lists all necessary Python packages.

<!-- end list -->

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

## \#\# Setup & Configuration

Follow these steps to set up the project on your local machine.

1.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
2.  **Install Dependencies**
    Run `pip install -r requirements.txt` to install all necessary packages. The contents of `requirements.txt` should be:
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

-----

## \#\# Usage (Command Line) 📝

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

## \#\# Usage (GitHub Action) 🤖

You can run the script directly from your GitHub repository's "Actions" tab.

1.  **Add Repository Secret**
      * In your GitHub repo, go to **Settings** \> **Secrets and variables** \> **Actions**.
      * Create a **New repository secret** named `OPENAI_API_KEY` and paste your API key.
2.  **Run the Workflow**
      * Go to the **Actions** tab.

      * Select the **Manual Resume Tailor** workflow.

      * Click the **Run workflow** button.

      * Fill in the input fields. The **"Export format"** field is a dropdown menu where you can select `none`, `docx`, or `pdf` for your output.

      * Click the final "Run workflow" button to start. The generated files will be available as downloadable **artifacts** on the workflow summary page.

-----

## 🎨 Custom Styling

You can easily change the look and feel of your exported documents by editing the files in the `styling/` folder.

* **PDF Styling**: To change the PDF's appearance (fonts, colors, margins), simply edit the `styling/style.css` file.
* **DOCX Styling**: To change the DOCX's appearance, open the `styling/reference.docx` file in Microsoft Word or Google Docs. Modify the default styles (e.g., "Normal", "Heading 1") and page layout, then save the file. The script will use your saved styles for all future DOCX exports.

-----

## 📌 Roadmap (one day I'll get to it...)

  * [ ] Add support for batch processing multiple job descriptions.
  * [ ] Integrate a web scraper to pull job descriptions directly from URLs.
  * [ ] Develop an interactive mode for CLI execution.

-----

## 🧑‍💻 Author

**Ulysses Grant, IV**

  * [LinkedIn](https://www.linkedin.com/in/usgrant4/)
  * [GitHub](https://www.google.com/search?q=https://github.com/usgrant4)
