# Claude-Code-Hooks — verifizierte Fakten (2026-08-22)

Quelle: https://code.claude.com/docs/en/hooks.md (gelesen 2026-08-22). Bei Abweichungen im Bau: hier aktualisieren und Spec §5 nachziehen.

## Ereignisse, die Desk-Mate nutzt
| Ereignis | Zweck | Ampel |
|---|---|---|
| `UserPromptSubmit` | Claude arbeitet | gelb |
| `PermissionRequest` | Claude würde fragen → Hook wartet auf Taste | rot |
| `Notification` (`permission_prompt`, `idle_prompt`, `agent_needs_input`) | Claude wartet auf dich | rot blinkend |
| `PreToolUse` Matcher `AskUserQuestion` | Frage an dich (ob `tool_input` die Frage trägt: **testen**) | rot |
| `Stop` | fertig | grün |
| `SessionStart` / `SessionEnd` | Zeiterfassung, commit/push (projektlokal) | — |

Weitere existierende Ereignisse (nicht genutzt): Setup, UserPromptExpansion, PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, MessageDisplay, SubagentStart/Stop, TaskCreated/Completed, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, DirectoryAdded, FileChanged, WorktreeCreate/Remove, PreCompact, PostCompact, Elicitation, ElicitationResult.

## Antwort des Freigabe-Hooks (`PermissionRequest`)
```json
{ "hookSpecificOutput": { "hookEventName": "PermissionRequest",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Desk-Mate: Taste Weiter" } }
```
Werte: `allow` · `deny` · `escalate` (= normaler Prompt). Exit 0 + JSON entscheidet; Exit 2 blockt immer.

## Stdin-JSON (alle Hooks)
`hook_event_name`, `session_id`, `cwd`, `transcript_path`, `permission_mode`; bei Notification zusätzlich `notification_type`. Umgebungsvariable `$CLAUDE_PROJECT_DIR` gesetzt. Kein `CLAUDE_SESSION_ID` — `session_id` aus stdin nehmen.

## Konfiguration
`~/.claude/settings.json` (global) bzw. `.claude/settings.json` (Projekt):
`hooks → <Ereignis> → [{ matcher, hooks: [{ type: "command", command, timeout }] }]`. `timeout` in Sekunden.

## Nicht abfangbar / offen
- Trust-Dialog beim Start: **kein Hook** (verifiziert) → Tastendruck-Fallback des Agents.
- Maximaler Hook-Timeout: nicht dokumentiert → mit 60 s testen, Ergebnis in CLAUDE.md „Bekannte Fallen“.
- SessionEnd ohne dokumentiertes `reason`-Feld; Git im SessionEnd-Hook hat keine Timeout-Garantie → unser Hook hat `timeout: 120` und bricht leise ab (Log in `vault/Log/push-fehler.log`).
