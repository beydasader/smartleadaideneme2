import requests
from flask import current_app


class AIServiceError(Exception):
    pass


class AIService:

    def _system_prompt(self):
        return current_app.config["BUSINESS_CONTEXT"]

    def yanit_uret(self, mesaj, gecmis=None):

        api_key = current_app.config["GROQ_API_KEY"]

        if not api_key:
            return (
                "Demo modu: Groq API anahtarı "
                "henüz ayarlanmamış."
            )

        if gecmis is None:
            gecmis = []

        messages = [
            {
                "role": "system",
                "content": self._system_prompt()
            }
        ]

        messages.extend(gecmis)

        messages.append(
            {
                "role": "user",
                "content": mesaj
            }
        )

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-oss-20b",
                    "messages": messages
                },
                timeout=30
            )

            if response.status_code != 200:
                raise AIServiceError(
                    "Yapay zeka servisine ulaşılamadı."
                )

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except requests.RequestException as error:
            raise AIServiceError(
                "Yapay zeka bağlantısında hata oluştu."
            ) from error


ai_service = AIService()