# ogn-python

[![Build Status](https://travis-ci.org/Meisterschueler/ogn-silentwings.svg?branch=master)](https://travis-ci.org/Meisterschueler/ogn-silentwings)
[![Coverage Status](https://img.shields.io/coveralls/Meisterschueler/ogn-silentwings.svg)](https://coveralls.io/r/Meisterschueler/ogn-silentwings)

A database backend for the [Open Glider Network](http://wiki.glidernet.org/).
The ogn-python module saves all received beacons into a database with [SQLAlchemy](http://www.sqlalchemy.org/).
It connects to the OGN aprs servers with [python-ogn-client](https://github.com/glidernet/python-ogn-client).
It requires [PostgreSQL](http://www.postgresql.org/) and [PostGIS](http://www.postgis.net/).


## Installation and Setup
1. Checkout the repository

   ```
   git clone https://github.com/Meisterschueler/ogn-silentwings.git
   ```

2. Install python requirements

    ```
    pip install -r requirements.txt
    ```

3. Create database

    ```
    ./flask db.init
    ```


## License
Licensed under the [AGPLv3](LICENSE).
