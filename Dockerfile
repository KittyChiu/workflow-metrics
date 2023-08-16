FROM python:3.9-slim-buster
LABEL org.opencontainers.image.source https://github.com/kittychiu/workflow-metrics

# Create the /github/workspace/ directory if it doesn't exist
RUN if [ ! -d "/github/workspace/" ]; then mkdir -p /github/workspace/; fi
# Set the working directory to /github/workspace/
WORKDIR /github/workspace/
# Copy the current python scripts to /github/workspace/
COPY *.py /github/workspace/

# Update pip
RUN python -m pip install --upgrade pip

# Install the GitHub CLI and jq
RUN apt-get update && \
  apt-get install -y gnupg && \
  apt-get install -y curl && \
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg && \
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
  apt-get update && \
  apt-get install -y gh && \
  apt-get install -y jq

CMD ["python", "/github/workspace/workflow_metrics.py"]