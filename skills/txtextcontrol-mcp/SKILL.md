---
name: txtextcontrol-mcp
description: "TXTextcontrol - guidelines to use textcontrol MCP"
applyTo: "**/*"
---

# Text Control MCP Serve

> The Text Control MCP server is a read-only Model Context Protocol endpoint that exposes 30 tools across 8 content domains. Each domain supports search, list, and get operations over JSON-RPC 2.0 via Streamable HTTP. Compatible with Claude Code, VS Code, Cursor, and JetBrains.

- **Author:** Jonathan Maron
- **Published:** 2026-04-07
- **Modified:** 2026-04-08
- **Description:** The Text Control MCP server is a read-only Model Context Protocol endpoint that exposes 30 tools across 8 content domains. Each domain supports search, list, and get operations over JSON-RPC 2.0 via Streamable HTTP. Compatible with Claude Code, VS Code, Cursor, and JetBrains.
- **19 min read** (3669 words)
- **Tags:**
  - MCP
  - AI
- **Web URL:** https://www.textcontrol.com/blog/2026/04/07/text-control-mcp-server/
- **LLMs URL:** https://www.textcontrol.com/blog/2026/04/07/text-control-mcp-server/llms.txt
- **LLMs-Full URL:** https://www.textcontrol.com/blog/2026/04/07/text-control-mcp-server/llms-full.txt

---

Today we are proud to announce the release of our **Text Control MCP Server**, a read-only [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) endpoint that gives AI assistants direct access to our blog posts, product features, API documentation, pricing, career postings, conference listings, newsletter archives, and the full-text site search index.

Add one URL to your AI assistant's configuration, and it can search, list, and retrieve Text Control content without leaving your editor.

#### Why Model Context Protocol (MCP)

The [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-03-26) is an open standard that defines how AI assistants communicate with external data sources. Before MCP, connecting an assistant to a new data source meant writing custom integration code for each client. MCP replaces that with a single interface: the assistant sends JSON-RPC 2.0 requests over HTTP, and any conforming server responds with structured data.

One server, every client. Claude Code, VS Code with GitHub Copilot, Cursor, Claude Desktop, and JetBrains IDEs all connect to the same endpoint using the same protocol.

#### What the MCP Server Provides

30 tools organized into 8 content domains. Each domain follows a consistent pattern of **search**, **list**, and **get** operations. Search and list tools return up to 15 results by default. Ask for a specific number to control the `limit` parameter. Use the `offset` parameter to page through larger result sets. The examples below show what to ask your AI assistant and which tool it calls behind the scenes.

## Blog Tools

Search, list, and retrieve posts, tags, and authors.

## blog_search_posts

Search posts by keywords across titles, summaries, authors, slugs, and tags.

```plaintext
Search the Text Control blog for posts about document editing.
```

Calls `blog_search_posts` with `query: "document editing"`.

```plaintext
Find the 5 most relevant blog posts about mail merge.
```

Calls `blog_search_posts` with `query: "mail merge"` and `limit: 5`.

```plaintext
Are there any blog posts about PDF export?
```

Calls `blog_search_posts` with `query: "PDF export"`.

## blog_get_post

Retrieve a single post by ID or by date and slug. Set `content: true` to include the full Markdown body.

```plaintext
Get the blog post with ID 20260217a.
```

Calls `blog_get_post` with `id: "20260217a"`.

```plaintext
Show me the blog post from February 17, 2026 about building a custom backstage view.
```

Calls `blog_get_post` with `year: "2026"`, `month: "02"`, `day: "17"`, and the matching `slug`.

```plaintext
Get the full Markdown content of blog post 20260217a.
```

Calls `blog_get_post` with `id: "20260217a"` and `content: true`.

## blog_list_posts

List posts with optional date filters. All parameters — `year`, `month`, `day`, and `limit` — are optional.

```plaintext
List the 10 most recent blog posts.
```

Calls `blog_list_posts` with `limit: 10`.

```plaintext
What blog posts were published in March 2025?
```

Calls `blog_list_posts` with `year: "2025"` and `month: "03"`.

```plaintext
Show me all blog posts from March 28, 2025.
```

Calls `blog_list_posts` with `year: "2025"`, `month: "03"`, and `day: "28"`.

