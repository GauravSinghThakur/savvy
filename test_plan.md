Test Plan: Business Entity Resolution Tool (MVP)
1. Objective
To ensure the Business Entity Resolution Tool MVP is reliable, functional, secure, and meets all requirements defined in the PRD before launch.

2. Scope of Testing
This plan covers the testing of two primary components:

The Core Verification & Screening API.

The Investigator Dashboard (Web Application).

3. Test Cases: API (/verify endpoint)
TC-API-01: Successful Verification ("Happy Path")

Action: Send a request with a valid business name and country.

Expected Result: 200 OK response with accurate data and "status": "clear".

TC-API-02: Business Not Found

Action: Send a request with a fictitious business name.

Expected Result: 404 Not Found response with a clear error message.

TC-API-03: Invalid Input Data

Action: Send a request with a missing or malformed field (e.g., no country).

Expected Result: 400 Bad Request response with a validation error message.

TC-API-04: Unauthorized Access

Action: Call the API without a valid authentication token.

Expected Result: 401 Unauthorized response.

TC-API-05: Screening Hit

Action: Send a request for a business known to be on a sanctions list (using test data).

Expected Result: 200 OK response with risk flags and "status": "review_required".

4. Test Cases: Investigator Dashboard (UI)
TC-UI-01: Successful Login

Action: Enter valid credentials on the login page.

Expected Result: User is redirected to the main search dashboard.

TC-UI-02: Invalid Login

Action: Enter invalid credentials.

Expected Result: An error message is displayed on the login page.

TC-UI-03: Perform Manual Search

Action: Use the search form to look up a valid business.

Expected Result: The results are displayed clearly and accurately on the page.

TC-UI-04: View Search History

Action: Navigate to the search history page.

Expected Result: A list of recent searches is displayed correctly.