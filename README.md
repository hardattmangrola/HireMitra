# AI Job Recommendation System

An AI-assisted job recommendation application that analyzes a PDF resume and surfaces top job postings from LinkedIn and Naukri. The app is built with Streamlit, uses Groq for language model capabilities, PyMuPDF for PDF text extraction, and Apify for job data.

## Features

- Resume analysis from PDF upload
- AI-generated summary, skill gaps, and improvement roadmap
- Top 5 job recommendations from LinkedIn and Naukri
- Robust display with graceful handling of missing fields (title, company, link, location)

## Architecture

- `app.py`: Streamlit UI and application flow
- `src/helper.py`: PDF extraction and Groq API integration
- `src/job_api.py`: Job fetching via Apify actors (LinkedIn and Naukri)
- `mcp_server.py`: Minimal MCP server exposing job-fetch tools for external clients

## Requirements

- Python 3.13+
- Groq API key
- Apify API token

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project root with your keys:

```env
GROQ_API_KEY=your_groq_api_key_here
APIFY_API_TOKEN=your_apify_api_token_here
```

Notes:
- The application reads these with `python-dotenv` on startup.
- If variables are missing, the code raises a clear `ValueError` to help diagnose configuration issues.

## Running the Streamlit App

From the project root:

```bash
streamlit run app.py
```

Open the provided local URL in your browser.

## Usage

1. Upload a PDF resume in the app.
2. Review the generated summary, skill gaps, and roadmap.
3. Click "Get Job Recommendations" to fetch and view the top 5 LinkedIn and Naukri postings.

## Configuration and Behavior

- Job count is limited to the top 5 results per source.
- The UI attempts to resolve job links from multiple possible fields (`link`, `url`, `jobUrl`) and location from (`location`, `locationName`).
- Default search location is set in `src/job_api.py` and can be adjusted if needed.

## MCP Server (`mcp_server.py`)

This repository includes a lightweight Model Context Protocol (MCP) server that exposes job-fetching as tools which can be consumed by MCP-compatible clients (for example, IDE assistants or MCP-capable apps).

### What it Provides

- Tool: `fetchlinkedin(listofkey)` → calls `fetch_linkedin_jobs`
- Tool: `fetchnaukri(listofkey)` → calls `fetch_naukri_jobs`

Both tools currently forward the provided keyword string to the corresponding Apify-powered job fetchers and return the raw job items.

### How to Run

Run the server over stdio:

```bash
python mcp_server.py
```

Clients that support MCP over stdio can connect to this process and invoke the tools.

### Extending the MCP Server

- Add new tools by defining async functions decorated with `@mcp.tool()`.
- Validate and structure input parameters (e.g., allow `location`, `rows`, or filters).
- Post-process and normalize job items before returning to clients (e.g., unify `title`, `companyName`, `location`, `url`).
- Add error handling and input validation to return informative messages to clients.


## Troubleshooting

- Import errors for Groq: ensure `from groq import Groq` is used and dependencies are installed.
- Environment variable errors: verify `.env` exists and contains valid `GROQ_API_KEY` and `APIFY_API_TOKEN` values.
- PDF parsing issues: confirm the uploaded file is a valid PDF; the app reads bytes from Streamlit `UploadedFile`.
- Job links or locations missing: the UI includes fallbacks, but upstream data may be incomplete.

## Project Structure

```
.
├─ app.py
├─ mcp_server.py
├─ requirements.txt
├─ pyproject.toml
├─ src/
│  ├─ helper.py
│  └─ job_api.py
└─ README.md
```

## License

MIT License. See `LICENSE` for details.
