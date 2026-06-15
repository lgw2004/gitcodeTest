"""
╔══════════════════════════════════════════════════════════════╗
║           LangChain 核心概念 Demo                            ║
║  运行: python langchain_demo.py                              ║
║  无需 API Key，使用模拟 LLM 演示所有核心概念                   ║
╚══════════════════════════════════════════════════════════════╝

LangChain 是什么？
  - 一个用于构建 LLM（大语言模型）应用的框架
  - 把 "调用 LLM" 这件事，变成可组合的 "链"（Chain）
  - 提供了 Prompt 管理、工具调用、记忆、RAG 等开箱即用的模块

这个 Demo 演示 5 个核心概念：
  1. Prompt Template  —— 模板化管理提示词
  2. Chain             —— 把多个步骤串联成流水线
  3. LCEL              —— LangChain 表达式语言（现代写法）
  4. Tool / Agent      —— 让 LLM 能调用外部工具
  5. Memory            —— 让对话有"记忆"
"""

import sys

# ============================================================================
# 第 0 步：环境检查
# ============================================================================
print("\n" + "=" * 60)
print("  第 0 步：检查依赖")
print("=" * 60)

try:
    from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
    from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
    from langchain_core.runnables import RunnableLambda, RunnablePassthrough
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_core.tools import tool
    print("  ✓ langchain-core 已安装")
except ImportError:
    print("  ✗ 请先安装: pip install langchain-core langchain")
    sys.exit(1)

# 检查是否有真实 LLM 可用
HAS_OPENAI = False
try:
    from langchain_openai import ChatOpenAI
    HAS_OPENAI = True
    print("  ✓ langchain-openai 已安装（可使用真实 LLM）")
except ImportError:
    print("  ℹ langchain-openai 未安装（将使用模拟 LLM 演示）")

print("\n  提示: 如果想用真实 GPT，设置环境变量 OPENAI_API_KEY 并")
print("        安装: pip install langchain-openai")


# ============================================================================
# 模拟 LLM —— 没有 API Key 也能跑 Demo
# ============================================================================

class MockLLM:
    """
    模拟大语言模型：不调用任何 API，但行为模式和真实 LLM 完全一致。
    这让你可以在没有 API Key 的情况下理解 LangChain 的运作方式。
    """

    def __call__(self, prompt, **kwargs):
        
        return self.invoke(prompt, **kwargs)

    def invoke(self, prompt, **kwargs):
        """模拟 LLM 调用"""
        import random
        text = str(prompt)

        # 根据输入内容返回不同的模拟回复
        if "翻译" in text and "英文" in text:
            if "你好" in text:
                return AIMessage(content="Hello")
            elif "世界" in text:
                return AIMessage(content="World")
            elif "人工智能" in text:
                return AIMessage(content="Artificial Intelligence")
            return AIMessage(content="[模拟翻译结果] This is a translated text.")

        if "笑话" in text or "joke" in text:
            jokes = [
                "为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 == Dec 25！",
                "一个 SQL 查询走进酒吧，看到两张表，问：'我可以 JOIN 你们吗？'",
            ]
            return AIMessage(content=random.choice(jokes))

        if "总结" in text or "summarize" in text or "摘要" in text:
            return AIMessage(content="[模拟摘要] 这段内容主要讨论了人工智能在医疗领域的应用...")

        # 默认回复
        return AIMessage(content=f"[模拟 LLM 回复] 收到你的消息。核心要点：这是一个 LangChain Demo。")


