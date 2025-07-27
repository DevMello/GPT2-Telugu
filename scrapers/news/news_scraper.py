import requests
from bs4 import BeautifulSoup

def news():
    with open('all_articles.txt', 'a', encoding='utf-8') as outfile:
        for k in range(100000, 500000): 
            url = f'http://www.andhrajyothy.com/artical?SID={k}'
            resp = requests.get(url)
            
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')

                try:
                    updated_date_span = soup.find("span", {"id": "ContentPlaceHolder1_lblUpdatedDate"})
                    date_str = updated_date_span.text.strip().replace("-", "")[:8]
                    year = updated_date_span.text.strip()[6:10]

                    headline_span = soup.find("span", {"id": "ContentPlaceHolder1_lblStoryHeadLine"})
                    headline = headline_span.text.strip() if headline_span else "No Headline"

                    content_span = soup.find("span", {"id": "ContentPlaceHolder1_lblStoryDetails"})
                    content_blocks = content_span.find_all("div") if content_span else []

                    content_text = "\n".join([div.text.strip() for div in content_blocks if div.text.strip()])

                    if not content_text and content_span:
                        content_text = content_span.text.strip()

                    if content_text:
                        outfile.write("<DOC>\n")
                        outfile.write(f"<DOCNO>{k}</DOCNO>\n")
                        outfile.write("<TEXT>\n")
                        outfile.write(f"{updated_date_span.text.strip()}\n\n")
                        outfile.write(f"{headline}\n\n")
                        outfile.write(f"{content_text}\n")
                        outfile.write("</TEXT>\n</DOC>\n\n")
                        print(f"Saved article SID={k}")
                except Exception as e:
                    print(f"Error parsing SID={k}: {e}")
            else:
                print(f"Error fetching SID={k} - Status code: {resp.status_code}")

news()
