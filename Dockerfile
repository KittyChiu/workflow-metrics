FROM python:3.9-slim-buster
LABEL org.opencontainers.image.source https://github.com/kittychiu/workflow-metrics

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

COPY *.py /github/workspace/
RUN ls -al /github/workspace/
WORKDIR /github/workspace

CMD ["python", "/github/workspace/workflow_metrics.py"]