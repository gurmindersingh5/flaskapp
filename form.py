from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, SubmitField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Email


class Customer_Entry(FlaskForm):
    id = IntegerField(label='id')
    name = StringField(label='Name', validators=[DataRequired()])
    address = TextAreaField(label='Address', validators=[DataRequired()])
    contact = IntegerField(label='Contact')
    submit = SubmitField(label='Submit')


class Part(FlaskForm):
    name = TextAreaField(label="Product Name", validators=[DataRequired()])
    price = DecimalField(label="Price/item", validators=[DataRequired()])
    qty = IntegerField(label='Qty', validators=[DataRequired()])
    submit = SubmitField(label='Add to Inventory')


class DataEntry(FlaskForm):

    # Customer_name = StringField(label="Customer_name", validators=[DataRequired()])
    # Address = StringField(label="Address", validators=[DataRequired()])
    Parts_purchased = StringField(label="Parts_purchased", validators=[DataRequired()])
    Qty = IntegerField(label='Qty', default='1')
    Price = DecimalField(label='Price')
    Submit = SubmitField(label="Submit")


class search_form(FlaskForm):
    S_name = StringField(label='Search by Name: ')
    S_address = StringField(label='Search by Address: ')
    Submit = SubmitField(label="Submit")

# class Mechanic_Entry(FlaskForm):
#     id = IntegerField(nullable=False, primary_key=True)
#     name = StringField(length=30, unique=False, nullable=True)
#     address = StringField(db.String(length=100), nullable=True)
#     contact = IntegerField()
