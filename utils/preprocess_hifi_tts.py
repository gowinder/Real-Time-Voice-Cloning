import argparse
import json
from itertools import chain
from pathlib import Path

from argutils import print_args


def preprocess_hifi_tts(datasets_root: Path, datasets_name: 
        str, subfolders: str, out_dir: Path):
    dataset_root = datasets_root.joinpath(datasets_name)
    input_dirs = [dataset_root.joinpath(subfolder.strip()) for subfolder in subfolders.split(",")]
    print("\n    ".join(map(str, ["Using data from:"] + input_dirs)))
    assert all(input_dir.exists() for input_dir in input_dirs)
    
    manifest_files = list(chain.from_iterable(input_dir.glob("*.json") for input_dir in input_dirs))
    for manifest_file in manifest_files:
        print(manifest_file)
        with manifest_file.open("r") as f:
            lines = f.readlines()
            for line in lines:
                manifest = json.loads(line)
                filepath = Path(dataset_root.joinpath(
                    manifest["audio_filepath"])).with_suffix(".txt")
                text = manifest["text"].upper()
                with filepath.open("w") as wf:
                    wf.write(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="preprocess hifi tts dataset: https://openslr.magicdatatech.com/resources/109/hi_fi_tts_v0.tar.gz",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("datasets_root", type=Path, help=\
        "Path to the directory containing your hifi_tts_v0/audio datasets.")
    parser.add_argument("--datasets_name", type=str, default="hifi_tts_v0", help=\
        "Name of the dataset directory to process.")
    parser.add_argument("--subfolders", type=str, default="audio", help=\
        "Comma-separated list of subfolders to process inside your dataset directory")
    args = parser.parse_args()

    # Process the arguments
    if not hasattr(args, "out_dir"):
        args.out_dir = args.datasets_root.joinpath("SV2TTS", "synthesizer")

    # Create directories
    assert args.datasets_root.exists()
    args.out_dir.mkdir(exist_ok=True, parents=True)

    # Preprocess the dataset
    print_args(args, parser)
    preprocess_hifi_tts(**vars(args))
