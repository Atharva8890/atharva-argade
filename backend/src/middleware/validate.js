'use strict';

const { HttpError } = require('./error');

const validate = (schema, where = 'body') => (req, _res, next) => {
  const { value, error } = schema.validate(req[where], { abortEarly: false, stripUnknown: true });
  if (error) {
    return next(
      new HttpError(400, 'Validation failed', error.details.map((d) => ({ path: d.path, message: d.message })))
    );
  }
  req[where] = value;
  return next();
};

module.exports = { validate };
