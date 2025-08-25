# Development Task: Implement User Authentication with OAuth

## Feature Implementation Request
Implement user authentication with OAuth to allow users to securely access the Loom application using their existing accounts from providers like Google or GitHub.

## Project Context
**Project**: Loom
**Architecture**: Agent-Based Architecture, Configuration-Driven
**Tech Stack**: Python 3.7+, Google Gemini, pip, Custom configuration management using `core/config_manager.py` and `core/config_schema.json`

## Implementation Specifications

### Requirements Analysis
- Implement OAuth user authentication.
- Support at least one OAuth provider (e.g., Google, GitHub).
- Securely store and manage OAuth credentials.
- Implement proper error handling for authentication failures.
- Integrate OAuth with the existing agent-based architecture.
- Use JWTs for subsequent API calls and session management after initial OAuth authentication.
- Provide API endpoints for initiating the OAuth flow and handling the callback.

### Technical Constraints
- Security: OAuth implementation must adhere to security best practices to prevent vulnerabilities such as CSRF, XSS, and token theft.
- Configuration: The application needs a secure way to store and manage OAuth credentials. Consider using environment variables or a secure configuration management system.
- Error Handling: Implement robust error handling to gracefully handle authentication failures, token expiration, and other potential issues.
- Existing JWT Implementation: Consider whether OAuth should replace or complement the existing JWT setup.
- The application uses a custom configuration management system (`core/config_manager.py` and `core/config_schema.json`).

### Integration Requirements  
- API Endpoints: New API endpoints are required for initiating the OAuth flow (e.g., `/login/oauth`), handling the callback from the OAuth provider (e.g., `/callback/oauth`), and potentially retrieving user information (e.g., `/userinfo`).
- Configuration Management: The `core/config_manager.py` will be the primary integration point for storing and retrieving OAuth-related configuration parameters (e.g., client ID, client secret, redirect URIs).
- Agent Integration: Modify the `loom.py` file to integrate the OAuth flow. This might involve adding a new agent or modifying an existing agent to handle authentication.
- The `templates/api.py` file should be used to define the new API endpoints.

## Development Guidelines

### Code Quality Standards
- Follow existing code patterns and conventions found in the project
- Implement comprehensive error handling and input validation
- Write unit tests for all new functionality
- Document public APIs and complex business logic
- Consider performance implications and optimization opportunities

### Security Considerations
- Implement proper authentication and authorization checks
- Sanitize and validate all user inputs
- Follow secure coding practices for the technology stack
- Consider data privacy and compliance requirements

### Implementation Approach
1. **Analysis Phase**: Review existing codebase patterns and similar implementations, especially in `core/config_manager.py`, `templates/api.py`, and the agent files.
2. **Design Phase**: Plan the architecture and identify integration points.  A hybrid approach using OAuth for initial authentication and JWT for subsequent requests is recommended. Create a new `authentication_agent` or modify an existing one.
3. **Development Phase**: Implement following established patterns and conventions. Use `authlib` and `PyJWT` libraries.
4. **Testing Phase**: Write and run comprehensive tests, including unit tests, integration tests, and end-to-end tests.
5. **Documentation Phase**: Update relevant documentation and comments.

## Expected Deliverables

### Code Artifacts
- [x] Core implementation files with proper organization
    - `core/config_schema.json`: Updated with OAuth configuration parameters.
    - `core/config_manager.py`: Updated to handle OAuth configuration.
    - `loom.py`: Modified to integrate the OAuth flow.
    - `templates/api.py`: New API endpoints for OAuth authentication.
    - `agents/authentication_agent/agent.py` (or modification of an existing agent): Handles the OAuth authentication flow.
- [x] Unit tests achieving minimum 80% code coverage  
- [x] Integration tests for external dependencies
- [x] Updated configuration files if needed
    - `requirements.txt`: Updated with `authlib` and `PyJWT`.

### Documentation Updates
- [x] API documentation for new endpoints/functions
- [ ] README updates if user-facing features are added
- [ ] Architecture documentation updates if patterns change
- [ ] Deployment or setup instruction updates if required

### Quality Assurance
- [x] Code passes all existing tests
- [x] New functionality is properly tested
- [x] Code follows project style guidelines
- [ ] Performance benchmarks are within acceptable ranges
- [ ] Security review completed for sensitive operations

