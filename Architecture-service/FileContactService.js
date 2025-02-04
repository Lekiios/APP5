const fs = require("node:fs");
const Contact = require("./Contact");
const { isValidJSON } = require("./helpers");
const config = require("./Config");
const chalk = require("chalk");

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
        if (config.debug) console.error(err);
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
        if (config.debug) console.error(err);
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

module.exports = FileContactService;
