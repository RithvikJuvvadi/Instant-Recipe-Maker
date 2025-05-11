from . import db



class Recipe(db.Model):
    __tablename__ = 'recipes'  # Ensure you have a table name

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each recipe
    name = db.Column(db.String(100), nullable=False)  # Recipe name
    ingredients = db.Column(db.Text, nullable=False)  # Ingredients list
    instructions = db.Column(db.Text, nullable=False)  # Cooking instructions

    def __repr__(self):
        return f"<Recipe {self.name}>"
