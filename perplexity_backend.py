import os
from dotenv import load_dotenv
from perplexity import Perplexity
from urllib.parse import urlparse

class PerplexityChat:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        
        if not self.api_key:
            try:
                import streamlit as st
                self.api_key = st.secrets.get("PERPLEXITY_API_KEY")
            except:
                pass
        
        if not self.api_key:
            raise ValueError("API key not found!")
        
        self.client = Perplexity(api_key=self.api_key)
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]
        
        self.available_models = {
            "sonar": "General factual Q&A; fast, concise, default",
            "sonar-pro": "Enhanced retrieval and deeper chat (Pro)",
            "sonar-reasoning": "Step-by-step reasoning and explanations",
            "sonar-reasoning-pro": "Advanced real-time reasoning (Pro, strongest)"
        }
    
    def get_ai_process_explanation(self):
        return {
            "steps": [
                {"icon": "🔎", "title": "Query Analysis", "description": "Parses your question to understand intent and identifies key entities"},
                {"icon": "🌐", "title": "Search Decision", "description": "Determines if web search is needed for current information"},
                {"icon": "🧠", "title": "Chain-of-Thought Reasoning", "description": "Breaks down complex problems using DeepSeek-R1 (128K context)"},
                {"icon": "📊", "title": "Information Synthesis", "description": "Retrieves and cross-references multiple sources for accuracy"},
                {"icon": "🔗", "title": "Citation Generation", "description": "Attributes each fact to its source with transparent tracking"}
            ]
        }
    
    def ask(self, question, model="sonar-reasoning-pro"):
        self.messages.append({"role": "user", "content": question})
        completion = self.client.chat.completions.create(model=model, messages=self.messages)
        response = completion.choices[0].message.content
        citations = getattr(completion, "citations", [])
        
        citation_map = {}
        formatted_citations = []
        for i, url in enumerate(citations, 1):
            domain = urlparse(url).netloc.replace("www.", "")
            year = "n.d."
            citation_map[f"[{i}]"] = f"({domain}, {year})"
            formatted_citations.append({"number": i, "domain": domain, "year": year, "url": url})
        
        formatted_response = response
        for tag, citation in citation_map.items():
            formatted_response = formatted_response.replace(tag, citation)
        
        self.messages.append({"role": "assistant", "content": response})
        return {"question": question, "answer": formatted_response, "raw_answer": response, "citations": formatted_citations, "model_used": model}
    
    def clear_history(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]
