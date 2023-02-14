# edyta-web-be

## Configure `.env` file
1. Create `.env` file in project root or append to `.env` file following content

	```
    # Database
	DB_ENGINE=MYSQL # supported engines: MYSQL
    DB_HOST=<host> # e.g. 127.0.0.1
	DB_USER=<user> # e.g. john
	DB_PASSWD=<password> # e.g. doe123!
    DB_DATABASE=<database> # e.g. edyta

    # Message Broker
    MESSAGE_BROKER_ENGINE=RabbitMQ # supported engines: RabbitMQ
    MESSAGE_BROKER_HOST=<host> # e.g. 127.0.0.1
    MESSAGE_BROKER_USER=<user> # e.g. john
    MESSAGE_BROKER_PASSWORD=<password> # e.g. doe12345!

    ## Message Broker Queue names
    MESSAGE_BROKER_QUEUE_REGISTRATION_EMAIL=<queue-name> # e.g. registration-email
    MESSAGE_BROKER_ENTITY_IS_PUBLIC_STATUS=<queue-name> # e.g. entity-is-public-status

    # JWT Secret token
    JWT_SECRET=<jwt_secret_token> # how to is described down below
    JWT_EXPIRES_IN_SECONDS=<seconds> # e.g. 604800 # 7 days

    # Threshold
    USER_MANAGEMENT_ROLE_MIN_COUNT=<count> # e.g. 2

    # Application
    APP_REGISTRATION_BY_KEY_URL=<registration_url> # ! NOTE: the registration URL must end with the slash ! # e.g. http://app.edyta.cz/user/registration/key/ 
	```

## How to generate JWT_SECRET token

1. Create `jwt_token_generator.js` file with following content

    ```
    console.log(require('crypto').randomBytes(64).toString('hex'));
    ```

2. Perform following command in terminal

    `> node ./jwt_token_generator.js`