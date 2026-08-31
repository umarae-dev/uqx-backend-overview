# UQX Backend — Account Services Compatibility Layer

> **Production-derived FastAPI account/security modules retained behind the current UQX self-custody wallet product.**

UQX is currently positioned as a **self-custody Web3 wallet**. The native Android wallet owns the wallet trust boundary: recovery phrase and private key generation/storage happen on the device, while supported BNB Smart Chain state is read against the public wallet address.

This repository documents a separate server-side account-services layer from earlier/current application infrastructure. It contains authentication, session, notification and legacy account-ledger/referral components that may remain operational for backwards compatibility while the wallet-first product surface is migrated.

**Production stack:** Python · FastAPI · PostgreSQL / asyncpg  
**Private production repository:** `uqx-backend`  
**Public repository:** selected production-safe modules + tests + architecture/security documentation  
**Current wallet overview:** [`uqx-app-overview`](https://github.com/umarae-dev/uqx-app-overview)

## Product boundary

```text
Current UQX Product
       │
       ▼
Self-Custody Android Wallet
       │
       ├── device-owned BIP39 recovery phrase
       ├── device-owned EVM keypair
       ├── Android Keystore-backed encrypted storage
       └── supported BNB Smart Chain reads

Separate account-services boundary
       │
       ├── authentication / sessions
       ├── notifications
       ├── profile / settings
       ├── 2FA
       └── legacy account-ledger / referral APIs retained where compatibility requires
```

The account backend does **not** need the self-custody wallet mnemonic/private key to provide account services or to identify the wallet's public address where product workflows require it.

## Legacy terminology

Older production code contains routes and models named around:

- mining;
- reward sessions;
- referral rewards;
- internal reward balances;
- leaderboards.

Those names document implementation history and compatibility surfaces. They are **not current UQX product branding** and should not be used in app-store copy, website positioning, investor material or the main Android navigation.

Removing a deployed API simply to improve naming could break older clients. The safe migration path is:

1. remove legacy surfaces from the current client/product experience;
2. mark server routes/models as compatibility/legacy where practical;
3. confirm operational/client dependencies;
4. retire unused endpoints in a dedicated API migration rather than a branding-only change.

## Reviewer start here

The public safe subset includes:

- [`production-safe/app/security.py`](production-safe/app/security.py) — production-derived bcrypt password hashing/verification;
- [`production-safe/app/referral_tiers.py`](production-safe/app/referral_tiers.py) — historical/referral-tier logic retained for source provenance;
- [`SOURCE_MANIFEST.md`](SOURCE_MANIFEST.md) — private production path/blob lineage;
- [`tests/test_production_safe.py`](tests/test_production_safe.py) — executable tests for published modules;
- [`ARCHITECTURE.md`](ARCHITECTURE.md) and [`SECURITY.md`](SECURITY.md) — system/security boundaries.

Publication of a legacy-safe module does not mean that feature defines the current product.

## Account security services

Production account infrastructure includes patterns such as:

- bcrypt password hashing;
- finite bearer sessions;
- blocked/deleted account enforcement;
- active-session listing/revocation;
- login security notifications;
- disposable-email rejection;
- TOTP two-factor authentication;
- hashed one-time backup codes;
- recovery/pre-auth state.

Full production auth/session/2FA routing remains private because it is coupled to live accounts and operational controls.

## Wallet separation

| Capability | Account backend | Self-custody Android wallet |
|---|---|---|
| Login/session state | Yes | No |
| 2FA/account controls | Yes | No |
| Notification/profile services | Yes | No |
| Recovery phrase/private key | Never required | Device-owned |
| BIP39/EVM wallet generation | No | Yes |
| Direct supported BSC state reads | No | Yes |
| Presale/vesting position reads | No | Yes |

Canonical token/vesting/presale contract source and deployment evidence live in [`uqx-bnb-contracts-overview`](https://github.com/umarae-dev/uqx-bnb-contracts-overview).

## Historical ledger/referral services

The private backend still contains older internal-accounting and referral logic. These systems are documented here only as compatibility/provenance context.

They must not be confused with:

- the user's BNB Smart Chain wallet balance;
- self-custody;
- on-chain transaction signing;
- current UQX wallet branding.

## Public/private boundary

Public here:

- approved production-safe modules;
- source/blob provenance;
- executable unit tests;
- architecture/security documentation;
- CI and public-secret guards.

Kept private:

- production database credentials;
- email/push/service credentials;
- bearer/session data;
- user records;
- complete auth/legacy-ledger/2FA router implementations;
- bypass-sensitive abuse controls;
- operational runbooks/deployment configuration.

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

## Production lineage

The private backend predates this public extraction. Public commit history represents the publication/maintenance timeline rather than the complete private development history.

## Current status

The current UQX brand is the self-custody Web3 wallet. This backend should be understood as an account-services and compatibility layer while legacy product surfaces are retired safely.
