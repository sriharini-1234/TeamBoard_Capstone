# Testing Report – TeamBoard

## Test cases
| ID | Test | Expected result |
|---|---|---|
| TC01 | GET /health | 200 and status ok |
| TC02 | Member logs in | 200 and JWT returned |
| TC03 | Member creates ticket | 201 |
| TC04 | Viewer attempts create | 403 |
| TC05 | Admin deletes ticket | 204 |
| TC06 | Invalid or missing token calls protected route | 401 |
| TC07 | Ticket title shorter than 3 characters | 422 |

## Execute tests
From `backend`:
```powershell
pytest -q
```

## Evidence
Paste actual terminal screenshots and observed results here after running the test suite. Do not mark tests as passed until they have been executed locally.
