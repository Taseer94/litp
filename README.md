# LITP

LITP is a python program to load data from SQLite3 database to a PSQL database. The user configures the settings for both of the databases. Due to difference in the schema, such as that in data types etc, LITP provides the user to set the appropriate ones as per his/her choice. However this tool
may not work for all cases. Every DB is structured in its own way, it is almost impossible to cover all aspects.

This tool works well for fingerbank database, https://fingerbank.org/

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

Where name is the database located in databases/ directory.

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

#### Convert the schema

Load the schema from SQLiteDB to PSQLDB.

```
  litp psql load schema [-l|--lite] <sqlite_db> [-p|--psql] <psql_db>
```

#### Convert the data

Load the data from SQLiteDB to PSQLDB.

```
  litp psql load data [-l|--lite] <sqlite_db> [-p|--psql] <psql_db> [-t|--table] <table_name>
```
