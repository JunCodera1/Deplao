const db = require('../backend_chat/db');
const bcrypt = require('bcryptjs');

const User = {
  async create(username, password) {
    const hash = await bcrypt.hash(password, 10);
    const result = await db.query(
      'INSERT INTO users (username, password_hash) VALUES ($1, $2) RETURNING id, username, created_at',
      [username, hash]
    );
    return result.rows[0];
  },

  async findByUsername(username) {
    const result = await db.query('SELECT * FROM users WHERE username = $1', [username]);
    return result.rows[0];
  },

  async findById(id) {
    const result = await db.query('SELECT id, username, created_at FROM users WHERE id = $1', [id]);
    return result.rows[0];
  },

  async searchByUsername(query, currentUserId) {
    const result = await db.query(
      'SELECT id, username FROM users WHERE username ILIKE $1 AND id != $2 LIMIT 10',
      [`%${query}%`, currentUserId]
    );
    return result.rows;
  },

  async verifyPassword(user, password) {
    return bcrypt.compare(password, user.password_hash);
  },
};

module.exports = User;