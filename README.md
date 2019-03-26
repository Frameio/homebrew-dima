
# DIMA

A command-line tool to list, inspect and kill database queries.

We've been using this tool since 2017 at Frame.io and decided to open source it. There will be a blog post with more details on the Frame.io Engineering Blog soon. Previous git history has been wiped by our security team.

# Setup:

1. Clone this repo
2. Set up the credentials (see below)
3. Run: `sudo ./deploy.sh`

(homebrew setup is being worked on)

# Credential Setup

Database credentials can be provided in 2 ways - in a `~/.dima_creds` file or as environment variables. DIMA will look first for the environment variables, and then to the creds file. You can set the following environment variables:

	DIMA_DB_DBNAME
	DIMA_DB_USER
	DIMA_DB_HOST
	DIMA_DB_PORT
	DIMA_DB_PASSWORD

or place them in a `~/.dima_creds` file (the prefix `~/` means that it should be in your home directory). A sample file `sample_creds` is in this repo. 

You can add more credentials for different databases underneath, as long as they use a different prefix. E.g.

	DIMA_DB2_DBNAME
	DIMA_DB2_USER
	...

To inspect a non-default DB, use the `-c` option, e.g. for a prefix `DIMA_DB2_...` use:

	dima -c DB2 show 123

# Usage:

	dima
Shows a list of running queries

	dima show [PID]
Inspects a specific running query

	dima rm [-f] [Lock / filter keyword / PID]	

Terminates queries either with `wait_event_type` "Lock" or according to a filter keyword or PID. Use -f to avoid the confirmation.

# Screenshots

<img src="https://github.com/Frameio/homebrew-dima/raw/master/img/dima_cmd.png" alt="dima command" width="500"/>
<img src="https://github.com/Frameio/homebrew-dima/raw/master/img/dima_show_cmd.png" alt="dima show command" width="500"/>
<img src="https://github.com/Frameio/homebrew-dima/raw/master/img/dima_rm_cmd.png" alt="dima rm command" width="500"/>

