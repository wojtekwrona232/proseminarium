from db.db_conn import *
from db.DAO import *
from sqlalchemy.orm.exc import *
from sqlalchemy.exc import *


class DBMethods:

    def __init__(self):
        self.util = SQLUtil()
        self.util.create_engine()
        self.util.open_session()

    def get_all(self, entity):
        try:
            return self.util.get_session().query(entity).all()
        except Exception:
            self.util.session_rollback()
            raise Exception
        finally:
            self.util.close_session()

    def get_query(self, entity):
        try:
            return self.util.get_session().query(entity)
        except Exception:
            self.util.session_rollback()
            raise Exception
        finally:
            self.util.close_session()

    def get(self, entity, id_sel):
        try:
            return self.util.get_session().query(entity).get(id_sel)
        except :
            self.util.session_rollback()
            raise
        finally:
            self.util.close_session()

    def add_entity(self, entity):
        try:
            self.util.get_session().add(entity)
            self.util.get_session().commit()
            return True
        except Exception:
            self.util.session_rollback()
            raise Exception
        finally:
            self.util.close_session()

    def add_all_entities(self, entity=list):
        try:
            self.util.get_session().add_all(entity)
            self.util.get_session().commit()
        except Exception:
            self.util.session_rollback()
            raise Exception
        finally:
            self.util.close_session()

    def delete_id(self, entity, e_id):
        try:
            a = self.util.get_session().query(entity).get(e_id)
            self.util.get_session().delete(a)
            self.util.get_session().commit()
        except Exception:
            self.util.session_rollback()
            raise Exception
        finally:
            self.util.close_session()

    def update_authors_data(self, e_id, new_entity):
        try:
            sel = self.util.get_session().query(AuthorData).get(e_id)
            sel.first_name = new_entity.__getitem__(0)
            sel.last_name = new_entity.__getitem__(1)
            self.util.get_session().commit()
        except Exception:
            self.util.session_rollback()
            raise Exception
        finally:
            self.util.close_session()

    def update_translators_data(self, e_id, new_entity):
        try:
            sel = self.util.get_session().query(TranslatorsData).get(e_id)
            sel.first_name = new_entity.__getitem__(0)
            sel.last_name = new_entity.__getitem__(1)
            self.util.get_session().commit()
        except Exception:
            self.util.session_rollback()
            raise Exception
        finally:
            self.util.close_session()

    def update_publishers(self, e_id, new_entity):
        try:
            sel = self.util.get_session().query(Publishers).get(e_id)
            sel.name = new_entity.__getitem__(0)
            self.util.get_session().commit()
        except Exception:
            self.util.session_rollback()
            raise Exception
        finally:
            self.util.close_session()

    def update_books(self, e_id, new_entity):
        try:
            sel = self.util.get_session().query(Books).get(e_id)
            sel.isbn = new_entity.__getitem__(0)
            sel.title = new_entity.__getitem__(1)
            sel.publisher_id = new_entity.__getitem__(2)
            sel.year_published = new_entity.__getitem__(3)
            sel.edition_nr = new_entity.__getitem__(4)
            self.util.get_session().commit()
        except Exception:
            self.util.session_rollback()
            raise Exception
        finally:
            self.util.close_session()

    def update_books_author(self, e_id, e_id1, new_entity):
        try:
            sel = self.util.get_session().query(Authors).get(book_id=e_id, author_id=e_id1)
            sel.author_id = new_entity.__getitem__(0)
            self.util.get_session().commit()
        except Exception:
            self.util.session_rollback()
            raise Exception
        finally:
            self.util.close_session()

    def update_books_translator(self, e_id, e_id1,new_entity):
        try:
            sel = self.util.get_session().query(Translators).get(book_id=e_id, translator_id=e_id1)
            sel.translator_id = new_entity.__getitem__(0)
            self.util.get_session().commit()
        except Exception:
            self.util.session_rollback()
            raise Exception
        finally:
            self.util.close_session()
