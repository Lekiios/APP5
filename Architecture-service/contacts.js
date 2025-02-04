const chalk = require("chalk");
const fs = require("fs");
const yargs = require("yargs/yargs");
const { hideBin } = require("yargs/helpers");
const _ = require("lodash");

/**
 * Colorize a string with Chalk
 * @param str string to colorize
 * @param color color to use (see Chalk documentation)
 * @returns {*} colorized string for console output
 */
function colored(str, color) {
  return args.colors ? chalk[color](str) : str;
}

/**
 * Check if a string is a valid JSON
 * @param str string to check
 * @returns {boolean} true if string is a valid JSON, false otherwise
 */
function isValidJSON(str) {
  try {
    JSON.parse(str);
    return true;
  } catch (e) {
    if (args.debug) console.error(e);
    return false;
  }
}

/**
 * Represents a contact with a first name, a last name, an address and a phone number
 */
class Contact {
  /**
   * Create a new contact
   * @param id id of the contact
   * @param firstName first name of the contact
   * @param lastName last name of the contact
   * @param address address of the contact
   * @param phone phone number of the contact
   */
  constructor(id, firstName, lastName, address, phone) {
    this.id = id;
    this.firstName = firstName;
    this.lastName = lastName;
    this.address = address;
    this.phone = phone;
  }

  /**
   * Get a string representation of the contact (full name)
   * @returns {string} full name of the contact
   */
  toString() {
    return `${colored(this.lastName.toUpperCase(), "blue")} ${colored(this.firstName, "red")}`;
  }
}

/*class ContactService {
    constructor() {
        this.c = data.map((c) => new Contact(c.id, c.firstName, c.lastName, c.address, c.phone));
    }

    get contacts() {
        return this.c;
    }

    print() {
        console.log("Contact list :");
        this.contacts.forEach((c) => console.log(c.toString()));
    }
}*/

/**
 * Service to manage contacts in a file
 */
class FileContactService {
  path = "contacts.json";

  /**
   * Read contacts from file
   * @param cb callback function called with contacts list
   */
  read(cb) {
    fs.readFile(this.path, "utf-8", (err, data) => {
      if (err) {
        if (args.debug) console.error(err);
        return;
      }
      if (!isValidJSON(data)) {
        return;
      }
      cb(
        JSON.parse(data).map(
          (c) => new Contact(c.id, c.firstName, c.lastName, c.address, c.phone),
        ),
      );
    });
  }

  /**
   * Write contacts to file
   * @param contacts contacts list to write
   * @param cb callback function called with contacts list
   */
  write(contacts, cb) {
    fs.writeFile(this.path, JSON.stringify(contacts), (err) => {
      if (err) {
        if (args.debug) console.error(err);
        return;
      }
      cb(contacts);
    });
  }

  /**
   * Get contacts list
   */
  get contacts() {
    return this.read((c) => c);
  }

  /**
   * Print contacts list
   */
  print() {
    console.log(chalk.underline("Contact list:"));
    this.read((c) => c.forEach((c) => console.log(c.toString())));
  }

  /**
   * Add a contact to the list
   * @param firstName first name of contact
   * @param lastName last name of contact
   * @param cb callback function called with contacts list
   */
  add(firstName, lastName, cb) {
    this.read((contacts) => {
      const contact = new Contact(
        contacts[contacts.length - 1].id + 1,
        firstName,
        lastName,
        "",
        "",
      );
      contacts.push(contact);
      this.write(contacts, cb);
    });
  }

  /**
   * Delete a contact from the list
   * @param id id of contact to delete
   * @param cb callback function called with contacts list
   */
  delete(id, cb) {
    this.read((contacts) => {
      const index = contacts.findIndex((c) => c.id === id);
      if (index !== -1) {
        this.write(contacts.splice(index, 1)[0], cb);
      }
    });
  }

  /**
   * Watch the contacts file for changes
   * @param cb callback function called with evenType, previous and new contacts list
   */
  watch(cb) {
    let content;
    this.read((contacts) => (content = contacts));

    fs.watch(this.path, (eventType) => {
      this.read((contacts) => {
        cb(eventType, content, contacts);
      });
    });
  }
}

const service = new FileContactService();

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
