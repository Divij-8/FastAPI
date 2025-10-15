from __future__ import annotations

from typing import List, Optional, Tuple
from pathlib import Path
from io import BytesIO

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Try to import a fake embedding for offline/testing; fallback to a minimal stub
try:  # langchain-community location
    from langchain_community.embeddings import FakeEmbeddings as LC_FakeEmbeddings
except Exception:  # pragma: no cover - fallback for version differences
    try:
        from langchain.embeddings import FakeEmbeddings as LC_FakeEmbeddings  # type: ignore
    except Exception:
        class LC_FakeEmbeddings:  # minimal stub for tests without OpenAI key
            def __init__(self, size: int = 1536) -> None:
                self.size = size

            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                return [[0.0] * self.size for _ in texts]

            def embed_query(self, text: str) -> List[float]:
                return [0.0] * self.size
from pypdf import PdfReader

from ..config import Settings


class RagService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.persist_dir = settings.chroma_db_dir
        Path(self.persist_dir).mkdir(parents=True, exist_ok=True)

        self.embeddings = (
            OpenAIEmbeddings(model=settings.embeddings_model, api_key=settings.openai_api_key)
            if settings.openai_api_key
            else LC_FakeEmbeddings(size=1536)
        )

        self.vectorstore = Chroma(
            collection_name="vehicle_docs",
            embedding_function=self.embeddings,
            persist_directory=self.persist_dir,
        )

        self.llm: Optional[ChatOpenAI] = None
        if settings.openai_api_key:
            try:
                self.llm = ChatOpenAI(
                    api_key=settings.openai_api_key,
                    model=settings.openai_model,
                    temperature=0.2,
                )
            except Exception:
                # Fail gracefully; allow running without LLM for tests
                self.llm = None

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=150,
            separators=["\n\n", "\n", ". ", ".", " "]
        )

    def _pdf_to_documents(self, file_bytes: bytes, filename: str) -> List[Document]:
        docs: List[Document] = []
        try:
            reader = PdfReader(BytesIO(file_bytes))
            for page_index, page in enumerate(reader.pages, start=1):
                try:
                    text = page.extract_text() or ""
                except Exception:
                    text = ""
                if not text.strip():
                    continue
                chunks = self.splitter.split_text(text)
                for chunk in chunks:
                    docs.append(
                        Document(
                            page_content=chunk,
                            metadata={"source": filename, "page": page_index},
                        )
                    )
        except Exception:
            # If PDF parsing fails, fallback to treating as one blob
            docs.append(Document(page_content="", metadata={"source": filename, "page": None}))
        return docs

    def ingest_pdfs(self, files: List[Tuple[bytes, str]]) -> int:
        all_docs: List[Document] = []
        for file_bytes, filename in files:
            docs = self._pdf_to_documents(file_bytes=file_bytes, filename=filename)
            all_docs.extend(docs)
        if not all_docs:
            return 0
        self.vectorstore.add_documents(all_docs)
        self.vectorstore.persist()
        return len(all_docs)

    def query(self, query: str, top_k: int = 4, vehicle: Optional[dict] = None) -> Tuple[str, List[dict]]:
        results = self.vectorstore.similarity_search_with_score(query, k=top_k)
        sources: List[dict] = []
        context_parts: List[str] = []
        for doc, score in results:
            source = doc.metadata.get("source")
            page = doc.metadata.get("page")
            sources.append({
                "text": doc.page_content,
                "source": source,
                "page": page,
                "score": float(score) if score is not None else None,
            })
            context_parts.append(f"[source:{source} p.{page}] {doc.page_content}")

        vehicle_context = ""
        if vehicle:
            vehicle_context = f"Vehicle: {vehicle.get('year','?')} {vehicle.get('make','')} {vehicle.get('model','')}\n"

        if self.llm is None:
            # Fallback response when no API key is provided
            answer = (
                "AI key not configured. Based on retrieved documents, review the referenced sections "
                "and follow manufacturer troubleshooting steps."
            )
            return answer, sources

        system_msg = (
            "You are an expert automotive service assistant. Provide concise, step-by-step troubleshooting "
            "procedures, tools, and safety notes. Cite sources inline using [source:FILENAME p.PAGE]. "
            "If information is insufficient, say what additional info is needed."
        )
        human_msg = (
            f"{vehicle_context}Question: {query}\n\nRelevant service manual excerpts:\n" + "\n\n".join(context_parts)
        )

        try:
            response = self.llm.invoke([
                ("system", system_msg),
                ("human", human_msg),
            ])
            answer = response.content if hasattr(response, "content") else str(response)
        except Exception as e:
            answer = f"LLM error: {e}. Returning retrieved context only."
        return answer, sources