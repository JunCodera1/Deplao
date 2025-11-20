const express = require('express');
const Message = require('../../models/Message');
const authMiddleware = require('../middleware/authMiddleware');

const router = express.Router();

// GET /api/chat/:conversationId/messages
router.get('/:conversationId/messages', authMiddleware, async (req, res) => {
  const { conversationId } = req.params;
  const { limit = 50, offset = 0 } = req.query;

  try {
    const messages = await Message.findByConversation(conversationId, limit, offset);
    res.json(messages);
  } catch (error) {
    console.error('Error fetching messages:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

module.exports = router;
