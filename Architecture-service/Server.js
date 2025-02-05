const express = require("express");
const bodyParser = require("body-parser");

const { PORT = 3000, HOST = "127.0.0.1" } = process.env;

function createServer(service) {
  const app = express();
  app.use(bodyParser.json());
  app.use(express.static("frontend"));

  app.listen(PORT, HOST, () => {
    console.log(`Server running at http://${HOST}:${PORT}/`);
  });
  return app;
}

module.exports = createServer;
