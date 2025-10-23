def format_prompt(context_chunks, question):
    """
    Build a structured prompt for the LLM using retrieved context chunks and the user's question.
    Each chunk should include its source citation.
    """
    context_text = ""
    for chunk in context_chunks:
        source = chunk.get("source", "unknown_source")
        content = chunk.get("content", "")
        context_text += f"From {source}:\n{content}\n\n"

    prompt = (
        "You are a helpful assistant for a utility company. Use the following context to answer the question.\n\n"
        f"Context:\n{context_text}"
        f"Question:\n{question}\n\n"
        "Instructions:\n"
        "- Be concise and accurate.\n"
        "- Cite the source document (e.g., tariff_policy.pdf).\n"
        "- Keep tone polite and professional.\n"
        "- If unsure, say 'I'm not sure' and suggest escalation to a human agent."
    )

    return prompt


# Example usage
if __name__ == "__main__":
    chunks = [
        {"source": "tariff_policy.pdf", "content": "Late payment fee is $15."},
        {"source": "outage_faqs.txt", "content": "Report outages via the online portal."}
    ]
    question = "What is the late payment fee?"
    formatted_prompt = format_prompt(chunks, question)
    print(formatted_prompt)
