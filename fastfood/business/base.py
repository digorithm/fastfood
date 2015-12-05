from fastfood import db
from fastfood.utils import _extract_selections

# IMPORTANT: db.engine.dispose is being tested
# if something is wrong, undo that

class BaseBO(object):

    def __init__(self, session=None):
        self._session = db.session()


class CrudBO(BaseBO):

    def list(self, limit=50):
        return self._list(limit=limit)

    def _list(self, model=None, selections=None, limit=50, query=None):
        model = model or self.model
        selections = selections or self.model_selections

        if query is None:
            query = self._session.query(model)

        if limit is not None:
            query = query.limit(limit)

        try:
            objects = query.all()
            return _extract_selections(objects, selections)
        finally:
            self._session.close()
            db.engine.dispose()

    def get(self, id):
        try:
            obj = self._session.query(self.model).filter(self.model.id == id)\
                                                 .first()
            return _extract_selections(obj, self.model_selections)
        finally:
            self._session.close()
            db.engine.dispose()

    def _create(self, obj, return_id=False):

        try:
            self._session.add(obj)
            self._session.commit()

        except Exception as e:
            raise e

        finally:
            if return_id:
                return obj.id
            self._session.close()
            db.engine.dispose()

    def update(self, id, changes):
        success = True
        try:
            self._session.query(self.model) \
                .filter(self.model.id == id) \
                .update(changes)
            self._session.commit()
        except:
            success = False
        finally:
            self._session.close()
            db.engine.dispose()
        return success

    def update_many(self, ids, changes):
        for _id in ids:
            self.update(_id, changes)

    def delete(self, id):
        """
          Creates a simple query filter by the given ID and delete the entry from the DB;
          If a custom behavior is wanted, you should inherit from it.
        """
        return self._delete(query=self._session.query(
            self.model).filter(self.model.id == id))

    def _delete(self, query):
        """
          Deletes using the given query filter
        """
        success = True
        try:
            query.delete()
            self._session.commit()
        except:
            success = False
        finally:
            self._session.close()

        return success

