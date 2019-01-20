# Arbitrage

Arbitrage is a simple Django app for finding arbitrage opportunities between crypto exchanges.

## Getting Started

If you have Docker and Docker Compose installed, you should be able to get everything up and running using
```
docker-compose up --build
```

and then going to localhost:8000


## Todo

Currently optimized for a single user; runs scrape for every page request. Tradeoff - 3 second page loads, latest data only when requested. Should be updated to scrape every minute or so automatically.

The prices should not be stored in a relational database, given they are only stored for a minute or so, and then deleted/replaced.

Walletstatus.py - On many exchanges, the only way to check their wallet statuses is to request a deposit address. This requires having a personal API key/secret.
