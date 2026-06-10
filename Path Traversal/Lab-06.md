# Lab 06 — Validation of file extension with null byte bypass

**Difficulty:** 🟡 Practitioner  
**Technique:** Path Traversal — null byte bypass  
**Link:** https://portswigger.net/web-security/file-path-traversal/lab-validate-file-extension-null-byte-bypass

---

## Concept

The application validates that the `filename` parameter ends with an allowed file extension (`.png`, `.jpg`). By injecting a null byte (`%00`) before the extension, the OS truncates the string at that point while the application's validation still sees the required extension at the end.

---

## Reconnaissance

Same injection point:

```
GET /image?filename=18.jpg
```

Previous bypasses are blocked. The app appears to require a valid image extension.

---

## Process

### Step 1 — Identify the extension validation

Supplying `../../../etc/passwd` without an extension returns an error. Adding `.png` at the end alone doesn't help because the traversal is still detected.

### Step 2 — Inject a null byte before the extension

```
GET /image?filename=../../../etc/passwd%00.png
```

The app validates the string: sees `.png` at the end → passes.  
The OS processes the path: encounters `\0` (null byte) → truncates → reads `/etc/passwd`.

---

## Result

Full `/etc/passwd` contents returned with 200 OK.

---

## Issues encountered

None. Extension used was `.png` matching the lab's expected format.

---

## Takeaways

- The null byte `%00` acts as a string terminator in C and languages built on top of it
- The application validates the full string but the OS truncates at the null byte
- Most effective against apps written in PHP (older versions) or C/C++
- In modern PHP (>= 5.3.4) null bytes in file paths are sanitized by default

---

## References

- [Path Traversal — PortSwigger](https://portswigger.net/web-security/file-path-traversal)
