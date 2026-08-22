# Security Policy — UQX Backend Overview

This repository documents the public architecture of the UQX production backend. It is **not** the production source repository and must never be used to publish live credentials, private operational data or security-sensitive abuse controls.

## Current public security posture

The reviewed production backend currently includes controls such as:

- bcrypt password hashing;
- cryptographically random bearer-session tokens;
- session expiration and remote session revocation;
- blocked/deleted-account enforcement;
- TOTP two-factor authentication;
- hashed one-time backup codes;
- short-lived 2FA pre-authentication state;
- password + email ownership recovery path for 2FA lockout;
- server-side balance validation;
- row locking and database transactions for internal transfers;
- duplicate active reward-session prevention;
- defensive one-time reward finalization;
- referral records tied to actual credited activity;
- disposable-email rejection during native registration;
- device/account abuse checks;
- security notifications for new logins.

## Never publish here

Do not commit:

- production database URLs or passwords;
- bearer/session tokens;
- email or Firebase credentials;
- OAuth secrets;
- private API keys;
- raw recovery/authentication secrets;
- user PII;
- exact anti-abuse signatures or thresholds when publishing them would make bypass easier;
- private infrastructure addresses or runbooks;
- blockchain private keys or seed phrases.

## Important trust boundary

The UQX backend's internal account ledger is **not** the Android app's self-custody BNB wallet.

The backend does not need the user's wallet mnemonic or private key to credit reward sessions, referral rewards or internal P2P transfers.

## Current hardening priorities

The public documentation does not claim the system is fully audited. Areas that deserve continued review include:

- token-at-rest protection and session-token hashing strategy;
- rate limiting and credential-stuffing protections;
- stronger Sybil/device-abuse resistance;
- recovery-code storage and replay protections;
- explicit CORS restriction to production client origins where appropriate;
- database constraints supporting accounting invariants;
- structured security/audit logging;
- automated concurrency and double-credit tests;
- independent security review before larger-scale token distribution or withdrawals.

## Reporting

Please report suspected vulnerabilities privately to the Zynost/UQX team rather than posting exploit details in a public issue. Include the affected component, reproduction steps, impact and any suggested remediation.