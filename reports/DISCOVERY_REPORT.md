# Discovery Report

Date: 2026-11-05 · Method: GitHub REST API through the authenticated `gh` CLI.

## Pipeline

1. Ran 10 repository searches covering OpenCode, plugins, skills, MCP servers, themes and agents.
2. Deduplicated the result pages into **757 unique repositories**; **675** contained an OpenCode signal in the name, description or topics.
3. Reviewed descriptions, recency, license metadata and repository structure.
4. Selected **91** candidates for metadata verification and README inspection.
5. Fetched `repos/{owner}/{repo}`, `readme` and `releases/latest` metadata for every selected repository.
6. Kept unresolved brief entries in the raw inventory instead of promoting them.

## Queries

| Query | Rows reviewed | Reported total |
| --- | --- | --- |
| opencode in:name,description,readme | 100 | 269,381 |
| topic:opencode | 100 | 10,997 |
| opencode agent in:name,description | 100 | 10,905 |
| opencode plugin in:name,description | 100 | 5,441 |
| opencode skills in:name,description | 100 | 4,880 |
| opencode mcp in:name,description | 100 | 2,312 |
| topic:opencode-plugin | 100 | 1,598 |
| opencode theme in:name,description | 100 | 283 |
| topic:opencode-skills | 100 | 252 |
| topic:opencode-mcp | 2 | 2 |

## Selection rules

- The project explicitly targets OpenCode, or is a multi-agent skill/MCP resource with a clear OpenCode path.
- The repository is public, not archived and not a fork.
- It has a usable README and a declared capability that fits an existing category.
- Offensive-security, OSINT and CTF resources are included only with warning labels and authorized-use notes.
- Permission-bypass and guardrail-removal projects are excluded.

## Limits

- Discovery used GitHub search, not a complete census. Private repositories and unindexed projects are out of scope.
- Stars and recency are signals, not quality claims.
- The 91 additions were verified from registry metadata and READMEs; their runtime behavior was not audited.
- A full per-query export is not committed because it would add hundreds of irrelevant repositories. The reproducible queries are listed above.
