# Logging: Session Logs and Reviews

Adapted (slimmed) from claude-code-my-workflow. This repo is small, so the
trigger is light — but design decisions about theme layout are easy to lose,
so capture them.

---

## 1. Session Logging

**Location:** `quality_reports/session_logs/YYYY-MM-DD_description.md`
**Template:** `templates/session-log.md`

### Triggers

**Incremental logging.** Append 1–3 lines whenever a layout/design decision is
made, a spacing problem is solved, the user corrects something, or the approach
changes. Do not batch.

**Hard-cap reminder (enforced by the Stop hook).** `log-reminder.py` fires if
**10 responses** pass without a session-log edit. When it fires, append progress
to the most recent session-log file before stopping. It is a safety net for the
incremental rule — hitting the hook means the incremental rule was already missed.

**End-of-session.** When wrapping up: high-level summary, what was changed in
which `.sty`, open questions, and whether the preview PDFs were regenerated.

Durable, reusable facts (not session narrative) belong in `MEMORY.md` as
`[LEARN:category]` entries, not only in the session log.

---

## 2. Review and Analysis Reports

**Location:** `quality_reports/reviews/YYYY-MM-DD_description.md`

Any review or analysis output longer than ~20 lines must be saved as a markdown
file, not just printed to the conversation. This includes the
`beamer-tikz-reviewer` agent's reports and any layout/consistency audit.

### Rules

1. **Save to disk first**, then give a concise summary in the conversation.
2. **File naming:** `quality_reports/reviews/YYYY-MM-DD_short-description.md`.
3. **Use markdown** — headers, tables, bullets for scanability.
4. **Include severity** (CRITICAL / MAJOR / MINOR or High / Medium / Low).
5. **Reference specific files and line numbers / coordinates** where issues are found.