# ============================================================================
# 第 1 步：Prompt Template —— 模板化管理提示词
# ============================================================================
def demo_1_prompt_template(llm):
    """
    概念：Prompt Template（提示词模板）

    问题：如果每次都手写完整的 prompt 字符串，会很乱。
    方案：用模板把"结构"和"数据"分离 —— 就像 HTML 模板一样。

    {变量名} 是占位符，运行时会被实际值替换。
    """
    print("\n" + "=" * 60)
    print("  第 1 步：Prompt Template（提示词模板）")
    print("=" * 60)

    # ---------- 简单模板 ----------
    print("\n▶ 1.1 简单模板（PromptTemplate）")

    template = PromptTemplate.from_template(
        "请把以下中文翻译成英文：{chinese_text}"
    )
    # 填入具体值 → 生成完整 prompt
    filled = template.format(chinese_text="你好，世界！")
    print(f"  模板: {template.template}")
    print(f"  填入后: {filled}")

    # ---------- 聊天模板 ----------
    print("\n▶ 1.2 聊天模板（ChatPromptTemplate）")

    chat_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的{role}，请用{style}的风格回答问题。"),
        ("human", "{question}"),
    ])
    filled_chat = chat_template.format_messages(
        role="Python 讲师",
        style="通俗易懂",
        question="什么是装饰器？"
    )
    for msg in filled_chat:
        print(f"  [{msg.type}] {msg.content}")

    # ---------- 多轮对话模板 ----------
    print("\n▶ 1.3 少样本示例（Few-Shot Prompting）")

    few_shot = ChatPromptTemplate.from_messages([
        ("system", "你是一个情感分析助手，输出只能是 positive / negative / neutral。"),
        ("human", "这部电影太棒了！"),      # 示例 1
        ("ai", "positive"),
        ("human", "服务态度很差"),           # 示例 2
        ("ai", "negative"),
        ("human", "{text}"),                 # 真正要分析的内容
    ])
    filled_fs = few_shot.format_messages(text="还行吧，没什么特别的感觉")
    for msg in filled_fs:
        print(f"  [{msg.type}] {msg.content}")

    print("\n  💡 核心思想：Prompt 和代码分离，方便复用、测试、版本管理")


# ============================================================================
# 第 2 步：Chain —— 串联多个步骤
# ============================================================================
def demo_2_chain(llm):
    """
    概念：Chain（链）

    一个 LLM 应用通常不止一步：
      输入 → 套模板 → 调 LLM → 解析输出 → 返回

    LangChain 用"链"把每一步串起来，像搭积木一样。
    """
    print("\n" + "=" * 60)
    print("  第 2 步：Chain（链）—— 串联多个步骤")
    print("=" * 60)

    # ---------- 基础链 ----------
    print("\n▶ 2.1 基础链：输入 → 模板 → LLM → 解析")

    from langchain_core.output_parsers import StrOutputParser

    # 定义每一步
    prompt = ChatPromptTemplate.from_template(
        "讲一个关于{topic}的简短笑话"
    )
    parser = StrOutputParser()

    # 用管道符 | 串联（这是 LCEL 语法，下一步会详解）
    chain = prompt | llm | parser

    result = chain.invoke({"topic": "程序员"})
    print(f"  输入: topic='程序员'")
    print(f"  输出: {result}")

    # ---------- 顺序链 ----------
    print("\n▶ 2.2 顺序链（Sequential Chain）：多个步骤依次执行")

    # 第一步：生成大纲
    outline_prompt = ChatPromptTemplate.from_template(
        "为关于'{subject}'的文章生成一个 3 点大纲。"
    )
    outline_chain = outline_prompt | llm | parser

    # 第二步：基于大纲写正文
    expand_prompt = ChatPromptTemplate.from_template(
        "根据以下大纲，写一段 50 字的简介：\n{outline}"
    )
    expand_chain = expand_prompt | llm | parser

    # 组合：先写大纲，再扩写
    outline = outline_chain.invoke({"subject": "Python 异步编程"})
    print(f"  第一步 - 生成大纲:\n    {outline}")

    article = expand_chain.invoke({"outline": outline})
    print(f"\n  第二步 - 扩写正文:\n    {article}")

    # ---------- 路由链 ----------
    print("\n▶ 2.3 路由链（Router Chain）：根据输入选择不同分支")

    # 简单路由：根据内容关键词选择
    def simple_router(text: str) -> str:
        if any(w in text for w in ["翻译", "translation", "英文"]):
            return "翻译任务"
        elif any(w in text for w in ["总结", "摘要", "summarize"]):
            return "总结任务"
        else:
            return "通用问答"

    test_texts = [
        "请把'机器学习'翻译成英文",
        "帮我总结一下这篇文章的内容",
        "今天天气怎么样",
    ]
    for t in test_texts:
        route = simple_router(t)
        print(f"  输入: '{t}' → 路由到: {route}")

    print("\n  💡 核心思想：Chain 像流水线，每一步只做一件事，组合起来就很强大")


