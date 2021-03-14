FROM node:15.11.0-alpine

WORKDIR /app
COPY . .

RUN npm install
RUN npm -g install serve

RUN npm run build

CMD serve -s build -l 4001
