# app.py
from core.state_manager import StateManager
from core.context_analyzer import ContextAnalyzer
from core.emotion_resolver import EmotionResolver
from core.prompt_assembler import PromptAssembler
from core.memory_store import MemoryStore
from core.decay_manager import DecayManager
from core.emotion import Emotion


class DummyLLM:
    """
    Placeholder LLM used to validate prompt flow.
    Replace later with a real model client.
    """
    def generate(self, prompt: str) -> str:
        return "DUMMY RESPONSE: (LLM output would appear here)"


def main():
    print("=== Desktop AI Companion (CLI Prototype) ===")
    print("Type 'exit' to quit.\n")

    # Core system components
    state_manager = StateManager()
    context_analyzer = ContextAnalyzer()
    emotion_resolver = EmotionResolver()
    prompt_assembler = PromptAssembler()

    # Memory + decay
    memory_store = MemoryStore()
    decay_manager = DecayManager(state_manager, memory_store)

    # LLM stub
    llm = DummyLLM()

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            print("(no input)")
            continue

        if user_input.lower() == "exit":
            print("Shutting down.")
            break

        # ⏱ background decay (emotion + memory)
        decay_manager.tick()

        # 1️⃣ Context analysis
        context = context_analyzer.analyze(user_input)

        # 2️⃣ Emotion proposal
        proposed_emotion = emotion_resolver.resolve(context)

        # 3️⃣ FSM enforcement
        if proposed_emotion is not None:
            final_emotion = state_manager.request_transition(proposed_emotion)
        else:
            final_emotion = state_manager.current_emotion

        # 4️⃣ Forced decay check (safety)
        final_emotion = state_manager.decay_if_needed()

        # 5️⃣ Memory summary (read-only, safe)
        memory_summary = memory_store.get_memory_summary()

        # 6️⃣ Prompt assembly
        prompt = prompt_assembler.assemble(
            user_input=user_input,
            emotion=final_emotion,
            memory_summary=memory_summary
        )

        # 7️⃣ LLM call (dummy)
        response = llm.generate(prompt)

        # 8️⃣ Output
        print("\n--- DEBUG ---")
        print(f"Intent: {context.intent}")
        print(f"Emotional Pressure: {context.emotional_pressure}")
        print(f"Flags: {context.flags}")
        print(f"Proposed Emotion: {proposed_emotion}")
        print(f"Final Emotion: {final_emotion}")
        print("--- MEMORY SUMMARY ---")
        print(memory_summary if memory_summary else "(none)")
        print("--- PROMPT ---")
        print(prompt)
        print("--- RESPONSE ---")
        print(response)
        print("--------------\n")


if __name__ == "__main__":
    main()
