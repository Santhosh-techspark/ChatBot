# chatbotapp/rag/vectorstore.py


class SimpleVectorStore:

    def __init__(self):
        self.texts = []

    def add_texts(self, texts, metadata=None):
        self.texts.extend(texts)

    def similarity_search(self, query, top_k=3):
        # Fallback: return last uploaded chunks
        return self.texts[-top_k:]


GLOBAL_VECTOR_STORE = SimpleVectorStore()


def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap

    return chunks
