# YouTube Transcript API Server

A REST API server that wraps the [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) Python library, providing a simple HTTP interface to fetch YouTube video transcripts.

## Features

- Simple REST API to fetch YouTube video transcripts
- Docker support with multi-architecture builds (amd64 and arm64)
- Health check endpoint
- Proper error handling

## API Endpoints

### Health Check

```
GET /health
```

Returns the health status of the server.

**Response:**
```json
{
  "status": "healthy"
}
```

### Get Transcript

```
GET /transcript/<video_id>
```

Fetches the transcript for a YouTube video.

**Parameters:**
- `video_id`: The YouTube video ID (e.g., `dQw4w9WgXcQ`)

**Response:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "transcript": [
    {
      "text": "Hello world",
      "start": 0.0,
      "duration": 1.5
    }
  ]
}
```

**Error Responses:**
- `404`: Transcript not found or video unavailable
- `403`: Transcripts are disabled for this video
- `500`: Internal server error

## Running Locally

### With Python

```bash
pip install -r requirements.txt
python app.py
```

The server will start on `http://localhost:8080`.

### With Docker

```bash
docker build -t youtube-transcript .
docker run -p 8080:8080 youtube-transcript
```

## Development

### Install Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run Tests

```bash
pytest tests/ -v
```

## CI/CD

The project includes GitHub Actions workflows that:

1. Run tests on every push and pull request
2. Build multi-architecture Docker images (amd64 and arm64)

## License

Apache License 2.0