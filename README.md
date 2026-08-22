# UQX Backend — Rewards, Referral & Account Ledger Infrastructure

> **The server-side accounting and identity layer behind the UQX native Android ecosystem.**

UQX Backend is the private production API that powers UQX account authentication, recurring engagement-reward sessions, referral accounting, the internal UQX account ledger, user-to-user transfers, leaderboards, notifications, active sessions and two-factor authentication.

The backend is intentionally separate from the app's **self-custody BNB Smart Chain wallet**. Server-accounted rewards live in the UQX account layer; private keys for the on-device wallet are not generated or stored by this backend.

**Client overview:** [UQX Native App](https://github.com/umarae-dev/uqx-app-overview)  
**API stack:** Python · FastAPI · PostgreSQL / asyncpg

---

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

The backend can account for app rewards and internal transfers. It does **not** need the user's self-custody wallet recovery phrase or private key to do this work.

---

## Engagement reward sessions

UQX uses a recurring 24-hour participation/reward session that the mobile product calls "mining".

This is an **engagement-based reward mechanism**, not proof-of-work mining performed by the phone.

High-level lifecycle:

```text
Authenticated user
      │
      ▼
Start reward session
      │
      ├── reject duplicate active session
      ├── apply current reward policy
      └── record session
      │
      ▼
24-hour active window
      │
      ▼
Atomic completion guard
      │
      ├── credit user's UQX account ledger
      ├── record referral rewards where applicable
      └── create notification
```

### Defensive auto-completion

A completed 24-hour session does not rely on the user pressing a special "claim" button at exactly the right moment.

Authenticated surfaces can defensively check whether the user's latest active session has expired. If it has, the backend finalizes it before returning wallet/dashboard state.

This avoids the common failure mode where a finished reward remains invisible simply because the user closed the app before the timer ended.

### Double-processing protection

Session completion updates only a session that is still marked active. If another request has already finalized the same session, the second completion attempt does not credit it again.

This is a critical accounting invariant:

> **one completed reward session should produce one account credit.**

---

## Referral accounting

Referral rewards are derived from **credited activity**, not merely from the existence of an invite record.

The production system supports a two-level referral graph:

```text
User C completes rewarded activity
        │
        ├── Level 1 reward → direct referrer B
        │
        └── Level 2 reward → upstream referrer A (where applicable)
```

Each referral reward is stored as its own accounting record linked to:

- referrer;
- referred user;
- source reward session;
- referral level;
- credited amount;
- timestamp.

The referrer's account balance is then credited and a user notification is generated.

This produces a traceable relationship between the original activity and the resulting referral reward instead of maintaining only one opaque aggregate number.

---

## Referral tiers and activity boosts

The referral system also maintains direct-network counts and tier information used by the product to present rank/progress and engagement-speed bonuses.

The public architecture intentionally does not publish production anti-abuse thresholds or every operational tuning constant.

The important boundary is:

- network/tier state is derived server-side;
- the Android client displays the result;
- a modified client cannot grant itself a higher tier by editing local state.

---

## Internal UQX account ledger

The backend maintains an **internal account balance** for rewards and in-app transfers.

This is distinct from the user's self-custody BSC address.

Sources that can appear in account history include:

- completed reward sessions;
- referral rewards;
- internal sends;
- internal receives;
- withdrawal records where applicable.

The API merges these sources into a chronological transaction view for the mobile client.

---

## Atomic user-to-user transfers

Internal UQX sends are processed inside a database transaction.

High-level flow:

```text
Sender chooses recipient UID
        │
        ▼
Resolve recipient server-side
        │
        ├── reject missing recipient
        ├── reject self-transfer
        └── validate positive amount
        │
        ▼
Lock sender balance row
        │
        ├── verify available balance
        ├── debit sender
        ├── credit receiver
        └── record transfer
        │
        ▼
Commit transaction
        │
        ▼
Notify recipient
```

The sender balance is locked while the transfer is evaluated, preventing two simultaneous requests from both spending the same pre-transfer balance.

---

## Account ledger vs. blockchain wallet

| Capability | Backend account ledger | Android self-custody wallet |
|---|---|---|
| Reward-session credits | Yes | No |
| Referral rewards | Yes | No |
| Internal P2P send | Yes | Separate from chain transfer |
| Recovery phrase | Never required | Device-only |
| Private key | Never required | Device-only |
| BNB address | Optional account metadata | Core wallet identity |
| Direct BSC token reads | No | Yes |
| Presale/vesting chain reads | No | Yes |

This separation prevents the word "wallet" from hiding two very different trust models.

---

## External withdrawal status

The current production backend keeps external on-chain withdrawal from the **internal reward ledger** disabled until the product's external-liquidity/DEX flow is ready for that capability.

Users can still move account-layer UQX between UQX users through the internal P2P ledger.

This is intentionally documented rather than presenting a disabled route as a live blockchain-withdrawal product.

---

## Authentication

The production backend supports account authentication with server-issued bearer sessions.

Current security/account behavior includes:

- bcrypt password hashing;
- cryptographically random session tokens;
- finite session expiration;
- blocked/deleted-account enforcement;
- device/session metadata;
- active-session listing;
- remote revocation of another session;
- new-login security notifications;
- disposable-email rejection during native registration;
- referral attribution during account creation.

Authentication and reward authorization are enforced by the backend rather than by client-side visibility rules.

---

## Two-factor authentication

UQX supports TOTP-based two-factor authentication.

The flow includes:

- authenticator-app setup;
- TOTP verification before enabling 2FA;
- one-time backup codes;
- hashed storage of backup codes;
- 2FA-gated login sessions;
- expiring pre-authentication state;
- email-based recovery for a user who has already passed the password step;
- security notification when a verified login creates a new session.

Backup codes are shown to the user at setup and stored as hashes rather than recoverable plaintext copies.

See [`SECURITY.md`](SECURITY.md) for the public security boundary and current hardening priorities.

---

## Active sessions

Authenticated users can inspect their active login sessions and revoke sessions that are no longer trusted.

The API identifies the current session separately so the product can require normal logout for the device currently being used while allowing remote revocation of other devices.

---

## Leaderboard & mining history

The backend provides server-derived weekly and monthly reward leaderboards.

Ranking comes from completed reward-session data rather than a client-submitted score.

The current user's own position can still be returned even when they fall outside the top result set.

Users can also retrieve paginated reward-session history including earned amount, status and timing information.

---

## Notifications

Reward, referral, transfer and security events can create user-facing notifications.

Examples include:

- reward session started;
- reward credited;
- referral bonus credited;
- UQX received from another user;
- new account login.

The native app also integrates push-notification infrastructure for timely delivery.

---

## Server-side trust model

```text
Untrusted client input
        │
        ▼
FastAPI validation + authenticated user context
        │
        ▼
Server-owned rules
        │
        ├── session state
        ├── balance state
        ├── referral graph
        ├── tier state
        └── authorization
        │
        ▼
PostgreSQL transaction / durable record
```

The mobile application is not treated as the source of truth for balances, completed rewards, referral earnings or account authorization.

---

## Abuse-resistance philosophy

A rewards application must assume that some clients will be modified, automated or repeatedly reinstalled.

The production system therefore includes server-side controls around areas such as:

- duplicate active reward sessions;
- account/device association;
- referral uniqueness;
- authenticated ownership;
- balance locking during transfers;
- blocked/deleted accounts;
- disposable-email registration;
- session expiration/revocation.

Exact operational thresholds and detection details are intentionally not published here because exposing them can make abuse easier.

These controls reduce casual and repeated abuse but are not presented as perfect Sybil resistance. Stronger identity/reputation/device-attestation controls remain an ongoing security area.

---

## Technology

- Python
- FastAPI
- PostgreSQL
- asyncpg
- Pydantic
- bcrypt
- PyOTP / TOTP
- Docker
- email / push notification services

The API exposes a health endpoint and uses an application lifespan to initialize and close the database connection pool cleanly.

---

## Public vs. private repository boundary

This repository is a **public product, accounting and security architecture overview**. The production API source remains private.

### Public here

- reward-session lifecycle;
- referral-accounting model;
- account-vs-self-custody distinction;
- internal transfer invariants;
- authentication/session concepts;
- 2FA architecture;
- leaderboard model;
- security philosophy.

### Kept private

- production source code;
- database credentials;
- email/push credentials;
- exact anti-abuse thresholds and signatures;
- internal operational configuration;
- private recovery/authentication internals not required for review;
- user data;
- production runbooks.

**Never commit production database credentials, bearer tokens, email credentials, API secrets, private keys, seed phrases or user-private information to this repository.**

---

## BNB Chain relationship

The backend is the **off-chain community/accounting layer** of UQX.

BNB Smart Chain remains the on-chain layer for the BEP-20 token, presale/vesting contracts and the native Android self-custody wallet.

```text
Community activity / referrals
            │
            ▼
       UQX Backend
            │
            ▼
    internal reward ledger

            ║ trust boundary

    Android self-custody wallet
            │
            ▼
      BNB Smart Chain
            │
            ├── UQX token
            └── presale / vesting state
```

This hybrid architecture lets the consumer product run high-frequency engagement/accounting workflows without pretending every app interaction is itself a blockchain transaction.

---

## Status

**Active production development.**

The private backend currently includes authentication, reward-session processing, two-level referral accounting, internal UQX transfers, leaderboards/history, notifications, active-session management and TOTP two-factor authentication.

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the system map and [`SECURITY.md`](SECURITY.md) for the public security posture.
