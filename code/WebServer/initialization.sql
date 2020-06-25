CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS SupportedDevices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  manufacturer TEXT,
  name TEXT,
  api TEXT
);

CREATE TABLE IF NOT EXISTS ActiveDevices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  manufacturer TEXT,
  macaddress TEXT
);

INSERT INTO SupportedDevices (manufacturer, name, api)
VALUES ('Belkin', 'Insight Switch', 'WeMo');
--
-- INSERT INTO SupportedDevices (manufacturer, name, api)
-- VALUES ('Beaglebone', 'DC Motor', 'BB');
