const { Server } = require('socket.io');
const jwt = require('jsonwebtoken');
const config = require('../config');
const Message = require('../../models/Message');
const Conversation = require('../../models/Conversation');

// In-memory store for active users { userId: socketId }
const activeUsers = new Map();

function initializeSocket(server) {
  const io = new Server(server, {
    cors: {
      origin: '*', // Adjust for your client's origin
    },
  });

  // Middleware for socket authentication
  io.use((socket, next) => {
    const token = socket.handshake.auth.token;
    if (!token) {
      return next(new Error('Authentication error: Token not provided.'));
    }
    jwt.verify(token, config.jwtSecret, (err, decoded) => {
      if (err) {
        return next(new Error('Authentication error: Invalid token.'));
      }
      socket.user = decoded;
      next();
    });
  });

  io.on('connection', (socket) => {
    console.log(`User connected: ${socket.user.username} (ID: ${socket.user.id})`);
    activeUsers.set(socket.user.id.toString(), socket.id);

    // Broadcast online status to other users
    socket.broadcast.emit('status:user-online', { userId: socket.user.id });

    socket.on('disconnect', () => {
      console.log(`User disconnected: ${socket.user.username}`);
      activeUsers.delete(socket.user.id.toString());
      // Broadcast offline status
      socket.broadcast.emit('status:user-offline', { userId: socket.user.id });
    });

    socket.on('message:send', async (data) => {
        const { recipientId, content } = data;
        const senderId = socket.user.id;

        try {
            let conv = await Conversation.findBetween(senderId, recipientId);
            if (!conv) {
                conv = await Conversation.create([senderId, recipientId]);
            }
            const conversationId = conv.conversation_id;

            const message = await Message.create(conversationId, senderId, 'text', content);

            const recipientSocketId = activeUsers.get(recipientId.toString());
            if (recipientSocketId) {
                io.to(recipientSocketId).emit('message:receive', message);
            }
            // Echo back to sender
            socket.emit('message:receive', message);

        } catch (error) {
            console.error('Error sending message:', error);
            socket.emit('error', { message: 'Failed to send message.' });
        }
    });
    
    socket.on('file:send', async (data) => {
        const { recipientId, fileUrl, fileName, fileType } = data;
        const senderId = socket.user.id;
        const contentType = fileType.startsWith('image/') ? 'image' : 'file';
        const content = JSON.stringify({ url: fileUrl, name: fileName, type: fileType });

        try {
            let conv = await Conversation.findBetween(senderId, recipientId);
            if (!conv) {
                conv = await Conversation.create([senderId, recipientId]);
            }
            const conversationId = conv.conversation_id;

            const message = await Message.create(conversationId, senderId, contentType, content);
            
            const recipientSocketId = activeUsers.get(recipientId.toString());
            if (recipientSocketId) {
                io.to(recipientSocketId).emit('message:receive', message);
            }
            // Echo back to sender
            socket.emit('message:receive', message);

        } catch (error) {
            console.error('Error sending file message:', error);
            socket.emit('error', { message: 'Failed to send file message.' });
        }
    });

    socket.on('typing', (data) => {
      const { recipientId } = data;
      const recipientSocketId = activeUsers.get(recipientId.toString());
      if (recipientSocketId) {
        io.to(recipientSocketId).emit('typing', { senderId: socket.user.id });
      }
    });

  });

  return io;
}

module.exports = { initializeSocket };
