import urllib3
import csv
import json

def request(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    return json.loads(r.data.decode('utf8'))


def writeCSV(filename, data):
    f = open(filename, 'w')
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)
    f.close()


def getCandidates(candidates, fec_key):
    rows = []
    cols = ["candidate_id", "name", "state", "party", "office", "incumbent_challenge"]
    rows.append(cols)
    for candidate in candidates:
        url = "https://api.open.fec.gov/v1/candidate/"+candidate["candidate_id"]+"/?api_key="+fec_key
        data = request(url)["results"][0]
        row = []
        for col in cols:
            row.append(data[col])
        rows.append(row)

    writeCSV("candidates.csv", rows)


def getPacsAndMemberships(candidates, fec_key):
    pacs = []
    rows = []
    joinrows = [["candidate_id", "committee_id"]]
    cols = ["committee_id", "name", "affiliated_committee_name", "party", "candidate_ids", "website", "committee_type_full", "state", "designation_full", "first_file_date"]
    rows.append(cols)
    for candidate in candidates:
        url = "https://api.open.fec.gov/v1/candidate/"+candidate["candidate_id"]+"/committees/?api_key="+fec_key
        data = request(url)["results"]
        for datarow in data:
            row = []
            for col in cols:
                row.append(datarow[col])
            rows.append(row)

            if(datarow["committee_id"] not in pacs):
                pacs.append(datarow["committee_id"])

            for member in datarow["candidate_ids"]:
                joinrows.append([member, datarow["committee_id"]])

    writeCSV("pacs.csv", rows)
    writeCSV("pac_memberships.csv", joinrows)

    return pacs


def getCandidateFilings(candidates, fec_key):
    rows = []
    cols = ["candidate_id", "report_type_full", "document_description", "coverage_start_date", "coverage_end_date", "csv_url", "pdf_url", "html_url", "total_disbursements", "total_receipts", "debts_owed_by_committee", "debts_owed_to_committee", "cash_on_hand_beginning_period", "cash_on_hand_end_period", "primary_general_indicator"]
    rows.append(cols)
    for candidate in candidates:
        url = "https://api.open.fec.gov/v1/candidate/"+candidate["candidate_id"]+"/filings/?api_key="+fec_key
        data = request(url)["results"]
        for datarow in data:
            row = []
            for col in cols:
                row.append(datarow[col])
            rows.append(row)

    writeCSV("candidate_filings.csv", rows)


def getPacFilings(pacs, fec_key):
    rows = []
    cols = ["committee_id", "report_type_full", "document_description", "coverage_start_date", "coverage_end_date", "csv_url", "pdf_url", "html_url", "total_disbursements", "total_receipts", "debts_owed_by_committee", "debts_owed_to_committee", "cash_on_hand_beginning_period", "cash_on_hand_end_period", "primary_general_indicator"]
    rows.append(cols)
    for pac in pacs:
        url = "https://api.open.fec.gov/v1/committee/"+pac+"/filings/?api_key="+fec_key
        data = request(url)["results"]
        for datarow in data:
            row = []
            for col in cols:
                row.append(datarow[col])
            rows.append(row)

    writeCSV("pac_filings.csv", rows)


def getNews(candidates, newsdata_key):
    rows = []
    cols = ["news_id", "candidate_id", "title", "link", "pubDate", "source_id"]
    rows.append(cols)
    for candidate in candidates:
        url = "https://newsdata.io/api/1/news?apikey="+newsdata_key+"&q="+candidate["name"].replace(" ", "%20")+"&country=us&language=en"
        data = request(url)["results"]
        for datarow in data:
            row = []
            row.append(candidate["name"]+" "+datarow["source_id"]+" "+datarow["pubDate"])
            row.append(candidate["candidate_id"])
            for col in cols[2:]:
                row.append(datarow[col])
            rows.append(row)

    writeCSV("news.csv", rows)

fec_key = open("fec_key.txt").read()
newsdata_key = open("newsdata_key.txt").read()
candidates = [
    {"name": "John Fetterman", "candidate_id": "S6PA00274"},
    {"name": "Mehmet Oz", "candidate_id": "S2PA00638"}
]

#getCandidates(candidates, fec_key)
#pacs = getPacsAndMemberships(candidates, fec_key)
#getCandidateFilings(candidates, fec_key)
#getPacFilings(pacs, fec_key)
getNews(candidates, newsdata_key)