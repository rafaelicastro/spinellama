from metapub import PubMedFetcher
from metapub import FindIt
#from metapub.pubmedcentral import get_pmcid_for_otherid

import pandas as pd

#import urllib.request
import requests

#import json

#import certifi
#cw = "C:\\Users\\castrora\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python313\\site-packages\\certifi\\cacert.pem"

d = "C:\\Users\\castrora\\Desktop\\spllama\\script\\"
#reasons = open(d + "reasons.txt", "w")

#upwAPI = "https://api.unpaywall.org/v2/"
#email = "?email=rafaelignaciocastro@gmail.com"

query = open(d + "query.txt")
#query = "spine AND fusion"

fetch = PubMedFetcher()
articles = fetch.pmids_for_query(query.read(), retmax = 2000000)

#articles = [5429107, 39182131, 19783494, 32682611]

#s = FindIt(str(articles[0]))
#print(s.url)

df = pd.DataFrame(columns=["PMID", "abstract", "pdf_url"])

for a in articles:
    try:
        print(a) 
        art = fetch.article_by_pmid(a)
        #print(art.abstract)
        s = FindIt(a)
        pdf_url = s.url

        pdfExists = False

        if (pdf_url != None):
            response = requests.get(pdf_url)
            filename = f"{d}{art.pmid}.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded PDF for PMID {art.pmid}")
            pdfExists = True
        else:
            print(f"No PDF available for PMID {art.pmid}")

        newRow = {"PMID": a, "abstract": art.abstract, "pdf_url": pdfExists}
        df = pd.concat([df, pd.DataFrame([newRow])], ignore_index=True)

    except Exception as e:
        print(f"Error downloading {art.pmid}: {e}")

df.to_csv(d + "export.csv", index=False)

"""
for a in articles:
    art = fetch.article_by_pmid(a)
    title = art.title
    doi = art.doi

    print(title + ", " + doi + ", " + art.pmid)

    apiURL = upwAPI + doi + email
    # print(apiURL)

    upwRAW = requests.get(apiURL, verify=False)
    
    rawtext = upwRAW.text

    if (rawtext[0:14] == "<!DOCTYPE HTML"): # not in UPW database
        reasons.write(doi + ": not in database\n")
        continue

    upwJSON = json.loads(upwRAW.text)

    if (upwJSON["is_oa"] == False):
        reasons.write(doi + ": " + "not OA\n")
        continue

    if (upwJSON["best_oa_location"] == None):
        reasons.write(doi + ": " + "OA but no location\n")
        continue

    if (upwJSON["best_oa_location"]["url_for_pdf"] == None):
        reasons.write(doi + ": " + "OA but no PDF\n")
        continue

    pdfURL = upwJSON["best_oa_location"]["url_for_pdf"]
    
    try:
        urllib.request.urlretrieve(pdfURL, d + "pdfs\\" + title + ".pdf")
        print("worked")
    except:
        reasons.write(doi + ": PDF not present\n")

"""
