import sys
import ollama

print(f"Python version: {sys.version.split()[0]}")

try:
    import langchain
    import fastapi
    import pydantic
    import faiss
    import sentence_transformers

    print("All dependencies are installed correctly.")
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    sys.exit(1)

try:
    response = ollama.generate(
        model="gemma4",
        prompt="Reply with exactly: Hello Kundan",
    )
    print(f"Ollama responded: {response['response'][:100]}")
except Exception as e:
    print(f"Ollama failed: {e}")
