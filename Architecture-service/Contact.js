const { colored } = require("./helpers");

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

module.exports = Contact;
