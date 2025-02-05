const FileContactService = require("./FileContactService");
const { setupCli } = require("./Cli");
const createServer = require("./Server");
const { router } = require("./Router");

const service = new FileContactService();
setupCli(service);
const server = createServer(service);
router(server, service);
