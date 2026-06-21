from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_references_present_and_nonempty():
    for fn in ["frappe-methods.md", "git-conventions.md",
               "definition-of-done.md", "severity-levels.md",
               "erp-coverage-map.md"]:
        p = ROOT / "shared" / "references" / fn
        assert p.is_file(), f"missing {fn}"
        assert len(p.read_text().strip()) > 200, f"{fn} too thin"


def test_coverage_map_has_core_modules():
    text = (ROOT / "shared" / "references" / "erp-coverage-map.md").read_text().lower()
    for module in ["selling", "buying", "stock", "manufacturing", "accounts",
                   "payroll", "permissions", "data migration"]:
        assert module in text, f"coverage map missing {module}"
