# 🧠 MCP Demo with Database Interactions

This project demonstrates how to use **Model Context Protocol (MCP)** to connect an LLM (like ChatGPT or Cursor) with a local SQLite database. It uses [`uv`](https://docs.astral.sh/uv/) as the package/runtime manager and showcases how to run and query a pre-populated database (`mall.db`) via MCP tools.

---

## 📁 Project Structure

```
shaknoah-mcp_demo_with_db_interactions/
├── README.md             # Project documentation
├── init_db.py            # Script to initialize and populate the SQLite database
├── mall.db               # SQLite database file (auto-generated or preloaded)
├── pyproject.toml        # Project dependency definitions (PEP 621 format)
├── script.py             # Optional script for manual or client interaction
├── server.py             # MCP server exposing database tools
├── transactions.py       # Logic for querying and processing database info
├── uv.lock               # uv lock file for reproducibility
└── .python-version       # Specifies Python version used (optional)
```

---

## 🧰 Requirements

- [uv](https://astral.sh/blog/uv-is-here/) (Fast Python package & runtime manager)
- Python 3.10+ (recommended)
- SQLite3

---

## 🚀 Setup Instructions

### 1. 📦 Install `uv`

If you don't have `uv` installed:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### 2. 🛠️ Clone and Navigate

```bash
git clone https://github.com/your-username/shaknoah-mcp_demo_with_db_interactions.git
cd shaknoah-mcp_demo_with_db_interactions
```

### 3. 📥 Install Dependencies

This project uses `pyproject.toml` to manage dependencies:

```bash
uv pip install -e .
```

If you're missing a `pyproject.toml`, use the template below:

```toml
[project]
name = "mcp_demo"
version = "0.1.0"
dependencies = [
    "fastapi",
    "uvicorn",
    "sqlite-utils",
    "faker",
    "mcp==0.2.0"
]
```

> Replace `mcp==0.2.0` with the correct version you use.

---

### 4. 🧱 Initialize the Database

If `mall.db` is not present, create it using:

```bash
uv run init_db.py
```

This script generates a mock transaction dataset with customers, items, and stores.

---

## 🔌 Running the MCP Server

Start the MCP server with:

```bash
uv run server.py
```

Your server will now expose a set of tools to query the database in real time.

---

## 🔗 Connect with MCP Client

Connect this server to any MCP-compatible client like:

- **ChatGPT (Custom GPTs with MCP support)**
- **Cursor IDE**
- **Any LLM interface that supports JSON-RPC 2.0 over MCP**

### Example `mcpServers` Block (Cursor/ChatGPT setup):

```json
{
  "mcpServers": {
    "mall_db_demo": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/shaknoah-mcp_demo_with_db_interactions",
        "run",
        "server.py"
      ]
    }
  }
}
```

Replace the `/ABSOLUTE/PATH/...` with the actual project path on your machine.

---

## 🧪 Example Questions You Can Ask

Once the server is running and connected, you can ask:

- "Which 5 customers have spent the most?"
- "What’s the most purchased item across all stores?"
- "Which store generated the highest revenue?"
- "Total quantity sold and revenue by product category?"
- "How much has customer `CUST0420` spent?"

These are handled by functions in `transactions.py`.

---

## 🧹 Clean Up and Reset

To regenerate or clear the database:

```bash
rm mall.db
uv run init_db.py
```

---

## 📄 License

MIT License

---

## ✍️ Author

**MOHD SHAKIR**  
Made with ❤️ using MCP, SQLite, and uv
