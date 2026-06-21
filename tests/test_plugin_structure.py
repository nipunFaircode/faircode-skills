import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _read_frontmatter_name(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    assert m, f"{skill_md} missing YAML frontmatter"
    block = m.group(1)
    nm = re.search(r"^name:\s*(.+?)\s*$", block, re.MULTILINE)
    assert nm, f"{skill_md} frontmatter missing name:"
    return nm.group(1).strip()


def test_plugin_json_valid():
    data = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert data["name"] == "faircode"
    assert re.match(r"^\d+\.\d+\.\d+$", data["version"])
    assert data["skills"] == "skills"


def test_marketplace_lists_existing_skills():
    mkt = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    plugin = mkt["plugins"][0]
    assert plugin["name"] == "faircode"
    for rel in plugin["skills"]:
        skill_dir = ROOT / rel
        assert skill_dir.is_dir(), f"listed skill missing: {rel}"
        name = _read_frontmatter_name(skill_dir / "SKILL.md")
        assert name == skill_dir.name, f"name {name} != folder {skill_dir.name}"


def test_no_hardcoded_token():
    # crude secret scan across tracked python and yaml
    pattern = re.compile(r"token\s+[A-Za-z0-9]{8,}:[A-Za-z0-9]{8,}")
    for path in ROOT.rglob("*"):
        if path.suffix in {".py", ".yml", ".yaml", ".md"} and path.is_file():
            if "test_plugin_structure" in path.name:
                continue
            if ".venv" in path.parts:
                continue
            assert not pattern.search(
                path.read_text(encoding="utf-8", errors="ignore")
            ), f"possible token in {path}"
