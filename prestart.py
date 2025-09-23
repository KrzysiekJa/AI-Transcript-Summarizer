import sys
import subprocess

from alembic import command
from alembic.config import Config

from app.config import ROOT


alembic_cfg = Config(ROOT / "alembic.ini")

subprocess.run([sys.executable, "./app/db/backend_pre_start.py"])
command.upgrade(alembic_cfg, "head")
