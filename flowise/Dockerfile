# --------------------------------------------
# Stage 1: Build stage
# --------------------------------------------
    FROM node:20-alpine AS build

    USER root
    ENV PUPPETEER_SKIP_DOWNLOAD=true
    
    # Install Flowise globally in the build stage
    RUN npm install -g flowise@2.2.7

    # --------------------------------------------
    # Stage 2: Runtime stage
    # --------------------------------------------
    FROM node:20-alpine
    
    # 1) Install runtime dependencies for Flowise
    RUN apk add --no-cache \
        chromium \
        git \
        python3 \
        py3-pip \
        make \
        g++ \
        build-base \
        cairo-dev \
        pango-dev \
        curl
    
    # 2) Switch to root (to fix ownership and create directories)
    USER root
    
    # 3) Remove any leftover /root/.flowise if it exists, then create it
    #    Also create logs, storage subdirs in /root/.flowise. Then do the same in /home/node.
    RUN rm -rf /root/.flowise || true \
        && mkdir -p /root/.flowise/logs \
        && mkdir -p /root/.flowise/storage \
        && mkdir -p /home/node/.flowise/logs \
        && mkdir -p /home/node/.flowise/storage
    
    # 4) Copy Flowise from the build stage
    COPY --from=build /usr/local/lib/node_modules /usr/local/lib/node_modules
    COPY --from=build /usr/local/bin /usr/local/bin
    
    # 5) Make sure both /root/.flowise and /home/node/.flowise are owned by node
    RUN chown -R node:node /root/.flowise \
        && chown -R node:node /home/node \
        && chown -R node:node /usr/local/lib/node_modules \
        && chown -R node:node /usr/local/bin
    
    # 6) Switch to the built-in non-root "node" user
    USER node
    
    # 7) Environment variables so Flowise writes by default to /home/node/.flowise
    #    But if any Flowise code references /root/.flowise, that’s now writable too.
    ENV DATABASE_PATH=/home/node/.flowise
    ENV APIKEY_PATH=/home/node/.flowise
    ENV LOG_PATH=/home/node/.flowise/logs
    ENV SECRETKEY_PATH=/home/node/.flowise
    ENV BLOB_STORAGE_PATH=/home/node/.flowise/storage
    ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
    
    # 8) Use /home/node as working directory
    WORKDIR /home/node
    
    # 9) Expose Flowise default port
    EXPOSE 3000
    
    # 10) Launch Flowise
    ENTRYPOINT ["flowise", "start"]
    
