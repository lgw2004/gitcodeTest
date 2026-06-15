"""
╔══════════════════════════════════════════════════════════════╗
║           RAG（检索增强生成）Demo                             ║
║  运行: python rag_demo.py                                    ║
║  无需 API Key！使用本地嵌入模型 + 本地向量库                   ║
╚══════════════════════════════════════════════════════════════╝

RAG 是什么？
  Retrieval-Augmented Generation（检索增强生成）

  问题：LLM 的知识截止于训练日期，而且可能会"幻觉"（编造不存在的事实）
  方案：在提问时，先从外部知识库检索相关信息，再让 LLM 基于这些信息回答

  类比：开卷考试 vs 闭卷考试
    · 普通 LLM = 闭卷考试，全靠"记忆"
    ·  RAG    = 开卷考试，可以查阅参考资料再作答

  RAG 的 5 个步骤：
    1. 加载文档    （Document Loading）
    2. 文本切块    （Text Splitting / Chunking）
    3. 向量嵌入    （Embedding）
    4. 向量检索    （Retrieval）
    5. 增强生成    （Augmented Generation）

  这个 Demo 模拟一个"公司内部知识库"问答系统。
"""

import sys
import os

# ============================================================================
# 第 0 步：环境检查
# ============================================================================
print("\n" + "=" * 60)
print("  第 0 步：检查依赖")
print("=" * 60)

MISSING = []

try:
    import chromadb
    print("  ✓ chromadb 已安装（本地向量数据库）")
except ImportError:
    MISSING.append("chromadb")
    print("  ✗ chromadb 未安装")

try:
    from sentence_transformers import SentenceTransformer
    print("  ✓ sentence-transformers 已安装（本地嵌入模型）")
except ImportError:
    MISSING.append("sentence-transformers")
    print("  ✗ sentence-transformers 未安装")

try:
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("  ✓ langchain 文档处理模块已安装")
except ImportError:
    MISSING.append("langchain-text-splitters")
    print("  ✗ langchain 文档处理模块未安装")

if MISSING:
    print(f"\n  ⚠ 缺少依赖: {', '.join(MISSING)}")
    print("  请运行: pip install chromadb sentence-transformers langchain langchain-text-splitters")
    print("  或者: pip install -r requirements_demo.txt")
    sys.exit(1)


# ============================================================================
# 模拟知识库文档（一个科技公司的内部知识库）
# ============================================================================

