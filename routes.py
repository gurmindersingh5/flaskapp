import datetime
from sqlalchemy import desc
from app import app
from flask import render_template, redirect, url_for, request
from form import DataEntry, Customer_Entry, search_form, Part
from models import CEntry, DEntry, PEntry
from app import db


@app.route('/')
def home():
    content = "Welcome"
    return render_template('home.html', content=content)


LASTENTRY = {'Name': '', 'Address': '', 'Parts_purchased': '',
             'date': '', 'time': ''}
error_note = ""


@app.route('/eform', methods=['GET', 'POST'])
def e_form():
    form_data = DataEntry()
    data_list = CEntry.query.all()
    part_list = PEntry.query.all()
    address_list = {}
    parts = {}
    for item in data_list:
        address_list[item.name] = item.address
    for part in part_list:
        parts[part.name] = float(part.price)
    if request.method == "POST":
        global LASTENTRY
        global error_note

        error_note = ""
        if form_data.validate_on_submit():
            data = DEntry(
                parts=request.form['Parts_purchased'],
                qty=form_data.Qty.data,
                price=request.form['Price'] * form_data.Qty.data,
                cust_id=request.form['custid'],
                # time=datetime.strptime(datetime.datetime.now().strftime('%d-%m-%Y ~ %H:%M'), '%d-%m-%Y ~ %H:%M')
            )

            selected_customer = CEntry.query.filter_by(cust_id=request.form['custid']).first()
            print(selected_customer, "   -    ", '\n', datetime.datetime.now().second)
            LASTENTRY['Name'] = selected_customer.name
            LASTENTRY['Address'] = selected_customer.name
            LASTENTRY['Name'] = selected_customer.name
            LASTENTRY['Name'] = selected_customer.name

            inv = PEntry.query.filter_by(name=request.form['Parts_purchased']).first()
            if inv.qty - form_data.Qty.data >= 0:
                inv.qty = inv.qty - form_data.Qty.data
                db.session.add(data)
                db.session.commit()
                LASTENTRY['Name'] = selected_customer
            else:
                error_note = f"Not enough Inventory. Available qty: {inv.qty}"

            print("=" * 10, form_data.Qty.data,
                  PEntry.query.filter_by(name=request.form['Parts_purchased']).first().qty)
            return redirect(url_for('e_form'))
        if form_data.errors != {}:
            for err_msg in form_data.errors.values():
                print(f" There was an error {err_msg, form_data.errors}")

    return render_template('eform.html', form=form_data, name_list=data_list, part_list=parts,
                           address_list=address_list,
                           lastentry=LASTENTRY, error_note=error_note)


NOTE = ""


@app.route('/pform', methods=['GET', 'POST'])
def p_form():
    global NOTE
    form_data = Part()
    if form_data.validate_on_submit():
        data = PEntry(name=form_data.name.data,
                      price=form_data.price.data,
                      qty=form_data.qty.data
                      )
        db.session.add(data)
        db.session.commit()
        NOTE = f"Last entry: Part- {data.name} for ({data.price}) was saved to Inventory"
        return redirect(url_for('p_form'))
    return render_template('pform.html', form=form_data, note=NOTE)


success_note = ""


@app.route('/cform', methods=['GET', 'POST'])
def c_form():
    global success_note
    form_data = Customer_Entry()
    if request.method == "POST":
        if form_data.validate_on_submit():
            print(form_data.validate_on_submit())
            data = CEntry(name=form_data.name.data,
                          address=form_data.address.data,
                          contact=form_data.contact.data
                          )
            db.session.add(data)
            db.session.commit()
            success_note = f"Success: Customer - {data.name}, {data.address}, {data.contact} was created."
            return redirect(url_for('c_form'))
    if form_data.errors != {}:
        for err_msg in form_data.errors.values():
            print(f" There was an error {err_msg}")

    return render_template('cform.html', form=form_data, success_note=success_note)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    Query = db.session.query(PEntry)

    if request.method == "GET":
        if request.args.get('sort') and request.args.get('sort') == 'name':
            results = Query.order_by(PEntry.name).all()
        else:
            results = Query.all()
        if request.args.get('delete_btn'):
            Query.filter_by(part_id=request.args.get('delete_btn')).delete()
            db.session.commit()
            return redirect(url_for('delete'))
        if request.args.get('edit'):
            item = Query.filter_by(part_id=request.args.get('edit')).first()
            return render_template('edit.html', item=item)
        if request.args.get('newval'):
            Query.filter_by(part_id=request.args.get('hid')).first().qty = request.args.get('newval')
            db.session.commit()
            return redirect(url_for('delete'))

    NOTE = ""
    print(request.method, request.args, request.form)
    if request.method == "POST":
        results = []
        if request.form['name']:
            results += Query.filter(PEntry.name.like(f"%{request.form['name']}%"))
            print(results, Query)
            if not results:
                NOTE = "Not found in database"
            else:
                NOTE = f"{len(results)} entry/ies found"
    # print(results)
    return render_template('delete.html', results=results, note=NOTE)


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    Query = db.session.query(PEntry)
    if request.method == "GET":
        if request.args.get('sort') and request.args.get('sort') == 'name':
            results = Query.order_by(PEntry.name).all()
        else:
            results = Query.all()
    NOTE = ""
    print(request.method, request.args, request.args.get('sort'))
    if request.method == "POST":
        results = []
        if request.form['name']:
            results += Query.filter(PEntry.name.like(f"%{request.form['name']}%"))
            print(results, Query)
            if not results:
                NOTE = "Not found in database"
            else:
                NOTE = f"{len(results)} entry/ies found"
    return render_template('inventory.html', results=results, note=NOTE)


@app.route('/customerlist', methods=["GET", "POST"])
def customerlist():
    query = db.session.query(CEntry)
    results = query.order_by(CEntry.name).all()
    form_data = search_form()
    NOTE = ""

    if request.args.get('sort'):
        if request.args.get('sort') == 'name':
            items = query.order_by(desc(CEntry.name)).all()
            return render_template('customerlist.html', form=form_data, results=items, note=NOTE)
        else:
            slug_id = request.args.get('sort')
            t = 0
            total = ""
            customer_data = CEntry.query.filter_by(cust_id=slug_id).first()
            customer_purchased_data = DEntry.query.filter_by(cust_id=slug_id)
            print("slug", slug_id, datetime.datetime.now().strftime('%H:%M'))
            print(customer_data, customer_purchased_data)
            for item in customer_purchased_data:
                t += item.price
            c = 0
            l = len(str(int(t)))
            for item in reversed(str(int(t))):
                c += 1
                total += item
                l -= 1
                if c == 3 and l > 0:
                    total += ","
                    c = 0

            return render_template('customerdata.html', customer_data=customer_data,
                                   customer_purchased_data=customer_purchased_data.all(), total=total[::-1])

    if request.method == "POST":
        results = []
        if form_data.data['S_name']:
            results += query.filter(CEntry.name.like(f"%{form_data.data['S_name']}%"))
        if form_data.data['S_address']:
            results += query.filter(CEntry.address.like(f"%{form_data.data['S_address']}%"))
    if not results:
        NOTE = "Not found in database"
    else:
        NOTE = f"{len(results)} entry/ies"

    return render_template('customerlist.html', form=form_data, results=results, note=NOTE)


