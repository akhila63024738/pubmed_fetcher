import argparse
from .core import fetch_papers  # assumes fetch_papers is defined in core.py

def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers with non-academic (company) authors only."
    )
    parser.add_argument("query", help="Search query for PubMed")
    parser.add_argument("-f", "--file", help="CSV file to write output")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()
    fetch_papers(query=args.query, output_file=args.file, debug=args.debug)