# ============================================================================
# 第 3 步：LCEL —— LangChain 表达式语言
# ============================================================================
def demo_3_lcel(llm):
    """
    概念：LCEL (LangChain Expression Language)

    这是 LangChain 的"现代写法"——用 | 管道符串联组件。
    语法: component_a | component_b | component_c

    核心接口只有两个方法：
      - invoke()  同步调用，输入 → 输出
      - stream()  流式输出，一个字一个字地返回

    LCEL 的好处：
      1. 自动支持流式输出
      2. 自动支持异步 (ainvoke/astream)
      3. 自动支持批处理 (batch)
      4. 语法简洁，一目了然
    """
    print("\n" + "=" * 60)
    print("  第 3 步：LCEL 表达式语言")
    print("=" * 60)

    parser = StrOutputParser()

    # ---------- 基本语法 ----------
    print("\n▶ 3.1 基本语法：用 | 拼接组件")
    print("""  写法:
    chain = prompt | llm | output_parser
    # 等价于:
    # 1. 先把输入传给 prompt 生成消息
    # 2. 再把消息传给 llm 生成回复
    # 3. 再把回复传给 parser 转成纯文本
    """)

    # ---------- RunnableLambda ----------
    print("▶ 3.2 自定义处理步骤（RunnableLambda）")

    # RunnableLambda 可以把任意 Python 函数变成链中的一环
    def uppercase_output(text: str) -> str:
        return text.upper()

    def add_emoji(text: str) -> str:
        return f"🎉 {text} 🎉"

    chain = (
        ChatPromptTemplate.from_template("用一句话介绍{movie}")
        | llm
        | parser
        | RunnableLambda(uppercase_output)  # 转大写
        | RunnableLambda(add_emoji)          # 加 emoji
    )

    result = chain.invoke({"movie": "盗梦空间"})
    print(f"  输出: {result}")

    # ---------- RunnablePassthrough ----------
    print("\n▶ 3.3 RunnablePassthrough：保持数据流")

    # 有时候需要把中间结果和原始输入一起往下传
    chain = (
        RunnablePassthrough.assign(
            # 原始输入原封不动传下去，同时新增一个 processed 字段
            summary=lambda x: (llm | parser).invoke(
                ChatPromptTemplate.from_template(
                    "用一句话总结：{topic}"
                ).format_messages(topic=x["topic"])
            )
        )
    )
    result = chain.invoke({"topic": "量子计算"})
    print(f"  输入: {{'topic': '量子计算'}}")
    print(f"  输出: {result}")

    # ---------- 并行链 ----------
    print("\n▶ 3.4 数据流可视化")

    print("""
  典型 LCEL 链的数据流：

    {topic: "AI"}
        │
        ▼
  ┌─────────────┐
  │  Prompt 模板  │  组装成完整提示词
  └──────┬──────┘
         │  ChatPromptValue
         ▼
  ┌─────────────┐
  │    LLM      │  调用大模型
  └──────┬──────┘
         │  AIMessage
         ▼
  ┌─────────────┐
  │ StrOutputParser│  提取纯文本
  └──────┬──────┘
         │  str
         ▼
  ┌─────────────┐
  │  自定义函数   │  后处理（可选）
  └──────┬──────┘
         │  str
         ▼
      返回结果
  """)

    print("  💡 核心思想：| 就是数据流动的方向，从左到右依次处理")


