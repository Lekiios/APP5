const Contact = require("./Contact");

// Write a function to log the request method and URL to the console
function logRequest(req) {
  console.log(`${req.method} ${req.url}`);
}

function router(server, service) {
  server.get("/rest/contacts/", (req, res) => {
    logRequest(req);
    service.read((contacts) => {
      res.json(contacts);
    });
  });

  server.get("/rest/contacts/:id", (req, res) => {
    logRequest(req);
    service.read((contacts) => {
      const contact = contacts.find((c) => +c.id === +req.params.id);
      if (contact) {
        res.json(contact);
      } else {
        res.status(404).send("Contact not found");
      }
    });
  });

  server.post("/rest/contacts/", (req, res) => {
    logRequest(req);
    service.read((contacts) => {
      const contact = new Contact(
        contacts[contacts.length - 1].id + 1,
        req.body.firstName,
        req.body.lastName,
        req.body.address ?? "",
        req.body.phone ?? "",
      );
      contacts.push(contact);
      service.write(contacts, () => {
        res.json(contact);
      });
    });
  });

  server.put("/rest/contacts/:id", (req, res) => {
    logRequest(req);
    service.read((contacts) => {
      const contact = contacts.find((c) => +c.id === +req.params.id);
      if (contact) {
        contact.firstName = req.body.firstName;
        contact.lastName = req.body.lastName;
        contact.address = req.body.address;
        contact.phone = req.body.phone;
        service.write(contacts, () => {
          res.json(contact);
        });
      } else {
        res.status(404).send("Contact not found");
      }
    });
  });
}

module.exports = { router };
