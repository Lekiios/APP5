const FileContactService = require("./FileContactService");
const { setupCli } = require("./Cli");

const service = new FileContactService();
setupCli(service);
