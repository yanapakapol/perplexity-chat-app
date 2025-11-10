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
        
        # Expanded model list based on Perplexity Pro availability
        self.available_models = {
            # Sonar Family
            "sonar": {
                "name": "Sonar",
                "description": "Fast, accurate search",
                "tier": "Free",
                "reasoning": False,
                "icon": "⚡"
            },
            "sonar-pro": {
                "name": "Sonar Pro",
                "description": "Enhanced retrieval & depth",
                "tier": "Pro",
                "reasoning": False,
                "icon": "🔍"
            },
            "sonar-reasoning": {
                "name": "Sonar Reasoning",
                "description": "Step-by-step thinking",
                "tier": "Free",
                "reasoning": True,
                "icon": "🧠"
            },
            "sonar-reasoning-pro": {
                "name": "Sonar Reasoning Pro",
                "description": "Advanced real-time reasoning",
                "tier": "Pro",
                "reasoning": True,
                "icon": "⚡🧠"
            },
            
            # OpenAI Models
            "gpt-5": {
                "name": "GPT-5",
                "description": "Expert-level reasoning",
                "tier": "Pro",
                "reasoning": False,
                "icon": "🤖"
            },
            "gpt-4o": {
                "name": "GPT-4 Omni",
                "description": "Fast multimodal tasks",
                "tier": "Pro",
                "reasoning": False,
                "icon": "🔷"
            },
            "o3-pro": {
                "name": "o3-Pro",
                "description": "Cost-efficient reasoning",
                "tier": "Max",
                "reasoning": True,
                "icon": "💎"
            },
            
            # Anthropic Models
            "claude-sonnet-4.5": {
                "name": "Claude Sonnet 4.5",
                "description": "Strong coding & reasoning",
                "tier": "Pro",
                "reasoning": False,
                "icon": "🎵"
            },
            "claude-sonnet-4.5-thinking": {
                "name": "Claude Sonnet 4.5 Thinking",
                "description": "Extended thinking mode",
                "tier": "Pro",
                "reasoning": True,
                "icon": "🎵💭"
            },
            "claude-opus-4.1": {
                "name": "Claude Opus 4.1",
                "description": "200K context window",
                "tier": "Max",
                "reasoning": False,
                "icon": "🎼"
            },
            "claude-opus-4.1-thinking": {
                "name": "Claude Opus 4.1 Thinking",
                "description": "Deep analytical thinking",
                "tier": "Max",
                "reasoning": True,
                "icon": "🎼💭"
            },
            
            # Google Models
            "gemini-2.5-pro": {
                "name": "Gemini 2.5 Pro",
                "description": "1M token context",
                "tier": "Pro",
                "reasoning": False,
                "icon": "♊"
            },
            "gemini-2.5-flash": {
                "name": "Gemini 2.5 Flash",
                "description": "Fast multimodal",
                "tier": "Free",
                "reasoning": False,
                "icon": "⚡♊"
            },
            
            # xAI Models
            "grok-4": {
                "name": "Grok 4",
                "description": "Real-time analysis",
                "tier": "Pro",
                "reasoning": False,
                "icon": "🤠"
            }
        }
    
    def get_models_by_tier(self, tier=None):
        """Get models filtered by tier"""
        if tier is None:
            return self.available_models
        return {k: v for k, v in self.available_models.items() if v["tier"] == tier}
    
    def get_reasoning_models(self):
        """Get only reasoning models"""
        return {k: v for k, v in self.available_models.items() if v["reasoning"]}
    
    def ask(self, question, model="sonar-reasoning-pro"):
        self.messages.append({"role": "user", "content": question})
        
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=self.messages
            )
            
            response = completion.choices[0].message.content
            citations = getattr(completion, "citations", [])
            
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
            
            formatted_response = response
            for tag, citation in citation_map.items():
                formatted_response = formatted_response.replace(tag, citation)
            
            self.messages.append({"role": "assistant", "content": response})
            
            return {
                "question": question,
                "answer": formatted_response,
                "raw_answer": response,
                "citations": formatted_citations,
                "model_used": model
            }
        except Exception as e:
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "raw_answer": str(e),
                "citations": [],
                "model_used": model
            }
    
    def clear_history(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]
