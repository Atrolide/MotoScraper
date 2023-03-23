# Moto Scraper

This is a python-based web scraper for car auction websites set up on Docker with a PostgreSQL database.<br>
Currently, it supports only one website: [otomoto.pl](https://otomoto.pl).

## Configuration

To use this scraper, you will need to download and install the following:

- [Python](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [PostgreSQL](https://www.postgresql.org/download/)

Once you have installed these dependencies, you can clone this repository and navigate to the project directory using the command line. Then, run the following command:

`docker-compose up --build`

This will set up a **PostgreSQL** and **Python** images as well as a full Postgres database configuration using **Docker**.

### Database Server Connection

To view the changes and send queries on our database, you need to connect to the server of a database that has just been created.<br>
To accomplish this, you can use a GUI tool like pgAdmin to configure the database.<br> 
First, [start your container](#starting-the-container).<br>
Then you can open pgAdmin.<br>
Next, you will need to add a new server in pgAdmin. <br>
To do this, click on `Servers` in the left sidebar, then click on `Register` -> `Server...`.<br>
Feel free to name the server as you wish! 

In the `Connection` tab, enter the following:

- Host: `localhost`
- Port: `5433`
- Username: `postgres`
- Password: `admin`

Then, click on the "Save" button to create the server. You should now be connected to the docker server. You should be able to see a database called `carprices` and a table called `cars`.

## Usage

### Stopping the container

If you want to stop the container and its server, using the command line navigate to the project directory. 
Then, run the following command:

`docker-compose down`

Or in **Docker Desktop** click on the `square(stop)` symbol next to your container

### Starting the container

If you want to start the container and its server, using the command line navigate to the project directory. 
Then, run the following command:

`docker-compose up`

Or in **Docker Desktop** click on the `arrow(start)` symbol next to your container

### Running the code

Now you can open the folder cloned from github as a project in your favourite IDE(I suggest PyCharm) and run the `main` file.
You should be able to see the same output in console as in your database.  

