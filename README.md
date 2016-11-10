# Django-Instant2FA

Example for using Instant2FA with Django's built-in authentication system.

## Requirements


* [Docker Compose](https://docs.docker.com/compose/install/) 1.8.0+
* Instant2FA API credentials. You can generate these at [https://dashboard.instant2fa.com](https://dashboard.instant2fa.com)

## Getting Started

1. Update the `ACCESS_KEY` and `ACCESS_SECRET` environment variables in
`docker-compose.yml` with your credentials

2. Start the container for the application with the `docker-compose up` command

3. At this point the application should be running at port `8000` on  your
Docker host. If you are using a Docker Machine VM, you can use the
`docker-machine ip MACHINE_NAME` command to get the IP address. If you're using
[Dinghy](https://github.com/codekitchen/dinghy) on OS X, you can access the
application at `mydjangoapp.docker/`.

4. Log in with username `admin` and password `password` and see how Instant2FA
works!

