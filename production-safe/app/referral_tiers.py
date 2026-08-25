TIERS = [
    {"name": "Bronze", "min_referrals": 5, "speed_bonus_pct": 5.0, "color": "#CD7F32"},
    {"name": "Silver", "min_referrals": 15, "speed_bonus_pct": 10.0, "color": "#B0B8C1"},
    {"name": "Gold", "min_referrals": 25, "speed_bonus_pct": 20.0, "color": "#FFD54F"},
    {"name": "Platinum", "min_referrals": 50, "speed_bonus_pct": 35.0, "color": "#7FDBFF"},
    {"name": "God Tier", "min_referrals": 100, "speed_bonus_pct": 50.0, "color": "#B388FF"},
]


def tier_for_count(direct_referrals: int) -> dict | None:
    """Returns the highest tier unlocked by this many direct (level-1) referrals, or None."""
    unlocked = None
    for tier in TIERS:
        if direct_referrals >= tier["min_referrals"]:
            unlocked = tier
    return unlocked


def speed_bonus_pct(direct_referrals: int) -> float:
    tier = tier_for_count(direct_referrals)
    return tier["speed_bonus_pct"] if tier else 0.0


def next_tier(direct_referrals: int) -> dict | None:
    for tier in TIERS:
        if direct_referrals < tier["min_referrals"]:
            return tier
    return None
