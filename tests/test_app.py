"""Tests for the YouTube Transcript REST API."""

from unittest.mock import patch, MagicMock

import pytest

import app
from app import app as flask_app
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test the health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_transcript_success(client):
    """Test successful transcript retrieval."""
    mock_transcript = [
        {"text": "Hello world", "start": 0.0, "duration": 1.5},
        {"text": "This is a test", "start": 1.5, "duration": 2.0},
    ]
    mock_fetched = MagicMock()
    mock_fetched.to_raw_data.return_value = mock_transcript
    with patch.object(
        app.api, "fetch", return_value=mock_fetched
    ):
        response = client.get("/transcript/test_video_id")
        assert response.status_code == 200
        data = response.get_json()
        assert data["video_id"] == "test_video_id"
        assert data["transcript"] == mock_transcript


def test_transcript_not_found(client):
    """Test transcript not found error."""
    with patch.object(
        app.api, "fetch",
        side_effect=NoTranscriptFound("test_video_id", [], None),
    ):
        response = client.get("/transcript/test_video_id")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data


def test_transcript_disabled(client):
    """Test transcripts disabled error."""
    with patch.object(
        app.api, "fetch",
        side_effect=TranscriptsDisabled("test_video_id"),
    ):
        response = client.get("/transcript/test_video_id")
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data


def test_video_unavailable(client):
    """Test video unavailable error."""
    with patch.object(
        app.api, "fetch",
        side_effect=VideoUnavailable("test_video_id"),
    ):
        response = client.get("/transcript/test_video_id")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data


def test_generic_error(client):
    """Test generic error handling."""
    with patch.object(
        app.api, "fetch",
        side_effect=Exception("Some error"),
    ):
        response = client.get("/transcript/test_video_id")
        assert response.status_code == 500
        data = response.get_json()
        assert data["error"] == "Some error"
