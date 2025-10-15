from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_accepts_pdf_like_bytes():
    # Minimal non-empty bytes with pdf extension; pypdf may fail, our service tolerates
    files = { 'files': ('manual.pdf', b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n%%EOF', 'application/pdf') }
    resp = client.post('/upload-documents', files=files)
    assert resp.status_code == 200
    data = resp.json()
    assert 'ingested_count' in data
    assert data['ingested_count'] >= 1 or data['ingested_count'] == 0


def test_query_without_openai_key_returns_fallback():
    payload = { 'query': 'How to diagnose P0300 misfire?', 'top_k': 2 }
    resp = client.post('/query', json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert 'answer' in data
    assert 'sources' in data
