"""
╔══════════════════════════════════════════════════════════════╗
║       LangChain + RAG 综合 Demo                             ║
║  运行: python combined_demo.py                              ║
║  无需 API Key！用 LangChain 的方式构建一个 RAG 问答系统      ║
╚══════════════════════════════════════════════════════════════╝

这个 Demo 用 LangChain 的 LCEL 语法 + 组件，完整实现 RAG：
  - PromptTemplate（提示词模板）
  - Chain / LCEL（管道串联）
  - TextSplitter（文本切块）
  - VectorStore（向量存储）
  - Retrieval（检索）

一句话总结：
  LangChain 是"框架"，RAG 是"模式"，
  用 LangChain 可以优雅地实现 RAG。
"""

import sys

# ============================================================================
# 环境检查
# ============================================================================
try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough, RunnableLambda
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    import chromadb
    # chromadb 已导入
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    print(f"缺少依赖: {e}")
    print("请运行: pip install -r requirements_demo.txt")
    sys.exit(1)


# ============================================================================
# 模拟 LLM（无需 API Key）
# ============================================================================
class SimulatedLLM:
    """模拟 LLM，根据检索到的上下文回答问题。"""

    def __call__(self, prompt, **kwargs):
        """让 SimulatedLLM 可被 LCEL 管道符调用"""
        return self.invoke(prompt, **kwargs)

    def invoke(self, prompt):
        # 提取问题和上下文
        text = str(prompt)
        return f"[基于知识库回答] 根据公司内部文档，相关信息已在上方参考资料中标注。\n具体来说：文档中明确规定了相关流程和注意事项，请参考上述检索结果的详细内容。"


# ============================================================================
# 1. 准备知识库文档
# ============================================================================
print("\n" + "=" * 60)
print("  第一步：准备知识库")
print("=" * 60)

DOCUMENTS = [
    Document(
        page_content="LangChain 是一个用于构建 LLM 应用的框架。核心概念包括：Chain（链）、Agent（智能体）、Tool（工具）、Memory（记忆）。LangChain 支持 Python 和 JavaScript。最新版本是 0.3.x。",
        metadata={"topic": "langchain"}
    ),
    Document(
        page_content="RAG（Retrieval-Augmented Generation）是一种结合检索和生成的技术。工作流程：1) 将文档向量化存入向量库；2) 用户提问时检索相关文档；3) 将检索结果与问题一起传给 LLM 生成答案。RAG 可以有效减少幻觉。",
        metadata={"topic": "rag"}
    ),
    Document(
        page_content="LCEL（LangChain Expression Language）是 LangChain 的声明式编程接口。使用 | 管道符串联组件：prompt | llm | parser。LCEL 自动支持流式输出、异步调用、批处理等功能。",
        metadata={"topic": "lcel"}
    ),
    Document(
        page_content="VectorStore（向量数据库）用于存储和检索向量化的文档。常用选择：ChromaDB（轻量本地）、FAISS（高性能）、Pinecone（云端）、Weaviate（开源）。选择标准：数据量、查询速度、部署方式。",
        metadata={"topic": "vectorstore"}
    ),
    Document(
        page_content="Embedding（嵌入）是将文本转换为向量的过程。中文推荐模型：text2vec-large-chinese、bge-large-zh。多语言模型：all-MiniLM-L6-v2。embedding 质量直接影响 RAG 的检索效果。",
        metadata={"topic": "embedding"}
    ),
]

print(f"  准备了 {len(DOCUMENTS)} 篇文档，涵盖 LangChain、RAG、LCEL 等主题")


# ============================================================================
# 2. 文本切块
# ============================================================================
print("\n" + "=" * 60)
print("  第二步：文本切块")
print("=" * 60)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)
chunks = text_splitter.split_documents(DOCUMENTS)
print(f"  {len(DOCUMENTS)} 篇文档 → {len(chunks)} 个文本块")

for i, chunk in enumerate(chunks):
    topic = chunk.metadata.get("topic", "?")
    print(f"  Chunk {i} [{topic}]: {chunk.page_content[:60]}...")


# ============================================================================
# 3. 向量嵌入 & 存入 ChromaDB
# ============================================================================
print("\n" + "=" * 60)
print("  第三步：向量嵌入 + 存储")
print("=" * 60)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# 嵌入所有文本块
chunk_texts = [c.page_content for c in chunks]
embeddings = embedding_model.encode(chunk_texts)
print(f"  生成 {len(embeddings)} 个 {len(embeddings[0])} 维向量")

# 存入 ChromaDB
chroma_client = chromadb.EphemeralClient()  # 内存模式，Demo 用
try:
    chroma_client.delete_collection("langchain_rag_demo")
except Exception:
    pass

collection = chroma_client.create_collection("langchain_rag_demo")
collection.add(
    ids=[f"c{i}" for i in range(len(chunks))],
    embeddings=embeddings.tolist(),
    documents=chunk_texts,
    metadatas=[c.metadata for c in chunks],
)
print(f"  ChromaDB 中现有 {collection.count()} 条记录")


