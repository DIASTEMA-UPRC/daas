# daas
The Diastema DaaS service. This service is responsible for handling requests for time-consuming data processes.

## How to Use
This project is inteded to by used by [the DaaS API](https://github.com/DIASTEMA-UPRC/daas-api). If you need information on what operations are supported, please check out that documentation. If you need to run this in isolation, follow the steps below:

### Prerequisites
+ Docker
+ RabbitMQ
+ Mongo
+ MinIO
+ [Diastema DaaS API](https://github.com/DIASTEMA-UPRC/daas-api)

### How to Build
```bash
docker build -t daas:latest .
```

### How to Run
The dev Docker-compose creates an isolated environment and you can check results via the MinIO web UI. Other than that you can simply run the service exactly how its described below and perform your requests

```bash
docker-compose up
```

## License
Licensed under the [Apache License Version 2.0](README) by [Konstantinos Voulgaris](https://github.com/konvoulgaris) for the research project Diastema
