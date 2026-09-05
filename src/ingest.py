import fitz
import os


def load_pdf(filepath: str) -> dict:
    """ 
    Load pdfs with pymu pdf
    
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

        doc.close()

        return {"source": filepath, "pages": pages}



def load_all_pdf(directory: str) -> list:

    """
    Loads all the pdf in the directory

    """
    results=[]
    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):
            filepath=os.path.join(directory, filename)

            try:
                results.append(load_pdf(filepath))
                print(f"Loading : {filename}")

            except Exception as e:
                print(f" Failed to load {filename} : {e}")

    return results            