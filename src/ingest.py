import fitz
import os


def load_pdf(filepath: str) -> dict :
    """
      Load PDF from directory
    """
    doc=fitz.open(filepath)
    pages=[]
    for page_num, page in enumerate(doc, start=1):
        text=page.get_text()

        if text.strip():
            pages.append({
                "page_num": page_num,
                "text": text
            })

    return {
        "source":filepath,
        "pages":pages
    }


def load_all_pdf(directory: str)-> list[dict]:
    """
    Load every PDF in a directory
    """

    results=[]
    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):
            filepath=os.path.join(directory, filename)
            print(f"Loading: {filename}")

            try:
                doc_data=load_pdf(filepath)
                results.append(doc_data)
            except Exception as e:
                print(f"Failed to load {filename} : {e}")

    return results



if __name__=="__main__":
    docs=load_all_pdf("data/papers")
    print(f"\nLoaded {len(docs)} documents")

    if docs:
        first=docs[0]
        print(f"\nSamples from : {first['source']}")
        print(f"Total pages with text: {len(first['pages'])}")
        print(f"page 1 preview: \n {first['pages'][0]['text'][:300]}")