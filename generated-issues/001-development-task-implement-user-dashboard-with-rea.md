```
# Development Task: Implement User Dashboard with Real-Time Metrics

## Feature Implementation Request
Create a user dashboard with real-time metrics.

## Project Context
**Project**: Loom
**Architecture**: Agent-Based Architecture, Templating, Configuration-Driven
**Tech Stack**: Python (3.7+), Google Gemini, Templating UI (potentially Flask/Django backend with React/Vue/Angular frontend), likely relational or NoSQL database, structured configuration management.

## Implementation Specifications

### Requirements Analysis
- User-specific dashboard displaying real-time metrics.
- Authentication required, leveraging existing JWT token-based system.
- Real-time updates using WebSockets or Server-Sent Events (SSE).
- Performance considerations: fast loading and efficient updates.
- Security: secure API endpoints and data validation.
- Scalability: handle a large number of concurrent users.

### Technical Constraints
- Real-time updates require WebSockets or SSE implementation.
- Performance optimization is crucial for responsiveness.
- Security must align with existing authentication patterns.
- Scalability must be considered for a large user base.

### Integration Requirements
- Integrate with existing JWT authentication system.
- Define new API endpoints for fetching real-time metrics.
- Integrate with the data source providing real-time metrics.
- Create new UI components for the dashboard.

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
1. **Analysis Phase**: Review existing codebase patterns and similar implementations, especially authentication and API endpoint definitions.
2. **Design Phase**: Plan the architecture using FastAPI for the backend, React for the frontend, and WebSockets for real-time updates.
3. **Development Phase**: Implement following established patterns and conventions.
4. **Testing Phase**: Write and run comprehensive tests.
5. **Documentation Phase**: Update relevant documentation and comments.

## Expected Deliverables

### Code Artifacts
- [ ] Core implementation files with proper organization
- [ ] Unit tests achieving minimum 80% code coverage  
- [ ] Integration tests for external dependencies
- [ ] Updated configuration files if needed

### Documentation Updates
- [ ] API documentation for new endpoints/functions
- [ ] README updates if user-facing features are added
- [ ] Architecture documentation updates if patterns change
- [ ] Deployment or setup instruction updates if required

### Quality Assurance
- [ ] Code passes all existing tests
- [ ] New functionality is properly tested
- [ ] Code follows project style guidelines
- [ ] Performance benchmarks are within acceptable ranges
- [ ] Security review completed for sensitive operations

## Success Criteria
- User dashboard displays real-time metrics accurately.
- Authentication is secure and integrated with the existing system.
- Real-time updates are efficient and responsive.
- The dashboard is scalable to handle a large number of users.
- Code is well-tested, documented, and follows project standards.

---

**Instructions**: Implement the requested feature following the guidelines above. Use the provided project context to ensure consistency with existing patterns. Focus on creating maintainable, well-tested, and properly documented code.

**Final Output:**

This document provides a comprehensive guide for implementing a user dashboard with real-time metrics in the Loom project. The recommended approach leverages FastAPI for the backend, React for the frontend, and WebSockets for real-time communication.  It builds upon the existing JWT authentication system and emphasizes code quality, security, and scalability.

**Implementation Steps:**

1.  **Backend (FastAPI):**

    *   **Setup:** Create a new FastAPI project or integrate with the existing API structure.
    *   **Authentication:**  Utilize the existing JWT authentication mechanism as described in `generated-issues/2025-08-25-093113-user-authentication-with-jwt-tokens.md` and `generated-issues/20250722_085449_Add_user_authentication_with_JWT_tokens.md`.
    *   **API Endpoints:**
        *   Create a GET endpoint `/api/dashboard` to fetch initial dashboard data.  This endpoint should require JWT authentication.
        *   Create a WebSocket endpoint `/ws/dashboard` for real-time updates.  Implement authentication for the WebSocket connection, potentially using the JWT token during the initial handshake.
        *   Use `templates/api.py` as a template for defining API endpoints.
    *   **Data Fetching:** Implement logic to fetch real-time metrics from the data source.  Use `templates/data.py` as a template. The data source is currently undefined, so this will require further investigation to determine the appropriate integration method (database query, API call, etc.).
    *   **Real-time Updates:**  Use a WebSocket library (e.g., `websockets` or `starlette.websockets`) to push updates to connected clients.  Consider using a message queue (e.g., Redis Pub/Sub) to decouple the data source from the WebSocket connections.
    *   **Code Location:** Create a new file `api/dashboard.py` (or similar) to house the API endpoints and WebSocket logic.
    *   **Testing:** Implement unit tests for the API endpoints and WebSocket functionality in `tests/api/test_dashboard.py` (or similar).

2.  **Frontend (React):**

    *   **Setup:** Create a new React project or integrate with the existing UI framework.
    *   **Authentication:** Implement the authentication flow (login/logout) using the existing JWT authentication system.
    *   **UI Components:** Create React components to display the dashboard metrics. Consider using a UI component library (e.g., Material UI, Ant Design) for pre-built components.
    *   **WebSocket Connection:** Establish a WebSocket connection to the `/ws/dashboard` endpoint. Use a WebSocket client library (e.g., `ws`) to manage the connection.
    *   **Data Display:** Fetch initial dashboard data from the `/api/dashboard` endpoint and display it in the UI.
    *   **Real-time Updates:** Update the dashboard metrics in real-time as WebSocket messages are received.
    *   **Code Location:** Create a new file `ui/Dashboard.js` (or similar) to house the React components.

3.  **Configuration:**

    *   Update `core/config_manager.py` to include configuration settings for the dashboard, such as the data source connection details and WebSocket server address.

4.  **Testing:**

    *   Implement comprehensive unit and integration tests to ensure the dashboard functions correctly and securely.
    *   Pay particular attention to testing the real-time update functionality and authentication.

5.  **Deployment:**

    *   Follow the existing deployment procedures for the Loom project.
    *   Consider using Docker and Kubernetes for containerization and orchestration.

**Files to Modify vs Create:**

*   **Modify:**
    *   `core/config_manager.py`: Add configuration settings for the dashboard.
    *   Potentially `templates/ui.py` if integrating with an existing templating system, but React is the preferred approach.
*   **Create:**
    *   `api/dashboard.py`: Implement the API endpoints for the dashboard.
    *   `ui/Dashboard.js`: Implement the UI components for the dashboard.
    *   `data/dashboard_data.py`: Implement the data fetching logic for the dashboard.
    *   `tests/api/test_dashboard.py`: Implement tests for the new API endpoints.

**Key Considerations:**

*   **Data Source:**  The specific data source for the metrics is not defined in the provided context.  This needs to be determined and integrated accordingly.
*   **UI Framework:**  While the context suggests a templating approach in `templates/ui.py`, the recommendation is to use React for a more dynamic and maintainable frontend.  This may require adapting the existing UI infrastructure.
*   **Error Handling:** Implement robust error handling throughout the application, especially for WebSocket connections and data fetching.
*   **Security:**  Ensure that all API endpoints and WebSocket connections are properly authenticated and authorized.  Sanitize all user input to prevent XSS attacks.

By following these steps and adhering to the project's existing standards, you can successfully implement a user dashboard with real-time metrics for the Loom project. Remember to prioritize code quality, security, and scalability throughout the development process.
```