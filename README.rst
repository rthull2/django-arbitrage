=====
Arbitrage
=====

Arbitrage is a simple Django app for finding arbitrage opportunities between crypto exchanges.


Quick start
-----------

1. Add "arbitrage" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'arbitrage',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('arbitrage/', include('arbitrage.urls')),

3. Run `python manage.py migrate` to create the models.

4. Run 'python manage.py exchanges' to create the default exchanges.

5. Run 'python manage.py namesymbols' to load all the coins on coinmarketcap.com

6. Run 'python manage.py scrape' to load the latest prices.


TODO:

Currently optimized for a single user; runs scrape for every page request. Tradeoff - 3 second page loads, latest data only when requested.  Should be updated to scrape every minute or 
so automatically.

The prices should not be stored in a relational database, given they are only stored for a minute or so, and then deleted/replaced.  

Walletstatus.py - On many exchanges, the only way to check their wallet statuses is to request a deposit address.  This requires having a personal API key/secret.
