import os
import random
import time
from pathlib import Path

import boto3
import pandas as pd
import torch
from config import (aws_model_names, coqui_single_speaker_models,
                    coqui_vkts_speaker_indices, data_dir, dev_output_dir,
                    gcp_model_names)
from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2.service_account import Credentials
from TTS.api import TTS
from utils import logger, nautilus_editors_note, to_snake_case

load_dotenv()


def tts_coqui_single_speaker(model_name, text, save_path):
    gpu_available = bool(torch.cuda.is_available())
    tts = TTS(model_name=model_name, gpu=gpu_available)
    if save_path.parent.exists() is False:
        save_path.parent.mkdir(parents=True)
    start = time.time()
    tts.tts_to_file(text=text, file_path=save_path)
    end = time.time()
    logger.info(
        f"Successuflly Synthesized Speech for {str(save_path)} using Coqui {model_name} in {end - start} seconds"
    )


def tts_coqui_vctk_multi_speaker(speaker_index, text, save_path):
    gpu_available = bool(torch.cuda.is_available())
    tts = TTS(model_name="tts_models/en/vctk/vits", gpu=gpu_available)
    if save_path.parent.exists() is False:
        save_path.parent.mkdir(parents=True)
    start = time.time()
    tts.tts_to_file(text=text, file_path=save_path, speaker=speaker_index)
    end = time.time()
    logger.info(
        f"Successuflly Synthesized Speech for {str(save_path)} using Cocqui VCTK {speaker_index} in {end - start} seconds"
    )


def tts_aws(model_name, text, save_path):
    # config
    polly_client = boto3.Session().client("polly")

    # configure/create output dir
    if save_path.parent.exists() is False:
        save_path.parent.mkdir(parents=True)

    # synthesize the speech
    start = time.time()
    response = polly_client.synthesize_speech(VoiceId=model_name, OutputFormat="mp3", Text=text)
    with open(str(save_path), "wb") as file:
        file.write(response["AudioStream"].read())
    end = time.time()
    logger.info(f"Successuflly Synthesized Speech for {str(save_path)} using AWS {model_name} in {end - start} seconds")


def tts_gcp(model_name, text, save_path):
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
    if save_path.parent.exists() is False:
        save_path.parent.mkdir(parents=True)

    # finally synthesize the speech..
    start = time.time()
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(str(save_path), "wb") as file:
        file.write(response.audio_content)
    end = time.time()
    logger.info(f"Successuflly Synthesized Speech for {str(save_path)} using GCP {model_name} in {end - start} seconds")


def sample_tts_providers():
    for coqui_model in coqui_single_speaker_models:
        save_path = dev_output_dir / "coqui" / f"{to_snake_case(Path(coqui_model).name)}_nautilus_editors_note.mp3"
        tts_coqui_single_speaker(coqui_model, nautilus_editors_note, save_path)

    for speaker_index in coqui_vkts_speaker_indices:
        save_path = dev_output_dir / "coqui" / f"vtks_{speaker_index}_nautilus_editors_note.mp3"
        tts_coqui_vctk_multi_speaker(speaker_index, nautilus_editors_note, save_path)

    # AWS Polly
    for aws_model_name in aws_model_names:
        save_path = dev_output_dir / "aws" / f"{to_snake_case(aws_model_name)}_nautilus_editors_note.mp3"
        tts_aws(aws_model_name, nautilus_editors_note, save_path)

    # GCP
    for gcp_model_name in gcp_model_names:
        save_path = dev_output_dir / "gcp" / f"{to_snake_case(gcp_model_name)}_nautilus_editors_note.mp3"
        tts_gcp(gcp_model_name, nautilus_editors_note, save_path)


def tts_all_articles():
    # re-assign issue/article numbers, whoops
    df = (
        pd.read_csv(data_dir / "naut_all.csv")
        .assign(issue_number=lambda x: x.issue_title.factorize()[0] + 1)
        .assign(article_number=lambda x: x.groupby("issue_number").cumcount() + 1)
        .query('issue_number < 47')
    )
    output_dir = Path(__file__).parents[0] / "data/tts_output"
    log_records = []

    for idx, row in df.iterrows():
        issue_dir = output_dir / f"{row.issue_number}_{to_snake_case(row.issue_title)}"
        if issue_dir.exists() is False:
            issue_dir.mkdir(parents=True)

        article_fp = issue_dir / f"{row.article_number}_{to_snake_case(row.headline)}.mp3"
        if article_fp.exists():
            logger.info(f"{article_fp} already exists; skipping..")
            continue

        speaker_index = random.choice(coqui_vkts_speaker_indices)
        try:
            start = time.time()
            tts_coqui_vctk_multi_speaker(speaker_index, row.article, article_fp)
            end = time.time()
            log_records.append(
                {
                    "issue_number": row.issue_number,
                    "article_number": row.article_number,
                    "n_tokens": len(row.article.split(" ")),
                    "time_elapsed": end - start,
                }
            )
        except Exception:
            logger.error(f"Unable to synthesize text for: {row.headline}")

    pd.DataFrame(log_records).to_csv(data_dir / "tts_logs.csv", index=False)


if __name__ == "__main__":
    tts_all_articles()
