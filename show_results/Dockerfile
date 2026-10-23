FROM node:22

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install
EXPOSE 5004

COPY . .

RUN useradd appuser
USER appuser

CMD ["node", "server.js"]