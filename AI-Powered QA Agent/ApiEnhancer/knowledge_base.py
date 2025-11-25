import os
from typing import List, Dict, Optional
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from document_parser import DocumentParser


class KnowledgeBase:
    """
    Manages the knowledge base using ChromaDB for vector storage.
    Handles document ingestion, chunking, embedding, and retrieval.
    """
    
    def __init__(self, collection_name: str = "qa_agent_docs", persist_directory: str = "./chroma_db"):
        """
        Initialize the knowledge base.
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the database
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "QA Agent documentation and HTML knowledge base"}
        )
        
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=api_key  # type: ignore
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        self.document_count = 0
        self.chunk_count = 0
        self.html_content = None
    
    def ingest_document(self, file_content, filename: str, file_type: Optional[str] = None) -> Dict:
        """
        Ingest a single document into the knowledge base.
        
        Args:
            file_content: Content of the file (string or bytes)
            filename: Name of the file
            file_type: Optional file type override
            
        Returns:
            Dictionary with ingestion statistics
        """
        parsed_doc = DocumentParser.parse_document(file_content, filename, file_type)
        
        if parsed_doc["type"] == "html":
            self.html_content = parsed_doc.get("raw_html", parsed_doc["content"])
        
        text_chunks = self.text_splitter.split_text(parsed_doc["content"])
        
        chunk_ids = []
        chunk_texts = []
        chunk_metadatas = []
        
        for i, chunk in enumerate(text_chunks):
            chunk_id = f"{filename}_chunk_{i}"
            chunk_ids.append(chunk_id)
            chunk_texts.append(chunk)
            chunk_metadatas.append({
                "source": filename,
                "chunk_index": i,
                "doc_type": parsed_doc["type"],
                "total_chunks": len(text_chunks)
            })
        
        if chunk_texts:
            embeddings_list = self.embeddings.embed_documents(chunk_texts)
            
            self.collection.add(
                ids=chunk_ids,
                documents=chunk_texts,
                embeddings=embeddings_list,  # type: ignore
                metadatas=chunk_metadatas
            )
            
            self.document_count += 1
            self.chunk_count += len(chunk_texts)
        
        return {
            "filename": filename,
            "type": parsed_doc["type"],
            "chunks_created": len(text_chunks),
            "success": True
        }
    
    def ingest_multiple_documents(self, files: List[tuple]) -> List[Dict]:
        """
        Ingest multiple documents into the knowledge base.
        
        Args:
            files: List of tuples (file_content, filename, file_type)
            
        Returns:
            List of ingestion results
        """
        results = []
        for file_data in files:
            if len(file_data) == 2:
                file_content, filename = file_data
                file_type = None
            else:
                file_content, filename, file_type = file_data
            
            result = self.ingest_document(file_content, filename, file_type)
            results.append(result)
        
        return results
    
    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """
        Query the knowledge base using semantic search.
        
        Args:
            query_text: Query string
            n_results: Number of results to return
            
        Returns:
            Dictionary with query results
        """
        if self.chunk_count == 0:
            return {
                "documents": [],
                "metadatas": [],
                "distances": [],
                "message": "Knowledge base is empty"
            }
        
        query_embedding = self.embeddings.embed_query(query_text)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self.chunk_count)
        )
        
        return {
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "query": query_text
        }
    
    def get_html_content(self) -> Optional[str]:
        """
        Get the raw HTML content that was ingested.
        
        Returns:
            HTML content string or None
        """
        return self.html_content
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get knowledge base statistics.
        
        Returns:
            Dictionary with stats
        """
        return {
            "total_documents": self.document_count,
            "total_chunks": self.chunk_count,
            "has_html": self.html_content is not None
        }
    
    def reset(self):
        """
        Reset the knowledge base by deleting and recreating the collection.
        """
        try:
            self.client.delete_collection(name=self.collection_name)
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "QA Agent documentation and HTML knowledge base"}
        )
        
        self.document_count = 0
        self.chunk_count = 0
        self.html_content = None
