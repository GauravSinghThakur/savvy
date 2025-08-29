System Architecture: Business Entity Resolution Tool (MVP)
1. Architectural Approach
The system will be built using a microservices architecture to ensure scalability, separation of concerns, and independent deployment of components. A central API Gateway will manage all incoming requests and route them to the appropriate backend service.

2. Core Components & Technology Stack
API Gateway:

Technology: Managed Cloud Service (e.g., Amazon API Gateway).

Responsibility: Handles user authentication, rate limiting, and acts as the single entry point for all API requests.

Backend Microservices:

Technology: Python with FastAPI.

Services:

Verification Service: Connects to external government registries to validate business data.

Screening Service: Checks business and principal names against global sanctions and PEP watchlists.

Rationale: Python's strength in data handling combined with FastAPI's high performance and automatic documentation generation makes it ideal for our backend.

Frontend Web Application (Investigator Dashboard):

Technology: React.

Responsibility: Provides a user-friendly interface for Compliance Officers to perform manual searches, view results, and review search history.

Rationale: React is the industry standard for building modern, responsive single-page applications.

Database:

Technology: PostgreSQL.

Responsibility: Stores user account information, authentication details, and a log of all verification searches (search history).

Rationale: A reliable, open-source relational database that is perfect for handling our structured data needs.

3. High-Level Data Flow
[User/Developer] -> [API Gateway] -> [Verification Service] -> [External Data Sources]
                      |           -> [Screening Service]  -> [Sanctions Lists]
                      |
                      -> [Web Application (React)] <-> [Database (PostgreSQL)]
