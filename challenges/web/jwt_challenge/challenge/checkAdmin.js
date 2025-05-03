const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');
const url = require('url');

// Whitelisted domains only (no trailing slash)
const WHITELISTED_DOMAINS = [
  "http://localhost:3000",
];

const checkAdmin = async (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: "Missing or malformed token" });
  }

  const token = authHeader.split(' ')[1];

  let decodedHeader;
  try {
    decodedHeader = jwt.decode(token, { complete: true });
    if (!decodedHeader || !decodedHeader.header) {
      throw new Error("Invalid token header");
    }
  } catch (err) {
    return res.status(400).json({ error: "Invalid JWT" });
  }

  const { kid, jwks_uri } = decodedHeader.header;

  if (!jwks_uri) {
    return res.status(400).json({ error: "No jwks_uri found in token header" });
  }

  // Extract domain from jwks_uri
  const parsed = url.parse(jwks_uri);
  const jwksDomain = `${parsed.protocol}//${parsed.host}`;

  if (!WHITELISTED_DOMAINS.includes(jwksDomain)) {
    return res.status(403).json({ error: "Untrusted JWKS domain" });
  }

  const client = jwksClient({
    jwksUri: jwks_uri,
    timeout: 3000
  });

  console.log(jwks_uri)

  client.getSigningKey(kid, (err, key) => {
    if (err) {
      console.error("JWKS fetch error:", err);
      return res.status(500).json({ error: "Failed to fetch signing key 1" });
    }

    const signingKey = key.getPublicKey();
    jwt.verify(token, signingKey, (err, payload) => {
      if (err) {
        return res.status(401).json({ error: "Invalid token" });
      }

      if (payload.role !== "admin") {
        return res.status(403).json({ error: "Admin role required" });
      }

      req.user = payload;
      next();
    });
  });
};

const IsLoggedIn = (req, res, next) => {
	
	const IP = req.connection.remoteAddress;

  console.log(IP)
	if (IP == "127.0.0.1" || IP == "::1") {
		req.user = { sub: "admin", role: "admin" };
		return next();
	}

  const authHeader = req.headers.authorization;
	if (!authHeader || !authHeader.startsWith('Bearer ')) {
    console.log(authHeader)
		return res.status(401).json({ error: "Missing or malformed token 2" });
	}

  const token = authHeader.split(' ')[1];
	let decodedHeader;
	try {
		decodedHeader = jwt.decode(token, { complete: true });

		if (!decodedHeader || !decodedHeader.header) {
		  throw new Error("Invalid token header");
		}
	  } catch (err) {
		return res.status(400).json({ error: "Invalid JWT" });
	  }
	
	const { kid, jwks_uri } = decodedHeader.header;
	if (!jwks_uri) {
		return res.status(400).json({ error: "No jwks_uri found in token header" });
	}

	// Extract domain from jwks_uri

	const parsed = url.parse(jwks_uri);
	const jwksDomain = `${parsed.protocol}//${parsed.host}`;
	if (!WHITELISTED_DOMAINS.includes(jwksDomain)) {
		return res.status(403).json({ error: "Untrusted JWKS domain" });
	}

	const client = jwksClient({
		jwksUri: jwks_uri,
		timeout: 3000
	});
	client.getSigningKey(kid, (err, key) => {
		if (err) {
			console.error("JWKS fetch error:", err);
			return res.status(500).json({ error: "Failed to fetch signing key" });
		}
		const signingKey = key.getPublicKey();
		jwt.verify(token, signingKey, (err, payload) => {
			if (err) {
				return res.status(401).json({ error: "Invalid token" });
			}
			req.user = payload;
			next();
		});
	});
}

module.exports = { checkAdmin, IsLoggedIn };
