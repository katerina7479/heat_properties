# Latent Heat Properties of Substances

Web API that serves Heat of Fusion and Vaporization for Elements and Inorganic Compounds
Demonstration project utilizes:
 
 * [Docker](https://docs.docker.com/)
 * [Flask](http://flask.pocoo.org/)
 * [Flask-Restful](http://flask-restful-cn.readthedocs.io/en/0.3.5/)
 * [SqlAlchemy(Declarative)](http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html)
 
### Getting Started

Clone from github
> git clone 

### Running locally

Includes a makefile with the following commands:

Start a server locally with:
> make server

Remove any and all docker containers:
> make clean


### Running tests

Run Tests and style:
> make test

> make style

This project requires some starting data. To make it easier to
enter, you can parse the data into database fixtures from fixtures/data.text file
with:
> make set-fixtures

### Contributing

Submit a pull request!

### References

* Perry's Chemical Engineering Handbook

