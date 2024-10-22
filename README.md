# checkserve
-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

# Developer Command Reference
```zsh
# Test the application
hatch test

# Run the application
hatch run start-dev

### SQLite commands ###
# Intialize database via flask
hatch run flask db init

# Upgrade db
hatch run flask db upgrade

# Reset db
hatch run reset-sqlite
hatch run open-db

# Insert dummy data
hatch run insert-dummy-data
```

## License

`checkserve` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
