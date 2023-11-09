import subprocess

# Install Python packages
subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

# Download spaCy model
subprocess.check_call(["python", "-m", "spacy", "download", "fr_dep_news_trf"])
