import argparse
import logging
from pathlib import Path
from typing import Iterator

from Llama_cpp import (
    Llama,
    CreateChatCompletionResponse,
    CreateChatCompletionStreamResponse,
)

from data_engineering.config import (
    MODEL_DIR,
    PROMPT_DIR,
    TRANSCRIPT_DIR,
    SUMMARY_DIR,
    settings,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_model(model_path: Path) -> Llama:
    return Llama(
        model_path=str(model_path),
        n_ctx=settings.llm.CONTEXT_WINDOW,
        n_gpu_layers=settings.llm.N_GPU_LAYERS,
        chat_format=settings.llm.CHAT_FORMAT,
    )


def load_system_prompt() -> str:
    with open(PROMPT_DIR / "summarize_podcast_transcript.md.j2", "r") as file:
        return file.read()


def prepare_user_prompt(transcript_path: Path) -> str:
    with open(transcript_path, "r", encoding="utf-8") as file:
        return file.read()


def prepare_output(
    llm: Llama, user_prompt: str, system_prompt: str
) -> CreateChatCompletionResponse | Iterator[CreateChatCompletionStreamResponse]:
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=settings.llm.TEMPERATURE,
        max_tokens=settings.llm.MAX_TOKENS,
        stop=[],
        response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "minLength": 200,
                        "maxLength": 300,
                        "description": "A brief summary of the interview content.",
                    },
                    "quote": {
                        "type": "string",
                        "description": "A quote from the interview subject that captures a key theme of the podcast.",
                    },
                    "interview_date": {
                        "type": "string",
                        "format": "date",
                        "description": "The date when the interview was conducted.",
                    },
                },
                "required": [
                    "summary",
                    "interview_date",
                ],
            },
        },
    )
    return response["choices"][0]["message"]["content"]


def summarize_transcript(transcript_path: Path, llm: Llama) -> str:
    system_prompt = load_system_prompt()
    user_prompt = prepare_user_prompt(transcript_path)

    return prepare_output(llm=llm, user_prompt=user_prompt, system_prompt=system_prompt)


def write_summary_to_file(summary: str, transcript_file_name: Path) -> None:
    summary_file_name = f"{transcript_file_name.stem}_summary.json"
    summary_path = SUMMARY_DIR / summary_file_name

    with open(summary_path, "w") as file:
        file.write(summary)


def run_summary_pipeline(model: str, transcript_file_name: str) -> None:
    llm = load_model(model_path=MODEL_DIR / model)
    logger.info(f"Model {model} loaded successfully")

    transcript_path = TRANSCRIPT_DIR / transcript_file_name
    summary = summarize_transcript(transcript_path=transcript_path, llm=llm)

    write_summary_to_file(summary, Path(transcript_file_name))
    logger.info(f"Summary written to {SUMMARY_DIR / transcript_file_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Summarize a transcript using a pre-trained model."
    )
    parser.add_argument("transcript-file", "-t", type=str, required=True)
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=settings.llm.MODEL_FILE_NAME,
    )
    args = parser.parse_args()

    logger.info(f"Loading transcript from {args.transcript_file}...")

    run_summary_pipeline(model=args.model, transcript_file=args.transcript_file)
