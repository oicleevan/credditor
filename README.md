# credditor

Social credit bot for Discord

## what is this?

This is a discord bot that acts as a social credit monitor for servers. It is a reference to the notorious Chinese social credit system, and memes generated around it.

Server admins and mods can add or remove a specific amount of social credit points at will, and users can see their score!!

## running

External python dependencies are required, to install, execute `pip -r DEPENDENCIES.txt`.

Run the query.sql in your mysql db, and insert your db's credentials in `src/credditor.py` (see database configuration).

To start the bot, simply clone the repository, navgate to the `src/` folder, and execute `python3 credditor.py {bot token}`.

The Discord bot token has to be presented at runtime for secutity purposes.

## contributing

Contributing is welcome and appreciated. All you have to do is submit a pull request!

Features I would like to add in the future are listed in [ROADMAP.md](ROADMAP.md). If you want features added, feel free to request it in there -- if I find it to be worth my time, I'll accept the commit and it'll be in the ROADMAP for me to stare at and eventually do something with!

All contributions are licensed under the MIT License, as with this project. By submitting a pull request, you agree with this stipulation.
