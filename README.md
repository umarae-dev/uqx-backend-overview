# UQX Backend — Rewards, Referral & Account Ledger Infrastructure

> Production architecture plus selected production-safe backend source copied from the private FastAPI service.

UQX Backend is the server-side identity, rewards, referral and internal-ledger layer behind the native UQX Android application.

**Production stack:** Python · FastAPI · PostgreSQL / asyncpg  
**Private production repository:** `uqx-backend`  
**Public repository:** selected exact production modules + tests + architecture/security documentation  
**Client overview:** [`uqx-app-overview`](https://github.com/umarae-dev/uqx-app-overview)

## Reviewer start here

This repository is no longer documentation-only. Review:

- [`production-safe/app/security.py`](production-safe/app/security.py) — exact production bcrypt password hashing/verification module;
- [`production-safe/app/referral_tiers.py`](production-safe/app/referral_tiers.py) — exact production referral-tier calculation logic;
- [`SOURCE_MANIFEST.md`](SOURCE_MANIFEST.md) — exact private production paths/blob SHAs;
- [`tests/test_production_safe.py`](tests/test_production_safe.py) — executable tests for the published modules;
- [`ARCHITECTURE.md`](ARCHITECTURE.md) and [`SECURITY.md`](SECURITY.md) — system and security boundaries.

The full commercial backend remains private because it includes live database/service wiring, authentication/session internals, user data surfaces and abuse-control implementation that should not be exposed merely to make a public repository larger.

## System role

```text
UQX Native Android App
        │
        │ HTTPS + authenticated API
        ▼
UQX Backend
   │
   ├── Identity & Sessions
   ├── Reward Sessions
   ├── Referral Accounting
   ├── Internal UQX Ledger
   ├── P2P Transfers
   ├── Leaderboards / History
   ├── Notifications
   └── Security / 2FA

Separate trust boundary:

Android Self-Custody Wallet
        │
        └── BNB Smart Chain
```

The backend never needs the recovery phrase or private key of the native self-custody wallet in order to account for rewards or internal transfers.

## Reward-session accounting

The product's recurring 24-hour “mining” flow is an engagement/reward session, not proof-of-work mining by the phone.

Production invariants include:

- only one active reward session per account;
- expired sessions can be completed defensively by authenticated surfaces;
- completion is atomic so one session cannot be credited twice;
- reward/referral state is server-owned rather than trusted from the client.

## Device-abuse hardening

Recent production work hardened the mining-device boundary around a stable app-scoped device signal.

The public invariant is:

- normal login remains multi-device;
- mining identity can be associated with a stable app-scoped device signal;
- IP/User-Agent is not treated as physical-device identity because NAT/mobile networks can collide;
- deleting an account cannot be used as an immediate farming reset;
- legitimate shared/resold-device transfer can occur after the security cooldown;
- account identity is server user ID, not mutable email text.

The exact operational implementation and bypass-sensitive anti-abuse details remain private by design. The public repository documents the behavior without publishing a recipe for defeating it.

## Referral accounting

Referral rewards are tied to credited activity rather than just invite existence. The production service maintains direct/upstream referral relationships, linked reward records and tier state.

The exact public `referral_tiers.py` module currently defines the visible direct-referral tier progression and speed-bonus percentages used by the product. Because these are product-facing tier rules rather than hidden fraud-detection signatures, the module is safe to publish and test.

## Internal ledger and transfers

The backend maintains the in-app UQX reward/account balance separately from the Android self-custody BSC wallet.

Internal P2P transfer invariants include:

- server-side recipient resolution;
- no self-transfer;
- positive amount validation;
- locked sender balance during transfer evaluation;
- atomic debit/credit/transfer record;
- recipient notification after success.

This prevents two concurrent transfer attempts from spending the same pre-transfer account balance.

## Authentication and 2FA

Production features include:

- bcrypt password hashing;
- random bearer sessions with finite expiration;
- blocked/deleted account enforcement;
- active-session listing/revocation;
- login security notifications;
- disposable-email rejection;
- TOTP two-factor authentication;
- one-time backup codes stored as hashes;
- expiring pre-auth state and recovery flows.

The public `security.py` is the exact production bcrypt helper. Full login/session/2FA route code remains private because it is much more tightly coupled to live account and operational controls.

## Account layer vs blockchain wallet

| Capability | Backend account ledger | Android self-custody wallet |
|---|---|---|
| Reward-session credits | Yes | No |
| Referral rewards | Yes | No |
| Internal P2P send | Yes | Separate from chain transfer |
| Recovery phrase/private key | Never required | Device-only |
| Direct BSC token reads | No | Yes |
| Presale/vesting reads | No | Yes |

Canonical UQX contract source/deployments/transactions live in [`uqx-bnb-contracts-overview`](https://github.com/umarae-dev/uqx-bnb-contracts-overview), not in this backend repository.

## Public/private boundary

Public here:

- exact approved production-safe modules;
- source/blob provenance;
- executable unit tests;
- architecture/security model;
- CI and public-secret guard.

Kept private:

- production database URL/password;
- email/push/service credentials;
- bearer tokens/session data;
- user/customer records;
- complete auth/mining/wallet/2FA router implementation;
- operational anti-abuse thresholds/signatures;
- private runbooks and deployment configuration.

## Run the public subset

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/check_public_repo.py
python -m compileall -q production-safe tests scripts
pytest -q
```

No production credential or database connection is required.

## CI

GitHub Actions runs:

- install public test dependencies;
- public repository secret/file guard;
- Python compile check;
- tests for password hashing and referral-tier boundaries.

## Production lineage

The private FastAPI backend predates this public release. Public Git history represents the publication and maintenance history of the safe subset, not the complete production-development history.

See [`SOURCE_MANIFEST.md`](SOURCE_MANIFEST.md), [`ARCHITECTURE.md`](ARCHITECTURE.md) and [`SECURITY.md`](SECURITY.md).

## Status

The private production backend contains authentication, reward-session processing, two-level referral accounting, internal transfers, leaderboards/history, notifications, active-session management and TOTP 2FA. This repository now exposes a testable production-safe subset while keeping live credentials, user data and bypass-sensitive controls private.
