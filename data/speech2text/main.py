import os
import shutil
import pathlib
import asyncio
from concurrent.futures import ThreadPoolExecutor

import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence


def convert_mp3_to_wav(input_file: str, output_file: str):
    sound = AudioSegment.from_mp3(str(input_file))
    sound.export(str(output_file), format="wav")


def transcribe_chunk(chunk_path: str, recognizer: sr.Recognizer) -> str:
    with sr.AudioFile(chunk_path) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data, language="en-GB")
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return f"[ERROR: {e}]"


async def get_large_audio_transcript(
    path: str, dir_path: pathlib.Path, max_workers: int = 4
) -> str:
    folder_name = dir_path / "audio_chunks"
    os.makedirs(folder_name, mode=0o744, exist_ok=True)

    sound = AudioSegment.from_file(path)
    chunks = split_on_silence(
        sound, min_silence_len=500, silence_thresh=-45, keep_silence=100
    )

    loop, recognizer = asyncio.get_running_loop(), sr.Recognizer()
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        tasks = []

        for idx, chunk in enumerate(chunks, start=1):
            chunk_filename = os.path.join(folder_name, f"chunk{idx}.wav")
            chunk.export(chunk_filename, format="wav")
            tasks.append(
                loop.run_in_executor(pool, transcribe_chunk, chunk_filename, recognizer)
            )
        results = await asyncio.gather(*tasks)

    # join "non-false" transcripts
    return ". ".join(filter(None, (res.strip() for res in results)))


if __name__ == "__main__":
    dir_path = pathlib.Path(__file__).resolve().parent.parent
    mp3_path = dir_path / "audio" / "pythonbyte_podcast_ep440.mp3"
    wav_path = dir_path / "audio" / "ep440_audio.wav"

    convert_mp3_to_wav(mp3_path, wav_path)
    text = asyncio.run(get_large_audio_transcript(wav_path, dir_path))
    print(text)

    os.remove(wav_path)
    shutil.rmtree(dir_path / "speech2text" / "audio_chunks")
