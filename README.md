# CFLBot 3.0

A game thread bot for /r/CFL

## Prerequisites

- See [setip.py](./setup.py) for instructions on getting a refresh token

## Setup
You must define your configuration with the following format:

```json
{
    "database": {
        "databaseName": ""
    },
    "cfl": {
        "baseUrl": "https://cflscoreboard.cfl.ca/json/scoreboard/",
        "apiKey": ""
    },
    "reddit": {
        "clientId": "",
        "clientSecret": "",
        "userAgent": "",
        "refreshToken": "",
        "subreddit": ""
    },
    "pregame": false,
    "pregameMinutes": 360,
    "gameMinutes": 60,
    "postgame": false,
    "tz": "America/Toronto"
}
```

## Running the bot

## As script

`data/` must be created in your project's root directory

`python main.py <path-to-config-file>`

## With docker-compose

`config/` & `data/` must be created alongside your docker-compose.yaml file.

Here is a suggested docker-compose.yaml:

```yaml
version: "3.9"

services:
  bot:
    container_name: cflbot3
    image: cflbot3
    volumes:
      - ./config:/config
      - ./data:/data
    deploy:
      restart_policy:
        condition: any

```