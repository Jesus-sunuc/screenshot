FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install pnpm and dependencies
RUN npm install -g pnpm && pnpm install

# Copy application code
COPY . .

EXPOSE 5173

CMD ["pnpm", "run", "dev", "--", "--host"]
