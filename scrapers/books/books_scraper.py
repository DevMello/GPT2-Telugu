import requests
from bs4 import BeautifulSoup

def get_all_book_links():
    book_links = set()
    for k in range(0, 361, 30):
        print(f"Scraping list page offset: {k}")
        url = f'http://www.teluguone.com/grandalayam/books/novels{k}.html'
        resp = requests.get(url)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            i = 1
            prev = ""
            for anchor in soup.find_all("a"):
                link = anchor.get("href")
                if link and 'novels/' in link and link != prev:
                    if i >= 3:
                        book_links.add(link)
                    prev = link
                    i += 1
    return list(book_links)

def get_page_links(book_url):
    page_links = []
    resp = requests.get(book_url.strip())
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        select = soup.find_all("select")
        if select:
            for option in select[0].find_all("option"):
                link = option.get("value")
                if link:
                    page_links.append(link.strip())
    return page_links

def extract_and_save_all_text(book_links, output_file='all_books.txt'):
    with open(output_file, 'w', encoding='utf-8') as out:
        book_id = 1
        for book_url in book_links:
            print(f"\nProcessing book {book_id}: {book_url}")
            page_links = get_page_links(book_url)
            page_id = 0
            for page_url in page_links:
                print(f"  - Page {page_id}")
                resp = requests.get(page_url)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    paragraphs = soup.find_all("p")
                    if paragraphs:
                        out.write(f"\n\n<DOC>\n<DOCNO>Book{book_id}-Page{page_id}</DOCNO>\n<TEXT>\n")
                        for para in paragraphs:
                            text = para.get_text(strip=True)
                            if text:
                                out.write(text + "\n")
                        out.write("</TEXT>\n</DOC>\n")
                page_id += 1
            book_id += 1

def run_all():
    book_links = get_all_book_links()
    print(f"\nTotal books found: {len(book_links)}")
    extract_and_save_all_text(book_links)

if __name__ == "__main__":
    run_all()