require('dotenv').config();
const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// Debugging: Log available routes
app._router.stack.forEach(function (r) {
    if (r.route && r.route.path) {
        console.log(r.route.path);
    }
});

// Email sending route
app.post('/send-email', async (req, res) => {
    const { name, email, message } = req.body;

    if (!name || !email || !message) {
        return res.status(400).json({ message: 'All fields are required.' });
    }

    // Configure transporter for Gmail or another email service
    let transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: process.env.EMAIL_USER, // SMTP email
            pass: process.env.EMAIL_PASS  // SMTP app password (not personal password)
        }
    });

    const mailOptions = {
        from: process.env.EMAIL_USER, // Always use SMTP email as sender
        replyTo: email, // Allows the receiver to reply to the sender
        to: process.env.RECEIVER_EMAIL, // Recipient email
        subject: `New Contact Message from ${name}`,
        text: `From: ${name} (${email})\n\nMessage:\n${message}`
    };

    try {
        await transporter.sendMail(mailOptions);
        res.status(200).json({ message: 'Message sent successfully!' });
    } catch (error) {
        console.error('Email sending failed:', error);
        res.status(500).json({ message: 'Failed to send email.', error: error.message });
    }
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
