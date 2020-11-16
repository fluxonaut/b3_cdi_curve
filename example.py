import b3cdi

# Create and/or update local DB
b3cdi.update_db()

# Create time series for the desired duration
b3cdi.create_time_series(360)

print("> end")