FROM node:24-slim AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including dev for build)
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Production image
FROM node:24-slim

# Create non-root user
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install only production dependencies
RUN npm ci --omit=dev

# Copy built application from builder
COPY --from=builder /app/dist ./dist

# Install mcp-proxy globally for HTTP/SSE transport
RUN npm install -g mcp-proxy

# Change ownership to non-root user
RUN chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# Expose HTTP port
EXPOSE 8080

# Use mcp-proxy to expose over HTTP (both /mcp streamable and /sse endpoints)
ENTRYPOINT ["mcp-proxy", "--port", "8080", "--host", "0.0.0.0", "--shell", "node dist/cli.js"]
