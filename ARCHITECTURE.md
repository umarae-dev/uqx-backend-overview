# UQX Backend — Account Services Architecture

## Current system boundary

```text
UQX Native Android Wallet
        │
        ├── on-device BIP39/EVM wallet generation
        ├── Android Keystore-backed encrypted storage
        ├── device authentication
        └── supported read-only BNB Smart Chain state

Separate HTTPS account-services boundary
        │
        ▼
FastAPI Application
        │
        ├── Authentication / Sessions
        ├── Account Recovery / 2FA
        ├── Notifications
        ├── Profile / Settings
        └── legacy compatibility services
                ├── historical account ledger
                ├── historical referral accounting
                ├── historical leaderboard/history routes
                └── historical mining/reward API contracts
        │
        ▼
PostgreSQL
```

The current UQX product is the self-custody Web3 wallet. The backend is not the custody authority for the native wallet recovery phrase or private key.

## Wallet trust boundary

```text
Android device
  ├── BIP39 recovery phrase
  ├── EVM private key
  ├── BNB Smart Chain address
  └── encrypted local wallet store
            │
            ▼
      supported chain reads
```

A backend login token is not a wallet private key. Losing or revoking an application session should not be described as equivalent to losing or revoking the self-custody wallet.

## Account-service invariants

### Authentication

Protected routes resolve bearer/session state server-side, verify expiry and user status, and apply the production session controls before returning authenticated account state.

### Two-factor authentication

TOTP login uses bounded pre-authentication state. Recovery/backup credentials should be stored and consumed according to the production security implementation rather than exposed as plaintext account secrets.

### Notifications / settings

Notification, profile and settings data are account-level services. They can be provided without the backend taking possession of the native wallet mnemonic/private key.

## Legacy compatibility services

Older production versions contain account-ledger, referral, leaderboard and mining/reward routes. Where still operational, their invariants remain important for data integrity, but they are not current product features.

Examples of historical invariants include:

- account-ledger mutations happen transactionally;
- referral/accounting records preserve source linkage;
- historical session finalization cannot be repeated arbitrarily;
- internal account transfers must not be represented as BNB Smart Chain wallet transfers.

These routes should be retired through an explicit API/client migration after dependency checks, not cosmetically renamed in a branding change.

## Account and chain separation

```text
Legacy/internal account state             Self-custody BNB wallet
  ├── server-side records                   ├── BIP39 mnemonic
  ├── compatibility balances               ├── private key
  └── historical referral/session data      ├── public BSC address
                                            └── on-chain token/contract state
```

The two systems must never be described as the same wallet or balance.

## Public documentation boundary

This public reference documents architecture, source provenance and trust boundaries. Production SQL schema, user records, credentials, anti-abuse thresholds and operational secrets remain private.
