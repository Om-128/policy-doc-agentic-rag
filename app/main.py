import os
import sys
from custom_exception import CustomException

from app.agents.graph import app

def run():
    """
    Entry point to run the Agentic RAG system.
    """
    print("=== Agentic RAG System ===")
    print("Type 'exit' to quit\n")

    while True:
        question = input("Ask a question: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        
        if not question:
            print("Please enter a valid question.\n")
            continue

        result = app.invoke({
            "question":question
        })

        print("\n--- Answer ---")
        print(result["answer"])
        print("\n--- Source Used ---")
        print(result["source"])
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    run()