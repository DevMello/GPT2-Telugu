import re

INPUT_FILE = "data/news_website.txt"
OUTPUT_FILE = "data/news_website_cleaned.txt"

def clean_news_file():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = f.read()

    # Find all <DOC>...</DOC> blocks
    docs = re.findall(r"<DOC>(.*?)</DOC>", data, flags=re.DOTALL)

    cleaned_documents = []

    for doc in docs:
        # Extract DOCNO (optional, for metadata)
        docno_match = re.search(r"<DOCNO>(.*?)</DOCNO>", doc)
        docno = docno_match.group(1).strip() if docno_match else None

        # Extract TEXT content
        text_match = re.search(r"<TEXT>(.*?)</TEXT>", doc, flags=re.DOTALL)
        if text_match:
            content = text_match.group(1).strip()
            # Combine (optional DOCNO + text) and add <|endoftext|>
            if docno:
                full_doc = f"<DOCNO>{docno}</DOCNO>\n{content}\n<|endoftext|>"
            else:
                full_doc = f"{content}\n<|endoftext|>"
            cleaned_documents.append(full_doc)

    # Save cleaned output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n".join(cleaned_documents))

    print(f"Saved cleaned dataset to {OUTPUT_FILE} with {len(cleaned_documents)} documents.")

if __name__ == "__main__":
    clean_news_file()