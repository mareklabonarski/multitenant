FROM nginx:latest

RUN apt update && apt install inotify-tools -y

WORKDIR /entrypoint

COPY docker-entrypoint.sh /entrypoint
RUN chmod +x /entrypoint/docker-entrypoint.sh
COPY nginxReloader.sh /entrypoint
RUN chmod +x /entrypoint/nginxReloader.sh

ENTRYPOINT ["/entrypoint/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]