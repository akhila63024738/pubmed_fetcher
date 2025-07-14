# PubMed Fetcher

A command-line tool to fetch research papers from PubMed that include at least one non-academic author  
(e.g., affiliated with a biotech or pharmaceutical company).

---

## 🚀 Features

- Search PubMed using full query syntax.
- Identify and extract papers with at least one non-academic author.
- Output results to a CSV file with:
  - PubmedID
  - Title
  - Publication Date
  - Non-academic Author(s)
  - Company Affiliation(s)
  - Corresponding Author Email
- CLI options for query input, output file path, and debug logging.
- Heuristics to detect non-academic authors (e.g., excluding `university`, `college`, `institute` in affiliations).

---

## 🧪 Requirements

- Python 3.10+
- [Poetry](https://python-poetry.org/) (for dependency and project management)

---

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/pubmed_fetcher.git
cd pubmed_fetcher

2. Install dependencies
poetry install

3. Activate the virtual environment
poetry shell

🚀 Usage

poetry run get-papers-list "covid vaccine" -f results.csv -d

Arguments
query: PubMed search string (required)
-f, --file: Output CSV file path (optional)
-d, --debug: Print debug logs to the console (optional)
-h, --help: Show usage information

🗂 Project Structure

pubmed_fetcher/
├── pyproject.toml
├── README.md
├── src/
│   └── pubmed_fetcher/
│       ├── __init__.py
│       ├── cli.py
│       └── core.py
├── tests/

🧠 Heuristics for Non-Academic Authors

Authors are flagged as non-academic if their affiliations:

    Do not contain academic keywords like:

        university, college, institute, school, hospital, lab

    Or contain company-style domain names or corporate keywords.

📚 Tools & Libraries Used

    PubMed E-Utilities API

    Requests

    LXML

    Poetry

Example Output
Example results.csv:
PubmedID,Title,Publication Date,Non-academic Author(s),Company Affiliation(s),Corresponding Author
Email
40651308,Purification and characterization...,2025,Brooks Hayes,Expression Systems,nico.lingg@boku.ac.at

✅ Evaluation Criteria (Met)

    ✅ Uses PubMed API

    ✅ Full query support

    ✅ Filters non-academic authors

    ✅ Outputs required CSV fields

    ✅ Command-line arguments implemented

    ✅ Poetry-based setup

    ✅ Typed Python with readable, modular code

    ✅ README included

📌 Notes

    This tool uses best-effort heuristics to detect non-academic affiliations and may miss or misclassify some cases.

    Built using OpenAI tools and guidance
