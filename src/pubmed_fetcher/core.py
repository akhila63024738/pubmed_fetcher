import requests
import xml.etree.ElementTree as ET
from typing import Optional
import csv


def is_non_academic(affiliation: str) -> bool:
    academic_keywords = [
        "university", "college", "institute", "school", "hospital", "lab", "dept",
        "center", "centre", "faculty", "public health", "government", "nhs",
        ".edu", ".ac.", ".gov", ".org", "medical center", "foundation"
    ]
    return not any(keyword in affiliation.lower() for keyword in academic_keywords)


def fetch_papers(query: str, output_file: Optional[str] = None, debug: bool = False) -> None:
    # Step 1: Search PubMed
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

    if not ids:
        print("No papers found.")
        return

    # Step 2: Fetch paper details
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

            # Extract email from affiliation
            if "@" in affiliation_info and not email:
                email_parts = [part for part in affiliation_info.split() if "@" in part]
                if email_parts:
                    email = email_parts[0].strip(";,")

            # Check for non-academic affiliation
            if is_non_academic(affiliation_info):
                name_parts = []
                if author.find("ForeName") is not None:
                    name_parts.append(author.find("ForeName").text)
                if author.find("LastName") is not None:
                    name_parts.append(author.find("LastName").text)
                full_name = " ".join(name_parts)
                if full_name:
                    non_academic_authors.append(full_name)
                companies.append(affiliation_info)

        # Only include papers with at least one non-academic author
        if non_academic_authors:
            results.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(set(companies)),
                "Corresponding Author Email": email
            })

    # Step 3: Output
    if results:
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
    else:
        print("No matching non-academic papers found.")

