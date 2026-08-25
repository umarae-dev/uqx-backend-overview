# Production Source Manifest

This manifest records private-production files reviewed and approved for public release.

Private source repository: `umarae-dev/uqx-backend` (private)

| Public file | Private production path | Private blob SHA | Publication status |
| --- | --- | --- | --- |
| `production-safe/app/security.py` | `app/security.py` | `4e151fb6d5b5fd4467588e0b6d3d1151c660434e` | Exact production source |
| `production-safe/app/referral_tiers.py` | `app/referral_tiers.py` | `f0417fdd367daab16ea0ea639c29e5b1d29256d0` | Exact production source |

## Reviewed but intentionally private

The production backend also contains authentication, mining/reward-session processing, wallet/account endpoints, settings, 2FA, notifications, leaderboards and session-management code.

Recent production hardening includes stable app-scoped device identity and cooldown/rebinding rules intended to reduce reward-farming abuse without device-locking normal login. The invariant is documented publicly, but exact abuse-control implementation and operational thresholds are not mirrored because publishing them would make bypass attempts easier.

No database URL/password, email credential, push credential, bearer token, private environment value, user record or operational anti-abuse signature is approved for public release.
