import requests
from typing import List, Union, Generator, Iterator
import json

class Pipeline:
    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        self.name = "Ollama Pipeline"

    async def on_startup(self):
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")
        pass

    def pipe(
        self, 
        user_message: str, 
        model_id: str, 
        messages: List[dict], 
        body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")

        OLLAMA_BASE_URL = "http://localhost:11434"
        MODEL = "llama3"

        if "user" in body:
            print("######################################")
            print(f'# User: {body["user"]["name"]} ({body["user"]["id"]})')
            print(f"# Message: {user_message}")
            print("######################################")

        try:
            # 1. Send the message to the first LLaMA model for completion
            r = requests.post(
                url=f"{OLLAMA_BASE_URL}/v1/chat/completions",
                json={**body, "model": MODEL},
                stream=True,
            )
            r.raise_for_status()

            if body["stream"]:
                return r.iter_lines()
            else:
                response = r.json()
                print("First Response:")
                print(response)

                # 2. Send the message and response to the second LLaMA model for improvement
                improved_response = requests.post(
                    url=f"{OLLAMA_BASE_URL}/v1/chat/completions",
                    json={
                        **body, 
                        "model": MODEL,
                        "prompt": f"Improve {response['output']}"
                    },
                    stream=True,
                )
                improved_response.raise_for_status()

                if body["stream"]:
                    return improved_response.iter_lines()
                else:
                    improved_response_data = improved_response.json()
                    print("Improved Response:")
                    print(improved_response_data)

        except Exception as e:
            return f"Error: {e}"