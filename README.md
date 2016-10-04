# Latent Heat Properties of Substances

Web API that serves Heat of Fusion and Vaporization for Elements and Inorganic Compounds
Demonstration project utilizes:
 
 * [Docker](https://docs.docker.com/)
 * [Flask](http://flask.pocoo.org/)
 * [Flask-Restful](http://flask-restful-cn.readthedocs.io/en/0.3.5/)
 * [SqlAlchemy(Declarative)](http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html)
 
### Getting Started

Clone from github
> git clone https://github.com/katerina7479/heat_properties.git 
 

### Running locally

Includes a makefile with the following commands:

Start a server locally with:
> make server

Remove any and all docker containers:
> make clean

**Explore the API**

The API can be reached in the browser, using json-api style queries, e.g.:

> localhost:5000/latent_heats/?filter[melting_point__gte]=100&page[limit]=10

> localhost:5000/substances/122/

### Running tests

Run Tests and style:
> make test

> make style

This project requires some starting data. To make it easier to
enter, you can parse the data into database fixtures from fixtures/data.text file
with:
> make set-fixtures

### Contributing

Submit a [pull request!](https://help.github.com/articles/creating-a-pull-request/)

### References

* Perry, Robert H., Don W. Green, and James O. Maloney. 
"Latent Heats - Table 2-190", Perry's Chemical Engineers' Handbook. 
7th ed. New York, NY: McGraw-Hill, 1997. 2-151--153. Print.
