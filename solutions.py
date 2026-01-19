from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai._streaming import Stream
from husfort.qutility import SFG, SFY
from typedef import Models


def parse_response_stream(response: Stream[ChatCompletionChunk], model: Models):
    reasoning_content = ""
    content = ""
    if model == Models.DEEPSEEK_REASONER:
        print(SFG("Thingking:"), end="")
        for chunk in response:
            new_reasoning_content = chunk.choices[0].delta.reasoning_content or ""
            if new_reasoning_content:
                reasoning_content += new_reasoning_content
                print(new_reasoning_content, end="")
                continue
            new_content = chunk.choices[0].delta.content or ""
            content += new_content
        print("\n")
        print(SFG("Deepseek:"), content)
    else:
        print(SFG("Deepseek:"), end="")
        for chunk in response:
            new_content = chunk.choices[0].delta.content or ""
            print(new_content, end="")
            content += new_content
        print("\n")

    msg_answer = {
        "role": "assistant",
        "reasoning_content": reasoning_content,
        "content": content,
    }
    return msg_answer


def parse_response(response: ChatCompletion, model: Models) -> dict:
    msg_answer = response.choices[0].message.to_dict()
    if model == Models.DEEPSEEK_REASONER:
        print(SFG("Thingking:"), msg_answer["reasoning_content"])
    print(SFG("Deepseek:"), msg_answer["content"])
    return msg_answer


def main(
    api_key: str,
    base_url: str,
    model: Models,
    stream: bool,
    temperature: float,
):
    client = OpenAI(api_key=api_key, base_url=base_url)
    messages: list = []
    round: int = 0
    while True:
        print(f"\n\n{SFG(f'Round {round}'):-^64s}")
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
        if stream:
            msg_answer = parse_response_stream(response, model=model)
        else:
            msg_answer = parse_response(response, model=model)

        # save for next round
        if model == Models.DEEPSEEK_REASONER:
            msg_answer.pop("reasoning_content")
        messages.append(msg_answer)
        round += 1
