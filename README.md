# 🔭 ORBIT AI — Multi-Agent Research System

ORBIT AI is a Streamlit-based research assistant that uses a multi-agent workflow to search for information, inspect relevant sources, generate a structured report, and review the report with a critic agent.

**Search. Read. Synthesize. Review.**

## ✨ Features

- **Search Agent** — searches for relevant information about a user-provided topic.
- **Reader Agent** — selects relevant URLs and extracts useful facts, dates, evidence, and source links.
- **Writer** — combines the available research into a structured report.
- **Critic Agent** — reviews the generated report and provides feedback.
- **Progress tracking** — displays the four workflow stages as they run.
- **Research history** — lets you revisit reports generated during the current app session.
- **Download reports** — export the report as Markdown or download a full research record as plain text.
- **Dark interface** — a custom Streamlit UI with navigation for New Research, Research History, and About.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and workflow logic |
| Streamlit | Web interface, progress indicators, tabs, history, and downloads |
| LangChain | Agent and language-model workflow components |
| LLM provider (Groq or another configured provider) | Language-model responses used by the agents and chains |
| Web search tool | Finds relevant pages and information |
| Webpage-reading/scraping tools | Extracts information from selected sources |
| `datetime` | Adds timestamps to completed research tasks |

> The exact LLM provider, search backend, and scraping implementation depend on the configuration in `agents.py` and related project files.

## 🔄 How It Works

A research task passes through four stages:

1. **Search Agent**  
   Receives the topic and searches for recent, relevant information. The prompt asks it to include source URLs, dates, and useful facts without inventing sources.

2. **Reader Agent**  
   Uses the search results to identify relevant URLs and extract deeper source information. It is instructed to note inaccessible sources and avoid inventing facts.

3. **Writer**  
   Combines the topic, search results, and extracted source content into a research report.

4. **Critic Agent**  
   Reviews the report and returns feedback.

The app then presents the report, search results, reader output, and critic feedback in separate tabs.

## 🖥️ Requirements

- Windows, macOS, or Linux
- Python compatible with the installed project dependencies
- `pip` or [`uv`](https://docs.astral.sh/uv/)
- API credentials for the LLM/search services configured by your project, if required

Check `agents.py` and the project's dependency file to confirm the exact provider, environment variables, and package versions used by your setup.

## 📁 Project Structure

The following is a suggested structure based on the files used by the app. Adjust it to match your repository:

```text
ORBIT-AI/
├── app.py                 # Streamlit user interface (rename to your actual entry file)
├── agents.py              # Agent builders and writer/critic chains
├── requirements.txt       # Python dependencies
├── .env                   # API keys; do not commit this file
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

Replace the URL with your GitHub repository URL:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Alternatively, download the repository ZIP from GitHub and extract it.

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If the repository contains `requirements.txt`:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you use `uv` and the repository contains `pyproject.toml`:

```bash
uv sync
```

If no dependency file exists yet, create one containing the packages your code actually imports. The provided UI imports `streamlit` and `agents`; the `agents` module may itself require additional packages. Install the project's actual dependencies rather than relying on this README alone.

### 4. Configure environment variables

Create a `.env` file in the project root and add the API keys required by your implementation. For example:

```dotenv
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Only include variables your code uses. The names above are examples; verify the exact variable names in `agents.py` and your search-tool configuration.

**Security:** Never commit real API keys, tokens, or credentials to GitHub. Add `.env` to `.gitignore`.

Example `.gitignore` entries:

```gitignore
.venv/
__pycache__/
.env
.streamlit/secrets.toml
*.py[cod]
```

### 5. Run the application

If your Streamlit entry file is named `app.py`:

```bash
streamlit run app.py
```

If your entry file has a different name, replace `app.py` with that filename. Streamlit will print a local URL, usually `http://localhost:8501`, which you can open in your browser.

## 🚀 Usage

1. Start the application.
2. Select **New Research** from the sidebar.
3. Enter a clear research topic, such as `How are AI agents changing data engineering?`
4. Select **Start Research**.
5. Follow the progress through Search Agent, Reader Agent, Writing Report, and Critic Agent.
6. Review the output in the available tabs:
   - **Final Report** — the generated report.
   - **Search Results** — the search agent's output.
   - **Reader Output** — content extracted from relevant sources.
   - **Critic Feedback** — the critic's review.
7. Download the report as Markdown or download the full research output as a text file.
8. Open **Research History** to revisit reports created during the current session. History is stored in Streamlit session state, so it is not guaranteed to persist after the session ends or the app restarts.
9. Use **About** to view the workflow and technology overview.

### Tips for better results

- Use specific, focused research questions.
- Ask for a time range when recency matters.
- Prefer topics where sources and evidence can be checked.
- Verify important claims and citations in the original source pages before relying on a report.

## 🛠️ Troubleshooting

### `ModuleNotFoundError: No module named 'streamlit'`

Activate the virtual environment and install the project dependencies:

```bash
pip install -r requirements.txt
```

### `ModuleNotFoundError: No module named 'agents'`

Make sure `agents.py` is in the project root or is importable from the directory where you run Streamlit. Run the command from the repository root.

### Missing API key or provider error

Check that the `.env` file exists, that the variable names match the code, and that your application loads environment variables where needed. Do not paste secrets into issues or public logs.

### Search or webpage reading fails

Check your internet connection, search-provider credentials, rate limits, and whether the target websites allow automated access. Some pages may block requests or be unavailable.

### Reports are inaccurate or incomplete

The output depends on the search results, accessible page content, model behavior, and prompts. Check primary sources and verify critical details independently.

## 🔐 Limitations and Responsible Use

- Generated reports can contain mistakes, omissions, or unsupported conclusions.
- Search results may be outdated or incomplete.
- Websites may block automated reading or return incomplete content.
- The critic agent provides feedback; it does not guarantee factual correctness.
- Review the original sources before using research for important decisions.

## 🗺️ Roadmap

Potential future improvements:

- Persistent research history
- Export to PDF or DOCX
- Source-level citations and reference formatting
- Configurable models and search providers
- More robust retries, logging, and error handling

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository.
2. Create a branch for your change.
3. Make and test your changes.
4. Open a pull request describing the change.

## 📄 License

No license has been specified yet. Add a `LICENSE` file before presenting the project as open source, and choose a license that matches your intentions.

---

**Note:** This README describes the Streamlit interface shown in the project code. Update the entry filename, dependency list, environment variable names, and provider details to match the actual files in your repository before publishing.
