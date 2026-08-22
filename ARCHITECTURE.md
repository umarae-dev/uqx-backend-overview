# UQX Backend — Architecture

## System map

```text
Native Android Client
        │
        │ HTTPS
        ▼
FastAPI Application
        │
        ├── Authentication / Sessions
        ├── Reward Sessions
        ├── Referral Accounting
        ├── Internal Wallet Ledger
        ├── P2P Transfers
        ├── Leaderboards / History
        ├── Notifications
        ├── Settings
        └── Two-Factor Authentication
        │
        ▼
PostgreSQL
```

The production backend is an off-chain account/reward system. The Android app's self-custody BNB wallet is a separate trust boundary and does not require this backend to hold private keys.

## Core invariants

### Reward session

A reward session may be finalized only while its database state is active. The finalization path updates the session, credits the account ledger, applies eligible referral credits and creates notifications.

### Internal transfer

An internal send is processed in one database transaction. The sender balance row is locked before available balance is checked, then sender debit, receiver credit and the transfer record are committed together.

### Referral reward

Referral credits are attached to the source reward session and stored as separate records instead of being represented only as a mutable aggregate counter.

### Authentication

Protected routes resolve the bearer token server-side, verify expiration and user status, and update session activity before returning the authenticated user identity.

### 2FA

TOTP login uses a short-lived pre-authentication state. Backup codes are stored as hashes and marked used after successful consumption.

## Account and chain separation

```text
Internal account ledger
  ├── reward credits
  ├── referral credits
  └── UQX user-to-user sends

Self-custody BNB wallet
  ├── BIP39 mnemonic
  ├── private key
  ├── BSC address
  └── on-chain token / contract state
```

These two systems should not be described as the same wallet.

## Public documentation boundary

This file intentionally describes architecture and invariants rather than production SQL schema, credentials, anti-abuse thresholds or operational secrets.