#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
from pathlib import Path

import torch
from funasr import AutoModel


# SenseVoice 控制标签，例如：
# <|zh|><|NEUTRAL|><|Speech|><|woitn|>
SPECIAL_TOKEN_RE = re.compile(r"<\|.*?\|>")


def clean_text(text: str) -> str:
    """
    Remove SenseVoice control tokens from recognition output.

    Example:
        <|zh|><|NEUTRAL|><|Speech|><|woitn|>打开空调

    becomes:
        打开空调
    """
    text = str(text)
    text = SPECIAL_TOKEN_RE.sub("", text)
    return text.strip()


def extract_text(result) -> str:
    """
    Extract recognition text from common FunASR return formats.
    """

    if isinstance(result, tuple):
        result = result[0]

    if isinstance(result, list):
        if not result:
            return ""
        result = result[0]

    if isinstance(result, dict):
        return str(result.get("text", ""))

    if isinstance(result, str):
        return result

    raise RuntimeError(
        f"Unsupported FunASR result type: {type(result)}"
    )


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Inference with SenseVoiceSmall-SmartHome-Finetuned"
        )
    )

    parser.add_argument(
        "audio",
        help="Path to input audio file",
    )

    parser.add_argument(
        "--model",
        default="./SenseVoiceSmall",
        help=(
            "Path to local fine-tuned SenseVoiceSmall model directory "
            "(default: ./SenseVoiceSmall)"
        ),
    )

    parser.add_argument(
        "--device",
        default="cuda:0" if torch.cuda.is_available() else "cpu",
        help=(
            "Inference device, e.g. cuda:0 or cpu "
            "(default: automatically selected)"
        ),
    )

    args = parser.parse_args()

    audio_path = Path(args.audio)
    model_path = Path(args.model)

    # --------------------------------------------------------
    # Check input
    # --------------------------------------------------------

    if not audio_path.is_file():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    if not model_path.is_dir():
        raise FileNotFoundError(
            f"Model directory not found: {model_path}"
        )

    if not (model_path / "model.pt").is_file():
        raise FileNotFoundError(
            f"model.pt not found in model directory: {model_path}"
        )

    # --------------------------------------------------------
    # Basic information
    # --------------------------------------------------------

    print(f"Model : {model_path.resolve()}")
    print(f"Audio : {audio_path.resolve()}")
    print(f"Device: {args.device}")
    print()

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    model = AutoModel(
        model=str(model_path),
        device=args.device,
        trust_remote_code=True,
        disable_update=True,
    )

    # --------------------------------------------------------
    # Inference
    # --------------------------------------------------------

    result = model.generate(
        input=str(audio_path),
        cache={},
        language="zh",
        use_itn=False,
        batch_size=1,
    )

    # --------------------------------------------------------
    # Extract and clean text
    # --------------------------------------------------------

    raw_text = extract_text(result)
    text = clean_text(raw_text)

    if not text:
        raise RuntimeError(
            "Recognition finished, but no text was returned."
        )

    print()
    print("Recognition result:")
    print(text)


if __name__ == "__main__":
    main()