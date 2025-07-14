import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
import csv
from datetime import datetime


def fetch_papers(query: str, output_file: Optional[str] = None, debug: bool = False) -> None:
    # Construct the search URL
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": "20"
    }

    if debug:
        print(f"Searching PubMed with query: {query}")

    search_response = requests.get(search_url, params=search_params)
    ids = search_response.json().get("esearchresult", {}).get("idlist", [])

    if debug:
        print(f"Found {len(ids)} papers.")

    # Fetch details for each paper
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }

    fetch_response = requests.get(fetch_url, params=fetch_params)
    root = ET.fromstring(fetch_response.content)

    results = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or "Unknown"
        authors = article.findall(".//Author")

        non_academic_authors = []
        companies = []
        email = ""

        for author in authors:
            affiliation_info = author.findtext(".//AffiliationInfo/Affiliation")
            if not affiliation_info:
                continue

            # Heuristic: check if the author is likely from a company
            if not any(keyword in affiliation_info.lower() for keyword in ["university", "college", "institute", "school", "hospital", "lab"]):
                name_parts = []
                if author.find("ForeName") is not None:
                    name_parts.append(author.find("ForeName").text)
                if author.find("LastName") is not None:
                    name_parts.append(author.find("LastName").text)
                full_name = " ".join(name_parts)
                if full_name:
                    non_academic_authors.append(full_name)
                companies.append(affiliation_info)

            if "@" in affiliation_info and not email:
                email = affiliation_info.split()[-1]  # crude but works for basic cases

        results.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "; ".join(non_academic_authors),
            "Company Affiliation(s)": "; ".join(set(companies)),
            "Corresponding Author Email": email
        })

    if output_file:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        if debug:
            print(f"Saved results to {output_file}")
    else:
        for row in results:
            print(row)

