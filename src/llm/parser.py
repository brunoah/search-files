import json
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

SYSTEM = """
Tu transformes la demande utilisateur en JSON strict :

{
  "ext": "pdf" ou null,
  "contains": "facture" ou null,
  "limit": 20
}

Réponds uniquement en JSON.
"""

def parse_query(user_text: str):
    response = client.chat.completions.create(
        model="typhoon2-qwen2.5-7b-instruct",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_text}
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()
    content = content.strip("`")

    return json.loads(content)