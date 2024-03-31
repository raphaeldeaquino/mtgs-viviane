import sqlite3
import logging
import json
import os

logger = logging.getLogger()


class Connect(object):

    def __init__(self, db_name):
        try:
            # conectando...
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            logger.debug("Conectando ao banco %s", db_name)
            self.cursor.execute('SELECT SQLITE_VERSION()')
            self.data = self.cursor.fetchone()
            logger.debug("SQLite version: %s" % self.data)
        except sqlite3.Error:
            logger.error("Erro ao abrir banco.")

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.close()
            logger.debug("Conexão com o banco fechada.")


class DatabaseController(object):

    db_name = 'smart_planning'
    db = None
    constants_map = None

    def __init__(self):
        self.db = Connect(self.db_name + '.db')
        self.constants_map = {}

    def get_constants_map(self):
        return self.constants_map

    def close_connection(self):
        self.db.close_db()

    def create_schema(self, schema_name=os.path.dirname(__file__) + '/../../smart_planning/data/'
                                                                    'smart_planning_schema.sql'):
        try:
            with open(schema_name, 'rt') as f:
                schema = f.read()
                self.db.cursor.executescript(schema)
        except sqlite3.Error as e:
            logger.error("SQLite error: %s", e)
            return False

        logger.debug("Esquema criado com sucesso.")

    def save_entity(self, entity):
        try:
            entity_id = entity["id"]
            entity_type = entity["type"]

            sql = f"SELECT * FROM entities WHERE id='{entity_id}'"
            r = self.db.cursor.execute(sql)
            result = r.fetchall()
            if len(result) == 0:
                data = json.dumps(entity)
                sql = """
                INSERT INTO entities (id, type, data)
                VALUES ('{}', '{}', '{}')
                """.format(entity_id, entity_type, data)
                self.db.cursor.execute(sql)
                # gravando no banco
                self.db.commit_db()
                logger.debug(f"Entity ('{entity_id}') saved.")
                return True
            else:
                logger.error(f"Entity {entity_id} already saved")
                return False
        except KeyError as e:
            logger.error("Bad entity: %s", e)
            raise e
        except sqlite3.IntegrityError as e:
            logger.error("SQLite error: %s", e)
            raise e

    def get_entity(self, entity_id, entity_type=None):
        try:
            if entity_type:
                sql = f"SELECT * FROM entities WHERE id='{entity_id}' AND type='{entity_type}'"
            else:
                sql = f"SELECT * FROM entities WHERE id='{entity_id}'"
            r = self.db.cursor.execute(sql)
            result = r.fetchall()
            if len(result) == 0:
                return None
            else:
                return result[0]
        except sqlite3.IntegrityError as e:
            logger.error("SQLite error: %s", e)
            raise e
