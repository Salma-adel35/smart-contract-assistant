def format_sources(docs):
    formatted = []
    for doc in docs:
        snippet = doc.page_content[:300]
        source = doc.metadata.get("source", "Unknown")
        formatted.append(f"Source: {source}\nSnippet:\n{snippet}\n")
    return "\n---\n".join(formatted)
