import os
from dotenv import load_dotenv
from perplexity import Perplexity
from urllib.parse import urlparse

# -------- STEP 1: Load API key --------
load_dotenv()
api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    raise ValueError("API key could not be loaded. Check .env file and format!")

# -------- STEP 2: Setup message history --------
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]

# -------- STEP 3: Model selection --------
available_models = {
    "sonar":      "General factual Q&A; fast, concise, default",
    "sonar-pro":  "Enhanced retrieval and deeper chat (Pro, best for complex Q&A)",
    "sonar-reasoning":      "Step-by-step reasoning and explanations",
    "sonar-reasoning-pro":  "Advanced, real-time reasoning (Pro, strongest thinking)"
}
selected_model = "sonar-reasoning-pro"

# -------- STEP 4: Initialize client --------
client = Perplexity(api_key=api_key)

# -------- STEP 5: Make API call --------
print("="*70)
print("🔍 SENDING REQUEST TO PERPLEXITY AI...")
print("="*70)
print(f"Model: {selected_model}")
print(f"Query: {messages[-1]['content']}")
print("="*70 + "\n")

completion = client.chat.completions.create(
    model=selected_model,
    messages=messages
)

# -------- STEP 6: Display AI's processing logic --------
print("="*70)
print("⚙️ AI PROCESSING LOGIC")
print("="*70)
print("The sonar-reasoning-pro model uses the following process:")
print()
print("1. 🔎 Query Analysis")
print("   - Parses your question to understand intent")
print("   - Identifies key entities and required information type")
print()
print("2. 🌐 Search Decision")
print("   - Determines if web search is needed for current information")
print("   - Selectively triggers real-time search when relevant")
print()
print("3. 🧠 Chain-of-Thought Reasoning")
print("   - Breaks down complex problems into logical steps")
print("   - Uses DeepSeek-R1 reasoning capabilities")
print("   - Processes up to 128K tokens of context")
print()
print("4. 📊 Information Synthesis")
print("   - Retrieves and analyzes multiple sources")
print("   - Cross-references information for accuracy")
print("   - Combines findings into coherent answer")
print()
print("5. 🔗 Citation Generation")
print("   - Attributes each fact to its source")
print("   - Provides transparent reference tracking")
print("="*70 + "\n")

# Extract the main response
response = completion.choices[0].message.content

# -------- STEP 7: Extract citations (list of URLs) --------
citations = getattr(completion, "citations", [])

print("="*70)
print("📚 SOURCES CONSULTED")
print("="*70)
print(f"Total sources found: {len(citations)}")
if citations:
    for i, url in enumerate(citations, 1):
        domain = urlparse(url).netloc.replace("www.", "")
        print(f"  [{i}] {domain}")
else:
    print("  No external sources cited (answer from model knowledge)")
print("="*70 + "\n")

# -------- STEP 8: Build citation map with website name and year --------
citation_map = {}
for i, url in enumerate(citations, 1):
    domain = urlparse(url).netloc.replace("www.", "")
    year = "n.d."  # Not available from citations list alone
    citation_map[f"[{i}]"] = f"({domain}, {year})"

# Replace citation tags in response
for tag, citation in citation_map.items():
    response = response.replace(tag, citation)

# -------- STEP 9: Display final answer with formatted citations --------
print("="*70)
print("✅ FINAL ANSWER (with formatted citations)")
print("="*70)
print(response)
print("="*70 + "\n")

# -------- STEP 10: Print full citation list --------
print("="*70)
print("📖 REFERENCES")
print("="*70)
if citations:
    for i, url in enumerate(citations, 1):
        domain = urlparse(url).netloc.replace("www.", "")
        print(f"{i}. ({domain}, n.d.)")
        print(f"   URL: {url}\n")
else:
    print("No citations available for this response.")
print("="*70)
