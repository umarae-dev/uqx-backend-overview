from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, relative_path: str):
    spec = spec_from_file_location(name, ROOT / relative_path)
    module = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_password_hash_round_trip():
    security = load("security", "production-safe/app/security.py")
    hashed = security.hash_password("correct horse battery staple")
    assert hashed != "correct horse battery staple"
    assert security.verify_password("correct horse battery staple", hashed)
    assert not security.verify_password("wrong password", hashed)


def test_referral_tier_boundaries():
    tiers = load("referral_tiers", "production-safe/app/referral_tiers.py")
    assert tiers.tier_for_count(0) is None
    assert tiers.tier_for_count(5)["name"] == "Bronze"
    assert tiers.tier_for_count(15)["name"] == "Silver"
    assert tiers.tier_for_count(100)["name"] == "God Tier"
    assert tiers.next_tier(15)["name"] == "Gold"
    assert tiers.speed_bonus_pct(50) == 35.0
