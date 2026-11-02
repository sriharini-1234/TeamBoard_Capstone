# Testing Report – TeamBoard

## Automated coverage

The current automated tests are in [`backend/tests/test_api.py`](../backend/tests/test_api.py):

| Test | Expected result |
|---|---|
| Health endpoint | Returns `{"status": "ok"}` |
| Member creates a ticket | Returns 201 |
| Viewer attempts to create a ticket | Returns 403 |
| Admin deletes a ticket | Returns 204 |

Run them from the `backend` folder with the virtual environment active:

```powershell
python -m pytest -q
```

## Manual demonstration checklist

These are useful behaviors to demonstrate through the app or Swagger. They are not all covered by the current automated test file:

- Sign in with each demo role and confirm the available actions.
- Update a ticket and verify its status and board counts.
- Confirm that a member cannot delete tickets and an admin can.
- Submit an invalid short title and observe request validation.
- Open two browser windows and demonstrate a live ticket update.

## Record your actual test run

Fill this in after running the command above. Do not mark tests as passed until you have observed the result.

- Date:
- Command:
- Result (copy the actual terminal summary):
- Failures or notes:
- Evidence screenshot filename:
