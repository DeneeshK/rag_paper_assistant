import tiktoken

tokenizer= tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))



def split_into_paragraphs(text: str) -> list[str]:
    """
    split the text into paragraphs

    """
    paragraphs=text.split("\n\n")

    return [p.strip() for p in paragraphs if p.strip()]



def split_into_sentences(text:str) -> list[str]:
    """
    split the input text into sentences 

    """

    import re

    sentences=re.split(r'(?<=[.!?])\s+', text)

    return [s.strip() for s in sentences if s.strip()]



def _get_overlap_text(text: str, overlap_tokens: int) -> str:
    if not text:
        return ""
    tokens=tokenizer.encode(text)
    overlap=tokens[-overlap_tokens:] if len(tokens)> overlap_tokens else tokens

    return tokenizer.decode(overlap)



def chunk_text(text: str, max_tokens: int=512, overlap_tokens: int =50 ) -> list[dict]:
    """
    chuck input text based on the max_tokens constraint
    """
    paragraphs = split_into_paragraphs(text)
    chunks=[]
    current_chunk = ""
    current_tokens = 0

    for para in paragraphs:
        para_tokens = count_tokens(para)

        if para_tokens> max_tokens:
            sentences = split_into_sentences(para)
            for sent in sentences:
                sent_tokens = count_tokens(sent)

                if current_tokens+sent_tokens > max_tokens:
                    if current_tokens:
                        chunks.append(current_chunk.strip())
                    current_chunk = _get_overlap_text(current_chunk, overlap_tokens) + " " + sent
                    current_tokens = count_tokens(current_chunk)

                else:
                    current_chunk += " " + sent
                    current_tokens+=sent_tokens

        else:
            if current_tokens + para_tokens > max_tokens:
                if current_chunk:
                    chunks.append(current_chunk.strip())

                current_chunk=_get_overlap_text(current_chunk, overlap_tokens) + " " + para

            else:
                current_chunk += "\n\n"+para
                current_tokens+= para_tokens


    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def chunk_document(doc: dict, max_tokens: int=512, overlap_tokens: int=50) -> list[dict]:
    all_chunks=[]
    for page in doc['pages']:
        page_chunks=chunk_text(page["text"], max_tokens, overlap_tokens)
        for i , chunk_content in enumerate(page_chunks):
            all_chunks.append({
                "text": chunk_content,
                "source": doc["source"],
                "page_num":page["page_num"],
                "chunk_id": f"{doc['source']}_p{page['page_num']}_c{i}"
            })

    return all_chunks