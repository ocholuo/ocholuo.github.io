# Note placement and folder-map maintenance

Applies whenever a note is created, moved or merged under `_posts/`, and whenever a folder under `_posts/` is added, renamed or removed.

## Where does a new note go?

The folder map is `_tabs/contents.md`. Read it first.

1. Search `_posts/` for an existing note on the topic. If one exists, merge into it or expand a section. Do not create a duplicate.
2. Pick the most specific existing second-level folder from the map.
3. If no second-level folder fits, use the matching top-level folder and put the note at its root.
4. Create a new folder only when none fits. Name it in the same style as its siblings, then update `_tabs/contents.md` in the same commit.

## Naming and front matter

- File name: `YYYY-MM-DD-topic-slug.md`. Posts without a date in the name are not published.
- `categories` is `[TopFolder, SubCategory]` and must use the exact top-level folder name first, for example `[10CyberAttack, Vulnerability]`. Older notes contain typos and sub-folder-first values (for example `10SecConcept`, `13Cryptography`, `01AWS` as the first entry). Do not copy them.
- Images go in `assets/img/post/` and are linked as `./assets/img/post/<descriptive-name>.ext`.

## Folder choice rules

- Exam material goes in `certification/` and stays grouped by exam.
- Hands-on write-ups go in `Lab/`.
- Concept explanations go in the topic folder, not in `Lab/`.

## Maintenance

- Update `_tabs/contents.md` whenever a folder is added, renamed or removed, and when a folder's scope changes.
- Keep one line per folder. Do not list individual notes there; the Archives and Tags pages do that.
- Keep the approximate note counts roughly current when a folder grows or shrinks by a large amount.
- Keep the page's color scheme: group, top-level folder and second-level folder each use their own `<font color=...>`.
