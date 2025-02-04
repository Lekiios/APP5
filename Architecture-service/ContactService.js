const data = require("./contacts.json");
const Contact = require("./Contact");

class ContactService {
  constructor() {
    this.c = data.map(
      (c) => new Contact(c.id, c.firstName, c.lastName, c.address, c.phone),
    );
  }

  get contacts() {
    return this.c;
  }

  print() {
    console.log("Contact list :");
    this.contacts.forEach((c) => console.log(c.toString()));
  }
}