KNOWLEDGE_BASE = [
    {
        "title": "公司考勤制度",
        "content": """
        公司考勤制度（2024版）

        第一条：工作时间
        公司实行弹性工作制，核心工作时间为上午10:00至下午4:00。
        员工每日工作时长不少于8小时，每周不少于40小时。

        第二条：打卡方式
        使用企业微信或门禁卡刷卡进行考勤打卡。
        每日需完成上下班两次打卡，缺卡需在48小时内提交补卡申请。

        第三条：请假流程
        年假需提前3个工作日向直属上级申请，通过OA系统提交。
        病假需在当天上午9:00前通知上级，并在3个工作日内补交医院证明。
        事假每年累计不超过15天。

        第四条：远程办公
        经主管批准，每月最多可远程办公5天。
        远程办公期间需保持企业微信在线，响应时间不超过30分钟。

        第五条：迟到处理
        每月累计迟到超过3次，第4次起每次扣减当日餐补。
        单次迟到超过1小时按旷工半天处理。
        """,
    },
    {
        "title": "Python 编码规范",
        "content": """
        Python 编码规范 v2.0

        一、命名约定
        - 类名使用 PascalCase：MyClass, UserProfile
        - 函数和变量使用 snake_case：get_user, user_name
        - 常量使用 UPPER_SNAKE_CASE：MAX_RETRY_COUNT = 3
        - 私有属性以单下划线开头：_internal_method

        二、代码格式
        - 使用 4 个空格缩进，禁止使用 Tab
        - 每行最多 120 个字符
        - 函数之间空两行，类之间空两行
        - import 语句放在文件顶部，按标准库、第三方库、本地模块分组

        三、类型注解
        - 所有公共函数必须有类型注解
        - 使用 mypy 进行类型检查
        - 示例：def get_user(user_id: int) -> User | None:

        四、异常处理
        - 永远不要使用裸 except:，至少指定 Exception
        - 自定义异常继承自项目基类，而非直接继承 Exception
        - 在日志中记录异常堆栈：logger.exception("详细描述")

        五、测试规范
        - 使用 pytest 框架
        - 测试覆盖率不低于 80%
        - 测试文件命名：test_模块名.py
        - CI/CD 流水线中必须通过所有测试才能合并
        """,
    },
    {
        "title": "项目管理流程",
        "content": """
        敏捷开发项目管理流程

        一、Sprint 周期
        - 每个 Sprint 为 2 周（10 个工作日）
        - Sprint 启动会议在周一上午 10:00
        - 每日站会 9:30，不超过 15 分钟
        - Sprint 评审会议在最后一周周五下午 3:00

        二、需求管理
        - 所有需求录入 JIRA 系统
        - 使用 Story Point 进行工作量估算（1, 2, 3, 5, 8, 13）
        - Product Backlog 由 PO（产品负责人）维护优先级
        - 每个 Sprint 的 Story Point 总量不超过 30 点

        三、代码评审
        - 每个 PR 至少需要 2 位 Reviewer 的 Approve
        - PR 超过 500 行代码需要 Tech Lead 额外审核
        - 评审重点：逻辑正确性、性能、安全性、可读性
        - 评审意见需在 24 小时内回复

        四、发布流程
        - 测试环境：每次合并到 develop 分支自动部署
        - 预发环境：需要 QA 确认后手动触发
        - 生产环境：需 Tech Lead 审批，仅限工作日 10:00-16:00 发布
        - 每次发布必须有 Release Notes 和回滚方案
        """,
    },
    {
        "title": "数据安全规范",
        "content": """
        数据安全规范

        一、数据分级
        - L1 公开数据：产品文档、公开 API 说明
        - L2 内部数据：员工通讯录、项目进度（需 VPN 访问）
        - L3 敏感数据：用户个人信息、财务数据（需额外权限审批）
        - L4 机密数据：密钥、证书、核心算法（需安全审计）

        二、密码策略
        - 密码长度不少于 12 位，包含大小写字母、数字、特殊字符
        - 每 90 天必须更换密码
        - 禁止使用最近 5 次使用过的密码
        - 生产环境必须使用 SSH Key + 密码双因素认证

        三、数据存储
        - 用户数据必须加密存储（AES-256 及以上）
        - 禁止将敏感数据存储在本地电脑
        - 数据库备份保留 30 天，异地备份
        - 日志中的敏感信息（手机号、身份证）必须脱敏

        四、应急响应
        - 发现安全事件立即上报安全部门（security@company.com）
        - 重大事件 30 分钟内启动应急响应小组
        - 事后 48 小时内提交事件分析报告
        - 每季度进行一次安全演练
        """,
    },
    {
        "title": "新人入职指南",
        "content": """
        新人入职指南 —— 欢迎加入！

        一、入职第一天
        - 上午 9:30 到 HR 部门办理入职手续，领取工牌和设备
        - 上午 10:30 参加公司介绍和部门 orientation
        - 下午 2:00 配置开发环境（参考 Wiki: /onboarding/dev-setup）
        - 下午 4:00 与 Mentor 一对一交流

        二、开发环境
        - 操作系统：推荐 Ubuntu 22.04 或 macOS 14+
        - IDE：推荐 VS Code 或 PyCharm Professional（公司提供 License）
        - 版本控制：Git + GitLab（内部部署）
        - 常用工具：Docker、Postman、Wireshark

        三、权限申请
        - GitLab 仓库权限：让 Mentor 在对应项目添加你
        - JIRA 权限：发送邮件给 PMO 团队
        - 数据库只读权限：通过 JumpServer 提交工单
        - 服务器 SSH 权限：走堡垒机审批流程（通常 1-2 个工作日）

        四、学习资源
        - 内部 Wiki：http://wiki.internal.company.com
        - 技术分享：每周五下午 3:00，会议室 301
        - 在线课程：公司购买了 Udemy Business 全站课程
        - 书籍借阅：HR 旁边书架，自助扫码借阅

        五、试用期考核
        - 试用期 3 个月
        - 第 1 个月：熟悉项目 + 完成 2 个小需求
        - 第 2 个月：独立完成 1 个中型功能
        - 第 3 个月：参与一次完整的 Sprint 开发周期
        - 考核通过后 Mentor 提交转正申请
        """,
    },
]


