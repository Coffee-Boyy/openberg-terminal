# Build stage — produces the Vite SPA in /app/apps/web/dist
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY apps/web/package.json ./apps/web/
RUN corepack enable && pnpm install --frozen-lockfile || true
COPY . .
RUN cd apps/web && pnpm build

# Production — nginx serves the SPA and proxies /api/* to the backend
FROM nginx:alpine
COPY --from=build /app/apps/web/dist /usr/share/nginx/html

# Custom nginx config: serve SPA on port 80, proxy /api/ to the FastAPI server.
RUN cat > /etc/nginx/conf.d/default.conf <<NGINX
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    # Proxy all API requests to the backend (docker-compose service name)
    location /api/ {
        proxy_pass http://server:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # SPA fallback — any route that isn't a file returns index.html
    location / {
        try_files $uri $uri/ /index.html;
    }
}
NGINX

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