# ============================================================================
# 4. 用 LangChain LCEL 构建 RAG 链
# ============================================================================
print("\n" + "=" * 60)
print("  第四步：用 LCEL 构建 RAG 链")
print("=" * 60)

llm = SimulatedLLM()

# ── 定义 RAG Prompt 模板 ──
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个技术知识助手。请严格基于以下参考资料回答问题。
如果参考资料中没有相关信息，请如实告知。

========== 参考资料 ==========
{context}
=============================="""),
    ("human", "{question}"),
])

print("  RAG Prompt 模板:")
print(f"    {rag_prompt.messages[0].prompt.template[:100]}...")

# ── 定义检索函数 ──
def retrieve(query: str, k: int = 3):
    """从向量库检索最相关的文档"""
    query_vec = embedding_model.encode([query])
    results = collection.query(
        query_embeddings=query_vec.tolist(),
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    # 拼成上下文字符串
    contexts = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        topic = meta.get("topic", "?")
        contexts.append(f"[主题: {topic}, 相关度: {1-dist:.2f}]\n{doc}")

    return "\n\n---\n\n".join(contexts), results

# ── 用 LCEL 构建 RAG 链 ──
# LCEL 语法: 每一步用 | 连接
rag_chain = (
    # 第一步：从输入中提取问题，并行执行检索
    RunnablePassthrough.assign(
        context=lambda x: retrieve(x["question"])[0]
    )
    # 第二步：套用 Prompt 模板
    | rag_prompt
    # 第三步：调用 LLM
    | llm
    # 第四步：提取纯文本
    | StrOutputParser()
)

print("\n  RAG Chain 结构:")
print("  input → RunnablePassthrough(检索上下文) → Prompt 模板 → LLM → StrOutputParser → output")

# ── 测试 ──
print("\n" + "=" * 60)
print("  第五步：测试 RAG 问答")
print("=" * 60)

test_questions = [
    "什么是 RAG？它如何减少幻觉？",
    "LangChain 有哪些核心概念？",
    "LCEL 有什么优势？",
    "今天天气怎么样？",  # 知识库中不存在的
]

for q in test_questions:
    print(f"\n{'─' * 50}")
    print(f"  ❓ {q}")

    # 先看看检索到了什么
    context, raw_results = retrieve(q)
    print(f"  检索到 {len(raw_results['documents'][0])} 个相关文档:")
    for i, (doc, meta, dist) in enumerate(zip(
        raw_results["documents"][0],
        raw_results["metadatas"][0],
        raw_results["distances"][0],
    )):
        print(f"    #{i+1} [{meta.get('topic', '?')}] 距离={dist:.3f} | {doc[:80]}...")

    # 用 RAG Chain 生成回答
    result = rag_chain.invoke({"question": q})
    print(f"\n  🤖 回答: {result}")


# ============================================================================
# 6. 对比：有无 RAG 的区别
# ============================================================================
print("\n" + "=" * 60)
print("  第六步：RAG vs 无 RAG 对比")
print("=" * 60)

# 不用 RAG 的简单链
no_rag_prompt = ChatPromptTemplate.from_messages([
    ("human", "回答问题（如果不知道就说不知道）：{question}"),
])
no_rag_chain = no_rag_prompt | llm | StrOutputParser()

comparison_q = "LangChain 的最新版本是多少？"

# 不用 RAG
no_rag_answer = no_rag_chain.invoke({"question": comparison_q})
print(f"\n  ❓ {comparison_q}")
print(f"\n  ❌ 不用 RAG: {no_rag_answer}")
print(f"     → LLM 可能编造版本号（幻觉）")

# 用 RAG
rag_answer = rag_chain.invoke({"question": comparison_q})
print(f"\n  ✅ 用 RAG: {rag_answer}")
print(f"     → 基于真实文档回答，有据可查")


# ============================================================================
# 7. 总结
# ============================================================================
print("\n" + "=" * 60)
print("  🎉 综合 Demo 完成！")
print("=" * 60)
print("""
  这个 Demo 展示了 LangChain 和 RAG 如何配合：

  ┌──────────────────────────────────────────┐
  │            LangChain（框架）               │
  │  ┌────────┐  ┌──────┐  ┌──────────────┐ │
  │  │Prompt   │  │Chain │  │Output Parser │ │
  │  │Template │  │ LCEL │  │              │ │
  │  └────────┘  └──────┘  └──────────────┘ │
  │                                          │
  │  用这些组件实现 ↓↓↓                       │
  │                                          │
  │            RAG（模式）                     │
  │  ┌────────┐  ┌──────┐  ┌──────────────┐ │
  │  │Chunking│→ │Embed │→ │Vector Store  │ │
  │  └────────┘  └──────┘  └──────┬───────┘ │
  │                               │          │
  │  用户提问 → 检索 → 拼装Prompt → LLM → 回答│
  └──────────────────────────────────────────┘

  LangChain = 工具箱（扳手、螺丝刀...）
  RAG      = 装修方案（怎么用这些工具装修房子）

  更多资源:
    · LangChain 文档: https://python.langchain.com
    · ChromaDB 文档: https://docs.trychroma.com
    · Sentence-Transformers: https://sbert.net
  """)

# Script runs top-to-bottom — no main() wrapper needed
