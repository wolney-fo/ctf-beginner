# Beginner Web CTF — Nimbus Logistics

A **beginner-friendly web CTF** in the style of TryHackMe. You get access to the
internal portal of a fictional logistics company (*Nimbus Logistics*) and your
goal is to find the security flaws hidden inside it and capture the **flags**
(format `FLAG{...}`).

> No prior security knowledge required — just curiosity, a browser, and a
> willingness to poke at things. Great for classrooms, study groups, workshops,
> or self-paced learning.

## Scenario

Nimbus is migrating its internal portal to version 2.3 and, in the rush, a few
things ended up... poorly done. Your mission is to act as a penetration tester
and show them everything that's wrong — before someone with bad intentions does.

## Ground rules

- Everything you need is reachable from the site. No heavy brute-forcing and no
  denial-of-service — this challenge is about **reasoning**, not noise.
- Explore like a curious tester: read the page source, pay attention to details,
  and test anything that looks "breakable".
- Each flag is worth one point. There are **6 flags** in total.

## Helpful tools (all free)

- The **browser** itself (*View Source* and the *DevTools* — F12).
- A notepad to track what you find.
- Optional: a cookie-editor extension, or `curl` in the terminal.

## Tracking your flags

Record each flag you find in a `flags.md` file (create your own, using the table
below) and describe **how** you got it. The "how" is what matters most — that's
where the learning happens.

| # | Category (light hint)      | Flag found | How I got it |
|---|----------------------------|------------|--------------|
| 1 | Reconnaissance             |            |              |
| 2 | Forgotten files            |            |              |
| 3 | Authentication             |            |              |
| 4 | Access control (data)      |            |              |
| 5 | Access control (area)      |            |              |
| 6 | Information disclosure      |            |              |

## Running it

See [`setup.md`](./setup.md) for a one-command deployment on any Linux server
(local VM or cloud), plus a quick local-dev option.

## Tech stack

Python 3 + Flask + SQLite. No external services required.

---

*Intentionally vulnerable, for educational use only. Do not host anything real on
the instance and do not use this in production.*

## License

Released under the MIT License. See [`LICENSE`](./LICENSE).
