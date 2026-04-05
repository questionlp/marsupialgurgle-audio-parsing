# Marsupial Gurgle Audio Clip Parsing Tool

This repository contains a Python script that's used to parse through a collection of [Marsupial Gurgle](https://marsupialgurgle.com/) audio clips, reads in audio tag metadata and stores the information a pair of MySQL database tables.

The first table, `clips`, is used to store file name and path information and flags to signify if there are MP3, MPEG-4 and/or MPEG-4 ringtone versions of each clip.

The second table, `tags`, is used to store data from each clip's metadata, including artist, album, title and year. The album and title columns are indexed for full-text search.

**Note:** The primary version of this repository now resides on Codeberg as [marsupialgurgle-audio-parsing](https://codeberg.org/qlp/marsupialgurgle-audio-parsing). The GitHub repository is now a mirror of the Codeberg repository.

## Code of Conduct

This project follows version 3.0 of the [Contributor Covenant's](https://www.contributor-covenant.org) Code of Conduct ([CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)).

## License

This project is licensed under the terms of the [MIT License](LICENSE).
