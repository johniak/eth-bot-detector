# Ethereum Bot Detector
## Stack + Technologies

- Python
- Faust
- Kafka
- Tortoise ORM
- PostgreSQL
- Firebase Cloud Messaging
- Docker + docker-compose
- web3 API
- ✨Magic ✨

## Description 
This project is total overkill to naive ethereum bot detection task. 
## Functions
1. Detect bot based on trashold, in selected window
2. Registering FCM tokens into database
3. Sending FCM push notifications (added simple debounce based on address with time specified in settings)

## How to run
 1. Create `.env` file based on `.env.example`, and fill empty fields
 2. ```bash
    $ docker-compose run app faust -A bot_detector.app init-database
    ```
3. ```bash
    $ docker-compose up
    ```
The whole stack is now running.

API can be accesed through http://localhost:6066
