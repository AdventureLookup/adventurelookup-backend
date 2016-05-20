# Getting started

The development environment makes use of Docker and two associated tools:

- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Machine](https://docs.docker.com/machine/)

If you are using OS X or Windows, you will need the
[Docker Toolbox](https://www.docker.com/products/docker-toolbox). If you are
on a native Linux platform, you can download the two tools indidivually
[here](https://docs.docker.com/compose/install/) and
[here](https://docs.docker.com/machine/install-machine/).

The package comes with a default `dev.env` that can be copied/renamed to `.env`
and used as-is.

Once you have the tools installed follow these steps:

1. Create a virtual machine to host the containers:

        docker-machine create -d virtualbox dev

   > You can call the machine anything you want, but we'll be using `dev`

2. Set up your shell to use to make use of the machine:

        // Windows
        @FOR /f "tokens=*" %i IN ('docker-machine env dev') DO @%i

        // OS X / Linux
        eval $(docker-machine env dev)

3. Build the virtual machines from the base images (takes a while):

        docker-compose build

4. Start the virtual machines:

        docker-compose up -d

   > The `-d` flag means we'll be running it as a daemon. If you want to
   > run it in the foreground (handy to get direct log output), omit the -d
   > To get log output otherwise, run `docker-compose logs`

5. To stop the virtual machines again, run:

        docker-compose down

You now have the base setup up and running. However, no database tables or
content has been setup and the static files have not been collected. We'll do
this now:

> On Windows, using `docker-compose run` allows only for non-interactive mode
> mandated by the `-d` flag. If you want to see the output of your commands
> (without running the log command), you can do run the following command:
>
> `docker exec <container> <command>`
>
> Note that the container is the full name of the container, in my case it is
> `adventurelookupbackend_web_1`.

1. Run migrations to set up the database structure:

        docker-compose run -d web python manage.py migrate

2. Add the initial superuser:

        docker-compose run -d web python initial_setup.py

   > This will setup the default superuser `admin` with the password `admin`.
   > You can alter `initial_setup.py` if you would like a different setting.

3. Collect all the static files to serve in one central folder:

        docker-compose run -d web python manage.py collectstatic --noinput

Once all of this is done, you should be up and running.
