FROM node:14-alpine

WORKDIR /app

COPY ./source/package*.json ./

RUN npm install
RUN npm run build

COPY ./source/ ./

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]