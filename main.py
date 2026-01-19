import os
import argparse
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
        default="chat",
        help="Model to use, default is 'chat'",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Enable streaming responses",
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
            stream=args.stream,
            temperature=args.temperature,
        )
    else:
        print("Please set the DEEPSEEK_API_KEY environment variable.")
