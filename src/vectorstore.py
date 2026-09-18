import chromadb


class VectorStore:
    def __init__(self, persist_dir: dir, collection_name: str):
        self.client=chromadb.PersistentClient(path=persist_dir)
        self.collection=self.client.get_or_Create_collection(
            name=collection_name,
            metadata={"hnsw:space" : "cosine" }
        )

    def add_chunk(self, chunks: list[dict], embeddings:list[list[float]]):
        self.collection.add(
            ids=[c["chunk_id"] for c in chunks],
            embeddings=embeddings,
            documents=[c["text"] for c in chunks],
            metadata=[{"source": c["source"], "page_num": c["page_num"]} for c in chunks]
        )

    def query(self, query_embedding:list[float], top_k:int =5)-> dict:
        return self.collection.query(query_embedding=[query_embedding], n_results=top_k)


    def count(self) -> int:
        return self.collection.count()