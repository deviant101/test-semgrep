/**
 * Simple Express application with intentional vulnerabilities for SAST testing
 */
const express = require('express');
const { exec } = require('child_process');
const sqlite3 = require('sqlite3');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

// In-memory SQLite DB to demonstrate SQL injection vulnerability
const db = new sqlite3.Database(':memory:');
db.serialize(() => {
  db.run('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)');
  db.run("INSERT INTO users (name) VALUES ('Alice')");
  db.run("INSERT INTO users (name) VALUES ('Bob')");
});

// Vulnerability: SQL Injection
app.get('/user', (req, res) => {
  const id = req.query.id;
  // Vulnerable: interpolating user input into SQL
  const q = `SELECT * FROM users WHERE id = ${id}`;
  db.get(q, (err, row) => {
    if (err) return res.status(500).send(err.message);
    res.send(JSON.stringify(row));
  });
});

// Vulnerability: Command Injection
app.get('/ping', (req, res) => {
  const host = req.query.host;
  // Vulnerable: passing unsanitized input to shell
  exec(`ping -c 1 ${host}`, (err, stdout, stderr) => {
    if (err) return res.status(500).send(stderr || err.message);
    res.type('text').send(stdout);
  });
});

// Vulnerability: XSS via unsanitized HTML
app.get('/greet', (req, res) => {
  const name = req.query.name || 'Guest';
  res.send(`<h1>Hello ${name}!</h1>`);
});

// Vulnerability: Hardcoded secret
const API_KEY = 'sk-secret-node-abc-12345';
app.get('/config', (req, res) => {
  res.send(`API configured with key: ${API_KEY.slice(0,5)}...`);
});

// Vulnerability: Insecure deserialization (eval on user input)
app.get('/load', (req, res) => {
  const data = req.query.data;
  if (data) {
    // Dangerous: eval on untrusted input
    try {
      const obj = eval('(' + data + ')');
      res.send(String(obj));
    } catch (e) {
      res.status(400).send('Invalid data');
    }
  } else {
    res.send('No data');
  }
});

app.listen(3000, () => {
  console.log('App listening on port 3000');
});