# ============================================================================
# 第 4 步：Tool / Agent —— 让 LLM 调用工具
# ============================================================================
def demo_4_tools():
    """
    概念：Tool & Agent（工具 & 智能体）

    LLM 本身只能"说话"，不能执行操作。
    Tool 让 LLM 能调用外部函数（查天气、搜网页、发邮件...）
    Agent 则是用 LLM 做决策引擎，自动选择调用哪个工具。

    工作流程：
      用户提问 → Agent 分析 → 决定调用哪个工具 → 执行 → 整合结果 → 回复
    """
    print("\n" + "=" * 60)
    print("  第 4 步：Tool（工具）& Agent（智能体）")
    print("=" * 60)

    # ---------- 定义工具 ----------
    print("\n▶ 4.1 定义工具：把 Python 函数变成 LLM 可调用的工具")

    # 用 @tool 装饰器，LangChain 会自动提取函数签名和 docstring
    # 生成工具描述给 LLM
    @tool
    def get_weather(city: str) -> str:
        """查询指定城市的天气情况"""
        # 模拟天气数据（真实场景会调 API）
        weather_data = {
            "北京": "晴，25°C，湿度 40%",
            "上海": "多云，28°C，湿度 65%",
            "深圳": "阵雨，30°C，湿度 80%",
            "成都": "阴，22°C，湿度 55%",
        }
        return weather_data.get(city, f"{city}：晴，23°C")

    @tool
    def calculator(expression: str) -> str:
        """执行数学计算，支持 + - * / 和括号"""
        try:
            result = eval(expression)
            return f"计算结果: {expression} = {result}"
        except Exception:
            return "计算失败，请检查表达式"

    @tool
    def search_knowledge(query: str) -> str:
        """搜索知识库，查询技术问题"""
        knowledge = {
            "python": "Python 是一种解释型、面向对象的高级编程语言，由 Guido van Rossum 于 1991 年发布。",
            "langchain": "LangChain 是一个用于构建 LLM 应用的框架，核心概念是 Chain、Agent、Tool。",
            "rag": "RAG（检索增强生成）是一种结合信息检索和文本生成的技术，让 LLM 能基于外部知识回答。",
            "装饰器": "装饰器是 Python 的一种语法糖，用于在不修改原函数的情况下增强其功能。",
        }
        for key, val in knowledge.items():
            if key in query.lower():
                return val
        return f"未找到关于 '{query}' 的相关信息"

    # 打印工具信息
    tools = [get_weather, calculator, search_knowledge]
    for t in tools:
        print(f"\n  工具: {t.name}")
        print(f"  描述: {t.description}")
        print(f"  参数: {t.args}")

    # ---------- 模拟 Agent 决策 ----------
    print("\n▶ 4.2 模拟 Agent 决策流程")

    queries = [
        "今天北京天气怎么样？",
        "计算 (15 + 7) * 3 - 8",
        "什么是 RAG？",
    ]

    for q in queries:
        print(f"\n  用户: {q}")
        # Agent 推理（简化演示，真实场景由 LLM 自主决策）
        if "天气" in q:
            city = "北京" if "北京" in q else "上海"
            result = get_weather.invoke({"city": city})
            print(f"  Agent 决策: 调用 get_weather 工具")
            print(f"  工具返回: {result}")
        elif any(op in q for op in ["+", "-", "*", "/", "计算"]):
            # 提取表达式
            expr = q.replace("计算", "").strip()
            result = calculator.invoke({"expression": expr})
            print(f"  Agent 决策: 调用 calculator 工具")
            print(f"  工具返回: {result}")
        elif any(kw in q for kw in ["什么是", "解释", "Python", "RAG", "LangChain"]):
            keyword = q.replace("什么是", "").replace("？", "").replace("?", "").strip()
            result = search_knowledge.invoke({"query": keyword})
            print(f"  Agent 决策: 调用 search_knowledge 工具")
            print(f"  工具返回: {result}")

    print("  核心思想: Agent = LLM + Tools，LLM 是「大脑」，Tools 是「手脚」")

