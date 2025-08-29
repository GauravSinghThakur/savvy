"""
Service layer

Holds application services and data-access abstractions used by API routers.
This keeps transport (HTTP) concerns separated from domain/data logic so we can
swap implementations (e.g., in-memory vs. external registries) without changing
endpoint code.
"""

