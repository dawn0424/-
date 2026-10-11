"""
文件名：master.py
功能：调用通义千问 API，模拟一个“赛博算命大师”回答用户的问题。

使用前准备：
1. 安装 dashscope 库：
   python3 -m pip install dashscope
2. 准备阿里云百炼 / DashScope API Key。
3. 在运行环境的环境变量或 Secrets 中配置 DASHSCOPE_API_KEY。
"""

# 导入 DashScope 提供的 Generation 类。
# Generation.call() 方法可以调用通义千问等生成式模型。
import os
import sys

import dashscope
from dashscope import Generation


# 从环境变量 DASHSCOPE_API_KEY 中读取 API Key。
# 不要把真实 API Key 直接写进代码，否则上传到 GitHub 后会泄露。
API_KEY = os.getenv("DASHSCOPE_API_KEY", "")


# 这是系统提示词。
# 系统提示词用于规定 AI 的身份、说话风格和回答方式。
# 注意：这里故意使用用户要求的“半文半白、结合科技和玄学”的风格。
SYSTEM_PROMPT = "你是一个赛博算命大师，说话半文半白，结合科技和玄学"


# 这里设置要使用的模型名称。
# qwen-plus 是通义千问系列中常用的模型。
# 如果你的账号或地区不支持这个模型，可以根据控制台可用模型进行替换。
MODEL_NAME = "qwen-plus"


def ask_master(user_question):
    """
    调用通义千问 API，并返回大师的回答。

    参数：
        user_question：用户输入的问题，类型是字符串。

    返回：
        AI 返回的回答文本，类型是字符串。

    异常：
        如果 API 调用失败，就抛出 RuntimeError，
        并附带比较容易理解的错误说明。
    """

    # 检查环境变量中是否已经配置 API Key。
    # 如果没有配置，程序会给出明确提示。
    if not API_KEY:
        raise RuntimeError(
            "没有找到 DASHSCOPE_API_KEY。\n"
            "请在运行环境的 Secrets 或环境变量中配置它。"
        )

    # 将 API Key 交给 dashscope 库。
    # 后面的 Generation.call() 会自动使用这个 Key 访问通义千问 API。
    dashscope.api_key = API_KEY

    # messages 是发送给大模型的对话内容。
    # system 消息用于规定 AI 的身份和回答风格。
    # user 消息就是用户实际提出的问题。
    messages = [
        {
            "role": "system",
            "content": """
            1.喜欢把现代科技和修仙术语还有魔法术语结合
            2.用抽象的语言，给出最离谱但好笑有有点合理的预测
            3.表现的高高在上
            4.适度怼人
            """,
        },
        {
            "role": "user",
            "content": user_question,
        },
    ]

    # 调用通义千问模型。
    # model 表示模型名称。
    # messages 表示发送给模型的对话消息。
    # result_format="message" 表示希望 API 返回消息格式，
    # 这样可以从 response.output.choices[0].message.content 中获取回答。
    response = Generation.call(
        model=MODEL_NAME,
        messages=messages,
        result_format="message",
    )

    # HTTP 状态码 200 一般表示请求成功。
    # 如果不是 200，就说明 API 调用出现了问题。
    if response.status_code != 200:
        raise RuntimeError(
            f"调用通义千问失败。\n"
            f"错误码：{response.code}\n"
            f"错误信息：{response.message}"
        )

    # 从返回结果中提取模型生成的文字。
    # choices[0] 表示取第一条回答。
    # message.content 就是回答正文。
    answer = response.output.choices[0].message.content

    # 将回答返回给调用这个函数的代码。
    return answer


def main():
    # 程序主函数。
    # 这个函数负责显示提示文字、读取用户问题、调用 AI、打印回答。
    # 下面使用普通的井号注释，避免多行字符串受到中文标点影响。

    # 打印程序标题，帮助用户确认程序已经启动.
    print("========== 赛博算命大师 ==========")
    print("输入你的问题，按回车提交。")
    print("输入 q、quit 或 exit 可以退出程序。")
    print()

    # 使用 while True 让程序可以连续回答多个问题。
    # 只有用户输入退出命令时，循环才会结束。
    while True:
        # input() 会暂停程序，等待用户从键盘输入文字。
        # strip() 用于删除问题前后的空格。
        user_question = input("请问：").strip()

        # 用户直接按回车时，不发送空问题，避免浪费 API 请求。
        if not user_question:
            print("问题不可为空，请重新输入。\n")
            continue

        # 判断用户是否想退出程序。
        if user_question.lower() in {"q", "quit", "exit"}:
            print("大师收起天机终端，后会有期。")
            break

        try:
            # 调用函数请求 AI 回答。
            answer = ask_master(user_question)

            # 打印回答结果。
            print("\n大师曰：")
            print(answer)
            print()

        except Exception as error:
            # 捕获程序运行过程中出现的错误。
            # 例如：API Key 未设置、网络错误、模型名称错误等。
            # str(error) 可以把错误对象转换成可读的文字。
            print("\n程序运行出错：")
            print(error)
            print("请根据上面的提示检查配置，然后重试。\n")


# 只有直接运行 python3 master.py 时，才会进入下面这个 if。
# 如果这个文件被其他 Python 文件 import，则不会自动启动程序。
if __name__ == "__main__":
    # sys.argv 是 Python 用来接收“命令行参数”的列表。
    #
    # 举例：
    #   python3 master.py
    # 此时 sys.argv 大概是：
    #   ["master.py"]
    #
    # 再举例：
    #   python3 master.py "我今天适合学习 C 语言吗？"
    # 此时 sys.argv 大概是：
    #   ["master.py", "我今天适合学习 C 语言吗？"]
    #
    # 所以：
    #   len(sys.argv) == 1 表示没有额外参数；
    #   len(sys.argv) > 1 表示用户在命令后面传入了问题。
    if len(sys.argv) > 1:
        # 把从第 2 个元素开始的所有内容合并成一个问题字符串。
        #
        # 为什么从 sys.argv[1] 开始？
        # 因为 sys.argv[0] 是脚本文件名 master.py，
        # 真正的问题参数从 sys.argv[1] 才开始。
        #
        # 为什么使用 " ".join(...)？
        # 如果用户没有加引号，输入类似：
        #   python3 master.py 我 今天 运势 如何
        # Python 会把它拆成多个参数。
        # 使用 join 可以把它们重新拼成一句话。
        question = " ".join(sys.argv[1:]).strip()

        try:
            # 调用原有的 ask_master() 函数。
            # 这样既保留了原来的 API 调用逻辑，
            # 又能让 master.py 像命令行工具一样工作。
            answer = ask_master(question)

            # 命令行工具模式下，只打印 AI 的回答。
            # 这样 C 程序用 popen() 读取结果时，会更干净。
            print(answer)

        except Exception as error:
            # 如果出错，把错误打印到标准错误 stderr。
            # 标准错误通常用于显示程序运行错误，
            # 和普通输出区分开来。
            print(f"程序运行出错：{error}", file=sys.stderr)

            # sys.exit(1) 表示程序异常退出。
            # 0 通常表示成功，非 0 通常表示失败。
            sys.exit(1)
    else:
        # 如果用户没有传入命令行参数，
        # 就继续使用原来的交互模式。
        main()
