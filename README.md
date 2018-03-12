# ogn-silentwings

[![Build Status](https://travis-ci.org/Meisterschueler/ogn-silentwings.svg?branch=master)](https://travis-ci.org/Meisterschueler/ogn-silentwings)
[![Coverage Status](https://img.shields.io/coveralls/Meisterschueler/ogn-silentwings.svg)](https://coveralls.io/r/Meisterschueler/ogn-silentwings)

A connector between  [Open Glider Network](http://wiki.glidernet.org/) and [Silent Wings](http://www.silentwings.no).
The ogn-silentwings module saves all received beacons into a database with [SQLAlchemy](http://www.sqlalchemy.org/).
It connects to the OGN aprs servers with [python-ogn-client](https://github.com/glidernet/python-ogn-client).


## Installation and Setup
1. Checkout the repository

   ```
   git clone https://github.com/Meisterschueler/ogn-silentwings.git
   ```

2. Install python requirements

    ```
    pip install -r requirements.txt
    ```


## License
Licensed under the [AGPLv3](LICENSE).
