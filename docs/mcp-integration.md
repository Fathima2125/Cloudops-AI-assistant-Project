# MCP Integration

## What is MCP?

MCP stands for Model Context Protocol. It allows an AI assistant to connect to external tools, documentation sources, and systems through controlled MCP servers.

## Why MCP is used in this project

This project uses MCP so Codex can retrieve official AWS documentation while creating CloudOps learning notes and reliability reports. This makes AI-generated explanations easier to verify and safer than relying only on model memory.

## MCP Server Used

- AWS Documentation MCP Server

## Workflow

User → Codex CLI → Prompts/CLI → AWS question → AWS Documentation MCP → Markdown report

## Safety

This phase uses documentation lookup only. Codex can search and read AWS documentation, but it does not inspect live AWS accounts, modify resources, run Terraform, or perform production actions.

## Future Enhancements

- AWS read-only resource inspection
- GitHub MCP
- CloudWatch MCP-style integration
