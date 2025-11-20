const db = require('../backend_chat/db');

const Conversation = {
  async create(participantIds) {
    const client = await db.pool.connect();
    try {
      await client.query('BEGIN');
      const convResult = await client.query('INSERT INTO conversations DEFAULT VALUES RETURNING id');
      const conversationId = convResult.rows[0].id;

      const participantPromises = participantIds.map(userId =>
        client.query(
          'INSERT INTO conversation_participants (user_id, conversation_id) VALUES ($1, $2)',
          [userId, conversationId]
        )
      );
      await Promise.all(participantPromises);

      await client.query('COMMIT');
      return { id: conversationId };
    } catch (e) {
      await client.query('ROLLBACK');
      throw e;
    } finally {
      client.release();
    }
  },

  async findByUser(userId) {
    const result = await db.query(
      `SELECT c.id, c.created_at FROM conversations c
       JOIN conversation_participants cp ON c.id = cp.conversation_id
       WHERE cp.user_id = $1`,
      [userId]
    );
    return result.rows;
  },

  async findBetween(userId1, userId2) {
    const result = await db.query(
      `SELECT cp1.conversation_id FROM conversation_participants cp1
       JOIN conversation_participants cp2 ON cp1.conversation_id = cp2.conversation_id
       WHERE cp1.user_id = $1 AND cp2.user_id = $2`,
      [userId1, userId2]
    );
    return result.rows[0];
  }
};

module.exports = Conversation;
