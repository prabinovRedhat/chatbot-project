from utils.model_handler import query_mistral

def test_query_mistral():
    prompt = "Test prompt"
    response = query_mistral(prompt)
    assert "text" in response
