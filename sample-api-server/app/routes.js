'use strict';

/**
 * Prepare response data object
 *
 * @param {boolean} success
 * @param {Object} data
 */
const makeResponse = (data, success = true) => {
  return {
    success: success,
    data: data
  };
};

/**
 * Process getUser route
 */
const getUser = (req, res) => {
  let userId = req.query.id;

  /**
   * Return error if userId is missing
   */
  if (!userId) {
    let message = "No id query param was found";

    res.json(makeResponse({message}, false))
  }

  /** @todo find user in DB */

  /**
   * User data to be returned
   */
  let user = {
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
  };

  /**
   * Return data
   */
  res.json(makeResponse(user));
}

/**
 * Process getUserPositions route
 */
const getUserPositions = (req, res) => {
  let userId = req.query.id;

  /**
   * Return error if userId is missing
   */
  if (!userId) {
    let message = "No id query param was found";

    res.json(makeResponse({message}, false))
  }

  /** @todo find user's positions in DB */

  /**
   * Positions data to be returned
   */
  let positions = [
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
  ];

  /**
   * Return data
   */
  res.json(makeResponse(positions));
};

/**
 * Process getUserPositions route
 */
const getProgramsByScores = (req, res) => {
  /** @todo get scores and find programs in DB */

  /**
   * Programs data to be returned
   */
  let programs = [
    {
        "name": "Информатика и программирование",
        "id": 10555,
        "score": 309,
        "requests": 391,
        "value": 121
    },
    {
        "name": "Прикладная и компьютерная оптика",
        "id": 10565,
        "score": 235,
        "requests": 102,
        "value": 26
    },
    {
        "name": "Лазеры для информационно-коммуникационных систем",
        "id": 10569,
        "score": 239,
        "requests": 90,
        "value": 25
    },
    {
        "name": "Физика наноструктур",
        "id": 10566,
        "score": 257,
        "requests": 15,
        "value": 13
    },
    {
        "name": "Вычислительные системы и сети",
        "id": 10556,
        "score": 272,
        "requests": 165,
        "value": 52
    },
    {
        "name": "Программирование и интернет-технологии",
        "id": 10557,
        "score": 300,
        "requests": 400,
        "value": 90
    },
    {
        "name": "Системное и прикладное программное обеспечение",
        "id": 10558,
        "score": 283,
        "requests": 89,
        "value": 80
    },
    {
        "name": "Компьютерные технологии в дизайне",
        "id": 10559,
        "score": 283,
        "requests": 101,
        "value": 14
    },
    {
        "name": "Нейротехнологии и программирование",
        "id": 10559,
        "score": 282,
        "requests": 100,
        "value": 20
    }
  ];

  /**
   * Return data
   */
  res.json(makeResponse(programs));
};

module.exports = app => {
  app.route('/getUser')
    .get(getUser);

  app.route('/getUserPositions')
    .get(getUserPositions);

  app.route('/getProgramsByScores')
    .get(getProgramsByScores);
};
