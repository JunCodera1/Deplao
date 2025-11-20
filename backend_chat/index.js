const express = require('express');
const http = require('http');
const cors = require('cors');
const path = require('path');
const config = require('./config');
const { initializeSocket } = require('./socket/socketManager');

const authRoutes = require('./routes/auth');
const chatRoutes = require('./routes/chat');
const uploadRoutes = require('./routes/upload');
const userRoutes = require('./routes/users');

const app = express();
const server = http.createServer(app);

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve uploaded files statically
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/chat', chatRoutes);
app.use('/api/upload', uploadRoutes);
app.use('/api/users', userRoutes);

// Initialize Socket.IO
const io = initializeSocket(server);

// Health check route
app.get('/', (req, res) => {
  res.send('Backend server is running.');
});

server.listen(config.port, () => {
  console.log(`Server listening on port ${config.port}`);
});