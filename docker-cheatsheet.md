# 🐳 Docker CLI Cheat Sheet

## Most Common Commands
```
docker ps                   # List running containers
docker images               # List local images
docker run -it <image>      # Run container interactively
docker stop <id|name>       # Stop a running container
docker rm <id|name>         # Remove a container
docker rmi <image>          # Remove an image
docker pull <image>         # Pull image from Docker Hub
docker exec -it <id|name> bash  # Exec bash in running container
docker logs <id|name>       # Show container logs
docker build -t myimg .               # Build image from Dockerfile

```

---

## System Info
```
docker version                # Show Docker client & server version
docker info                   # Show system-wide information
docker run hello-world        # Test Docker installation
```

## Image Commands
```
docker search <image>         # Search images on Docker Hub
docker pull <image>           # Download image from Docker Hub
docker images                 # List local images
docker rmi <image>            # Remove local image
docker tag <img> user/img:tag # Tag image for push
docker push <image>           # Push image to Docker Hub
```

## Container Commands
```
docker run -it <img>                  # Run container interactively (with bash)
docker run -d <img>                   # Run container in detached mode
docker run --name myapp <img>         # Run with custom name
docker run -p 8080:80 <img>           # Map host:container ports
docker run -v vol:/data <img>         # Attach volume
docker run -e VAR=val <img>           # Set environment variable
docker ps                             # List running containers
docker ps -a                          # List all containers
docker stop <id|name>                 # Stop container
docker start <id|name>                # Start stopped container
docker restart <id|name>              # Restart container
docker rm <id|name>                   # Remove stopped container
docker exec -it <id|name> bash        # Exec bash in running container
docker logs <id|name>                 # Show container logs
docker inspect <id|name>              # Show detailed config (JSON)
```

## Build, Tag & Cleanup
```
docker build -t myimg .               # Build image from Dockerfile
docker tag myimg myrepo/img:tag       # Tag image
docker builder prune                  # Clean build cache
docker volume prune                   # Remove unused volumes
docker system prune                   # Remove unused data
docker system prune -a                # Remove all unused images, containers, networks
```

## Volumes
```
docker volume ls                      # List volumes
docker volume create myvol            # Create volume
docker volume inspect myvol           # Inspect volume
docker volume rm myvol                # Remove volume
```

## Networks
```
docker network ls                     # List networks
docker network create mynet           # Create network
docker network rm mynet               # Remove network
docker network connect mynet cont     # Connect container to network
docker network disconnect mynet cont  # Disconnect container from network
```

## Login & Logout
```
docker login                          # Login to Docker Hub
docker logout                         # Logout from Docker Hub
docker login -u <username> -p <pwd>   # Login with credentials
docker info | grep Username           # Check login status
```

---

# 🛠️ Docker Compose

## Compose Basics
```
docker compose up                     # Start all services
docker compose up -d                  # Start in detached mode
docker compose down                   # Stop and remove services, networks, volumes
docker compose start                  # Start existing services
docker compose stop                   # Stop services
docker compose up --build             # Rebuild and start
```

## Compose Example
```yaml
version: "3.8"
services:
  mongo:
    image: mongo
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: qwerty
  mongo_express:
    image: mongo-express
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: qwerty
      ME_CONFIG_MONGODB_URL: "mongodb://admin:qwerty@mongo:27017"
```

---

# 📦 Docker Volumes

## Volume Types
- **Bind Mount**
  - Syntax: `docker run -v /host/path:/container/path <image>`
  - Use case: Development, config injection
  - Location: Host path
- **Named Volume**
  - Syntax: `docker run -v myvol:/container/path <image>`
  - Use case: Persistent, production data
  - Location: `/var/lib/docker/volumes/myvol/_data`
- **Anonymous Volume**
  - Syntax: `docker run -v /container/path <image>`
  - Use case: Temporary, short-lived data
  - Location: `/var/lib/docker/volumes/random_id/_data`

## Compose Volume Example
```yaml
version: "3.8"
services:
  app:
    image: ubuntu
    volumes:
      - myvol:/test/data
      - ./localdir:/containerdir
volumes:
  myvol:
```

---

# 📝 Dockerfile Examples

## Node App
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

## Python App
```dockerfile
FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

# 🌐 Docker Networks

## Network Types
- **bridge** (default)
  - Isolation: Yes
  - Use case: Default, multi-container apps
  - Example: `docker run --network bridge ...`
- **host**
  - Isolation: No
  - Use case: High performance, host services
  - Example: `docker run --network host ...`
- **none**
  - Isolation: Full
  - Use case: Security, no network needed
  - Example: `docker run --network none ...`

## Custom Bridge Example
```
docker network create my_custom_net
docker run -d --name app1 --network my_custom_net nginx
docker run -d --name app2 --network my_custom_net alpine sleep 1000
# app1 and app2 can communicate via container names
```

---

# 🧹 System Cleanup
```
docker system prune                # Remove unused containers, images, networks
docker system prune -a             # Remove all unused images
docker volume prune                # Remove unused volumes
```

---

# 📝 Dockerfile vs Compose
- **Dockerfile**: Build instructions for custom image. Used for single app/service image creation.
- **docker-compose.yaml**: Orchestrate multiple containers/services. Define images, build, env, ports, volumes, networks.

---

# 🔥 Tips & Troubleshooting
```
pkill -f docker-desktop              # Kill Docker Desktop process (Linux)
/opt/docker-desktop/bin/docker-desktop &  # Restart Docker Desktop
```

---

# 📚 Reference
- [Official Docs](https://docs.docker.com/)
- [Compose Docs](https://docs.docker.com/compose/)
- [CLI Reference](https://docs.docker.com/engine/reference/commandline/docker/)
