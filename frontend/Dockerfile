FROM node:latest

RUN git clone --depth 1 https://github.com/AdventureLookup/adventurelookup-frontend.git /src

WORKDIR /src
RUN npm i

VOLUME /src/dist

CMD ["npm", "run", "dist"]
