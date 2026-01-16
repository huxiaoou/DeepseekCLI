import os
import argparse
from enum import StrEnum
from openai import OpenAI
from husfort.qutility import SFG, SFY


class Models(StrEnum):
    DEEPSEEK_REASONER = "deepseek-reasoner"
    DEEPSEEK_CHAT = "deepseek-chat"


MODEL_CONVERSION = {
    "chat": Models.DEEPSEEK_CHAT,
    "reasoner": Models.DEEPSEEK_REASONER,
}


def parse_args():
    parser = argparse.ArgumentParser(description="DeepSeek Chat Client", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--model", type=str, choices=("chat", "reasoner"), default="chat", help="Model to use")
    parser.add_argument("--stream", action="store_true", help="Enable streaming responses")
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


def main(
    api_key: str,
    base_url: str,
    model: Models,
    stream: bool,
    temperature: float,
):
    client = OpenAI(api_key=api_key, base_url=base_url)
    messages = []
    while True:
        print("-----------------------------")
        user_input = input(SFY("User[Input 'q' to quit]: "))
        if user_input.lower() in ["q"]:
            break

        msg_question = {"role": "user", "content": user_input}
        messages.append(msg_question)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream,
            temperature=temperature,
        )
        msg_answer = response.choices[0].message.to_dict()
        print(SFG("Deepseek:"), msg_answer["content"])
        if model == Models.DEEPSEEK_REASONER:
            msg_answer.pop("reasoning_content")
        messages.append(msg_answer)


if __name__ == "__main__":
    if api_key := os.environ.get("DEEPSEEK_API_KEY"):
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
