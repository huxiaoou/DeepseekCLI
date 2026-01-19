from enum import StrEnum


class Models(StrEnum):
    DEEPSEEK_REASONER = "deepseek-reasoner"
    DEEPSEEK_CHAT = "deepseek-chat"


MODEL_CONVERSION = {
    "chat": Models.DEEPSEEK_CHAT,
    "reasoner": Models.DEEPSEEK_REASONER,
}
