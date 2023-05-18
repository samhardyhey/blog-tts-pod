from pathlib import Path

from tts import tts_aws, tts_coqui, tts_gcp
from utils import nautilus_editors_note

coqui_model_names = [
    "tts_models/en/ek1/tacotron2",
    "tts_models/en/ljspeech/tacotron2-DDC",
    "tts_models/en/ljspeech/tacotron2-DDC_ph",
    "tts_models/en/ljspeech/glow-tts",
]

aws_model_names = ["Nicole", "Russell"]

gcp_model_names = [
    "en-AU-Neural2-A",
    "en-AU-Neural2-B",
    "en-AU-Neural2-C",
    "en-AU-Neural2-D",
    "en-AU-News-E",
    "en-AU-News-F",
    "en-AU-News-G",
    "en-AU-Standard-A",
    "en-AU-Standard-B",
    "en-AU-Standard-C",
    "en-AU-Standard-D",
    "en-AU-Wavenet-A",
    "en-AU-Wavenet-B",
    "en-AU-Wavenet-C",
    "en-AU-Wavenet-D",
]

output_dir = Path("./data/tts_output/dev/")

if __name__ == "__main__":
    # coqui
    for coqui_model_name in coqui_model_names:
        tts_coqui(
            coqui_model_name,
            nautilus_editors_note,
            "nautilus_editors_note",
            output_dir,
        )

    # AWS Polly
    for aws_model_name in aws_model_names:
        tts_aws(aws_model_name, nautilus_editors_note, "nautilus_editors_note", output_dir)

    # # GCP
    # for gcp_model_name in gcp_model_names:
    #     tts_gcp(
    #         gcp_model_name, nautilus_editors_note, "nautilus_editors_note", output_dir
    #     )
