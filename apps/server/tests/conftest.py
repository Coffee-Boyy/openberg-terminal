"""Shared pytest configuration for the OpenBerg Terminal backend.

DB isolation is handled inside each test module:
  - test_user_data.py: autouse fixture patches DB_PATH per-test via tmp_path
  - test_endpoints.py:  module-level temp file with per-test table reset
  - test_adapters.py / test_services.py: no DB needed
"""