# ============================================================================
# 第 5 步：Memory —— 对话记忆
# ============================================================================
def demo_5_memory(llm):
    """
    概念：Memory（记忆）

    默认情况下，每次 LLM 调用都是"失忆"的——不记得上一轮说了什么。
    Memory 模块自动管理对话历史，让 LLM 能进行连贯的多轮对话。
    """
    print("\n" + "=" * 60)
    print("  第 5 步：Memory（对话记忆）")
    print("=" * 60)

    print("\n▶ 5.1 没有 Memory 的问题")

    # 模拟没有记忆的对话
    print("  无记忆模式：")
    messages = [
        "我叫张三，是一名程序员。",
        "我刚才说我叫什么名字？",  # LLM 不记得！
    ]
    for msg in messages:
        response = MockLLM().invoke(msg)
        print(f"  用户: {msg}")
        print(f"  LLM: {response.content}")

    print("\n▶ 5.2 有 Memory 的对话")

    # 手动维护对话历史（LangChain 有 ConversationBufferMemory 等封装）
    conversation_history = []

    def chat_with_memory(user_input: str) -> str:
        # 把历史消息和当前消息一起发给 LLM
        full_context = "\n".join(conversation_history + [f"用户: {user_input}"])
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个友好的助手。之前的对话记录：\n{history}"),
            ("human", "{input}"),
        ])
        response = llm.invoke(
            prompt.format_messages(history=str(conversation_history), input=user_input)
        )
        # 更新历史
        conversation_history.append(f"用户: {user_input}")
        conversation_history.append(f"助手: {response.content}")
        return response.content

    print("  有记忆模式：")
    r1 = chat_with_memory("我叫张三，是一名程序员。")
    print(f"  用户: 我叫张三，是一名程序员。")
    print(f"  LLM: {r1}")

    r2 = chat_with_memory("我刚才说我叫什么名字？做什么工作？")
    print(f"\n  用户: 我刚才说我叫什么名字？做什么工作？")
    print(f"  LLM: {r2}")
    print(f"\n  累积的对话历史: {len(conversation_history)} 条消息")

    # ---------- Memory 类型介绍 ----------
    print("\n▶ 5.3 LangChain 提供的 Memory 类型")

    memory_types = [
        ("ConversationBufferMemory", "保存完整对话历史", "简单直接，但长对话会占用大量 token"),
        ("ConversationBufferWindowMemory", "只保留最近 K 轮对话", "节省 token，适合长对话"),
        ("ConversationSummaryMemory", "用 LLM 总结历史，而非存原文", "最省 token，但需要额外 LLM 调用"),
        ("ConversationTokenBufferMemory", "按 token 数量限制历史长度", "精确控制 token 消耗"),
    ]
    for name, desc, note in memory_types:
        print(f"  · {name}")
        print(f"    {desc}")
        print(f"    特点: {note}")

    print("\n  💡 核心思想: Memory 让 LLM 从'金鱼记忆'变成'能聊天的助手'")


# ============================================================================
# 主程序
# ============================================================================
def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           🦜 LangChain 核心概念 Demo                        ║")
    print("║           5 个步骤，带你感受 LangChain 的运作方式             ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # 创建 LLM 实例
    if HAS_OPENAI:
        print("\n  🌟 检测到 OpenAI，使用真实 GPT-3.5")
        try:
            import os
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=os.environ.get("OPENAI_API_KEY", None),
            )
        except Exception:
            print("  ⚠ OpenAI 初始化失败，回退到模拟 LLM")
            llm = MockLLM()
    else:
        print("\n  📝 使用模拟 LLM（无需 API Key）")
        print("  💡 设置 OPENAI_API_KEY 环境变量即可使用真实 GPT")
        llm = MockLLM()

    # 依次运行每个 Demo
    demos = [
        ("Prompt Template",     lambda: demo_1_prompt_template(llm)),
        ("Chain",               lambda: demo_2_chain(llm)),
        ("LCEL",                lambda: demo_3_lcel(llm)),
        ("Tool & Agent",        demo_4_tools),          # 不需要 llm
        ("Memory",              lambda: demo_5_memory(llm)),
    ]

    for name, func in demos:
        try:
            func()
        except Exception as e:
            print(f"\n  ⚠ Demo '{name}' 出错: {e}")
            import traceback
            traceback.print_exc()

    # 总结
    print("\n" + "=" * 60)
    print("  🎉 Demo 完成！回顾 LangChain 的 5 个核心概念：")
    print("=" * 60)
    print("""
  1. Prompt Template  —— 模板化管理提示词，分离结构与数据
  2. Chain             —— 把多步骤串联成流水线
  3. LCEL              —— 用 | 管道符优雅地写链
  4. Tool & Agent      —— 让 LLM 能调用外部工具执行操作
  5. Memory            —— 让对话有记忆，支持多轮交互

  这些概念组合起来，就能构建复杂的 LLM 应用！
  下一步：试试 rag_demo.py 了解 RAG（检索增强生成）
  """)

    print("  📖 推荐阅读:")
    print("    · LangChain 官方文档: https://python.langchain.com")
    print("    · 命令行: pip install langchain langchain-community")


if __name__ == "__main__":
    main()
