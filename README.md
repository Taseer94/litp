# LITP

LITP is a python to load data from SQLite3 database to a PSQL database. The user configures the settings for both of the databases. Due to difference in the schema, such as that in data types etc, LITP provides the user to set the appropriate ones as per his/her choice.

## Getting Started

To get started, clone the repository on your local system. 

### Installation

In order to install all the dependencies for the tool,

```
   pip install .
```

### Hands on LITP

#### View the SQLite3 Schema

```
  litp slite show <name>
```

Where name is the database located in databases/ directory. To start with, a sample dataabse is provided.

#### View datatype mappings

```
  litp psql mapping show
```

This would present how the datatypes in SQLite would be mapped onto that of PSQL types

```
+------------+-----------+
| SQLite     | PSQL      |
+------------+-----------+
| int(11)    | int       |
| datetime   | timestamp |
| tinyint(1) | smallint  |
+------------+-----------+
```

These mappings are placed in litp/base/mapping.yaml file. One can edit the file for further customizations.