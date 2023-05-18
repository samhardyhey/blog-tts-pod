import os
import time
from pathlib import Path

import boto3
from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2.service_account import Credentials
from TTS.api import TTS

from utils import logger, to_snake_case

load_dotenv()

output_dir = Path("./data/tts_output/dev/")


def tts_coqui(model_name, text, save_path):
    tts = TTS(model_name=model_name, gpu=True)
    if save_path.parent.exists() is False:
        save_path.parent.mkdir(parents=True)
    # coqui_output_dir = output_dir / "coqui"
    # if coqui_output_dir.exists() is False:
    #     coqui_output_dir.mkdir(parents=True)
    # save_file = coqui_output_dir / f"{to_snake_case(Path(model_name).name)}_{text_name}.mp3"
    start = time.time()
    tts.tts_to_file(text=text, file_path=save_path)
    end = time.time()
    logger.info(f"Successuflly Coqui TTS {save_path.name} in {end - start} seconds")


def tts_aws(model_name, text, text_name, output_dir):
    # config
    polly_client = boto3.Session().client("polly")

    # configure/create output dir
    aws_polly_output_dir = output_dir / "aws"
    if aws_polly_output_dir.exists() is False:
        aws_polly_output_dir.mkdir(parents=True)
    save_file = aws_polly_output_dir / f"{to_snake_case(Path(model_name).name)}_{text_name}.mp3"

    # synthesize the speech
    start = time.time()
    response = polly_client.synthesize_speech(VoiceId=model_name, OutputFormat="mp3", Text=text)
    with open(str(save_file), "wb") as file:
        file.write(response["AudioStream"].read())
    end = time.time()
    logger.info(f"Successuflly AWS TTS {text_name} in {end - start} seconds")


def tts_gcp(model_name, text, text_name, output_dir):
    # load credentials/client/config (far out)
    GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    credentials = Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
    client = texttospeech.TextToSpeechClient(credentials=credentials)
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-AU",
        name=model_name,
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # configure/create output dir
    gcp_output_dir = output_dir / "gcp"
    if gcp_output_dir.exists() is False:
        gcp_output_dir.mkdir(parents=True)
    save_file = gcp_output_dir / f"{to_snake_case(model_name)}_{text_name}.mp3"

    # finally synthesize the speech..
    start = time.time()
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(str(save_file), "wb") as file:
        file.write(response.audio_content)
    end = time.time()
    logger.info(f"Successuflly GCP TTS {text_name} in {end - start} seconds")


# if __name__ == "__main__":
# tts_coqui(
#     "tts_models/en/ek1/tacotron2",
#     nautilus_edito rs_note,
#     "nautilus_editors_note",
#     output_dir,
# )
# tts_aws_polly("Nicole", nautilus_editors_note, "nautilus_editors_note", output_dir)
