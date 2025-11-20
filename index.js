const express = require('express');
const { Sequelize } = require('sequelize');

const app = express();
const port = 3000;

// --- Database Connection ---
// IMPORTANT: Make sure you have PostgreSQL running and update these credentials.
const dbName = 'deplao_chat';
const dbUser = 'postgres'; // replace with your postgres username
const dbPassword = ''; // replace with your postgres password

const sequelize = new Sequelize(dbName, dbUser, dbPassword, {
    host: 'localhost',
    dialect: 'postgres'
});

// Test the connection
async function testDbConnection() {
    try {
        await sequelize.authenticate();
        console.log('PostgreSQL connection has been established successfully.');
    } catch (error) {
        console.error('Unable to connect to the database:', error);
    }
}
testDbConnection();

// Export sequelize instance for models
module.exports.sequelize = sequelize;

// --- Middleware ---
app.use(express.json());

// --- API Routes ---
// We will re-integrate this after updating the routes file.
app.use('/api/auth', require('./routes/auth'));

app.get('/', (req, res) => {
    res.send('Node.js Auth Backend with PostgreSQL is running.');
});


// Sync database and start server
// The { force: true } option will drop tables if they exist. Be careful in production.
// We'll sync the models once they are defined and imported.
sequelize.sync(/*{ force: true }*/).then(() => {
    console.log('Database & tables created!');
    app.listen(port, () => {
        console.log(`Backend server listening at http://localhost:${port}`);
    });
}).catch(error => {
    console.error('Failed to sync database:', error);
});
