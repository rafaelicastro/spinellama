from Bio import Entrez
Entrez.email = "castrora@hss.edu"

import time
import json
import csv
import argparse
from typing import List, Dict, Optional
from datetime import datetime

def search_pubmed(keywords, max_results, database: str="pubmed", retmax_per_batch: int=20) -> List[str]:
    # search_query = " OR ".join([f'\"{keyword}\"[All fields]' for keyword in keywords])

    try:
        search_handle = Entrez.esearch(
            db=database,
            term=search_query,
            retmax=max_results,
            sort="relevance"
                )

        search_results = Entrez.read(search_handle)
        search_handle.close()

        id_list = search_results["IdList"]
        print(f"found {search_results['Count']} total results")

        return id_list

    except Exception as e:
        print(f"error: {e}")
        return []


def fetch_abstracts(pmid_list, batch_size) -> List[str]:
    abstracts = []

    for i in range(total_ids, batch_size):
        batch_ids = pmid_list[i:i+batch_size)
        batch_num = (i // batch_size) + 1
        total_batches = (len(pmid_list) + batch_size - 1) // batch_size

        try:
            fetch_handle = Entrez.efetch(
                    db="pubmed",
                    id=",".join(batch_ids),
                    rettype="abstract",
                    retmode="xml"
                    )

            records = Entrez.read(fetch_handle)
            fetch_handle.close()

            for r in records['PubmedArticle']:
                article_info = parse_article_record(record)
                if article_info:
                    abstracts.append(article_info)

            time.sleep(0.5)

        except Exception as e:
            print(f"error at batch_num {batch_num}: {e}")
            continue

        print("got abstracts")
        return abstracts

def parse_article_record(record) -> str: 
    try:
        medline_citation = record['MedlineCitation']
        article = medline_citation['Article']

        abstract = "NA"
        if ("Abstract" in article and "AbstractText" in article['Abstract']):
            abs_parts = article['Abstract']['AbstractText']
            if (isinstance(abs_parts, list)):
                abstract = " ".join([str(part) for part in abs_parts])
            else:
                abstract = str(abs_parts)

        return abstract

    except Exception as e:
        print(f"error parsing: {e}")
        return ""

def save_abstracts(abstracts):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"pubmed_abstracts_{timestamp}.csv"

    if abstracts:
        with open(filename, 'w', newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            for a in abstracts:
                writer.writerow([abstract['abstract']])

        print("saved abstracts")

def filter_by_keyword(abstracts):
    pass


def main():
    with open('keywords.txt', "r") as f:
        keywords = f.read()

        pmid_list = search_pubmed(keywords, 200)

        abstracts = fetch_abstracts(pmid_list)
        if (not abstracts):
            print("no abstracts")

        # TODO filter abstracts

        # this should be with filt_abs
        save_abstracts(abstracts)
