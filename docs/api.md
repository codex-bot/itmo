# @itmoabitbot API

This documentation describes programming interface (basic rules and available methods) for Abit Itmo Server.

## Basic rules

All responses JSON-format and should contain the following fields:

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

If error was occured `success` field should be equal `false`. Error message should be passed in `message` field in `data` object. Check out an example below.

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

List of available methods with descriptions, described params and examples.

- [getUser](#getUser)
- [getUserPositions](#getUserPositions)
- [getProgramsByScores](#getProgramsByScores)

### getUser

Return User's data by unique identifier.

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

Return User's positions in ratings.

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
| `program`  | string | Program's name                 |
| `position` | number | User's position                |
| `users`    | number | Total number of requests       |
| `value`    | number | Program's budget places number |

```json
{
  "success": true,
  "data": [
    {
      "program": "Прикладная и компьютерная оптика",
      "position": 13,
      "users": 67,
      "value": 120
    },
    {
      "program": "Световая инженерия",
      "position": 88,
      "users": 430,
      "value": 25
    },
    {
      "program": "Интеллектуальная робототехника",
      "position": 17,
      "users": 125,
      "value": 56
    },
    {
      "program": "Лазерные технологии",
      "position": 5,
      "users": 27,
      "value": 25
    }
  ]
}
```

### getProgramsByScores

Return list of programs for target scores. Programs should be ordered according to the complexity of entering from the lowest to the highest.

> More info will be added soon
