# @itmoabitbot API

[Version v1.1](#Changelog)

This documentation describes programming interface (basic rules and available methods) for Abit Server.

## Basic rules

All responses should be in JSON-format and contain the following fields:

| Field     | Type    | Description     |
|-----------|---------|-----------------|
| `success` | boolean | response result |
| `data`    | object  | response data   |


```json
{
  "success": true,
  "data": {
    ...
  }
}
```

### On errors

If error was occured `success` field should be equal `false`. Error message should be passed by `message` field at `data` object. Check out an example below.

```json
{
  "success": false,
  "data": {
    "message": "User does not exist"
  }
}
```

## Security

Bot can send requests with specific header to be authorized.

## Methods

List of available methods with descriptions, params and examples.

- [getUser](#getUser)
- [getUserPositions](#getUserPositions)
- [getProgramsByScores](#getProgramsByScores)

### getUser

Return User's data by identifier.

#### Request

`GET` request

| Field | Type   | Description       |
|-------|--------|-------------------|
| `id`  | string | User's identifier |

```
/getUser?id=227833
```

#### Response

| Field    | Type   | Description             |
|----------|--------|-------------------------|
| `name`   | string | User's name and surname |
| `scores` | array  | User's exams results    |

Each element in `scores` is an object with the following fields.

| Field     | Type   | Description       |
|-----------|--------|-------------------|
| `subject` | string | Subject name      |
| `score`   | number | User's exam score |

```json
{
  "success": true,
  "data": {
    "name": "Андрей Федотов",
    "scores": [
      {
        "subject": "Математика",
        "score": 89
      },
      {
        "subject": "Русский язык",
        "score": 93
      },
      {
        "subject": "Информатика",
        "score": 100
      },
      {
        "subject": "Физика",
        "score": 67
      }
    ]
  }
}
```

### getUserPositions

Return User's positions in ratings. Programs are sorted by User's priorities. 

#### Request

`GET` request

| Field | Type   | Description       |
|-------|--------|-------------------|
| `id`  | string | User's identifier |

```
/getUserPositions?id=227833
```

#### Response

Array of program's data contains elements with fields:

| Field      | Type   | Description                    |
|------------|--------|--------------------------------|
| `id`       | number | Program's ID                   |
| `program`  | string | Program's name                 |
| `position` | number | User's position                |
| `users`    | number | Total number of requests       |
| `value`    | number | Program's budget places number |

```json
{
  "success": true,
  "data": [
    {
      "id": 10555,
      "program": "Прикладная и компьютерная оптика",
      "position": 13,
      "users": 67,
      "value": 120
    },
    {
      "id": 10563,
      "program": "Световая инженерия",
      "position": 88,
      "users": 430,
      "value": 25
    },
    {
      "id": 10559,
      "program": "Интеллектуальная робототехника",
      "position": 17,
      "users": 125,
      "value": 56
    },
    {
      "id": 10596,
      "program": "Лазерные технологии",
      "position": 5,
      "users": 27,
      "value": 25
    }
  ]
}
```

### getProgramsByScores

Return list of programs for target scores.

<!-- Programs should be ordered according to the complexity of entering from the lowest to the highest. -->

> More info will be added soon.

<!--

#### Request

`GET` request

| Field    | Type   | Description                        |
|----------|--------|------------------------------------|
| `scores` | string | JSON-encoded list of score objects |

```
/getProgramsByScores?scores=%5B%7B%22subject%22%3A+%22%5Cu041c%5Cu0430%5Cu0442%5Cu0435%5Cu043c%5Cu0430%5Cu0442%5Cu0438%5Cu043a%5Cu0430%22%2C+%22score%22%3A+89%7D%2C+%7B%22subject%22%3A+%22%5Cu0420%5Cu0443%5Cu0441%5Cu0441%5Cu043a%5Cu0438%5Cu0439+%5Cu044f%5Cu0437%5Cu044b%5Cu043a%22%2C+%22score%22%3A+93%7D%2C+%7B%22subject%22%3A+%22%5Cu0418%5Cu043d%5Cu0444%5Cu043e%5Cu0440%5Cu043c%5Cu0430%5Cu0442%5Cu0438%5Cu043a%5Cu0430%22%2C+%22score%22%3A+100%7D%2C+%7B%22subject%22%3A+%22%5Cu0424%5Cu0438%5Cu0437%5Cu0438%5Cu043a%5Cu0430%22%2C+%22score%22%3A+67%7D%5D
```

-->

## Changelog

### v1.1

_Revision date: 29 Jun 2018_

Added field `id` to each Program in response for [getUserPositions](#getUserPositions) method and define sorting.

<!-- Added new method [getProgramsByScores](#getProgramsByScores). -->

### v1.0 

_Revision date: 19 Jun 2018_

Initial version