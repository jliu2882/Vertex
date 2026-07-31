# [Docker Keyword] Multi-stage build label setting up Node explicitly to compile code assets
FROM node:20-alpine AS build

# [Docker Keyword] Declares the primary directory container commands execute within
WORKDIR /app

# [Docker Keyword] Copies dependency manifests first to ensure fast caching when source code shifts
COPY package*.json ./

# [Docker Keyword] Executes package download internally
RUN npm install

# [Docker Keyword] Copies all components inside to prep for compilation
COPY . .

# [Docker Keyword] Triggers Vite to compile raw JSX code down into optimized static asset folders
RUN npm run build

# [Docker Keyword] Clears memory completely and initializes Stage 2 using an enterprise-grade static file server
FROM nginx:alpine

# [Docker Keyword] Extract strategy pulling Vite's output files ('dist') straight into Nginx's public rendering root
COPY --from=build /app/dist /usr/share/nginx/html

# [Docker Keyword] Exposes standard production internet channel (Port 80)
EXPOSE 80

# [Docker Keyword] Forces Nginx to lock into the container foreground process so it doesn't gracefully shut down
CMD ["nginx", "-g", "daemon off;"]