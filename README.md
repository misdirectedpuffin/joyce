## Flask Minimal

A minimal example of a flask app running locally in docker with gunicorn.

#### Develop
```
$ docker-compose up --build
```

#### Build
Run the entire build pipeline locally.
```
$ drone exec
```

#### Test

Unit tests can be run locally in a virtualenv

```
$ make unit
```

#### Deploy

### Prerequisites

Before deploying your service, you must create

1. Cloudwatch logs group
2. Application Load Balancer listener rule.

The listener rule defines the routing conditions for your service. Make sure to edit the `HealthCheckPath` property of `TargetGroup` and the `path-pattern` value in the listener rule.

Update the `awslogs-group` attribute of `deploy.yml`. This should be in the format `<environment>-<service name>`.
