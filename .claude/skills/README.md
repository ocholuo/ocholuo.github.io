# .claude/skills/

This directory contains project-level Claude Code skills — reusable workflows that
Claude automatically loads when working in this repository.

## How skills work

When you open a Claude Code session in this repo, any skill listed in `.claude/skills/`
becomes available. Claude reads the skill's description to decide when to invoke it.
You can also trigger a skill explicitly by describing what you want, e.g.:

> "check my repo for personal info"
> "scan for PII before I make this public"
> "privacy audit"

Skills are just markdown files — they contain instructions Claude follows, not code
that runs automatically. Nothing executes until you ask Claude to do something.

## Skills in this repo

### `privacy-audit/`

Scans `_posts/` for personally identifiable information (PII) that could de-anonymize
the blog author in a public repository.

**What it does:**
1. Runs grep patterns across all markdown posts
2. Reviews each match in context (filters out lab examples, CTF content, fictional data)
3. Presents a prioritized report with suggested replacements
4. Applies your chosen fixes with before/after confirmation

**What it won't flag:** Tutorial email addresses, CTF credentials, lab IPs, or anything
that is clearly fictional or example data. For ambiguous cases, it asks you to decide.

**Replacements:** When PII needs to be replaced, the skill uses a consistent set of
fictional values (fake name, fake financials, placeholder email, etc.) defined inside
`SKILL.md`. These are intentionally made-up — not derived from any real data.

**Design note:** This skill is intentionally written without hardcoded personal
identifiers. It reasons about what counts as "already public" from context rather than
maintaining a list of specific values. This means the skill file itself is safe to
commit to a public repo.

## Adding a new skill

Create a subdirectory with a `SKILL.md` file:

```
.claude/skills/
└── my-skill/
    └── SKILL.md        ← required: YAML frontmatter + instructions
```

The frontmatter needs at minimum:

```yaml
---
name: my-skill
description: >
  One paragraph describing what this skill does and when Claude should use it.
  Be specific about trigger phrases so Claude knows when to load it.
---
```

Optionally add a `references/` subdirectory for supporting docs that are too long
to inline in `SKILL.md`.

See the [Claude Code skills documentation](https://docs.anthropic.com/en/docs/claude-code)
for the full skill spec.
