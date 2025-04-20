from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
from typing import Optional
from dotenv import load_dotenv
import io
from openai.helpers import LocalAudioPlayer


# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="OpenAI TTS Server")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai = AsyncOpenAI()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Available voices in OpenAI
AVAILABLE_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "alloy"
    model: str = "tts-1"
    speed: float = 1.0


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "OpenAI TTS Server is running"}


@app.get("/voices")
async def list_voices() -> dict[str, list[str]]:
    """List all available voices"""
    return {"voices": AVAILABLE_VOICES}


@app.post("/tts")
async def text_to_speech(request: TTSRequest) -> None:
    """Convert text to speech using OpenAI's API"""
    try:
        # Validate voice
        if request.voice not in AVAILABLE_VOICES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid voice. Available voices: {AVAILABLE_VOICES}",
            )

        # Validate speed
        if not (0.25 <= request.speed <= 4.0):
            raise HTTPException(status_code=400, detail="Speed must be between 0.25 and 4.0")

        async with openai.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="coral",
            input="Today is a wonderful day to build something people love!",
            instructions="Speak in a cheerful and positive tone.",
            response_format="pcm",
        ) as response:
            await LocalAudioPlayer().play(response)
            # Create an in-memory bytes buffer
            # audio_buffer = io.BytesIO()

            # # Write the response content to the buffer
            # for chunk in response.iter_bytes():
            #     audio_buffer.write(chunk)

        # Seek to the beginning of the buffer
        # audio_buffer.seek(0)

        # # Return the audio as a streaming response
        # return StreamingResponse(
        #     audio_buffer,
        #     media_type="audio/mpeg",
        #     headers={"Content-Disposition": "attachment; filename=speech.mp3"},
        # )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
