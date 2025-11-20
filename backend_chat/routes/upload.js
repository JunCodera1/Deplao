const express = require('express');
const { upload } = require('../services/fileService');
const authMiddleware = require('../middleware/authMiddleware');

const router = express.Router();

// POST /api/upload
router.post('/', [authMiddleware, upload.single('file')], (req, res) => {
  if (!req.file) {
    return res.status(400).json({ message: 'No file uploaded.' });
  }

  // The file is saved by multer. We return the path to the client.
  // The client will then send a socket event with this info.
  const fileUrl = `/uploads/${req.file.filename}`;
  res.status(201).json({
    message: 'File uploaded successfully.',
    fileUrl: fileUrl,
    fileName: req.file.originalname,
    fileType: req.file.mimetype,
  });
});

module.exports = router;
