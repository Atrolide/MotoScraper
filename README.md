# Moto Scraper

This is a python-based web scraper for car auction websites set up on Docker with a PostgreSQL database.<br>
Currently, it supports only one website: [otomoto.pl](https://otomoto.pl).

## Usage

To use this scraper, you will need to download and install the following:

- [Python](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [PostgreSQL](https://www.postgresql.org/download/)

Once you have installed these dependencies, you can clone this repository and navigate to the project directory using the command line. Then, run the following command:

`docker-compose up --build`

This will set up a PostgreSQL database and python container based on the built Docker image.

### Database Configuration

To configure the database, you can use a GUI tool like pgAdmin to configure the database. Once the containers are running, you can open pgAdmin.
Next, you will need to add a new server in pgAdmin. To do this, click on `Servers` in the left sidebar, then click on `Register` -> `Server...`.
Feel free to name the server as you wish! 

In the `Connection` tab, enter the following:

- Host: `localhost`
- Port: `5433`
- Username: `postgres`
- Password: `admin`

Then, click on the "Save" button to create the server. You should now be connected to the docker server. You should be able to see a database called `carprices` and a table called `cars`.

### Running the code

Now you can open the folder cloned from github as a project in your favourite IDE(I suggest PyCharm) and run the `main` file.
You should be able to see the same output in console as in your database.  




