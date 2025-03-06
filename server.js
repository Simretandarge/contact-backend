require('dotenv').config();
const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

// Email sending route
app.post('/send-email', async (req, res) => {
    const { name, email, message } = req.body;

    // Configure transporter for Gmail or another email service
    let transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: process.env.EMAIL_USER, // Your email
            pass: process.env.EMAIL_PASS  // Your email password or app password
        }
    });

    const mailOptions = {
        from: email,
        to: process.env.RECEIVER_EMAIL, // Your recipient email
        subject: `New Contact Message from ${name}`,
        text: `From: ${name} (${email})\n\nMessage:\n${message}`
    };

    try {
        await transporter.sendMail(mailOptions);
        res.status(200).json({ message: 'Message sent successfully!' });
    } catch (error) {
        console.error('Email sending failed:', error);
        res.status(500).json({ message: 'Failed to send email.' });
    }
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
