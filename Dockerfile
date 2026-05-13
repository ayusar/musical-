FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project
COPY . /app/
WORKDIR /app/

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates bash ffmpeg git zip \
    build-essential python3-dev libssl-dev libffi-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies + Flask
RUN if [ -f "pyproject.toml" ]; then \
        uv sync && uv pip install flask; \
    elif [ -f "requirements.txt" ]; then \
        python -m venv .venv && \
        . .venv/bin/activate && \
        pip install --no-cache-dir -r requirements.txt flask; \
    else \
        python -m venv .venv && \
        . .venv/bin/activate && \
        pip install flask; \
    fi

# Ensure venv is used
ENV PATH="/app/.venv/bin:$PATH"

# Make start executable (VERY IMPORTANT)
RUN chmod +x start

# Expose port (if Flask used)
EXPOSE 8000

# Use your start script
CMD ["bash", "start"]
