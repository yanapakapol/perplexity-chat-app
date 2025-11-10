import os
from dotenv import load_dotenv
from perplexity import Perplexity
from urllib.parse import urlparse

class PerplexityChat:
    def __init__(self):
        # Load from .env for local development
        load_dotenv()
        
        # Try environment variable first (local)
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        
        # If not found, try Streamlit secrets (deployed)
        if not self.api_key:
            try:
                import streamlit as st
                self.api_key = st.secrets.get("PERPLEXITY_API_KEY")
            except:
                pass
        
        if not self.api_key:
            raise ValueError("API key not found! Check .env locally or Streamlit Secrets when deployed.")
        
        self.client = Perplexity(api_key=self.api_key)
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        
        self.available_models = {
            "sonar": "General factual Q&A; fast, concise, default",
            "sonar-pro": "Enhanced retrieval and deeper chat (Pro)",
            "sonar-reasoning": "Step-by-step reasoning and explanations",
            "sonar-reasoning-pro": "Advanced real-time reasoning (Pro, strongest)"
        }
    
    def get_ai_process_explanation(self):
        """Returns the AI's thinking process explanation"""
        return {
            "steps": [
                {
                    "icon": "🔎",
                    "title": "Query Analysis",
                    "description": "Parses your question to understand intent and identifies key entities"
                },
                {
                    "icon": "🌐",
                    "title": "Search Decision",
                    "description": "Determines if web search is needed for current information"
                },
                {
                    "icon": "🧠",
                    "title": "Chain-of-Thought Reasoning",
                    "description": "Breaks down complex problems using DeepSeek-R1 (128K context)"
                },
                {
                    "icon": "📊",
                    "title": "Information Synthesis",
                    "description": "Retrieves and cross-references multiple sources for accuracy"
                },
                {
                    "icon": "🔗",
                    "title": "Citation Generation",
                    "description": "Attributes each fact to its source with transparent tracking"
                }
            ]
        }
    
    def ask(self, question, model="sonar-reasoning-pro"):
        """Send question to Perplexity and get formatted response"""
        # Add user question to history
        self.messages.append({"role": "user", "content": question})
        
        # Make API call
        completion = self.client.chat.completions.create(
            model=model,
            messages=self.messages
        )
        
        # Extract response and citations
        response = completion.choices[0].message.content
        citations = getattr(completion, "citations", [])
        
        # Format citations
        citation_map = {}
        formatted_citations = []
        
        for i, url in enumerate(citations, 1):
            domain = urlparse(url).netloc.replace("www.", "")
            year = "n.d."
            citation_map[f"[{i}]"] = f"({domain}, {year})"
            formatted_citations.append({
                "number": i,
                "domain": domain,
                "year": year,
                "url": url
            })
        
        # Replace citation tags in response
        formatted_response = response
        for tag, citation in citation_map.items():
            formatted_response = formatted_response.replace(tag, citation)
        
        # Add assistant response to history
        self.messages.append({"role": "assistant", "content": response})
        
        return {
            "question": question,
            "answer": formatted_response,
            "raw_answer": response,
            "citations": formatted_citations,
            "model_used": model
        }
    
    def clear_history(self):
        """Clear conversation history"""
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
