const express = require('express'),
  app = express(),
  port = process.env.PORT || 3000,
  bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use(function (req, res, next) {
  console.log(req.method, req.originalUrl);
  next();
});

const routes = require('./app/routes');
routes(app); // register routes

app.listen(port);
console.log('API server started on: ' + port);