# ============================================================================
# 第 1 步：文档加载 & 切块
# ============================================================================
def step1_load_and_chunk():
    """
    步骤 1 & 2：加载文档 → 切块

    为什么需要切块？
      - 整篇文档太长，塞不进 LLM 的上下文窗口
      - 检索时，小块更精准 —— 你不会因为"考勤"问题而检索到整本员工手册
      - 每块需要有一定"重叠"，避免关键信息正好在边界上被切断
    """
    print("\n" + "=" * 60)
    print("  步骤 1 & 2：文档加载 → 文本切块")
    print("=" * 60)

    # 用 langchain 的 RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,        # 每块最多 500 字符
        chunk_overlap=100,     # 相邻块重叠 100 字符（防止关键信息在边界被切断）
        separators=["\n\n", "\n", "。", ".", " ", ""],  # 优先在段落/句子边界处切分
    )

    all_chunks = []
    for doc in KNOWLEDGE_BASE:
        doc_obj = Document(
            page_content=doc["content"],
            metadata={"title": doc["title"]}
        )
        chunks = text_splitter.split_documents([doc_obj])
        # 给每个 chunk 附加文档标题
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i
            chunk.metadata["source"] = doc["title"]
        all_chunks.extend(chunks)

        print(f"\n  📄 {doc['title']}")
        print(f"     原文长度: {len(doc['content'])} 字符")
        print(f"     切成 {len(chunks)} 块")
        for i, chunk in enumerate(chunks):
            preview = chunk.page_content[:80].replace("\n", " ")
            print(f"     Chunk {i}: {preview}...")

    print(f"\n  ✅ 共有 {len(all_chunks)} 个文本块，准备进入嵌入步骤")
    return all_chunks


# ============================================================================
# 第 2 步：向量嵌入 + 存储
# ============================================================================
def step2_embed_and_store(chunks):
    """
    步骤 3 & 4：向量嵌入 → 存入向量库

    嵌入（Embedding）是什么？
      - 把文本转成一串数字（向量），语义相近的文本，向量也相近
      - 例如 "猫" 和 "小猫" 的向量很接近，"猫" 和 "汽车" 的向量很远
      - 这样就能用数学方法（余弦相似度）来搜索相关文本

    这里使用 sentence-transformers 的本地模型，无需 API Key。
    """
    print("\n" + "=" * 60)
    print("  步骤 3：向量嵌入（Embedding）")
    print("=" * 60)

    # 加载本地嵌入模型（首次运行会下载模型文件 ~90MB）
    model_name = "all-MiniLM-L6-v2"  # 轻量、质量好、支持中文
    print(f"\n  加载嵌入模型: {model_name}")
    print("  (首次运行需要下载 ~90MB 模型文件，请稍候...)")

    embedding_model = SentenceTransformer(model_name)
    print(f"  ✓ 模型加载完成，向量维度: {embedding_model.get_sentence_embedding_dimension()}")

    # 将所有 chunk 转成向量
    chunk_texts = [chunk.page_content for chunk in chunks]
    print(f"\n  正在将 {len(chunk_texts)} 个文本块转成向量...")

    embeddings = embedding_model.encode(chunk_texts, show_progress_bar=True)
    print(f"  ✓ 嵌入完成，共 {len(embeddings)} 个 {len(embeddings[0])} 维向量")

    # ---------- 存入 ChromaDB ----------
    print("\n" + "=" * 60)
    print("  步骤 4：存入向量数据库（ChromaDB）")
    print("=" * 60)

    # 创建 ChromaDB 客户端（数据存到本地文件夹）
    # 新版 API: 使用 PersistentClient 替代旧的 Client(Settings(...))
    chroma_client = chromadb.PersistentClient(path="./chroma_db_demo")

    # 删掉旧数据（Demo 可重复运行）
    try:
        chroma_client.delete_collection("company_knowledge")
    except Exception:
        pass

    collection = chroma_client.create_collection(
        name="company_knowledge",
        metadata={"description": "公司内部知识库"}
    )

    # 准备数据：id、向量、文本、元数据
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [chunk.metadata for chunk in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=chunk_texts,
        metadatas=metadatas,
    )

    print(f"  ✓ 已存储 {collection.count()} 条记录到 ChromaDB")
    print(f"  数据持久化目录: ./chroma_db_demo/")

    return collection, embedding_model


