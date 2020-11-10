# B3 CDI Curve by Fluxonaut

This repo contains a Python script that extracts, consolidates and interpolates data from the Brazilian CDI Curve provided on the B3 Exchange web site.
It allows you to produce a historical data series for any given duration (considering it respects the maximum available duration). It stores all the term structure of the CDI curve in a local SQLite database as well.

## Setup

This repo contains a requirements.txt file with all the required dependencies. 
It was built and tested with Python 3.7.4.
Use pip to download the dependencies you'll need (more about pip and requirements.txt). 

```bash
pip install -r requirements.txt
```
## Usage

The script contains two "major" methods:

#### update_db

This method loops through all the dates between the start and end dates looking for the prices on the B3 web site. It generates and saves a SQLite database (located on ./output/cdi.db).

It has a 2 seconds minimum delay between each hit to prevent generating too many requests. This means that the first time you run this script, it'll take quite some time to get all the files. 

**The first run takes around two and half hours to build the database (respecting the minimum delay for requests) and it takes around 1.3 GB of disk space.**

After it runs once, it'll check for the last inserted date, so it'll look only for working days after the last update. This keeps the database updated for each time you run the code.



#### create_time_series

```python
create_time_series(db_conn: sqlite3.Connection, duration: int)
```

This method queries the database to produce a Pandas DataFrame with the historical series of the requested duration. It then saves it as a CSV file on the ./output/ folder.
**The second parameter of the method is where you input your desired duration.**


## Contributing
Pull requests are welcome. Please open an issue first to discuss what you would like to change.

## To-do
- [ ] Tests
- [ ] Optimize db size
- [ ] Create package from script


## Fluxonaut
This code was made possible by the amazing people working at Fluxonaut who dedicated their free time to help the community. Please be sure to check our our website at https://fluxonaut.com.

## License
This project is under the [MIT](https://opensource.org/licenses/MIT) license.