## blog_list_posts_by_tag

List posts filtered by a specific tag. The `id` parameter is the tag slug.

```plaintext
List all blog posts tagged with aspnet-core.
```

Calls `blog_list_posts_by_tag` with `id: "aspnet-core"`.

```plaintext
Show me the 5 most recent posts about Angular.
```

Calls `blog_list_posts_by_tag` with `id: "angular"` and `limit: 5`.

## blog_list_posts_by_author

List posts filtered by a specific author. The `id` parameter is the author slug.

```plaintext
List all blog posts written by Bjoern Meyer.
```

Calls `blog_list_posts_by_author` with `id: "bjoern-meyer"`.

```plaintext
Show me the 3 most recent posts by Jonathan Maron.
```

Calls `blog_list_posts_by_author` with `id: "jonathan-maron"` and `limit: 3`.

## blog_list_tags

List all tags with their labels and post counts.

```plaintext
What tags are used on the Text Control blog?
```

Calls `blog_list_tags` with no arguments.

```plaintext
List the 5 most popular blog tags.
```

Calls `blog_list_tags` with `limit: 5`.

## blog_get_tag

Get a single tag by ID, returning its label and post count.

```plaintext
How many posts are tagged with aspnet-core?
```

Calls `blog_get_tag` with `id: "aspnet-core"`.

## blog_get_author

Get a single author by ID, returning their name, bio, and post count.

```plaintext
Tell me about blog author Bjoern Meyer.
```

Calls `blog_get_author` with `id: "bjoern-meyer"`.

## blog_list_authors

List all authors with bios and post counts, sorted by post count descending.

```plaintext
Who writes for the Text Control blog?
```

Calls `blog_list_authors` with no arguments.

```plaintext
List the top 3 most prolific blog authors.
```

Calls `blog_list_authors` with `limit: 3`.

## Careers Tools

Search, list, and retrieve job postings. Ask for _full content_ or _full job description_ to retrieve the complete posting as Markdown.

## career_search

Search career postings by keywords across titles, summaries, locales, employment types, and offices.

```plaintext
Search Text Control job openings for C++ positions.
```

Calls `career_search` with `query: "C++"`.

```plaintext
Find career postings related to technical support, limit to 3.
```

Calls `career_search` with `query: "technical support"` and `limit: 3`.

## career_get

Retrieve a single career posting by ID. Set `content: true` to include the full job description as Markdown.

```plaintext
Show me the details of career posting 42388ff2.
```

Calls `career_get` with `id: "42388ff2"`.

```plaintext
Get the full job description for posting 42388ff2.
```

Calls `career_get` with `id: "42388ff2"` and `content: true`.

## career_list

List all visible career postings.

```plaintext
List all open positions at Text Control.
```

Calls `career_list` with no arguments.

```plaintext
Show me the 2 most recent job openings.
```

Calls `career_list` with `limit: 2`.

## Conferences Tools

Search, list, and retrieve industry events.

## conference_search

Search conferences by keywords in title or summary.

```plaintext
Search for Text Control conferences related to Visual Studio.
```

Calls `conference_search` with `query: "Visual Studio"`.

```plaintext
Find conferences about .NET, limit to 3.
```

Calls `conference_search` with `query: ".NET"` and `limit: 3`.

## conference_get

Get a single conference by its ID.

```plaintext
Get the details for the most recent conference.
```

Calls `conference_list` with `limit: 1`, then `conference_get` with the returned ID.

## conference_list

List all conferences, sorted newest first.

```plaintext
List all conferences where Text Control has presented.
```

Calls `conference_list` with no arguments.

```plaintext
Show me the 3 most recent conference appearances.
```

Calls `conference_list` with `limit: 3`.

## Documentation Tools

Search, list, and retrieve API documentation pages from the reference manuals. Documentation is available per product. Ask for _full content_ to retrieve the complete page as Markdown.

## documentation_search

Search documentation pages by keywords in title or description. Optionally filter by product.

```plaintext
Search the TX Text Control .NET Server documentation for MailMerge.
```

Calls `documentation_search` with `query: "MailMerge"`.

