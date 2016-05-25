# adventurelookup

[![Build Status](https://travis-ci.org/AdventureLookup/adventurelookup-backend.svg?branch=master)](https://travis-ci.org/AdventureLookup/adventurelookup-backend) [![codecov](https://codecov.io/gh/probably-not-a-cat/adventurelookup-backend/branch/master/graph/badge.svg)](https://codecov.io/gh/probably-not-a-cat/adventurelookup-backend)

A searchable tool, AdventureLookup.com, that will allow Dungeon Masters to find the adventure they're looking for.


# Getting started

The development environment makes use of Docker and two associated tools:

- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Machine](https://docs.docker.com/machine/)

If you are using OS X or Windows, you will need the
[Docker Toolbox](https://www.docker.com/products/docker-toolbox). If you are
on a native Linux platform, you can download the two tools individually
[here](https://docs.docker.com/compose/install/) and
[here](https://docs.docker.com/machine/install-machine/).

## Env
There is an `.env` file where you can tweak the settings for the project. (Recommended for production)

Once you have the tools installed follow these steps:

1. Create a virtual machine to host the containers:

        docker-machine create -d virtualbox dev

   > You can call the machine anything you want, but we'll be using `dev`

2. Set up your shell to use to make use of the machine:

        // Windows
        @FOR /f "tokens=*" %i IN ('docker-machine env dev') DO @%i

        // OS X / Linux
        eval $(docker-machine env dev)

3. Build the containers:

        docker-compose -f docker-compose.yml -f dev.yml build

4. Start the containers:

        docker-compose -f docker-compose.yml -f dev.yml up -d

   > The `-d` flag means we'll be running it as a daemon. If you want to
   > run it in the foreground (handy to get direct log output), omit the -d
   > To get log output otherwise, run `docker-compose logs`

You now have the base setup up and running. The application will auto-reload
when code changes, so you can see your changes live.

To check that everything is running smoothly, you can run `docker-compose ps`
and your output should look similar to this:

    Name                         Command               State                    Ports
    --------------------------------------------------------------------------------------------------------------
    adventurelookup_nginx_1      nginx -g daemon off;             Up      0.0.0.0:443->443/tcp, 0.0.0.0:80->80/tcp
    adventurelookup_postgres_1   /docker-entrypoint.sh postgres   Up      0.0.0.0:5432->5432/tcp
    adventurelookup_web_1        /usr/local/bin/gunicorn ad ...   Up      0.0.0.0:8000->8000/tcp

However, no database tables or content has been setup and the static files have
not been collected. We'll do this now:

> On Windows, using `docker-compose run` allows only for non-interactive mode
> mandated by the `-d` flag. If you want to see the output of your commands
> (without running the log command), you can do run the following command:
>
> `docker exec adventure-lookup_web_1 <command>`
>
> For OS X and Linux, you can simply omit the `-d` to see the output as the
> command is run.
>
> The following commands should be run while your containers are up -
> among other things, the commands need database access to take effect.

1. Run migrations to set up the database structure:

        docker-compose run --rm -d web python manage.py migrate

2. Add the initial superuser:

        docker-compose run --rm -d web python initial_setup.py

   > This will setup the default superuser `admin` with the password `admin`.
   > You can alter `initial_setup.py` if you would like a different setting.

3. (Optional) Collect all the static files to serve through nginx:

   > If you are just using gunicorn directly at :8000, this is not necessary.
   > However, if you are accessing the site through nginx at :80, it will need
   > this command to serve static files.

        docker-compose run --rm -d web python manage.py collectstatic --noinput

Once all of this is done, you should be up and running. To see the site, go
to the `dev` machine IP at port 8000 (or port 80 to test through nginx).
