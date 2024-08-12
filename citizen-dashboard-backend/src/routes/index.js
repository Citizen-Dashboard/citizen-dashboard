const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// Define routes
router.get('/users', userController.getAllUsers);
router.post('/users', userController.createUser);

module.exports = router;
