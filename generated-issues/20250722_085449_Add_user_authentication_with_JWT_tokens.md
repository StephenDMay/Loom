# FEATURE: User Authentication with JWT Tokens

## EXECUTIVE SUMMARY
This feature introduces user authentication to the Loom ecosystem, enabling secure communication between the `loom` CLI and a future backend service. It will allow developers to log in, and for the CLI to manage and use JSON Web Tokens (JWTs) for API requests, laying the groundwork for cloud-based features like project sharing, remote execution, and user-specific configurations.

## CODEBASE ANALYSIS
The current codebase is a standalone Python CLI tool with no existing user management, authentication, or web-facing components. 
- **`loom.py`**: The main entry point. It will need to be modified to handle new `login` and `logout` commands.
- **`agents/orchestrator.py`**: The core logic for running agents. It does not require direct changes, but services it calls might become authenticated.
- **`core/config_manager.py`**: Manages the `dev-automation.config.json`. This will be extended to store the JWT.
- **`requirements.txt`**: Currently minimal. It will need additions like `requests`, `PyJWT`, `fastapi`, `uvicorn`, `passlib[bcrypt]`, and `python-jose`.
- **Architecture**: The current architecture is purely local. This feature introduces a client-server model by adding a new, separate authentication service and making the CLI a client of that service. No significant refactoring of existing code is needed, but new components will be added.

## DOMAIN RESEARCH
- **User Workflow**: Developers will use a `loom login` command, enter credentials, and the CLI will fetch and store a JWT. Subsequent commands requiring authentication will automatically use this token. This is a standard pattern for CLI tools that interact with a web service (e.g., `gcloud auth login`, `docker login`).
- **Industry Patterns**: The use of a short-lived access token stored on the client and sent as a Bearer token in the `Authorization` header is the industry standard (OAuth 2.0). For the backend, using a mature Python web framework like FastAPI provides a robust, scalable, and well-documented foundation.
- **Competitive Analysis**: Similar developer tools with cloud components (e.g., Vercel, Netlify, Docker) all use this token-based CLI authentication model.

## TECHNICAL APPROACH
The recommended approach is to build a small, dedicated FastAPI service for authentication and user management. The `loom` CLI will be updated to communicate with this service.

1.  **Create a new Authentication Service**: A standalone FastAPI application responsible for user registration and issuing JWTs.
2.  **Update the CLI**:
    -   Add `login` and `logout` commands to `loom.py`.
    -   The `login` command will prompt for credentials, call the auth service, and store the returned JWT in the user's configuration.
    -   Create a new `ApiClient` class that encapsulates making authenticated requests to the backend, automatically attaching the JWT.
3.  **Token Storage**: The JWT will be stored in the `dev-automation.config.json` file. While more secure methods like system keychains exist, using the config file is sufficient for an initial implementation.

An alternative could be to use a third-party authentication provider (e.g., Auth0), but this adds external dependencies and costs. Building a simple service in-house provides more control and is a good starting point.

## IMPLEMENTATION SPECIFICATION
### Database Changes
- A new database (e.g., SQLite for simplicity, PostgreSQL for production) will be required for the authentication service.
- It will contain a `users` table with fields like `id`, `username`, `hashed_password`, `email`, `is_active`.

### API Design
A new FastAPI service will be created with the following endpoints:
- **`POST /token`**:
    -   Request Body: `username`, `password` (form data).
    -   Response: `{ "access_token": "...", "token_type": "bearer" }`
- **`POST /users/`**:
    -   Request Body: `{ "email": "...", "password": "..." }`
    -   Response: `{ "id": "...", "email": "...", "is_active": true }`
- **`GET /users/me/`**:
    -   Authentication: Required (Bearer Token).
    -   Response: `{ "id": "...", "email": "...", "is_active": true }`

### Frontend Components
- Not applicable, as this is a CLI tool. The "frontend" is the command-line interface.

### Backend Services
- A new Python package `auth_service` will be created.
- **`auth_service/main.py`**: Defines the FastAPI application and endpoints.
- **`auth_service/security.py`**: Contains all logic for password hashing and JWT creation/verification.
- **`auth_service/database.py`**: Manages the database connection.
- **`auth_service/models.py`**: Defines the SQLAlchemy User model.
- **`auth_service/schemas.py`**: Defines the Pydantic models for request/response validation.
- **`auth_service/crud.py`**: Contains the data access logic (Create, Read operations for users).

## RISK ASSESSMENT
### Technical Risks
- **Insecure Token Storage**: Storing the JWT in a plaintext config file is vulnerable. - **Mitigation**: For the initial version, we will proceed with this method but document the risk. Future iterations should use a more secure storage mechanism like the system keychain.
- **No Backend Infrastructure**: The project currently has no provision for deploying or managing a web service. - **Mitigation**: The authentication service will be developed as a standalone component that can be deployed independently (e.g., in a Docker container).

### Business Risks
- **Feature Adoption**: If no features immediately require login, users may not use it. - **Mitigation**: This feature should be developed in tandem with another feature that leverages authentication (e.g., saving results to the cloud).
- **User Experience**: A poorly implemented login flow can be frustrating. - **Mitigation**: The `login` command should be simple, with clear instructions and error messages.

## PROJECT DETAILS
**Estimated Effort**: 6 days
- Backend Service: 4 days
- CLI Integration: 2 days
**Dependencies**: Development of a feature that requires authentication.
**Priority**: Medium
**Category**: feature

## IMPLEMENTATION DETAILS
- **Files to create**:
    -   `auth_service/main.py`
    -   `auth_service/security.py`
    -   `auth_service/database.py`
    -   `auth_service/models.py`
    -   `auth_service/schemas.py`
    -   `auth_service/crud.py`
    -   `auth_service/Dockerfile` (for deployment)
    -   `core/api_client.py` (in the main loom project)
- **Files to modify**:
    -   `loom.py`: Add `login` and `logout` argument parsing and sub-commands.
    -   `core/config_manager.py`: Add `get_token()`, `set_token()`, `delete_token()` methods.
    -   `requirements.txt`: Add `fastapi`, `uvicorn`, `python-jose`, `passlib[bcrypt]`, `sqlalchemy`, `requests`.
- **Key classes/functions**:
    -   `loom.py`: `main()` to handle new commands.
    -   `core.api_client.ApiClient`: A class to handle requests, headers, and token management.
- **CLI command structure**:
    -   `python loom.py login`
    -   `python loom.py logout`

## SCOPE BOUNDARIES
**IN SCOPE**:
- A backend service that can create users and issue JWTs.
- `login` and `logout` commands in the CLI.
- Storing the token in the local config file.
- A basic `ApiClient` in the CLI for making authenticated requests.

**OUT OF SCOPE**:
- OAuth2/SSO integration (e.g., login with Google/GitHub).
- Password reset functionality.
- User roles and permissions.
- Using secure system keychains for token storage.
- Any UI other than the command line prompts.

## ACCEPTANCE CRITERIA
- [ ] A new user can be created via the backend.
- [ ] Running `python loom.py login` prompts for credentials, and on success, stores a JWT in `dev-automation.config.json`.
- [ ] The stored JWT can be used to successfully authenticate to the protected `/users/me/` endpoint.
- [ ] Running `python loom.py logout` removes the token from the configuration file.
- [ ] All new backend code is accompanied by unit tests.

## GITHUB ISSUE TEMPLATE
**Title**: Feature: Add User Authentication with JWT Tokens
**Labels**: `feature`, `backend`, `cli`, `auth`
**Assignee**:
**Project**: Loom MVP