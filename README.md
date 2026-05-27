# Condomicio

Welcome on board team Condomicio.

### QuickStart using Docker
Clone the repository and move onto the new folder and be sure you're using the development branch.
run ```source stack/local/local.env && docker-compose --project-directory ${COMPOSE_BASE_DIRECTORY} -f stack/local/docker-compose.yaml up --force-recreate --build -d```; 
and wait it to finish. Please then log in to the new container with ```docker exec -it django.condomicio bash```

You should be able to run the Django instance by running ```. ./stack/local/django/dryRun.sh```