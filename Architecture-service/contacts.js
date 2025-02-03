const chalk = require("chalk");
const fs = require("fs")
const yargs = require('yargs/yargs')
const {hideBin} = require('yargs/helpers')
const _ = require('lodash');

function colored(str, color) {
    return args.colors ? chalk[color](str) : str;
}

function isValidJSON(str) {
    try {
        JSON.parse(str);
        return true;
    } catch (e) {
        if (args.debug) console.error(e);
        return false;
    }
}


class Contact {
    constructor(id, firstName, lastName, address, phone) {
        this.id = id;
        this.firstName = firstName;
        this.lastName = lastName;
        this.address = address;
        this.phone = phone;
    }

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

class FileContactService {
    path = 'contacts.json';

    read(cb) {
        fs.readFile(this.path, 'utf-8', (err, data) => {
            if (err) {
                if (args.debug) console.error(err);
                return;
            }
            if (!isValidJSON(data)) {
                return;
            }
            cb(JSON.parse(data).map((c) => new Contact(c.id, c.firstName, c.lastName, c.address, c.phone)));
        });
    }

    write(contacts, cb) {
        fs.writeFile(this.path, JSON.stringify(contacts), (err) => {
            if (err) {
                if (args.debug) console.error(err);
                return;
            }
            cb(contacts);
        });
    }

    get contacts() {
        return this.read((c) => c);
    }

    print() {
        console.log(chalk.underline("Contact list :"));
        this.read(c => c.forEach((c) => console.log(c.toString())))
    }

    add(firstName, lastName, cb) {
        this.read((contacts) => {
            const contact = new Contact(contacts[contacts.length - 1].id + 1, firstName, lastName, "", "");
            contacts.push(contact);
            this.write(contacts, cb);
        });
    }

    delete(id, cb) {
        this.read((contacts) => {
            const index = contacts.findIndex((c) => c.id === id);
            if (index !== -1) {
                const contact = contacts.splice(index, 1)[0];
                this.write(contacts, cb);
            }
        });
    }

    watch(cb) {
        fs.watch(this.path, (eventType, filename) => {
            this.read((contacts) => {
                cb(eventType, filename);
            });
        });
    }
}

const service = new FileContactService();

const args = yargs(hideBin(process.argv))
    .command('list', 'List contacts', () => null, () => {
        service.print();
    }).command('add <firstName> <lastName>', 'Add a contact', (yargs) => {
        yargs.positional('firstName', {
            type: 'string',
            description: 'First name of contact to add'
        }).positional('lastName', {
            type: 'string',
            description: 'Last name of contact to add'
        });
    }, (argv) => {
        service.add(argv.firstName, argv.lastName, () => {
            console.log("Contact has been added");
            service.print();
        });
    }).command('delete <id>', 'Delete a contact', (yargs) => {
        yargs.positional('id', {
            type: 'number',
            description: 'Id of contact to delete'
        });
    }, (argv) => {
        service.delete(argv.id, () => {
            console.log("Contact has been deleted");
            service.print();
        });
    }).command('watch', 'Watch contacts file', {}, () => {
        service.watch((eventType, filename) => {
            console.log(`File ${filename} has been ${eventType}`)
        });
    })
    .option('colors', {
        alias: 'C',
        type: 'boolean',
        description: 'Activate colors in the output'
    })
    .option('debug', {
        alias: 'D',
        type: 'boolean',
        description: 'Activate debug mode'
    })
    .parse()


