#  SQL Injection — PortSwigger Labs

> [Web Security Academy — SQL Injection](https://portswigger.net/web-security/sql-injection)

## Progress

```
████████████████░░  16 / 18 — 89%
```

| Difficulty | Completed |
|---|---|
| 🟢 Apprentice | 2 / 2 |
| 🟡 Practitioner | 14 / 16 |

---

## Labs

| # | Lab | Technique | Status |
|---|---|---|---|
| 01 | [WHERE clause — hidden data](./writeups/01-where-clause.md) | Basic SQLi | ✅ |
| 02 | [Login bypass](./writeups/02-login-bypass.md) | Auth bypass | ✅ |
| 03 | [UNION — number of columns](./writeups/03-union-number-of-columns.md) | UNION attack | ✅ |
| 04 | [UNION — column containing text](./writeups/04-union-column-text.md) | UNION attack | ✅ |
| 05 | [UNION — data from other tables](./writeups/05-union-other-tables.md) | UNION attack | ✅ |
| 06 | [UNION — multiple values in single column](./writeups/06-union-multiple-values.md) | UNION attack | ✅ |
| 07 | [DB version — Oracle](./writeups/07-db-version-oracle.md) | Fingerprinting | ✅ |
| 08 | [DB version — MySQL & Microsoft](./writeups/08-db-version-mysql-mssql.md) | Fingerprinting | ✅ |
| 09 | [DB contents — non-Oracle](./writeups/09-db-contents-non-oracle.md) | Enumeration | ✅ |
| 10 | [DB contents — Oracle](./writeups/10-db-contents-oracle.md) | Enumeration | ✅ |
| 11 | [Blind — conditional responses](./writeups/11-blind-conditional-responses.md) | Blind SQLi | ✅ |
| 12 | [Blind — conditional errors](./writeups/12-blind-conditional-errors.md) | Blind SQLi | ✅ |
| 13 | [Visible error-based](./writeups/13-visible-error-based.md) | Error-based | ✅ |
| 14 | [Blind — time delays](./writeups/14-blind-time-delays.md) | Time-based | ✅ |
| 15 | [Blind — time delays + data retrieval](./writeups/15-blind-time-delays-retrieval.md) | Time-based | ✅ |
| 16 | [Blind — out-of-band interaction](./writeups/16-blind-oob-interaction.md) | OOB | ⏸ Requires Collaborator |
| 17 | [Blind — out-of-band exfiltration](./writeups/17-blind-oob-exfiltration.md) | OOB | ⏸ Requires Collaborator |
| 18 | [Filter bypass via XML encoding](./writeups/18-xml-filter-bypass.md) | WAF bypass | ✅ |

---

## Scripts

| Script | Description |
|---|---|
| [blind_sqli.py](./scripts/blind_sqli.py) | Automated extraction for blind SQLi (boolean, error and time-based) |

---

## Key concepts learned

- Difference between in-band, blind and out-of-band SQLi
- Database engine fingerprinting (Oracle, PostgreSQL, MySQL, MSSQL)
- UNION attack step by step
- Character-by-character data extraction in blind SQLi
- Python automation when Burp Community is too slow
- Basic WAF evasion via XML encoding
