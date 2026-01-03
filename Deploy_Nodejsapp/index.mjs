import express from 'express';
import os from 'os';

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
    const hostname = os.hostname();
const message = `Hello from Node.js app running on Pod: ${hostname}`;
    res.send(message);
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(`Pod Hostname: ${os.hostname()}`);
});