import subprocess
import shutil
import os

# Duplicate .env.example to .env
shutil.copy(".env.example", ".env")

# Delete .env.example
os.remove(".env.example")

# Install Python packages
subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

# Download spaCy model
subprocess.check_call(["python", "-m", "spacy", "download", "fr_dep_news_trf"])
