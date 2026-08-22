# Desk-Mate — Vault

Obsidian-Vault im Repo. Alles, was nicht Code ist: Tagesblätter mit Arbeitszeit, Entscheidungen, Hardware-Notizen, Bestellungen.

## Bereiche
- [[Log/2026-08-22]] — Tagesblätter (`Log/YYYY-MM-DD.md`), Start/Ende schreiben die Session-Hooks
- [[Entscheidungen/2026-08-22-Grilling]] — alle Design-Entscheidungen mit Begründung
- [[Hardware/Pin-Map]] · [[Hardware/Strombudget]]
- [[Firmware/Module]]
- [[Apps/Claude-Hooks]]
- [[Bestellungen/README]] — Vorlage; je Bestellung eine Notiz (Sponsoring-Material)

## Außerhalb des Vaults
- Spec: [docs/superpowers/specs/2026-08-22-desk-mate-design.md](../docs/superpowers/specs/2026-08-22-desk-mate-design.md)
- Plan Phase 0–2: [docs/superpowers/plans/2026-08-22-phase-0-2-infra-bauteile-kicad.md](../docs/superpowers/plans/2026-08-22-phase-0-2-infra-bauteile-kicad.md)
- Relikt: [docs/relic/2026-08-22-original-prompt.md](../docs/relic/2026-08-22-original-prompt.md)
- Arbeitsregeln: [CLAUDE.md](../CLAUDE.md)

## Arbeitszeit gesamt
Summe aller `dauer_min` in `Log/` — Dataview-Query, sobald das Plugin installiert ist:
```
TABLE dauer_min FROM "Log" SORT file.name DESC
```
