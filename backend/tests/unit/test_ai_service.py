import pytest
from unittest.mock import patch, MagicMock
from app.services import ai_service


class TestComputeEtoiles:
    def test_5_etoiles(self):
        result = ai_service.compute_etoiles(5.0)
        assert result == {"pleines": 5, "demies": 0, "vides": 0}

    def test_0_etoiles(self):
        result = ai_service.compute_etoiles(0)
        assert result == {"pleines": 0, "demies": 0, "vides": 5}

    def test_4_etoiles(self):
        result = ai_service.compute_etoiles(4.0)
        assert result == {"pleines": 4, "demies": 0, "vides": 1}

    def test_3_5_etoiles(self):
        result = ai_service.compute_etoiles(3.5)
        assert result == {"pleines": 3, "demies": 1, "vides": 1}

    def test_2_75_etoiles(self):
        result = ai_service.compute_etoiles(2.75)
        assert result == {"pleines": 3, "demies": 0, "vides": 2}

    def test_4_25_etoiles(self):
        result = ai_service.compute_etoiles(4.25)
        assert result == {"pleines": 4, "demies": 1, "vides": 0}

    def test_none_etoiles(self):
        result = ai_service.compute_etoiles(None)
        assert result == {"pleines": 0, "demies": 0, "vides": 5}

    def test_negative_etoiles(self):
        result = ai_service.compute_etoiles(-1)
        assert result == {"pleines": 0, "demies": 0, "vides": 5}


class TestParseLLMResponse:
    def test_parse_valid_json(self):
        note, justification = ai_service._parse_llm_response('{"note": 4.25, "justification": "Bon service."}')
        assert note == 4.25
        assert justification == "Bon service."

    def test_parse_with_markdown_block(self):
        response = '```json\n{"note": 3.00, "justification": "Mitige."}\n```'
        note, justification = ai_service._parse_llm_response(response)
        assert note == 3.00
        assert justification == "Mitige."

    def test_parse_clamps_too_high(self):
        note, _ = ai_service._parse_llm_response('{"note": 7.00, "justification": "test"}')
        assert note == 5.0

    def test_parse_clamps_too_low(self):
        note, _ = ai_service._parse_llm_response('{"note": 0.00, "justification": "test"}')
        assert note == 1.0

    def test_parse_invalid_json(self):
        with pytest.raises(Exception):
            ai_service._parse_llm_response("not json at all")


class TestBuildUserPrompt:
    def test_builds_prompt(self):
        commentaires = [
            {"contenu": "Super travail"},
            {"contenu": "Pas mal"},
        ]
        prompt = ai_service._build_user_prompt(commentaires)
        assert "Super travail" in prompt
        assert "Pas mal" in prompt
        assert "- \"" in prompt

    def test_empty_commentaires(self):
        prompt = ai_service._build_user_prompt([])
        assert prompt == ""


class TestAnalyzeCommentaires:
    def test_returns_none_for_empty(self):
        note, justification = ai_service.analyze_commentaires([])
        assert note is None
        assert "Aucun commentaire" in justification

    @patch("app.services.ai_service._call_gemini")
    def test_calls_gemini(self, mock_gemini, app):
        mock_gemini.return_value = '{"note": 4.00, "justification": "Bon."}'
        with app.app_context():
            app.config["GEMINI_API_KEY"] = "test-key"
            note, justification = ai_service.analyze_commentaires([{"contenu": "Bon"}])
            assert note == 4.0
            assert mock_gemini.called

    @patch("app.services.ai_service._call_gemini", side_effect=Exception("API error"))
    def test_returns_none_on_failure(self, mock_gemini, app):
        with app.app_context():
            app.config["GEMINI_API_KEY"] = "test-key"
            note, justification = ai_service.analyze_commentaires([{"contenu": "Test"}])
            assert note is None
            assert justification is None
