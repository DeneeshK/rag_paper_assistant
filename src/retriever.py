class Retriver:
    def __init__(self, embeder, vectorstore, top_k:int =5):
        self.embedder=embeder
        self.vectorstore=vectorstore
        self.top_k=top_k

    def retrieve(self, query:str) -> list[dict]:
        query_embedding=self.embedder.embed_query(query)
        raw=self.vectorstore.query(query_embedding, top_k=self.top_k)


        results=[]
        for i in range(len(raw["ids"][0])):
            results.append({
                "text": raw["documents"][0][i],
                "source":raw["metadata"][0][i]["source"],
                "page_num":raw["metadata"][0][i]["page_num"],
                "distance": raw["distances"][0][i]
            })

        return results