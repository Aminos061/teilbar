# Entwicklungs-Image für `docker compose up` (docs/adr/0003-ein-devcontainer.md, docs/adr/0007-tech-stack-der-app.md).
# Kein Produktions-Image: Wo die App gehostet wird, ist noch nicht entschieden.
FROM node:24.22.2-bookworm-slim

WORKDIR /app
COPY package.json package-lock.json .npmrc ./
RUN npm ci

COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]