```plaintext
Find documentation about ApplicationField in TX Text Control .NET Server, limit to 5.
```

Calls `documentation_search` with `query: "ApplicationField"`, `product_name_id: "tx-text-control-dotnet-server"`, and `limit: 5`.

```plaintext
Search for ServerTextControl in the TX Text Control .NET Server docs.
```

Calls `documentation_search` with `query: "ServerTextControl"` and `product_name_id: "tx-text-control-dotnet-server"`.

```plaintext
Find all documentation related to Barcode in TX Text Control .NET Server, limit to 10.
```

Calls `documentation_search` with `query: "Barcode"`, `product_name_id: "tx-text-control-dotnet-server"`, and `limit: 10`.

```plaintext
What document formats does TX Text Control .NET Server support for loading and saving?
```

Calls `documentation_search` with `query: "StreamType"` and `product_name_id: "tx-text-control-dotnet-server"`.

```plaintext
What does the TX Text Control .NET Server documentation say about tracking changes?
```

Calls `documentation_search` with `query: "tracking changes"` and `product_name_id: "tx-text-control-dotnet-server"`.

## documentation_get

Retrieve a single documentation page by product and page ID. Set `content: true` to include the full page body as Markdown.

```plaintext
What is the TXTextControl.ApplicationField class and what is it used for?
```

Calls `documentation_search` with `query: "ApplicationField class"` to find the page, then `documentation_get` with `content: true` to retrieve the full documentation.

```plaintext
Show me all properties of the TXTextControl.ServerTextControl class in TX Text Control .NET Server.
```

Calls `documentation_search` with `query: "ServerTextControl"` and `product_name_id: "tx-text-control-dotnet-server"`, then `documentation_get` with `content: true`.

```plaintext
What methods does the TXTextControl.DocumentServer.MailMerge class provide for mail merge operations?
```

Calls `documentation_search` with `query: "MailMerge class"`, then `documentation_get` with `content: true` to retrieve the class members.

```plaintext
What properties does the TXTextControl.SaveSettings class provide for saving documents?
```

Calls `documentation_search` with `query: "SaveSettings"` and `product_name_id: "tx-text-control-dotnet-server"`, then `documentation_get` with `content: true`.

```plaintext
What configuration options does the TXTextControl.LoadSettings object support?
```

Calls `documentation_search` with `query: "LoadSettings"` and `product_name_id: "tx-text-control-dotnet-server"`, then `documentation_get` with `content: true`.

```plaintext
Give me an overview of the TXTextControl namespace and its main classes.
```

Calls `documentation_search` with `query: "TXTextControl namespace"`, then `documentation_get` to retrieve the namespace overview page.

## documentation_list

List documentation pages for a product, optionally filtered by type or subpart.

```plaintext
List all TX Text Control .NET Server documentation pages of type "class".
```

Calls `documentation_list` with `product_name_id: "tx-text-control-dotnet-server"` and `type: "class"`.

```plaintext
Show me TX Text Control .NET Server documentation pages in the JavaScript API section, limit to 5.
```

Calls `documentation_list` with `product_name_id: "tx-text-control-dotnet-server"`, `subpart: "JavaScript API"`, and `limit: 5`.

```plaintext
List all namespaces in TX Text Control .NET Server.
```

Calls `documentation_list` with `product_name_id: "tx-text-control-dotnet-server"` and `type: "namespace"`.

```plaintext
Show me all enumerations in the TX Text Control .NET Server documentation, limit to 10.
```

Calls `documentation_list` with `product_name_id: "tx-text-control-dotnet-server"`, `type: "enumeration"`, and `limit: 10`.

```plaintext
List documentation pages in the TXTextControl.DocumentServer Namespace section.
```

Calls `documentation_list` with `product_name_id: "tx-text-control-dotnet-server"` and `subpart: "TXTextControl.DocumentServer Namespace"`.

```plaintext
What methods are available in the JavaScript API section of TX Text Control .NET Server? Limit to 10.
```

Calls `documentation_list` with `product_name_id: "tx-text-control-dotnet-server"`, `subpart: "JavaScript API"`, `type: "method"`, and `limit: 10`.

## Features Tools

Search, list, and retrieve product features. Mention a category name to filter results. Ask for _full content_ to retrieve the complete feature body as Markdown.

