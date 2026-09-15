from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5"):
        self.model=SentenceTransformer(model_name)

    def embed_text(self, texts: list[str]) -> list[list[float]]:
        embeddings=self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
    
        )
        return embeddings.tolist()

    def embed_query(self, query: str)  -> list[float]:
        instruction="Represent this sentence for searching relevant passage: "

        embedding=self.model.encode(instruction + query, normalize_embeddings=True)
        return embedding.tolist()