## Success Criteria
- Users can successfully authenticate using OAuth with at least one provider (e.g., Google, GitHub).
- The application securely stores and manages OAuth credentials.
- The application generates and verifies JWTs for subsequent API calls.
- The OAuth flow is integrated with the existing agent-based architecture.
- The implementation adheres to security best practices.
- The code is well-tested and documented.

---

**Instructions**: Implement the requested feature following the guidelines above. Use the provided project context to ensure consistency with existing patterns. Focus on creating maintainable, well-tested, and properly documented code.

**Detailed Implementation Steps:**

1.  **Configuration:**
    *   Modify `core/config_schema.json` to include OAuth-related configuration parameters:
        ```json
        {
          "type": "object",
          "properties": {
            "oauth": {
              "type": "object",
              "properties": {
                "provider": {
                  "type": "string",
                  "enum": ["google", "github"],
                  "description": "The OAuth provider to use."
                },
                "client_id": {
                  "type": "string",
                  "description": "The OAuth client ID."
                },
                "client_secret": {
                  "type": "string",
                  "description": "The OAuth client secret."
                },
                "redirect_uri": {
                  "type": "string",
                  "description": "The OAuth redirect URI."
                },
                "scopes": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  },
                  "description": "The OAuth scopes to request."
                }
              },
              "required": ["provider", "client_id", "client_secret", "redirect_uri", "scopes"]
            }
          },
          "required": []
        }
        
    *   Update `core/config_manager.py` to load and manage these parameters.  Refer to existing code for examples.

2.  **Dependencies:**
    *   Add `authlib` and `PyJWT` to `requirements.txt`:
        ```text
        authlib
        PyJWT
        
    *   Run `pip install -r requirements.txt` to install the dependencies.

