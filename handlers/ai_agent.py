from mistralai import Mistral
from decouple import config

api_key = config("AI_KEY")

with Mistral(
    api_key=api_key,
) as mistral:

    res = mistral.agents.complete(messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], agent_id="ag:02a07fe6:20250224:untitled-agent:bae3e05a", stream=False)

    # Handle response
    print(res)