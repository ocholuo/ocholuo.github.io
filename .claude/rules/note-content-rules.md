# Note content rules (PDF and exam-source conversions)

Applies whenever a note under `_posts/` is written or converted from a source document, in particular the large `draft.pdf` compendium of exam and textbook material.

## Fidelity: original wording is kept

- The notes prepare for exams that can ask for the exact words of the source. Source text (textbook, RFC, glossary, the author's own annotations) is kept word for word. Never replace it with a paraphrase.
- Formatting may be improved (headings, lists, code blocks, tables). The words are not changed. Suspected typos in the source are not corrected in place: list them in a "Suspected typos" line after the block.
- A summary in the writer's own words is an additional block that helps readability. It sits after the original text and is clearly labeled. It never stands in for the original.

## Source flag: every block says where it came from

Decision: three layers together (tags, section labels, generated review index).

- Content on the same subject from different sources (for example Security+ textbook and CISSP notes) is gathered into one topic note, with one section per source.
- **A. Tags.** Front matter `tags` carry one `src-<slug>` tag per source in the note, for example `src-security-plus`, `src-cissp`. The slug is lowercase, hyphenated, without `+` (so the tag URL stays valid). The Tags page then lists every note from a source.
- **B. Section label.** Each source section starts with a heading of the form `### [<Source>] <chapter or section>, p<pdf-page> - Original text`, for example `### [Security+] Ch10, p412 - Original text`. The page is the PDF page number, so it can be traced back. The own-words block follows as `**Summary:**`.
- **C. Review index.** One generated page per source in `certification/`, listing every note and section from that source in source order, so one book can be reviewed front to back. It is produced by a script and regenerated after notes change, never edited by hand.
- A new source gets a slug and a label name added to this list: `security-plus` / `[Security+]`, `cissp` / `[CISSP]`. Confirm any new source name with the user first.

## Images

- Images keep original quality. Extract the embedded image stream from the PDF; do not re-render or recompress unless a file is too large and the user approves.
- The PDF repeats one 160x160 bullet icon thousands of times, plus about 290 tiny graphics (under 100 px). Skip decorative bullets and tiny graphics. Real pictures: about 1,056 unique, about 173 MB as stored in the PDF.
- Pages whose graphics are vector drawings have no embedded image. List them and render them as a page image only with the user's approval.

- Images live under `assets/img/post/`. Existing files stay where they are (flat). New files from the PDF go one level down, in a folder named after the note's top-level `_posts/` folder in lowercase, for example `assets/img/post/13crypt/`.
- File name: `<source>-<topic>-<detail>-p<pdf-page>.<ext>`. The page number traces the image back to the PDF.
- Count the images and total size before copying anything into the repo, and report both to the user.

## Privacy: alert before every push

- Before any push that adds converted content, scan the text and look at the images for personal information (names, emails, phone numbers, IDs, account names, screenshots of private data).
- If anything is found, or anything is uncertain, stop and tell the user before pushing. Third-party contact details (for example an author email in a source) count as a finding.

## Duplicates: report, never delete

- When the same content appears more than once, or overlaps an existing note, do not delete or merge it silently.
- Produce a list of the duplicate candidates with their locations and wait for the user to decide what to delete.
- Until the user decides, keep both copies.