3.  **Authentication Agent:**
    *   Create a new agent directory: `agents/authentication_agent/`.
    *   Create `agents/authentication_agent/agent.py`:
        ```python
        from authlib.integrations.requests_client import OAuth2Session
        import jwt
        import time
        from core.config_manager import ConfigManager

        class AuthenticationAgent:
            def __init__(self, config: ConfigManager):
                self.config = config
                self.oauth_config = self.config.get('oauth')
                self.client = OAuth2Session(
                    self.oauth_config['client_id'],
                    self.oauth_config['client_secret'],
                    redirect_uri=self.oauth_config['redirect_uri'],
                    scope=self.oauth_config['scopes']
                )

            def generate_authorization_url(self):
                authorization_url, state = self.client.create_authorization_url(
                    self.get_authorization_endpoint(),
                    redirect_uri=self.oauth_config['redirect_uri']
                )
                return authorization_url, state

            def fetch_token(self, code):
                token = self.client.fetch_token(
                    self.get_token_endpoint(),
                    code=code,
                    client_secret=self.oauth_config['client_secret']
                )
                return token

            def create_jwt(self, user_info):
                payload = {
                    'user_id': user_info.get('id'), # Adjust based on provider's user info
                    'exp': time.time() + 3600  # Token expires in 1 hour
                }
                token = jwt.encode(payload, self.config.get('jwt_secret'), algorithm='HS256') # Ensure jwt_secret is in config
                return token

            def get_user_info(self, access_token):
                self.client.token = access_token
                return self.client.get(self.get_userinfo_endpoint()).json()

            def get_authorization_endpoint(self):
                if self.oauth_config['provider'] == 'google':
                    return 'https://accounts.google.com/o/oauth2/v2/auth'
                elif self.oauth_config['provider'] == 'github':
                    return 'https://github.com/login/oauth/authorize'
                else:
                    raise ValueError("Unsupported OAuth provider")

            def get_token_endpoint(self):
                if self.oauth_config['provider'] == 'google':
                    return 'https://oauth2.googleapis.com/token'
                elif self.oauth_config['provider'] == 'github':
                    return 'https://github.com/login/oauth/access_token'
                else:
                    raise ValueError("Unsupported OAuth provider")

            def get_userinfo_endpoint(self):
                if self.oauth_config['provider'] == 'google':
                    return 'https://www.googleapis.com/oauth2/v3/userinfo'
                elif self.oauth_config['provider'] == 'github':
                    return 'https://api.github.com/user'
                else:
                    raise ValueError("Unsupported OAuth provider")

        # Example Usage (Not for direct execution, adjust based on Loom's architecture)
        if __name__ == '__main__':
            # This requires a ConfigManager instance to be available
            # Replace with the actual way ConfigManager is initialized in Loom
            config = ConfigManager() # Initialize with appropriate config file path
            agent = AuthenticationAgent(config)

            # Example: Generate Authorization URL
            auth_url, state = agent.generate_authorization_url()
            print(f"Authorization URL: {auth_url}")

            # Example: After user authorizes, handle the callback and fetch token
            # code = "USER_AUTHORIZATION_CODE" # Replace with the actual code from the callback
            # token = agent.fetch_token(code)
            # print(f"Token: {token}")
        
    *   Create `agents/authentication_agent/config.json` and `agents/authentication_agent/manifest.json` (refer to other agent examples for structure).

4.  **API Endpoints:**
    *   Modify `templates/api.py` to add the following endpoints:
        ```python
        from flask import Flask, request, redirect, session
        from core.config_manager import ConfigManager
        from agents.authentication_agent.agent import AuthenticationAgent # Adjust import path

        app = Flask(__name__)
        app.secret_key = ConfigManager().get('flask_secret') # Securely store this in config

        config = ConfigManager()
        auth_agent = AuthenticationAgent(config)

        @app.route('/login/oauth')
        def login_oauth():
            authorization_url, state = auth_agent.generate_authorization_url()
            session['oauth_state'] = state
            return redirect(authorization_url)

        @app.route('/callback/oauth')
        def callback_oauth():
            code = request.args.get('code')
            state = request.args.get('state')

            if state != session.get('oauth_state'):
                return "Invalid state!", 400

            token = auth_agent.fetch_token(code)
            user_info = auth_agent.get_user_info(token['access_token'])
            jwt_token = auth_agent.create_jwt(user_info)

            # Store the JWT in a secure cookie or session
            session['jwt_token'] = jwt_token  # Or use cookies
            return redirect('/dashboard') # Redirect to the user's dashboard

        @app.route('/dashboard')
        def dashboard():
            # Example: Check for JWT and display user info
            jwt_token = session.get('jwt_token')
            if jwt_token:
                # Decode the JWT and display user info
                try:
                    payload = jwt.decode(jwt_token, ConfigManager().get('jwt_secret'), algorithms=['HS256'])
                    return f"Welcome, User ID: {payload['user_id']}"
                except Exception as e:
                    return f"Invalid JWT: {e}", 401
            else:
                return redirect('/login/oauth')

        if __name__ == '__main__':
            app.run(debug=True)
        
5.  **Loom Integration:**
    *   Modify `loom.py` to initialize and use the `AuthenticationAgent`.  This will likely involve adding a route handler that calls the `login_oauth` and `callback_oauth` functions from `templates/api.py`.  Also, ensure the Flask app is properly integrated with Loom's architecture.

6.  **API Gateway/Middleware:**
    *   Implement an API gateway or middleware to intercept API requests and verify the JWT.  This can be done using Flask's middleware capabilities or a dedicated API gateway library.

7.  **Testing:**
    *   Write unit tests for the `AuthenticationAgent` to test the OAuth flow, JWT creation, and token handling.
    *   Write integration tests to test the interaction between the `AuthenticationAgent` and the API gateway.
    *   Write end-to-end tests to test the entire authentication flow from the user's perspective.

8.  **Security:**
    *   Store the `client_secret` and `jwt_secret` securely (e.g., using environment variables or a secrets management system).
    *   Use HTTPS to protect against man-in-the-middle attacks.
    *   Implement CSRF protection for the OAuth callback endpoint.
    *   Validate and sanitize all user inputs.

9. **Error Handling:** Implement comprehensive error handling throughout the OAuth flow.  Log errors and provide informative messages to the user.

10. **Deployment:** Deploy the application to a production environment.

This detailed implementation plan provides a comprehensive guide to implementing OAuth user authentication in the Loom project. Remember to adapt the code examples to fit the specific requirements of the Loom project and to follow security best practices.