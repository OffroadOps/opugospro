"""VPS credentials -- gitignored, never commit. Or set UGOS_VPS_HOST/USER/PASSWORD env."""
import os

HOST = os.environ.get("UGOS_VPS_HOST", "5.181.177.120")
USER = os.environ.get("UGOS_VPS_USER", "root")
PASSWORD = os.environ.get("UGOS_VPS_PASSWORD", "yS0IuSXjvWwdgp3HJqP3")
