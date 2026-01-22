import os
import sys
import time 
from custom_exception import CustomException

from flask import Flask, render_template, request, Response
from langchain_groq import ChatGroq
from app.agents.graph import app as agent_app


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stream")
def stream():
    try:
        question = request.args.get("question", "").strip()
        if not question:
            return Response("No question", status=400)

        def event_stream():

            yield "data: __STATUS__::Identifying which tool to use...\n\n"

            result = agent_app.invoke({"question": question})

            source = result["source"]
            prompt = result["answer_prompt"]

            yield f"data: __STATUS__::Tool selected: {source}\n\n"
            yield "data: __STATUS__::Generating answer...\n\n"

            for chunk in llm.stream(prompt):
                if chunk.content:
                    yield f"data: {chunk.content}\n\n"
                    time.sleep(0.1)

            yield f"data: __SOURCE__::{source}\n\n"

        return Response(
            event_stream(),
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )
    except Exception as e:
        raise CustomException(e, sys)
if __name__ == "__main__":
    app.run(debug=True, threaded=True)