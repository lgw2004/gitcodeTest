# VS Code 中使用 Git 上传代码到 GitHub 完整教程

本文档手把手教你**如何在 VS Code 中用图形界面操作 Git**，把代码上传到 GitHub。不需要背命令，全鼠标操作。

---

## 目录

1. [前置准备](#1-前置准备)
2. [初始化 Git 仓库](#2-初始化-git-仓库)
3. [暂存文件（Stage）](#3-暂存文件stage)
4. [提交代码（Commit）](#4-提交代码commit)
5. [推送到 GitHub（Push）](#5-推送到-githubpush)
6. [日常更新流程](#6-日常更新流程)
7. [常见问题](#7-常见问题)

---

## 1. 前置准备

### 1.1 安装 Git

- 下载地址：https://git-scm.com/downloads
- 安装时一路点「Next」即可
- 验证：打开终端（CMD/PowerShell），输入 `git --version`，显示版本号即成功

### 1.2 注册 GitHub 账号

- 访问 https://github.com 注册
- 记住你的**用户名**和**邮箱**

### 1.3 VS Code 安装

- 下载地址：https://code.visualstudio.com/
- VS Code **自带 Git 支持**，不需要额外装插件

### 1.4 配置 Git 全局信息（只需一次）

打开 VS Code 终端（`Ctrl + ``）：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
```

示例：
```bash
git config --global user.name "lgw2004"
git config --global user.email "lgw2004@example.com"
```

---

## 2. 初始化 Git 仓库

> **目标**：把一个普通文件夹变成 Git 仓库

### VS Code 操作步骤

1. **打开项目文件夹**
   - VS Code → 文件 → 打开文件夹 → 选择你的项目目录
   - 例如 `C:\Users\12206\Desktop\Pyside6desktop`

2. **打开源代码管理面板**
   - 点击左侧活动栏的 ![分支图标](https://code.visualstudio.com/assets/docs/sourcecontrol/overview/scm-provider-icon.png) **源代码管理**图标（或按 `Ctrl + Shift + G`）

3. **初始化仓库**
   - 如果项目还没有 `.git` 文件夹，VS Code 会显示一个「初始化仓库」按钮
   - 点击它 → 项目文件夹下会生成 `.git` 文件夹（隐藏的），代表 Git 仓库创建成功

   ![初始化仓库](https://code.visualstudio.com/assets/docs/sourcecontrol/overview/scm-viewlet.png)

   > 💡 如果项目已经是一个 Git 仓库（比如本项目的 master），就不会显示这个按钮

### 补充：创建 `.gitignore` 文件

`.gitignore` 用来告诉 Git **哪些文件不需要跟踪**（比如缓存、临时文件）。

在项目根目录新建 `.gitignore` 文件，内容示例：

```gitignore
# Python 缓存
__pycache__/
*.py[cod]
*.pyo

# 环境变量
.env
venv/
.venv/

# 生成的临时数据
chroma_db_demo/

# IDE 设置
.vscode/
.idea/

# 系统文件
.DS_Store
Thumbs.db
```

> ✅ VS Code 中创建新文件就可以了

---

## 3. 暂存文件（Stage）

> **目标**：告诉 Git "我要把这些文件加入版本管理"

### VS Code 操作步骤

1. **打开源代码管理面板**（`Ctrl + Shift + G`）

2. **查看更改**
   - 「更改」列表里显示所有**被修改/新增**的文件
   - 鼠标悬停在文件名上会显示 `+` 和 `-` 符号

3. **暂存文件**

   | 操作 | VS Code 操作方法 | 对应命令 |
   |------|-----------------|---------|
   | 暂存单个文件 | 点击文件右侧的 `+` 号 | `git add 文件名` |
   | 暂存所有文件 | 点击「更改」右侧的 `+` 号 | `git add -A` |
   | 取消暂存 | 点击「暂存的更改」下的 `-` 号 | `git reset HEAD 文件名` |

   ![暂存操作示意图](https://code.visualstudio.com/assets/docs/sourcecontrol/overview/scm-viewlet.png)

4. **确认状态**
   - 「暂存的更改」区域列出了即将被提交的文件
   - 点击文件可以查看修改的具体内容（diff 视图）

---

## 4. 提交代码（Commit）

> **目标**：给当前的版本拍一张"快照"，写上一句话说明改了啥

### VS Code 操作步骤

1. **输入提交信息**
   - 在源代码管理面板顶部的输入框中**写提交说明**
   - 格式建议：`动词: 改了什么`
     - 初始化：`init: 项目初始化`
     - 新增功能：`feat: 添加用户登录功能`
     - 修 Bug：`fix: 修复登录报错`
     - 更新文档：`docs: 更新README`

2. **点击「提交」按钮**
   - 输入框上方有个 **✓ 提交** 按钮（或按 `Ctrl + Enter`）
   - 点击后即完成本地提交

3. **查看提交历史**
   - VS Code 底部状态栏 → 点击分支名（如 `master`）→ 选择「查看提交历史」
   - 或者安装 GitLens 插件可以有更好看的界面

---

## 5. 推送到 GitHub（Push）

> **目标**：把本地的代码上传到 GitHub 仓库

### 前置：在 GitHub 创建仓库

1. 浏览器打开 https://github.com/new
2. 填写仓库名（Repository name），例如 `gitcodeTest`
3. 选择 Public（公开）或 Private（私有）
4. 点击「Create repository」
5. 复制仓库地址：`https://github.com/lgw2004/gitcodeTest.git`

### VS Code 操作步骤

#### 方式一：使用 VS Code 图形界面（推荐）

1. **添加远程仓库（只需一次）**
   - 在源代码管理面板 → 点击 `···`（更多操作）→ **远程** → **添加远程仓库**
   - 输入远程仓库名称：`origin`（惯例叫这个名字）
   - 输入仓库 URL：`https://github.com/lgw2004/gitcodeTest.git`
   - 点击「添加」

   ![添加远程仓库](https://code.visualstudio.com/assets/docs/sourcecontrol/overview/scm-viewlet.png)

2. **推送代码**
   - 点击底部状态栏的 `↑ 发布` 或 `→ master` 旁边的同步按钮
   - 或者：点击 `···` → **推送**
   - VS Code 会弹窗让你登录 GitHub

3. **首次推送特殊操作**
   - 首次需要设置上游分支：`···` → **分支** → **发布分支**
   - 选择 `origin/master` 即可

#### 方式二：使用终端命令

按 `` Ctrl + ` `` 打开终端，粘贴：

```bash
# 添加远程仓库（只需一次）
git remote add origin https://github.com/lgw2004/gitcodeTest.git

# 推送到 GitHub
git push -u origin master
```

> 第一次推送会让你输入 GitHub 用户名和密码（或 Personal Access Token）

### 关于 GitHub 登录认证

从 2021 年起，GitHub 不再支持用密码 Push，需要用 **Personal Access Token**：

1. GitHub 网页 → 右上角头像 → Settings
2. 左侧 → Developer settings → Personal access tokens → Tokens (classic)
3. Generate new token → 勾选 `repo` 权限
4. 复制生成的 token（**只显示一次，保存好**）
5. 推送时提示输入密码 → 粘贴这个 token 即可

> 💡 **推荐方案**：安装 GitHub CLI（`gh`），登录一次后自动处理认证
> - 下载：https://cli.github.com/
> - 安装后终端运行 `gh auth login` 登录即可

---

## 6. 日常更新流程

以后改完代码想上传，只需 3 步：

```
步骤 A ──→ 步骤 B ──→ 步骤 C
暂存文件     提交代码     推送到 GitHub
(Ctrl+Shift+G)  (写说明按Ctrl+Enter)  (点推送按钮)
```

### 详细操作

#### 步骤 A：暂存文件

1. 打开源代码管理面板（`Ctrl + Shift + G`）
2. 查看「更改」区域，确认改了什么
3. 点击「更改」右侧的 `+` 号，暂存所有改动

#### 步骤 B：提交代码

1. 在输入框写提交说明，例如 "feat: 添加了 RAG 问答功能"
2. 按 `Ctrl + Enter` 提交

#### 步骤 C：推送到 GitHub

1. 点击底部状态栏的同步按钮（带箭头的圆形图标）
2. 或者 `···` → **推送**

> 如果提示 "没有上游分支"，选择「发布分支」即可

### VS Code 状态栏说明

底部状态栏的信息很有用：

```
master*  ↑1 ↓0   ○ → origin/master
│       │   │    └── 远程同步状态
│       │   └── 落后远程提交数
│       └── 领先远程提交数
└── 当前分支
```

- `*` 号表示有未提交的修改
- `↑1` 表示本地比远程多 1 个提交（需要 Push）
- `↓2` 表示远程比本地多 2 个提交（需要 Pull）

---

## 7. 常见问题

### Q1：Push 提示 "Failed to connect to github.com"

**原因**：网络无法直连 GitHub

**解决方法**：

配代理（如果有本地代理工具）：
```bash
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897
```

或者用 Gitee（码云）替代 GitHub。

### Q2：Push 提示 "could not read Username for 'https://github.com'"

**原因**：没有登录认证

**解决方法**：

- 方案 A：安装 GitHub CLI → `gh auth login` 登录
- 方案 B：用 Personal Access Token 代替密码（见上面第 5 节的说明）

### Q3：想撤销上一次提交

```bash
# 撤销最近一次提交，但保留改动
git reset --soft HEAD~1
```

### Q4：不小心忘了 Git 的认证密码

```bash
# Windows 凭据管理器里删除旧记录
# 控制面板 → 凭据管理器 → Windows 凭据 → 删除 git:https://github.com 相关的
```

### Q5：怎么看改了哪些文件？

- VS Code 左侧源代码管理面板 → 点击文件可以看到 diff（对比视图）
- 绿色 = 新增的行，红色 = 删除的行

---

## 总结：VS Code Git 操作速查表

| 操作 | VS Code 操作 | 快捷键 |
|------|-------------|--------|
| 打开源代码管理 | 点击左侧分支图标 | `Ctrl + Shift + G` |
| 暂存单个文件 | 文件右侧的 `+` | - |
| 暂存所有文件 | 「更改」右侧的 `+` | - |
| 提交 | 输入框写说明 → 点击 ✓ | `Ctrl + Enter` |
| 推送到 GitHub | 底部状态栏同步按钮 | - |
| 拉取最新代码 | 底部状态栏同步按钮 | - |
| 查看文件改动 | 点击文件名 | - |
| 查看提交历史 | 底部状态栏 → 分支名 | - |

---

> **一句话记住 Git 工作流**：
>
> **改代码 → 暂存（+）→ 提交（写说明）→ 推送（上传）**
