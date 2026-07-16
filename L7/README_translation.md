# L7 Agent

基于 Claude Agent SDK 构建的多 agent 系统，具备文档研究、仓库分析和 Web 研究能力。

## Setup

1. 安装依赖：
   ```bash
   uv sync
   ```

2. 在项目根目录创建 `.env` 文件：
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_api_key
   NOTION_TOKEN=your_notion_integration_token
   ```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | 用于访问 Claude 的 Anthropic API key |
| `NOTION_TOKEN` | 用于本地 MCP server 访问的 Notion integration token |

如果你选择不尝试 MCP server，可以跳过定义 `NOTION_TOKEN`。

### Getting an Anthropic API Key

1. 前往 <a href="https://console.anthropic.com/" target="_blank">Anthropic Console</a>
2. 注册或登录你的账户
3. 在设置中导航至 **API Keys**
4. 点击 **Create Key** 并复制生成的 key

### Optional - Getting a Notion Token
用于运行 Notion 本地 MCP server。

**Note:** 必须安装 Node.js，因为 MCP server 通过 `npx` 运行。在此下载 Node.js：<a href="https://nodejs.org/" target="_blank">here</a>。

1. 在 Notion 创建账户（使用免费计划）<a href="https://www.notion.so/signup" target="_blank">here</a>
2. 前往 <a href="https://www.notion.so/my-integrations" target="_blank">Notion Integrations</a>
3. 点击 **New integration**
4. 为其命名并选择 workspace
5. 点击 **Configure Internal Settings**
6. 复制 **Internal Integration Secret**
7. 将你想访问的 Notion 页面共享给你的 integration：
    - 导航至 **Access** 标签页
    - 点击 **Edit Access**
    - 搜索你想包含的页面

更多详情，请查看安装说明 <a href="https://github.com/makenotion/notion-mcp-server?tab=readme-ov-file#installation" target="_blank">here</a>。

## Running the Agent

```bash
uv run python agent.py
```

运行后，输入消息并按 Enter。输入 `exit` 退出。
