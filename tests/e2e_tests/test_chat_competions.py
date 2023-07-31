from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_completions():
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "",
            "max_tokens": 100,
            "messages": [
                {"role": "system", "content": "You are a chatbot"},
                {
                    "role": "user",
                    "content": "hello",
                },
            ],
            "stream": False,
            "temperature": 0.1,
        },
    )
    assert response.status_code == 200
    assert "hello" in response.json()["content"].lower()