## feature_search

Search product features by keywords in title or summary.

```plaintext
Search Text Control product features for mail merge.
```

Calls `feature_search` with `query: "mail merge"`.

```plaintext
Find features related to PDF, limit to 3.
```

Calls `feature_search` with `query: "PDF"` and `limit: 3`.

## feature_get

Retrieve a single feature by its ID (URL slug). Set `content: true` to include the full feature body as Markdown.

```plaintext
Get details about the mail-merge feature.
```

Calls `feature_get` with `id: "mail-merge"`.

```plaintext
Show me the full content of the mail-merge feature.
```

Calls `feature_get` with `id: "mail-merge"` and `content: true`.

## feature_list

List features with optional category filter. Both `category` and `limit` parameters are optional.

```plaintext
List all Text Control product features.
```

Calls `feature_list` with no arguments.

```plaintext
Show me features in the common category.
```

Calls `feature_list` with `category: "common"`.

```plaintext
List the first 5 features in the common category.
```

Calls `feature_list` with `category: "common"` and `limit: 5`.

## Newsletters Tools

Search, list, and retrieve newsletter issues. Ask for _full content_ to retrieve the complete newsletter body as Markdown.

## newsletter_search

Search newsletters by keywords in title or summary.

```plaintext
Search Text Control newsletters for release announcements.
```

Calls `newsletter_search` with `query: "released"`.

```plaintext
Find newsletters about service pack updates, limit to 5.
```

Calls `newsletter_search` with `query: "service pack"` and `limit: 5`.

## newsletter_list

List newsletters with an optional year filter. Both `year` and `limit` parameters are optional.

```plaintext
List all Text Control newsletters from 2025.
```

Calls `newsletter_list` with `year: "2025"`.

```plaintext
Show me the 5 most recent newsletters.
```

Calls `newsletter_list` with `limit: 5`.

## newsletter_get

Retrieve a single newsletter by ID or by date. Current-format newsletters include structured `lead` and `items` data. Set `content: true` to include the full body as Markdown.

```plaintext
Get the newsletter from February 18, 2026.
```

Calls `newsletter_get` with `year: "2026"`, `month: "02"`, and `day: "18"`.

```plaintext
Show me newsletter 20260218 with the full Markdown content.
```

Calls `newsletter_get` with `id: "20260218"` and `content: true`.

## Pricing Tools

Search, list, and retrieve product listings with prices in EUR and USD.

## pricing_search

Search products by keywords across product codes, names, technologies, editions, and descriptions.

```plaintext
Search Text Control products for enterprise editions.
```

Calls `pricing_search` with `query: "enterprise"`.

```plaintext
Find products related to server licenses, limit to 3.
```

Calls `pricing_search` with `query: "server"` and `limit: 3`.

## pricing_get

Retrieve a single product by its ID (product code).

```plaintext
What is the price of product TX-3400-DE-S?
```

Calls `pricing_get` with `id: "TX-3400-DE-S"`.

## pricing_list

List all products for sale with pricing in EUR and USD.

```plaintext
List all Text Control server products with pricing.
```

Calls `pricing_list` with no arguments.

```plaintext
Show me the first 3 products for sale.
```

Calls `pricing_list` with `limit: 3`.

## Web Search Tools

Full-text search across the entire Text Control website. Searches blog posts, documentation, product pages, newsletters, and code samples from a single search index. Filter by content section using `scope`, and narrow documentation results to a specific product with `product_name_id`. Ask for _full content_ to retrieve the complete page body as Markdown.

## web_search

Full-text search across the entire Text Control website — blog, documentation, product pages, newsletters, and code samples.

```plaintext
Search the Text Control website for MailMerge.
```

Calls `web_search` with `query: "MailMerge"`.

```plaintext
Find pages about PDF generation on the Text Control site.
```

Calls `web_search` with `query: "PDF generation"`.

```plaintext
Search Text Control newsletters for articles about PDF/A compliance.
```

Calls `web_search` with `query: "PDF/A compliance"` and `scope: "newsletter"`.

```plaintext
Find pages about digital signatures in the TX Text Control .NET Server documentation.
```

