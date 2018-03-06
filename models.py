import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Item(db.Model):
    """ Model for an Item """
    logger = logging.getLogger(__name__)
    app = None

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlists.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(100))

    def __repr__(self):
        return '<Item %r>' % (self.name)

    def save(self):
        """ Saves an Item to the database """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Deletes an Item from the database """
        if self.id:
            db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """
        Serializes an Item into a dictionary
        Returns:
            dict
        """
        return {
                "id": self.id,
                "wishlist_id": self.wishlist_id,
                "product_id": self.product_id,
                "name": self.name,
                "description": self.description
                }

    def deserialize(self, data, wishlist_id):
        """
        Deserializes an Item from a dictionary
        Args:
            data (dict): A dictionary containing the Item data
        Returns:
            self: instance of Item
        Raises:
            DataValidationError: when bad or missing data
        """
        try:
            self.wishlist_id = wishlist_id
            self.product_id = data['product_id']
            self.name = data['name']
            self.description = data['description']
        except KeyError as error:
            raise DataValidationError('Invalid item: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid item: body of request contained ' \
                                      'bad or no data')
        return self

    @staticmethod
    def init_db(app):
        """ Initializes the database session """
        Item.logger.info('Initializing database')
        Item.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def all():
        """
        Fetch all of the Items in the database
        Returns:
            List: list of Items
        """
        Item.logger.info('Processing all Items')
        return Item.query.all()

    @staticmethod
    def get(item_id):
        """
        Get an Item by id
        Args:
            item_id: primary key of items
        Returns:
            Item: item with associated id
        """
        Item.logger.info('Processing lookup for id %s ...', item_id)
        return Item.query.get(item_id)

    @staticmethod
    def find_by_name(name):
        """ Return all Items with the given name

        Args:
            name (string): the name of the Items you want to match
        """
        Item.logger.info('Processing name query for %s ...', name)
        return Item.query.filter(Item.name == name)


class Wishlist(db.Model):
    """ Model for an Wishlist """
    logger = logging.getLogger(__name__)
    app = None

    __tablename__ = "wishlists"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)
    wishlist_name = db.Column(db.String(40))


    def __repr__(self):
        return '<Wishlist>'

    def save(self):
        """ Saves an Wishlist to the database """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Deletes an Wishlist from the database """
        if self.id:
            db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """
        Serializes an Wishlist into a dictionary
        Returns:
            dict
        """
        return {
                "id": self.id,
                "customer_id": self.customer_id,
                "wishlist_name": self.wishlist_name,
                }

    def deserialize(self, data):
        """
        Deserializes an Wishlist from a dictionary
        Args:
            data (dict): A dictionary containing the Wishlist data
        Returns:
            self: instance of Wishlist
        Raises:
            DataValidationError: when bad or missing data
        """
        try:
            self.customer_id = data['customer_id']
            self.wishlist_name = data['wishlist_name']
        except KeyError as error:
            raise DataValidationError('Invalid wishlist: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid wishlist: body of request contained ' \
                                      'bad or no data')
        return self

    @staticmethod
    def init_db(app):
        """ Initializes the database session """
        Wishlist.logger.info('Initializing database')
        Wishlist.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def all():
        """
        Fetch all of the Wishlists in the database
        Returns:
            List: list of Wishlists
        """
        Wishlist.logger.info('Processing all Wishlists')
        return Wishlist.query.all()

    @staticmethod
    def get(wishlist_id):
        """
        Get an Wishlist by id

        Args:
            wishlist_id: primary key of wishlists

        Returns:
            Wishlist: wishlist with associated id
        """
        Wishlist.logger.info('Processing lookup for id %s ...', wishlist_id)
        return Wishlist.query.get(wishlist_id)

    @staticmethod
    def get_or_404(wishlist_id):
        """ Finds a Order by it's id """
        Wishlist.logger.info('Processing lookup or 404 for id %s ...', wishlist_id)
        return Wishlist.query.get_or_404(wishlist_id)

    @staticmethod
    def find_by_customer_id(customer_id):
        """ Returns all Wishlists placed by the given customer

        Args:
            customer_id (integer): the customer's id
        """
        Wishlist.logger.info('Processing customer_id query for %s ...', customer_id)
        return Wishlist.query.filter(Wishlist.customer_id == customer_id)