# ============================================================================
# 第 3 步：检索
# ============================================================================
def step3_retrieve(collection, embedding_model):
    """
    步骤 5：检索（Retrieval）

    给定一个用户问题：
      1. 把问题也转成向量
      2. 在向量库中搜索最相似的几个文本块
      3. 返回最相关的结果
    """
    print("\n" + "=" * 60)
    print("  步骤 5：检索（Retrieval）")
    print("=" * 60)

    # 测试问题
    test_queries = [
        "新人入职第一天需要做什么？",
        "代码评审有哪些要求？",
        "公司的密码安全策略是什么？",
        "如果迟到了会怎么样？",
    ]

    for query in test_queries:
        print(f"\n  ❓ 用户问题: {query}")

        # ① 把问题转成向量
        query_embedding = embedding_model.encode([query])

        # ② 在向量库中搜索
        results = collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=3,  # 返回最相关的 3 个
            include=["documents", "metadatas", "distances"],
        )

        # ③ 展示检索结果
        for i, (doc, meta, dist) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )):
            # 距离越小 = 越相关
            relevance = "★" * max(1, 5 - int(dist * 5))
            source = meta.get("source", "未知")
            preview = doc[:100].replace("\n", " ")
            print(f"    #{i+1} [{relevance}] 距离={dist:.3f} | 来源: {source}")
            print(f"        {preview}...")

    return results


