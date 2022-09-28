import os

ORG = "CLARIAH"
REPO = "pure3d"
BASE = os.path.expanduser(f"~/github/{ORG}/{REPO}")
DATA_DIR = f"{BASE}/data"
DATA_URL = "data"
YAML_DIR = f"{BASE}/src/pure3d/control/yaml"
SECRET_FILE = "/opt/web-apps/pure3d.secret"
