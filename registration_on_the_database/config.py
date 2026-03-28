import configparser

def get_db_config(file='database.ini',section='postgresql'):
    parser = configparser.ConfigParser()
    parser.read(file)
    if parser.has_section(section):
        return {param: parser.get(section,param) for param in parser.options(section)}
    else:
        raise Exception