# ============================================================================
# 第 4 步：增强生成 —— 把检索结果喂给 LLM
# ============================================================================
def step4_augmented_generation(collection, embedding_model):
    """
    步骤 6：增强生成（Augmented Generation）

    RAG 的核心：把检索到的相关文档拼到 prompt 里，再发给 LLM。

    对比两种模式：
      A. 普通模式（不用 RAG）—— LLM 纯靠记忆答
      B.  RAG 模式 —— 把检索结果作为"参考资料"给 LLM
    """
    print("\n" + "=" * 60)
    print("  步骤 6：增强生成（Augmented Generation）")
    print("=" * 60)

    def ask_llm(question: str, use_rag: bool = True):
        """统一的问答接口，可以开关 RAG"""

        if use_rag:
            # RAG 模式：先检索，再生成
            query_embedding = embedding_model.encode([question])
            results = collection.query(
                query_embeddings=query_embedding.tolist(),
                n_results=3,
                include=["documents", "metadatas"],
            )

            # 拼装上下文
            context_parts = []
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                context_parts.append(f"[来源: {meta['source']}]\n{doc}")

            context = "\n\n---\n\n".join(context_parts)

            prompt = f"""你是一个公司内部助手。请严格基于以下参考资料回答问题。
如果参考资料中没有相关信息，请明确说"参考资料中未找到相关信息"。

========== 参考资料 ==========
{context}
==============================

问题：{question}

回答："""
        else:
            # 普通模式：不提供任何上下文
            prompt = f"""你是一个公司内部助手。

问题：{question}

回答："""

        return prompt, context_parts if use_rag else None

    # ---------- 演示 ----------
    questions = [
        "新人入职开发环境需要安装哪些工具？",
        "Sprint 周期是多长？发布有什么限制？",
        "请假需要走什么流程？",
        "公司一共有多少个级别的人员？",  # 故意问一个知识库没有的问题
    ]

    for q in questions:
        print(f"\n{'─' * 50}")
        print(f"  ❓ {q}")

        # A. 普通模式
        prompt_no_rag, _ = ask_llm(q, use_rag=False)
        print(f"\n  📝 普通 LLM 的 Prompt（无参考资料）:")
        print(f"     {prompt_no_rag[:200]}...")

        # B. RAG 模式
        prompt_rag, contexts = ask_llm(q, use_rag=True)
        print(f"\n  📚 RAG 的 Prompt（含参考资料）:")
        print(f"     检索到 {len(contexts)} 个相关文档片段，拼入 Prompt")
        for i, ctx in enumerate(contexts):
            preview = ctx[:120].replace("\n", " ")
            print(f"     Context {i+1}: {preview}...")

        # 对比说明
        print(f"\n  💡 对比:")
        print(f"     普通模式: LLM 可能编造不存在的信息（幻觉）")
        print(f"     RAG 模式: LLM 基于真实文档回答，可溯源")


# ============================================================================
# 第 5 步：交互式问答 & RAG 可视化
# ============================================================================
def step5_interactive(collection, embedding_model):
    """交互式问答和 RAG 架构可视化"""
    print("\n" + "=" * 60)
    print("  RAG 系统架构全景图")
    print("=" * 60)

    print("""
  ┌─────────────────────────────────────────────────────────────┐
  │                      RAG 系统架构                            │
  │                                                              │
  │  【离线阶段：构建知识库】                                      │
  │                                                              │
  │   文档                                                       │
  │   ┌──┐ ┌──┐ ┌──┐                                            │
  │   │PDF│ │MD │ │DB │  ← 各种格式的文档                         │
  │   └─┬┘ └─┬┘ └─┬┘                                            │
  │     │    │    │                                              │
  │     ▼    ▼    ▼                                              │
  │  ┌──────────────────┐                                       │
  │  │  Document Loader  │  ← 加载文档                            │
  │  └────────┬─────────┘                                       │
  │           ▼                                                  │
  │  ┌──────────────────┐                                       │
  │  │  Text Splitter    │  ← 切成小块 (chunk_size=500)           │
  │  └────────┬─────────┘                                       │
  │           ▼                                                  │
  │  ┌──────────────────┐                                       │
  │  │ Embedding Model   │  ← 文本 → 向量                         │
  │  └────────┬─────────┘                                       │
  │           ▼                                                  │
  │  ┌──────────────────┐                                       │
  │  │  Vector Store     │  ← ChromaDB / FAISS / Pinecone       │
  │  └──────────────────┘                                       │
  │                                                              │
  │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
  │                                                              │
  │  【在线阶段：问答】                                           │
  │                                                              │
  │   用户提问: "新人第一天要做什么？"                              │
  │      │                                                       │
  │      ▼                                                       │
  │  ┌──────────────────┐                                       │
  │  │ 1. Query Embedding│  ← 问题 → 向量                         │
  │  └────────┬─────────┘                                       │
  │           ▼                                                  │
  │  ┌──────────────────┐                                       │
  │  │ 2. 向量相似度搜索  │  ← 在向量库中找最相近的块               │
  │  └────────┬─────────┘                                       │
  │           ▼                                                  │
  │  ┌──────────────────┐                                       │
  │  │ 3. 取出 Top-K 文档 │  ← 最相关的 3~5 个文本块               │
  │  └────────┬─────────┘                                       │
  │           ▼                                                  │
  │  ┌──────────────────┐                                       │
  │  │ 4. 拼装 Prompt    │  ← 问题 + 参考资料                      │
  │  └────────┬─────────┘                                       │
  │           ▼                                                  │
  │  ┌──────────────────┐                                       │
  │  │ 5.  LLM 生成回答   │  ← 基于参考资料回答，减少幻觉           │
  │  └────────┬─────────┘                                       │
  │           ▼                                                  │
  │      返回带来源引用的答案                                     │
  └─────────────────────────────────────────────────────────────┘
  """)

    # ---------- 交互式问答 ----------
    print("\n" + "=" * 60)
    print("  交互式问答 —— 试试 RAG 的效果！")
    print("=" * 60)
    print("\n  你可以输入问题来体验 RAG 检索效果")
    print("  输入 'quit' 退出\n")

    sample_questions = [
        "考勤制度中关于迟到的规定是什么？",
        "Python 代码中函数怎么命名？",
        "安全事件应该怎么上报？",
        "试用期考核标准是什么？",
    ]

    print("  💡 试试这些问题:")
    for q in sample_questions:
        print(f"     · {q}")

    # 先演示几个预设问题
    print("\n  ── 预设问题演示 ──")

    for q in sample_questions[:2]:  # 只演示前两个
        print(f"\n  ❓ {q}")
        query_embedding = embedding_model.encode([q])
        results = collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=2,
            include=["documents", "metadatas", "distances"],
        )
        for i, (doc, meta, dist) in enumerate(zip(
            results["documents"][0], results["metadatas"][0], results["distances"][0]
        )):
            source = meta.get("source", "未知")
            print(f"  📖 检索结果 #{i+1} (距离={dist:.3f}, 来源={source}):")
            print(f"     {doc.strip()[:200]}...")

    print("\n  (Demo 模式: 上面展示了检索效果，完整交互需要真实 LLM)")
    print("  如果你有 OpenAI API Key:")
    print("    1. set OPENAI_API_KEY=sk-xxx")
    print("    2. pip install langchain-openai")
    print("    3. 就可以实现真正的 RAG 问答了！")