Calls `web_search` with `query: "digital signatures"`, `scope: "documentation"`, and `product_name_id: "tx-text-control-dotnet-server"`.

## web_list

Browse all indexed pages on the Text Control website. Filter by content section using `scope`. When scope is `documentation`, narrow to a specific product with `product_name_id`.

```plaintext
List the most recent pages on the Text Control website.
```

Calls `web_list` with no arguments (defaults to all scopes).

```plaintext
Show me the latest blog posts on the Text Control website.
```

Calls `web_list` with `scope: "blog"`.

```plaintext
List documentation pages for TX Text Control .NET Server.
```

Calls `web_list` with `scope: "documentation"` and `product_name_id: "tx-text-control-dotnet-server"`.

```plaintext
List 25 sample pages from the Text Control website.
```

Calls `web_list` with `scope: "samples"` and `limit: 25`.

## web_get

Retrieve a single page by its ID (UUID). Use an `id` value returned by `web_search` or `web_list`. Set `content: true` to include the full page body as Markdown.

```plaintext
Search for MailMerge on the website, then show me the full content of the first result.
```

Calls `web_search` to find results, then `web_get` with the `id` of the first result and `content: true`.

```plaintext
What does the Text Control website say about document templates? Show me the full content of the most relevant page.
```

Calls `web_search` with `query: "document templates"`, then `web_get` with the `id` of the top result and `content: true`.

> **Public and Read-Only**
>
> The MCP server requires **no authentication**. All exposed data is public content already available on the Text Control website. The server supports read operations only — it cannot modify any data.

#### Connecting Your AI Assistant

Setup takes one step: add the server URL to your client's MCP configuration. The endpoint is:

```
https://www.textcontrol.com/mcp/v1
```

Select your client below for the exact configuration:

## Amazon Q Developer CLI

Amazon Q Developer CLI is AWS's AI-powered coding assistant that runs in your terminal. It supports MCP servers for connecting to external data sources during coding and debugging sessions. The MCP configuration is stored in your AWS configuration directory.

Add the following to your Amazon Q MCP configuration at `~/.aws/amazonq/mcp.json`:

```
// ~/.aws/amazonq/mcp.json
{
  "mcpServers": {
    "textcontrol": {
      "type": "http",
      "url": "https://www.textcontrol.com/mcp/v1"
    }
  }
}
```

For further configuration details, please refer to the [documentation](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-mcp-config-CLI.html).

## Claude Code

Claude Code is Anthropic's terminal-based AI coding assistant. It runs directly in your shell, reads your codebase, and executes commands on your behalf. MCP servers registered in the project or global configuration are available to Claude Code in every conversation.

Add the following to your project's `.mcp.json` or your global settings at `~/.claude.json`:

```
// .mcp.json (project) or ~/.claude.json (global)
{
  "mcpServers": {
    "textcontrol": {
      "type": "http",
      "url": "https://www.textcontrol.com/mcp/v1"
    }
  }
}
```

