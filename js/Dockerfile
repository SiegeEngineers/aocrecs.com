FROM node as build-deps
WORKDIR /usr/src/app
COPY package.json yarn.lock ./
RUN yarn
COPY public ./public
COPY src ./src
RUN REACT_APP_API="/api" yarn build

FROM nginx
COPY aocrecs.conf /etc/nginx/conf.d/default.conf
COPY --from=build-deps /usr/src/app/build /usr/share/nginx/html
