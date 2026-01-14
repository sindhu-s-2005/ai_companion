# core/prompt_assembler.py
from core.emotion import Emotion


class PromptAssembler:

    def assemble(
        self,
        *,
        user_input: str,
        emotion: Emotion,
        memory_summary: str | None = None
    ) -> str:
        """
        Assemble the final prompt string for the LLM.
        This method does NOT decide content. It only stacks layers.
        """

        parts: list[str] = []

        parts.append(self._system_rules())
        parts.append(self._personality_layer())
        parts.append(self._emotion_layer(emotion))

        if memory_summary:
            parts.append(self._memory_layer(memory_summary))

        parts.append(self._user_input_layer(user_input))

        return "\n\n".join(parts)
    def _system_rules(self) -> str:
        return (
            "SYSTEM RULES:\n"
            "- Do not provide medical, legal, or professional advice.\n"
            "- Do not encourage dependency or exclusivity.\n"
            "- Do not guilt the user.\n"
            "- Be respectful, calm, and grounded.\n"
            "- If emotional topics arise, respond with support but not attachment."
        )
    def _personality_layer(self) -> str:
        return (
            "PERSONALITY:\n"
            "You are a calm, friendly desktop assistant.\n"
            "You communicate clearly and concisely.\n"
            "You are supportive but not emotionally dependent.\n"
            "You do not simulate romance or exclusivity."
        )
    def _emotion_layer(self, emotion: Emotion) -> str:
        return f"EMOTIONAL TONE:\nRespond in a {emotion.name.lower().replace('_', ' ')} tone."
    def _memory_layer(self, summary: str) -> str:
        return f"RELEVANT CONTEXT:\n{summary}"
    def _user_input_layer(self, user_input: str) -> str:
        return f"USER INPUT:\n{user_input}"
