const { InfisicalClient, LogLevel } = require("@infisical/sdk");

const client = new InfisicalClient({
  clientId: process.env.INFISICAL_CLIENT_ID,
  clientSecret: process.env.INFISICAL_CLIENT_SECRET,
  logLevel: LogLevel.INFO
});

async function getSecrets() {
  const jwtSecret = await client.getSecret({
    projectId: process.env.INFISICAL_PROJECT_ID,
    environment: process.env.NODE_ENV || "development",
    secretName: "JWT_SECRET"
  });

  const dbUri = await client.getSecret({
    projectId: process.env.INFISICAL_PROJECT_ID,
    environment: process.env.NODE_ENV || "development",
    secretName: "MONGODB_URI"
  });

  return { jwtSecret, dbUri };
}

module.exports = getSecrets;