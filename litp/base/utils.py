from os import path


var_dict = {'int(11)': 'int', 'datetime': 'timestamp',
            'tinyint(1)': 'smallint'}


def data(lite_data):
    """ Load the schema"""
    for row in lite_data:
        values = []
        for i in range(0, len(row)):
            if isinstance(row[i], unicode):
                values.insert(i, row[i].encode('ascii', 'ignore'))
            elif row[i] is None:
                values.insert(i, 0)
            else:
                values.insert(i, row[i])
        values = tuple(values)
    return values
