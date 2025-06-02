FROM python:3.12-slim

ARG PORT=8050

WORKDIR /app

# Install uv
RUN pip install uv

# Copy the MCP server files
COPY . .

# Install packages directly without virtual environment
RUN uv pip install --system -e . ollama

EXPOSE ${PORT}

# Command to run the MCP server
CMD ["uv", "run", "src/main.py"]