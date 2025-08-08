from unittest.mock import Mock

from cheap_electricity.esios import get_prices_for_today


def test_get_prices_for_today_uses_requests(monkeypatch):
    fake_response = Mock()
    fake_response.json.return_value = {"ok": True}
    fake_response.raise_for_status.return_value = None
    mock_get = Mock(return_value=fake_response)

    monkeypatch.setattr("cheap_electricity.esios.requests.get", mock_get)
    monkeypatch.setattr("cheap_electricity.config.ESIOS_API_TOKEN", "TOKEN")
    monkeypatch.setattr("os.path.exists", lambda x: False)

    data = get_prices_for_today()

    assert data == {"ok": True}
    assert mock_get.call_count == 1
