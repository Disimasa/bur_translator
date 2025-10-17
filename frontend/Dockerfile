FROM node:20-alpine AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable && corepack prepare pnpm@9.15.2 --activate

WORKDIR /frontend
COPY . .

FROM base as prod-deps
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile

FROM base AS build
ENV NODE_OPTIONS --max-old-space-size=4096
ENV NODE_ENV=production
ENV VITE_MODE=production
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run build:prod

FROM base

COPY --from=prod-deps /frontend/node_modules /frontend/node_modules
COPY --from=build /frontend/build /frontend

EXPOSE 3000
CMD ["node", "./index.js"]

#FROM node:20-slim AS build
#
#WORKDIR /frontend
#
#COPY ./package*.json ./
#RUN npm install
#COPY . .
#RUN npm run build
#
#FROM node:20-slim AS production
#COPY --from=build /frontend/build .
#COPY --from=build /frontend/package.json .
#COPY --from=build /frontend/package-lock.json .
#RUN npm ci --omit dev
#EXPOSE 3000
#CMD ["node", "."]
