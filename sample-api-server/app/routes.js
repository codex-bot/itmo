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

const random = (min = 1, max = 100) => {
    return Math.floor((max - min)* Math.random()) + min;
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

  if (userId !== "4621") {
    let message = "User does not exist";

    res.json(makeResponse({message}, false))
  }

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
      "id": 10555,
      "position": 13,
      "users": 67,
      "value": 120
    },
    {
      "program": "Световая инженерия",
      "id": 10555,
      "position": 88,
      "users": 430,
      "value": 25
    },
    {
      "program": "Интеллектуальная робототехника",
      "id": 10555,
      "position": 17,
      "users": 125,
      "value": 56
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

  programs = [];

  for (let i = 0; i < 64; i++) {
      let name = Math.random().toString(36).replace(/w+/g, '').substr(0, 25),
          id = random(10500, 10600),
          score = random(180, 310),
          requests = random(10, 400),
          value = random(),
          possible_place = random(1, requests);

      programs.push({
        name,
        id,
        score,
        requests,
        value,
        possible_place
      });
  }



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
