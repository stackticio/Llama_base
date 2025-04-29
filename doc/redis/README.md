# redis Documentation

**Table of content**

<!-- TOC -->
* [redis documentation](#-cookiecuttercomponentname--documentation)
    * [Component](#component)
        * [Overview](#overview)
        * [Component Key Features](#component-key-features)
        * [Stacktic - Ready to use](#stacktic---ready-to-use)
    * [Structure Overview](#structure-overview)
    * [debug](#debug)

<!-- TOC -->

## Component

### Overview

Redis is an in-memory storage solution that functions as a distributed, in-memory key-value database, cache, and message broker, with optional durability. It is integrated into the stack with source code links (such as Python) and automatically caches all links to databases like RabbitMQ, MongoDB, and PostgreSQL.

### Component Key Features

As you connect Redis to the source code, a cache_decorator.py file will be created to configure the caching with a fallback mechanism. Additionally, a redis_provider.py file will be created to authenticate to the Redis host using the configmap environment variables from our metadata.

### Stacktic - Ready to use

<img width="823" alt="image" src="https://github.com/user-attachments/assets/9a6fb41a-5734-4653-a3f4-884f443d5a58">

## Structure Overview

```
redis
├── cookiecutter.json
├── hooks
│   └── pre_gen_project.py
└── redis
    ├── helm
    │   ├── generate-yaml.sh
    │   └── helm-values.yaml
    ├── k8s
    │   └── deploy
    │       ├── base
    │       │   ├── secret
    │       │   │   └── redis-password
    │       │   ├── kustomization.yaml
    │       │   ├── namespace.yaml
    │       └── overlays
    │           └── dev
    │               └── kustomization.yaml
    └── scripts
        └── validate.sh
```

## debug 
validate caching 
```
assafsauer@Assafs-MacBook-Pro dev_tools % kubectl exec -it redis-master-0 -n redis -- sh               

$ redis-cli
127.0.0.1:6379> AUTH auth_password
OK
127.0.0.1:6379> monitor
OK
1721674118.983190 [0 10.108.2.112:41562] "AUTH" "(redacted)"
1721674118.983588 [0 10.108.2.112:41562] "CLIENT" "SETINFO" "LIB-NAME" "redis-py"
1721674118.984086 [0 10.108.2.112:41562] "CLIENT" "SETINFO" "LIB-VER" "5.0.7"
1721674118.984505 [0 10.108.2.112:41562] "GET" "3748b9042e02385400a89cbb1450ed11"
1721674119.058688 [0 10.108.2.112:41562] "SETEX" "3748b9042e02385400a89cbb1450ed11" "60" "[{\"key1\": \"value1\", \"key2\": \"value2\"}, {\"key1\": \"value1\", \"key2\": \"value2\"}]"
1721674122.363245 [0 127.0.0.1:35154] "AUTH" "(redacted)"


curl -iks https://python.apps.source-lab.io/greeting-mongodb/default_collector

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 76
Connection: keep-alive
X-RateLimit-Limit-Second: 100
RateLimit-Limit: 100
RateLimit-Remaining: 99
RateLimit-Reset: 1
X-RateLimit-Remaining-Second: 99
Server: Werkzeug/3.0.3 Python/3.12.4
Date: Mon, 22 Jul 2024 18:48:39 GMT
Access-Control-Allow-Origin: *
Access-Control-Expose-Headers: X-Custom-Header
X-Kong-Upstream-Latency: 108
X-Kong-Proxy-Latency: 2
Via: kong/3.7.1
X-Kong-Request-Id: cf89781c519cb96236bbec29dbb02448

[{"key1": "value1", "key2": "value2"}, {"key1": "value1", "key2": "value2"}]%                                             assafsauer@Assafs-MacBook-Pro ecom % 
```
