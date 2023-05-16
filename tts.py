import pandas as pd
from TTS.api import TTS

if __name__ == "__main__":
    df = pd.read_csv("./data/naut_0.csv")

    # for model_name in TTS.list_models():
    #     # Init TTS
    #     tts = TTS(model_name)
    #     # Run TTS
    #     # ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language
    # Text to speech with a numpy output
    # wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])
    # Text to speech to a file
    # tts.tts_to_file(
    #     text="Hello world!",
    #     speaker=tts.speakers[0],
    #     language=tts.languages[0],
    #     file_path=f"./data/{model_name}.wav",
    # )

    model_name = "tts_models/en/ljspeech/tacotron2-DDC"
    tts = TTS(model_name)

    # for idx, row in df.iterrows():
    # tts.tts_to_file(text="Hello world this is me!", file_path="./data/test.wav")
    # TODO: long-form inputs > split? split sizes can't be bigger than kernel still
    tts.tts_to_file(text=df.iloc[0].parsed_content, file_path="./data/parsed_content.wav")
