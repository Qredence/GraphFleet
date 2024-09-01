from typing import List, Dict, Any, Tuple
# Remove or comment out the problematic import
# from graphrag import GraphRAG, GraphRAGConfig
from .config import settings
import networkx as nx
import matplotlib.pyplot as plt
import genaiscript.script
from genaiscript.agentic import AgentExecutor
from genaiscript.tools import ContainerizedTool, WebSearch, WebScraper
import PyPDF2
from bs4 import BeautifulSoup
import json
import os
from .storage import StorageBackend, LocalStorage, PostgresStorage


class GraphFleet:
    def __init__(self):
        # Comment out or remove GraphRAG-related initialization
        # self.graph_rag_config = GraphRAGConfig(
        #     api_key=settings.api_key,
        #     api_base=settings.api_base,
        #     api_version=settings.api_version,
        #     deployment_name=settings.deployment_name,
        #     embedding_model=settings.embedding_model,
        #     llm_model=settings.llm_model,
        #     api_type=settings.api_type
        # )
        # self.graph_rag = GraphRAG(self.graph_rag_config)
        self.knowledge_graph = nx.Graph()
        self.agent = AgentExecutor(model=settings.genaiscript_default_model)
        self.web_search = WebSearch()
        self.containerized_tool = ContainerizedTool("graphfleet-tool")
        self.confidence_threshold = 0.7
        self.learning_rate = 0.1
        self.human_feedback_count = 0
        self.web_scraper = WebScraper()

        # Initialize storage backend
        if settings.storage_backend == StorageBackend.LOCAL:
            self.storage = LocalStorage(
                settings.storage_connection_string, settings.parquet_storage_path)


        elif settings.storage_backend == StorageBackend.POSTGRES:
            self.storage = PostgresStorage(settings.postgres_host, settings.postgres_port,
            settings.postgres_user, settings.postgres_password, settings.postgres_db)
        # Initialize other storage backends similarly

    def preprocess_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Implement document preprocessing logic here
        return documents

    def extract_entities(self, document: Dict[str, Any]) -> List[str]:
        # Implement entity extraction logic here
        return []

    def map_relationships(self, entities: List[str]) -> List[tuple]:
        # Implement relationship mapping logic here
        return []

    def index_documents(self, documents: List[Dict[str, Any]]):
        for doc in documents:
            doc_id = self.storage.store_document(doc)
            # Update the knowledge graph with the new document
            self.update_knowledge_graph(doc, doc_id)

    def update_knowledge_graph(self, entities: List[str], relationships: List[tuple]):
        self.knowledge_graph.add_nodes_from(entities)
        self.knowledge_graph.add_edges_from(relationships)

    def query(self, question: str, method: str = "global") -> Tuple[str, float]:
        # Implement a basic query method without using GraphRAG
        # This is a placeholder implementation
        answer = f"This is a placeholder answer for the question: {question}"
        confidence = 0.5
        return answer, confidence

    def web_enhanced_query(self, question: str) -> Tuple[str, float]:
        script = genaiscript.script({
            "model": settings.genaiscript_default_model,
            "messages": [
                {"role": "system", "content": "You are an AI assistant that answers questions using web search. Provide a confidence score between 0 and 1 for your answer."},
                {"role": "user", "content": question}
            ],
            "tools": [self.web_search]
        })

        result = script.run()
        answer, confidence = self.parse_web_result(result.content)
        return answer, confidence

    def parse_web_result(self, content: str) -> Tuple[str, float]:
        # Implement parsing logic to extract answer and confidence from the web search result
        # This is a simplified example; you may need to adjust based on the actual output format
        parts = content.split("Confidence: ")
        answer = parts[0].strip()
        confidence = float(parts[1]) if len(parts) > 1 else 0.5
        return answer, confidence

    def learn_from_web_search(self, question: str, answer: str):
        # Implement logic to update the knowledge graph with new information from web search
        # This is a simplified example; you may need to implement more sophisticated learning
        document = {"content": f"Q: {question}\nA: {answer}", "metadata": {"source": "web_search"}}
        self.index_documents([document])

    def ask_human(self, question: str, ai_answer: str) -> str:
        print(f"Question: {question}")
        print(f"AI Answer (confidence < {self.confidence_threshold}): {ai_answer}")
        human_answer = input("Please provide a correct answer or press Enter to accept the AI answer: ")
        self.human_feedback_count += 1
        return human_answer if human_answer else ai_answer

    def learn_from_human(self, question: str, answer: str):
        document = {"content": f"Q: {question}\nA: {answer}", "metadata": {"source": "human_feedback"}}
        self.index_documents([document])
        self.update_confidence_threshold()

    def update_confidence_threshold(self):
        # Dynamically adjust confidence threshold based on human feedback frequency
        if self.human_feedback_count > 10:
            self.confidence_threshold += self.learning_rate
            self.confidence_threshold = min(self.confidence_threshold, 0.9)
            self.human_feedback_count = 0

    def self_improve(self):
        # Implement self-improvement logic
        # This could involve analyzing past queries, identifying weak areas, and generating new learning material
        weak_areas = self.identify_weak_areas()
        for area in weak_areas:
            self.generate_and_learn_new_material(area)

    def identify_weak_areas(self) -> List[str]:
        # Implement logic to identify areas where the model performs poorly
        # This is a placeholder implementation
        return ["topic1", "topic2", "topic3"]

    def generate_and_learn_new_material(self, topic: str):
        script = genaiscript.script({
            "model": settings.genaiscript_default_model,
            "messages": [
                {"role": "system", "content": "Generate learning material on the given topic."},
                {"role": "user", "content": f"Create a comprehensive explanation of {topic}."}
            ]
        })

        result = script.run()
        self.learn_from_web_search(topic, result.content)

    def visualize_graph(self):
        plt.figure(figsize=(12, 8))
        nx.draw(self.knowledge_graph, with_labels=True, node_color='lightblue', node_size=500, font_size=8, font_weight='bold')
        plt.title("GraphFleet Knowledge Graph")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('knowledge_graph.png')
        plt.close()

    def search(self, query: str, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        return self.storage.search_documents(query, limit, offset)

    def convert_to_text(self, file_path: str) -> str:
        _, file_extension = os.path.splitext(file_path)

        if file_extension.lower() == '.pdf':
            return self._convert_pdf_to_text(file_path)
        elif file_extension.lower() == '.json':
            return self._convert_json_to_text(file_path)
        elif file_extension.lower() in ['.html', '.htm']:
            return self._convert_html_to_text(file_path)
        elif file_extension.lower() == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def _convert_pdf_to_text(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _convert_json_to_text(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return json.dumps(data, indent=2)

    def _convert_html_to_text(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()

    def process_file_with_genaiscript(self, file_path: str) -> str:
        text_content = self.convert_to_text(file_path)

        script = genaiscript.script({
            "model": settings.genaiscript_default_model,
            "messages": [
                {"role": "system", "content": "You are an AI assistant that processes and enhances text content."},
                {"role": "user", "content": f"Process and enhance the following text:\n\n{text_content}"}
            ],
            "tools": [self.web_search, self.containerized_tool]
        })

        result = script.run()
        return result.content

    def index_file(self, file_path: str):
        processed_text = self.process_file_with_genaiscript(file_path)
        document = {"content": processed_text, "metadata": {"source": file_path}}
        self.index_documents([document])

    def generate_release_notes(self, version: str, changes: List[str]) -> str:
        script = genaiscript.script({
            "model": settings.genaiscript_default_model,
            "messages": [
                {"role": "system", "content": "You are an AI assistant that generates release notes."},
                {"role": "user", "content": f"Generate release notes for version {version} with the following changes:\n\n" + "\n".join(changes)}
            ]
        })

        result = script.run()
        return result.content

    def advanced_reasoning(self, question: str) -> str:
        return self.agent.run(question)

    def containerized_processing(self, data: Any) -> Any:
        return self.containerized_tool.run(data)

    def monthy_scrape(self, url: str, output_format: str = "text") -> str:
        scraper = WebScraper()
        script = genaiscript.script({
            "model": settings.genaiscript_default_model,
            "messages": [
                {"role": "system", "content": "You are Monthy, an AI assistant that scrapes and processes web content."},
                {"role": "user", "content": f"Scrape the content from {url} and format it as {output_format}."}
            ],
            "tools": [scraper]
        })

        result = script.run()

        if output_format == "csv":
            # Assuming the result is a string that can be converted to CSV
            # You might need to implement additional logic to properly format as CSV
            return result.content
        else:
            return result.content

    def ask_monty(self, request: str) -> str:
        script = genaiscript.script({
            "model": settings.genaiscript_default_model,
            "messages": [
                {"role": "system", "content": "You are Monty, an AI assistant with a wide range of capabilities including writing scripts, release notes, documentation, and code interpretation. Provide detailed and helpful responses."},
                {"role": "user", "content": request}
            ],
            "tools": [self.web_search, self.containerized_tool, self.web_scraper]
        })

        result = script.run()
        return result.content