# ============================================================================
# 主程序
# ============================================================================
def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           📚 RAG（检索增强生成）Demo                         ║")
    print("║          开卷考试 vs 闭卷考试 —— 让 LLM 不再「幻觉」      ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    chunks = step1_load_and_chunk()
    collection, embedding_model = step2_embed_and_store(chunks)
    step3_retrieve(collection, embedding_model)
    step4_augmented_generation(collection, embedding_model)
    step5_interactive(collection, embedding_model)

    # 总结
    print("\n" + "=" * 60)
    print("  🎉 RAG Demo 完成！核心要点回顾：")
    print("=" * 60)
    print("""
  RAG = 检索增强生成，解决了 LLM 的两大痛点：
    1. 知识过时      → 从实时文档库检索最新信息
    2. 幻觉问题      → 基于真实文档回答，而非凭"记忆"编造

  5 个关键步骤：
    1. 文档加载     Document Loader
    2. 文本切块     Text Splitter (chunk_size + overlap)
    3. 向量嵌入     Embedding (文本 → 数字向量)
    4. 向量检索     Retrieval (相似度搜索)
    5. 增强生成     Augmented Generation (检索结果 + 问题 → LLM)

  典型应用场景：
    · 企业知识库问答     · 客服机器人
    · 文档智能助手       · 法律/医疗等专业知识查询
    · 代码库问答         · 学术论文检索

  进阶方向：
    · 混合检索（向量 + 关键词）
    · 重排序（Reranking）优化检索精度
    · 多模态 RAG（文本 + 图片 + 表格）
    · Agentic RAG（用 Agent 决策何时检索、检索什么）
  """)


if __name__ == "__main__":
    main()
