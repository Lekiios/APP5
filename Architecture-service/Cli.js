const yargs = require("yargs/yargs");
const { hideBin } = require("yargs/helpers");
const config = require("./Config");

function setupCli(service) {
  const args = yargs(hideBin(process.argv))
    .command(
      "list",
      "List contacts",
      () => null,
      () => {
        service.print();
      },
    )
    .command(
      "add <firstName> <lastName>",
      "Add a contact",
      (yargs) => {
        yargs
          .positional("firstName", {
            type: "string",
            description: "First name of contact to add",
          })
          .positional("lastName", {
            type: "string",
            description: "Last name of contact to add",
          });
      },
      (argv) => {
        service.add(argv.firstName, argv.lastName, () => {
          console.log("Contact has been added");
          service.print();
        });
      },
    )
    .command(
      "delete <id>",
      "Delete a contact",
      (yargs) => {
        yargs.positional("id", {
          type: "number",
          description: "Id of contact to delete",
        });
      },
      (argv) => {
        service.delete(argv.id, () => {
          console.log("Contact has been deleted");
          service.print();
        });
      },
    )
    .command("watch", "Watch contacts file", {}, () => {
      service.watch((eventType, prev, next) => {
        if (eventType === "change") {
          console.log(chalk.underline("Contacts have changed:"));
          console.log(_.differenceWith(prev, next, _.isEqual));
        }
      });
    })
    .option("colors", {
      alias: "C",
      type: "boolean",
      description: "Activate colors in the output",
    })
    .option("debug", {
      alias: "D",
      type: "boolean",
      description: "Activate debug mode",
    })
    .parse();

  // Update config with CLI arguments explicitly
  config.colors = args.colors;
  config.debug = args.debug;

  return args;
}

module.exports = { setupCli };
