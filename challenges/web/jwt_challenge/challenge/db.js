
var sqlite3 = require('sqlite3');
var mkdirp = require('mkdirp');

mkdirp.sync('./var/db');

var db = new sqlite3.Database('./var/db/users.db');

db.serialize(function() {
	db.run(`CREATE TABLE IF NOT EXISTS users (
	  id INTEGER PRIMARY KEY,
	  username TEXT NOT NULL,
	  password TEXT NOT NULL,
	  skills TEXT NOT NULL,
	  role TEXT DEFAULT 'user'
	)`);
  });
  

module.exports = db;