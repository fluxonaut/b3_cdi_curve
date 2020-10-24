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
