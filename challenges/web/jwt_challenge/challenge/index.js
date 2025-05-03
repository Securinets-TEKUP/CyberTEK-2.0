const express = require('express');
const db = require('./db');
const app = express();

const { checkAdmin, IsLoggedIn } = require('./checkAdmin');

const jwt = require('jsonwebtoken');
const fs = require('fs');
const path = require('path');
const jose = require('node-jose');
const port = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

let signingKey;
let keyStore;

async function loadKeys() {
  const privateJwk = JSON.parse(fs.readFileSync("jwkPrivate.json"));
  keyStore = jose.JWK.createKeyStore();
  signingKey = await keyStore.add(privateJwk, "json");
}
loadKeys();

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public/index.html"));
});

app.get("/arcade", (req, res) => {
  res.sendFile(path.join(__dirname, "public/arcade.html"));
});

app.get("/api/leaderboard", (req, res) => {
  res.json([
    { name: "ArcadeKid91", score: 40000 },
    { name: "NeoPixel", score: 35600 },
    { name: "JoystickJunkie", score: 27890 }
  ]);
});

app.get("/api/arcade/highscores", (req, res) => {
  res.json({ game: "Galaga", topPlayer: "RetroRider", score: 42000 });
});

app.get("/admin/dashboard", (req, res) => {
  res.json({ message: "Admin dashboard under maintenance" });
});

app.post("/register", (req, res) => {
  const { username, password, skills } = req.body;

  if (!username || !password || !skills || typeof skills !== 'object') {
    return res.status(400).json({ error: "All fields are required and skills must be a key-value object" });
  }

  const skillsStr = JSON.stringify(skills);
  db.run("INSERT INTO users (username, password, skills) VALUES (?, ?, ?)", [username, password, skillsStr], function(err) {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: "Database error" });
    }

    res.redirect('/login');
  });
});

app.get("/register", (req, res) => {
  res.sendFile(path.join(__dirname, "public/register.html"));
});

app.post("/login", (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.status(400).json({ error: "Username and password are required" });
  }

  db.get("SELECT * FROM users WHERE username = ? AND password = ?", [username, password], (err, row) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: "Database error" });
    }

    if (!row) {
      return res.status(401).json({ error: "Invalid credentials" });
    }

    const payload = {
      sub: username,
      role: "user"
    };

    const token = jwt.sign(payload, signingKey.toPEM(true), {
		algorithm: "RS256",
		keyid: signingKey.kid,
		expiresIn: "1h",
		header: {
			alg: "RS256",
			kid: signingKey.kid,
			jwks_uri: "http://localhost:3000/.well-known/jwks.json"
		}
    });

    res.redirect('/arcade');
  });
});

app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "public/login.html"));
});

app.get("/api/profile/:id", IsLoggedIn, (req, res) => {
  const userId = req.params.id;

  db.get("SELECT * FROM users WHERE id = ?", [userId], (err, row) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: "Database error" });
    }

    if (!row) {
      return res.status(404).json({ error: "User not found" });
    }

	if (req.user.sub !== row.username && req.user.role !== "admin") {
		return res.status(403).json({ error: "Forbidden" });
	}

    res.status(200).json({ [row.username]: JSON.parse(row.skills) });
  });
});

app.get("/flag", checkAdmin, (req, res) => {
  const flag = "Securinets{This_IS_THE_FLAG}";
  res.status(200).json({ flag });
});

app.get("/.well-known/jwks.json", (req, res) => {
  res.json({ keys: keyStore.toJSON().keys });
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
