import openai
from decouple import config

openai.api_key = config("OPENAI_API_KEY")

def generate_ai_recommendations(interests):
    """
    Generate AI-powered article recommendations based on user interests.
    """
    prompt = f"Suggest 5 useful article titles about {', '.join(interests)}."

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that recommends self-help articles."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    ai_text = response.choices[0].message.content.strip()

    # Split into list of article titles
    recommendations = [line.strip("-• ") for line in ai_text.split("\n") if line.strip()]
    return recommendations
