# syntax=docker/dockerfile:1

###############################################
# Stage 1 — Build dependencies + install package
###############################################
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install build toolchain (needed for wheels)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy only project metadata first (cache-friendly)
COPY pyproject.toml .
COPY README.md .
COPY jenkinsctl ./jenkinsctl
# If you add tests or other folders later, include only what’s required

# Install dependencies + build wheels
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /build/wheels .

###############################################
# Stage 2 — Minimal runtime image
###############################################
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only the built wheels — NO compilers, NO build deps
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache /wheels/*

# Optional: define overridable env vars
ENV JENKINS_SERVER_URL=""
ENV JENKINS_USERNAME=""
ENV JENKINS_API_KEY=""

# Create non-root user
RUN useradd -m -u 1000 jenkinsctl && \
    chown -R jenkinsctl:jenkinsctl /app
USER jenkinsctl

# Default entrypoint — pure CLI
ENTRYPOINT ["jenkinsctl"]
CMD ["--help"]

