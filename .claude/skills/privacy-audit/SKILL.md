---
name: privacy-audit
description: >
  Scans the Jekyll blog's _posts/ directory for personally identifiable information (PII)
  that could de-anonymize the author in a public repository. Use this skill whenever the
  user asks anything like: "does my repo leak personal info?", "check my posts for PII",
  "review before going public", "is there anything traceable to me?", "scan for personal
  information", "make sure nothing identifies me", "check for my address/salary/employer",
  "privacy review", or any similar request to audit markdown content for private details.
  The skill finds PII across all blog posts, presents each finding with context, suggests
  anonymized replacements using the approved fake persona, and lets the user decide what to change.
---

# Privacy Audit

You are auditing the user's public Jekyll blog (`_posts/`) to find personally identifiable
information (PII) that could trace back to the real author's offline identity.

## Approved fake persona for replacements

When suggesting replacements, substitute from this table of intentionally fictional values:

| Field | Approved replacement |
|---|---|
| Name (fake) | 翠花 (Cuihua) |
| Birth year | 1993 |
| Location | SLU (South Lake Union), Seattle, WA |
| Annual income | $300,000 |
| Home purchase price | $1,350,000 |
| Down payment | $270,000 (20%) |
| Loan amount | $1,080,000 |
| Mortgage rate | 7.0% |
| Monthly payment | ~$7,194 |
| Lump-sum savings | $350,000 |
| Personal email | `user@example.com` |
| CI/CD git email | `41898282+github-actions[bot]@users.noreply.github.com` |
| AWS account ID | `12345678` |
| Employer | `[a tech company]` |

Any value already matching this table is an approved replacement — do not flag it as PII.

## What counts as PII worth flagging

The guiding question is: *would this information help someone identify the author's real-world
identity beyond what's already visible by browsing the site?*

Work through the context before flagging. Information that is visible on the blog's own
About page, post headers, or public GitHub profile is already intentionally disclosed —
it doesn't need to be redacted. When in doubt about whether something is already public,
note it as ambiguous so the user can decide.

**🔴 High priority — flag every time:**
- Employer or company name in a personal context ("I work at X", "my team at Z")
- Corporate email addresses in code, config files, or git settings
- Internal company Git domains (e.g., `github.[company].com`)
- Salary, hourly rate, bonus, or compensation in a personal (non-tutorial) context
- Physical home address, apartment number, zip/postal code
- Real property value, rent amount, or mortgage payment (not tutorial/fictional data)
- Personal phone number
- Full legal name that extends beyond what's publicly used on the blog
- Government ID numbers (SSN, passport, driver's license)
- Personal banking or financial account details
- AWS account IDs / ARNs containing real account numbers (not the approved placeholder)
- Internal LMS or training platform URLs that reveal employer identity

**🟡 Medium priority — flag with context:**
- Specific neighborhood, building, or street within a city
- Real names of colleagues, managers, or family members
- `author:` front matter with a name more specific than what's publicly used
- Zip codes embedded in scraper scripts or project files that reveal home area
- Local filesystem paths that expose the author's OS username (e.g., `/Users/[username]/`)
- Specific dates combined with locations that reveal routine or schedule

**Skip these (common false positives):**
- Company names appearing only as examples in security lab exercises or CTF writeups
- Lab/CTF IP addresses, passwords, and usernames (exercise environments, not real)
- Email addresses clearly used as fictional examples in security tutorials
- Any data explicitly labeled as fictional, example, placeholder, or redacted
- Values matching the approved fake persona table above

## Execution steps

### Step 1: Pattern scan

Use `Grep` to find candidate lines across all `_posts/**/*.md` files. Run these as
separate Grep calls so results stay readable:

- Salary/money in personal context: `I (earn|make|get paid|salary)`, `\$[0-9]`, `per (hour|year|month)`
- Employer: `(work|worked) (at|for|with)`, `my (company|employer|team|boss|manager|job at)`
- Corporate email: `@[a-z]+\.(com|net|org)` in git config, setup.py, or workflow files
- Internal git domains: `github\.[a-z]+\.com`, `gitlab\.[a-z]+\.com`
- Address: `\b\d{1,5} [A-Z][a-z]+ (St|Ave|Rd|Blvd|Dr|Ln|Ct|Way|Pl)\b`, `Apt \d`, `zip`, `postal code`
- Property: `(my|our) (house|apartment|condo|rent|mortgage|property)`, `worth \$`, `valued at`
- Phone: `\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}`
- AWS ARN / account: `arn:aws:`, `\b[0-9]{12}\b` (12-digit numbers)
- Full legal name: surnames or middle names that go beyond the author's publicly-used name
- Personal finance: `routing number`, `account number`, `my bank`, `my card`
- Zip codes in project scripts: `\b9[0-9]{4}\b` (Pacific Northwest zips)
- Local paths: `/Users/[a-z]+/` or `/home/[a-z]+/`

### Step 2: Contextual review

For every grep match, read at least 3 lines before/after to judge whether it is:
- **Real PII** → include in report
- **False positive** (lab content, fictional, already the approved placeholder) → discard silently
- **Ambiguous** → include with a note so the user can decide

### Step 3: Present the report

Format findings as an interactive checklist. If there are no findings, say so clearly —
a clean bill of health is good news.

```
## 🔍 Privacy Audit Report
Scanned: [N] files | Flagged: [N] items | Clean: [N] files

────────────────────────────────────────────
### 🔴 HIGH PRIORITY ([count])

[1] `_posts/path/to/file.md` — line 42
    Context: "...I currently work at Acme Security as a lead analyst..."
    Issue: Employer name in personal context
    Suggested: "...I currently work at [a tech company] as a lead analyst..."

────────────────────────────────────────────
### 🟡 MEDIUM PRIORITY ([count])

[2] `_posts/path/to/file.md` — line 88
    Context: "...living near [specific neighborhood]..."
    Issue: Specific neighborhood — ambiguous
    Suggested: "...living in the SLU area..."

────────────────────────────────────────────
### ✅ No issues in: [comma-separated list of clean post directories]
```

After the report, ask:
> "For each item, tell me:
> - **K** = Keep as-is (intentional or comfortable with it)
> - **R** = Apply suggested replacement
> - **E [your text]** = Use your own custom replacement
> - **S** = Skip for now
>
> Example: `1R, 2K, 3E [I live on the East Coast]`"

### Step 4: Apply changes

When the user responds, apply each accepted change using `Edit` to make the minimum-diff
replacement. Confirm each change and show the before/after line.

## Tone

Be matter-of-fact and helpful, not alarmist. Most cybersecurity blog posts will be clean.
When something is flagged, explain *why* it's a concern (what could someone do with it?)
in one sentence so the user understands the risk, not just the rule.
