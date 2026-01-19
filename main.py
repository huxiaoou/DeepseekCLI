import os
import argparse
import sys


script_dir = r"E:\Projects\DeepseekCLI"
sys.path.insert(0, script_dir)

from typedef import MODEL_CONVERSION


def parse_args():
    parser = argparse.ArgumentParser(
        description="DeepSeek Chat Client",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=MODEL_CONVERSION.keys(),
        default="reasoner",
        help="Model to use, default is 'reasoner'\n",
    )
    parser.add_argument(
        "--disable_stream",
        action="store_true",
        help="Disable streaming responses",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.3,
        help="Sampling temperature (0.0 - 2.0)\n"
        "Scenario	       temperature\n"
        "Coding/Math               0.0\n"
        "Data Analysis             1.0\n"
        "General Conversion        1.3\n"
        "Translation               1.3\n"
        "Creative Writing/Poetry   1.5",
    )
    return parser.parse_args()


if __name__ == "__main__":
    if api_key := os.environ.get("DEEPSEEK_API_KEY"):
        from solutions import main

        args = parse_args()
        base_url = "https://api.deepseek.com"
        main(
            base_url=base_url,
            model=MODEL_CONVERSION[args.model],
            api_key=api_key,
            stream=not args.disable_stream,
            temperature=args.temperature,
        )
    else:
        print("Please set the DEEPSEEK_API_KEY environment variable.")
