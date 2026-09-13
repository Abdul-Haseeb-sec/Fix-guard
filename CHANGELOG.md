# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] — 2026-09-13

### Added
- Core skill file with 8 verification rules (FR-1 through FR-8)
- Claude Code variant (`fix-guard.md`) with YAML frontmatter
- Cursor variant (`fix-guard.mdc`) with Cursor-specific formatting
- Generic prompt variant (`fix-guard-prompt.md`) for Antigravity, Windsurf, and other agents
- Verification Report Template for structured fix reporting
- Dead-code bypass example reproducing a real-world incident class
- README with origin story, before/after transcript, and per-agent install instructions
- MIT License
- Contributing guidelines and issue templates

### Origin
- All rules trace back to a real vibe-coding incident: a detection threshold bug where an AI agent reported "fixed" on dead code due to an argparse default bypass.
