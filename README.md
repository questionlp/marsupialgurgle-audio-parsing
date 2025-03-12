# Marsupial Gurgle Audio Clip Parsing Tool

This repository contains a Python script that's used to parse through a collection of [Marsupial Gurgle](https://marsupialgurgle.com/) audio clips, reads in audio tag metadata and stores the information a pair of MySQL database tables.

The first table, `clips`, is used to store file name and path information and flags to signify if there are MP3, MPEG-4 and/or MPEG-4 ringtone versions of each clip.

The second table, `tags`, is used to store data from each clip's metadata, including artist, album, title and year. The album and title columns are indexed for full-text search.

## Code of Conduct

This project follows version 2.1 of the [Contributor Covenant's](https://www.contributor-covenant.org) Code of Conduct ([CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)).

## License

This project is licensed under the terms of the [MIT License](LICENSE).
