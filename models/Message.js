const db = require('../backend_chat/db');

const Message = {
  async create(conversationId, senderId, contentType, content) {
    const result = await db.query(
      'INSERT INTO messages (conversation_id, sender_id, content_type, content) VALUES ($1, $2, $3, $4) RETURNING *',
      [conversationId, senderId, contentType, content]
    );
    return result.rows[0];
  },

  async findByConversation(conversationId, limit = 50, offset = 0) {
    const result = await db.query(
      `SELECT m.*, u.username as sender_username FROM messages m
       JOIN users u ON m.sender_id = u.id
       WHERE m.conversation_id = $1
       ORDER BY m.created_at DESC
       LIMIT $2 OFFSET $3`,
      [conversationId, limit, offset]
    );
    return result.rows.reverse();
  },
};

module.exports = Message;
