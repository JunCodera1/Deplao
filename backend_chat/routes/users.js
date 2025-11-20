const express = require('express');
const User = require('../../models/User');
const authMiddleware = require('../middleware/authMiddleware');

const router = express.Router();

// GET /api/users/search?q=...
router.get('/search', authMiddleware, async (req, res) => {
  const { q } = req.query;
  const currentUserId = req.user.id;

  if (!q) {
    return res.status(400).json({ message: 'Search query (q) is required.' });
  }

  try {
    const users = await User.searchByUsername(q, currentUserId);
    res.json(users);
  } catch (error) {
    console.error('User search error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

module.exports = router;