For further configuration details, please refer to the [documentation](https://code.claude.com/docs/en/mcp).

## Claude Desktop

Claude Desktop is Anthropic's standalone chat application for macOS and Windows. It connects to MCP servers, giving Claude access to external data sources during conversations. You can add remote servers through the UI via **Settings** _​_ **Connectors** _​_ **Add custom connector**. Alternatively, add the following to your `claude_desktop_config.json` using the `mcp-remote` bridge:

```
// claude_desktop_config.json
{
  "mcpServers": {
    "textcontrol": {
      "command": "npx",
      "args": ["mcp-remote", "https://www.textcontrol.com/mcp/v1"]
    }
  }
}
```

For further configuration details, please refer to the [documentation](https://modelcontextprotocol.io/docs/develop/connect-remote-servers).

## Cline (VS Code Extension)

Cline is one of the most popular AI coding extensions for VS Code. It brings agentic coding capabilities directly into the editor with full MCP support. MCP servers can be configured through the Cline sidebar panel or by editing the settings file directly.

In VS Code, open the Cline panel, click the **MCP Servers** icon, and add a new server. Alternatively, add the following to your Cline MCP settings file (`cline_mcp_settings.json`):

```
// cline_mcp_settings.json
{
  "mcpServers": {
    "textcontrol": {
      "type": "streamableHttp",
      "url": "https://www.textcontrol.com/mcp/v1"
    }
  }
}
```

For further configuration details, please refer to the [documentation](https://docs.cline.bot/mcp/configuring-mcp-servers).

## Codex CLI (OpenAI)

Codex CLI is OpenAI's open-source terminal-based coding agent. Like Claude Code, it runs in your shell and can read and modify your codebase. It supports MCP servers for connecting to external data sources during coding sessions.

Add the following to your global configuration at `~/.codex/config.toml`:

```
### ~/.codex/config.toml
[mcp_servers.textcontrol]
url = "https://www.textcontrol.com/mcp/v1"
```

For further configuration details, please refer to the [documentation](https://developers.openai.com/codex/mcp).

## Cursor

Cursor is an AI-native code editor built on the VS Code foundation. It supports MCP servers natively, allowing its built-in AI to query external tools and data sources during chat and inline editing sessions. MCP configuration is stored per project in the repository root.

Add the following to your Cursor MCP configuration at `.cursor/mcp.json`:

```
// .cursor/mcp.json
{
  "mcpServers": {
    "textcontrol": {
      "url": "https://www.textcontrol.com/mcp/v1"
    }
  }
}
```

For further configuration details, please refer to the [documentation](https://cursor.com/docs/context/mcp).

## JetBrains IDEs

JetBrains IDEs — IntelliJ IDEA, Rider, PhpStorm, WebStorm, PyCharm, and others — include an AI Assistant with Model Context Protocol support. MCP servers are configured through the IDE settings UI, making external tools available during AI-assisted coding sessions.

In your JetBrains IDE, navigate to **Settings** _​_ **Tools** _​_ **AI Assistant** _​_ **Model Context Protocol**, and add a new server with the URL `https://www.textcontrol.com/mcp/v1`.

For further configuration details, please refer to the [documentation](https://www.jetbrains.com/help/ai-assistant/mcp.html).

## VS Code + GitHub Copilot

GitHub Copilot integrates directly into VS Code as an AI pair programmer. With MCP support, Copilot can query external data sources during chat sessions. The MCP configuration lives in a dedicated `mcp.json` file, either at the workspace level or scoped to a user.

Add the following to `.vscode/mcp.json` in your workspace (or open the user-level config via Command Palette _​_ **MCP: Open User Configuration**):

```
// .vscode/mcp.json
{
  "servers": {
    "textcontrol": {
      "type": "http",
      "url": "https://www.textcontrol.com/mcp/v1"
    }
  }
}
```

For further configuration details, please refer to the [documentation](https://code.visualstudio.com/docs/copilot/customization/mcp-servers).

## Windsurf

Windsurf is an AI-powered code editor by Codeium that features deep codebase understanding and agentic workflows. It supports MCP servers natively, allowing its AI to access external data sources during chat and code generation. The MCP configuration is stored in a global settings file.

Add the following to your Windsurf MCP configuration at `~/.codeium/windsurf/mcp_config.json`:

```
// ~/.codeium/windsurf/mcp_config.json
{
  "mcpServers": {
    "textcontrol": {
      "serverUrl": "https://www.textcontrol.com/mcp/v1"
    }
  }
}
```

For further configuration details, please refer to the [documentation](https://docs.windsurf.com/windsurf/cascade/mcp).

## Zed

Zed is a high-performance, open-source code editor with built-in AI features. It supports MCP through its context server system, giving its AI assistant access to external data sources. MCP servers are configured in the Zed settings file.

Add the following to your Zed settings at `~/.config/zed/settings.json`:

```
// ~/.config/zed/settings.json (excerpt)
{
  "context_servers": {
    "textcontrol": {
      "url": "https://www.textcontrol.com/mcp/v1"
    }
  }
}
```

For further configuration details, please refer to the [documentation](https://zed.dev/docs/ai/mcp).

#### How It Works

The server implements the [MCP 2025-03-26 specification](https://modelcontextprotocol.io/specification/2025-03-26) using Streamable HTTP transport. Clients send JSON-RPC 2.0 requests via `POST` to a single endpoint. The server responds with structured JSON.

Four JSON-RPC methods handle the full lifecycle:

| Method       | Purpose                                                                             |
| ------------ | ----------------------------------------------------------------------------------- |
| `initialize` | Handshake — exchanges protocol version and server capabilities                      |
| `ping`       | Health check — confirms the server is reachable                                     |
| `tools/list` | Discovery — returns all 30 tool definitions with JSON Schema parameter descriptions |
| `tools/call` | Execution — runs a named tool with the supplied arguments and returns results       |

Internally, each request flows through three layers:

1. A **PSR-15 request handler** parses and validates the JSON-RPC envelope
2. A **central adapter** routes the tool name to one of 8 domain-specific adapters
3. Each **domain adapter** queries the existing business model layer, serializes the entities, and generates absolute URLs for every returned record

The MCP server shares the same models and database layer that power the Text Control website. There is no separate data store and no synchronization step. When content changes on the website, the MCP server reflects it immediately.

#### Get Started Today

The Text Control MCP server is live now. Add the endpoint URL to your AI assistant and start querying — blog posts, product features, pricing, open positions, and more.

We built this because we want our content available where developers already work: inside their editors and AI assistants. MCP makes that possible with one endpoint and a standard protocol.

Connect your assistant and see what it finds. Happy coding!

---

## About Jonathan Maron

Jonathan is a seasoned web development and operations leader based in Bremen, Germany. He has served as Head of Web Development and Operations at Text Control since 2012. Having joined the company in 1996 as a Web Developer, he has advanced through a range of technical and leadership roles, demonstrating sustained professional growth and long-term commitment.

With more than 30 years of industry experience, Jonathan brings deep expertise in Linux, Apache, MySQL, PHP, JavaScript, and SCSS. He combines strong architectural knowledge with operational excellence, and has consistently adapted to evolving technologies and industry standards throughout his career.

Fluent in English, French, and German, Jonathan communicates effectively across technical and business contexts, contributing to successful collaboration in international environments.

- [LinkedIn](https://www.linkedin.com/in/jonathanmaron/)
- [X](https://x.com/jonathanmaron)
- [GitHub](https://github.com/jonathanmaron?tab=repositories)

---

## Related Posts

- [AI Tools: MCP Server and Agent Skills](https://www.textcontrol.com/blog/2026/04/09/text-control-ai-tools-mcp-server-and-agent-skills/llms.txt)
- [Introducing Text Control Agent Skills](https://www.textcontrol.com/blog/2026/03/27/introducing-text-control-agent-skills/llms.txt)
- [AI-Ready Legal Documents: What to Fix Before Adding AI](https://www.textcontrol.com/blog/2026/01/12/ai-ready-legal-documents-what-to-fix-before-adding-ai/llms.txt)
- [Explaining Contract Tracked Changes Automatically Using .NET C# and AI](https://www.textcontrol.com/blog/2026/01/09/explaining-contract-tracked-changes-automatically-using-dotnet-csharp-and-ai/llms.txt)
- [Automating PDF/UA Accessibility with AI: Describing DOCX Documents Using TX Text Control and LLMs](https://www.textcontrol.com/blog/2025/10/16/automating-pdf-ua-accessibility-with-ai-describing-docx-documents-using-tx-text-control-and-llms/llms.txt)
- [Transforming Legal Review with AI and TX Text Control: A Smarter, Faster Approach to Legal Document Processing in .NET C#](https://www.textcontrol.com/blog/2024/11/01/transforming-legal-review-with-ai-and-tx-text-control-a-smarter-faster-approach-to-legal-document-processing/llms.txt)
- [Intelligent Document Processing (IDP) using TX Text Control in .NET C#](https://www.textcontrol.com/blog/2024/08/15/intelligent-document-processing-idp-using-tx-text-control-in-net-csharp/llms.txt)
- [Using OpenAI to Generate Content in TX Text Control](https://www.textcontrol.com/blog/2023/10/09/using-openai-to-generate-content-in-tx-text-control/llms.txt)
- [Integrating OpenAI ChatGPT with TX Text Control to Rephrase Content](https://www.textcontrol.com/blog/2023/03/27/integrating-open-ai-chatgpt-with-tx-text-control-to-rephrase-content/llms.txt)
