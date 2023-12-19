import xml.etree.ElementTree as ElementTree
import requests

def fetch_arxiv_papers(category, max_results=10):
    base_url = 'http://export.arxiv.org/api/query?'
    search_query = f'cat:{category}'
    params = {
        'search_query': search_query,
        'max_results': max_results,
        'sortBy': 'lastUpdatedDate',
        'sortOrder': 'descending',
    }
 
    response = requests.get(base_url, params=params)
    return response.text

def extract_paper_information(xml_string):
    root = ElementTree.fromstring(xml_string)
    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
        url = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
        papers.append({
            'title': title,
            'summary': summary,
            'url': url
        })
    return papers