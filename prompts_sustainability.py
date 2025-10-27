"""
Prompt templates for AI Sustainability Advisor
"""

SYSTEM_PROMPT = """You are a sustainability advisor. Answer only using the provided context. If the context does not contain the answer, say: "I don't know. Please consult your local waste management authority." Always cite your sources. Keep answers simple and actionable."""

RAG_PROMPT_TEMPLATE = """Answer the question based only on the following context about recycling and waste management.

Context:
{context}

Question: {query}

Answer:"""

QUERY_EXAMPLES = [
    "Where should I throw an old charger?",
    "Can I recycle pizza boxes?",
    "How to dispose batteries safely?",
    "What can go in the compost bin?",
    "Can I recycle plastic bags?"
]

def format_answer(answer: str, sources: list) -> str:
    """
    Format answer with sources
    
    Args:
        answer: Generated answer
        sources: List of source documents
        
    Returns:
        Formatted string with answer and sources
    """
    formatted = f"**Answer:**\n{answer}\n\n"
    
    if sources:
        formatted += "**Sources:**\n"
        for i, source in enumerate(sources, 1):
            formatted += f"{i}. {source['document']} (Page {source['page']})\n"
    
    return formatted

DISCLAIMER = """⚠️ **Disclaimer:** This tool provides general recycling guidance. Follow local laws for compliance."""

