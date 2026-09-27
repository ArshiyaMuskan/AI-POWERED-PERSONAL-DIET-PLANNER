# Test Plan

| ID | Scenario | Expected result |
|---|---|---|
| T01 | New registration | 201 + JWT |
| T02 | Existing email | 409 |
| T03 | Valid login | 200 + JWT |
| T04 | Invalid login | 401 |
| T05 | Unauthorized dashboard/API | 401 |
| T06 | Profile update | 200 |
| T07 | Plan generation | 201 |
| T08 | Vegetarian profile | Vegetarian meals |
| T09 | Vegan profile | Vegan meals |
| T10 | Different goal | Goal-aware educational note |
| T11 | AI unavailable | Local fallback |
| T12 | Save/retrieve plan | Same user's plan returned |
| T13 | File upload | 201 |
| T14 | Invalid file | 400 |
| T15 | File retrieval | Download works |
| T16 | User isolation | Other user's records return 404 |
| T17 | Logout | Token removed client-side |
| T18 | Database failure | API should return controlled server error; production adds retries/monitoring |
