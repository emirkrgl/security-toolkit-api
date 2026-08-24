from groq import Groq
from app.core.config import GROQ_API_KEY
client = Groq(api_key=GROQ_API_KEY)

def run(tarama_sonucu):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",#yada başka bir model seçebilirsiniz
        max_tokens=1000,
        messages=[
            {"role": "system", "content": "Sana bir port tarama sonucu vereceğim, bunu bir güvenlik uzmanı gibi yorumla, "
            "riskleri ve önerileri kısa bir şekilde açıkla."},
            {"role": "user", "content":str(tarama_sonucu)}
        ]
        )
    ai_message = completion.choices[0].message.content
    return {"status": "success", "response": ai_message}
    
