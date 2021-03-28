# Microservice for files downloading

The microservice processes requests for downloading archives with files. It helps a main website that based on CMS. Files can be downloaded via FTP or through the CMS admin panel.

The archive makes on users demand without saving on server and directly stream to user computer for downloading.

From unauthorized access the archive is protected by hash in the downloading url. For example: `http://host.ru/archive/3bea29ccabbbf64bdebcc055319c5745/`. Hash set up by files directory name. The directory looks something like this:

```
- photos
    - 3bea29ccabbbf64bdebcc055319c5745
      - 1.jpg
      - 2.jpg
      - 3.jpg
    - af1ad8c76fda2e48ea9aed2937e972ea
      - 1.jpg
      - 2.jpg
```

## Installation

For correct microservice work needs Python not less 3.6 version.

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 server.py arguments
```

The service support following arguments:

- `-l`, `--log` - logging enabled (INFO level).
- `-d sec`, `--delay sec` - delay response time. Sec can be float number from 0 to 5.
- `-p`, `--path` - path to files main directory.

For example:

```bash
python3 server -l --delay 1 --path photos
```

Server launches on 8080 port and for checking service follow this link [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

## How to deploy on a server

```bash
python3 server.py
```

After this redirect requests to this microservice, which beginning with `/archive/`. For example:

```
GET http://host.ru/archive/3bea29ccabbbf64bdebcc055319c5745/
GET http://host.ru/archive/af1ad8c76fda2e48ea9aed2937e972ea/
```

## License

You can copy, distribute and modify the software.

## Motivation

This project was created as part of online course for web developer [Devman](https://dvmn.org).
