# Nautilus TTS Pod 🎧

Convert Nautilus magazine articles into multi-speaker audio using Coqui TTS. Companion code for ["Behold the Humble Nautilus"](https://www.samhardyhey.com/behold-the-humble-nautilus).

## Features
- 📚 EPUB parsing and conversion
- 🗣️ Multi-speaker TTS synthesis
- 🎵 Audio streaming API
- ☁️ S3 integration

## Setup
```bash
# Install dependencies
./scripts/create_env.sh
```

## Usage
```bash
# Convert EPUB files
python transform/ebook.py

# Generate audio
python transform/tts.py

# Start streaming service
docker-compose up --build -d
```

## Structure
- 📖 `transform/ebook.py` # EPUB processing
- 🎤 `transform/tts.py` # Audio generation
- 🌐 `api/` # Streaming service
- 🐳 `docker-compose.yml` # Container config

*Note: Requires Nautilus subscription, S3 access, and GPU for TTS processing.*