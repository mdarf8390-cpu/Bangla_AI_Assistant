import ollama


class QwenPlugin:

    def __init__(self, model="qwen2.5:latest"):

        self.model = model



    def generate(self, prompt: str):

        try:

            response = ollama.chat(

                model=self.model,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                options={
                    "temperature": 0.7,
                    "num_predict": 300
                }

            )


            return response["message"]["content"]


        except Exception as e:

            return f"Qwen Error: {e}"