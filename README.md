# README

## 项目说明

一个简单的Deepseek命令行工具。

## 查看帮助

```bash
python main.py -h
```

输出结果

```bash
usage: main.py [-h] [--model {chat,reasoner}] [--stream] [--temperature TEMPERATURE]

DeepSeek Chat Client

options:
  -h, --help            show this help message and exit
  --model {chat,reasoner}
                        Model to use, default is 'chat'
  --stream              Enable streaming responses
  --temperature TEMPERATURE
                        Sampling temperature (0.0 - 2.0)
                        Scenario               temperature
                        Coding/Math               0.0
                        Data Analysis             1.0
                        General Conversion        1.3
                        Translation               1.3
                        Creative Writing/Poetry   1.5
```

## 安装OpenAI SDK

```bash
pip install openai
```

## 设置API_KEY

请在Deepseek官网申请api_key，并将其添加到环境变量**DEEPSEEK_API_KEY**中，以方便程序访问。
