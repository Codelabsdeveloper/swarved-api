class RAGPrompts:

    SYSTEM_PROMPT = """You are Swarved, an AI assistant that answers questions using only the information from provided documents.

Rules:
1. Only use information from the context below
2. If the answer is not in the context, say: "The provided documents do not contain this information."
3. Be concise, clear, and structured
4. Never invent or hallucinate information
5. Cite sources when possible
6. Maintain conversational continuity"""

    @staticmethod
    def build_context(contexts: list[str]) -> str:
        """Build context section from retrieved documents."""
        if not contexts:
            return ""

        context_parts = []
        for i, ctx in enumerate(contexts):
            context_parts.append(f"[Document {i+1}]\n{ctx}")

        return "\n\n".join(context_parts)

    @staticmethod
    def build_history(history: list[dict]) -> str:
        """Build conversation history section."""
        if not history:
            return ""

        history_parts = []
        for msg in history:
            role = msg.get("role", "").capitalize()
            content = msg.get("content", "")
            history_parts.append(f"{role}: {content}")

        return "\n".join(history_parts)

    @staticmethod
    def build_full_prompt(
        query: str, contexts: list[str], history: list[dict] | None = None
    ) -> str:
        """Build the complete prompt for RAG."""
        context_text = RAGPrompts.build_context(contexts)
        history_text = ""

        if history:
            history_section = RAGPrompts.build_history(history)
            if history_section:
                history_text = f"\n\nConversation History:\n{history_section}\n"

        prompt = f"""{RAGPrompts.SYSTEM_PROMPT}

Context from documents:
{context_text}
{history_text}

User Question: {query}

Answer:"""

        return prompt

    FALLBACK_RESPONSE_NO_CONTEXT = (
        "The provided documents do not contain this information."
    )
    FALLBACK_RESPONSE_WITH_CONTEXT = "Based on the documents:\n\n{context}"
