const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const getSecrets = require('./config');
const routes = require('./routes');

const app = express();
const PORT = process.env.PORT || 3000;

(async () => {
  const { jwtSecret, dbUri } = await getSecrets();

  // Middleware
  app.use(bodyParser.json());

  // JWT authentication middleware
  app.use((req, res, next) => {
    const token = req.headers['authorization'];
    if (!token) {
      return res.status(403).send('Token is required');
    }

    try {
      const decoded = jwt.verify(token, jwtSecret);
      req.user = decoded;
      next();
    } catch (err) {
      return res.status(401).send('Invalid token');
    }
  });

  // Routes
  app.use('/api', routes);

  // Database connection
  mongoose.connect(dbUri, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.log('MongoDB connection error:', err));

  // Start server
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
})();

module.exports = app;