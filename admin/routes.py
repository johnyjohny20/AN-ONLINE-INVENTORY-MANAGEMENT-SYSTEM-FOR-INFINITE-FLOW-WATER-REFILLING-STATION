

from flask import Blueprint, redirect, render_template, flash, request, url_for
from assets.form_fields import *
from db.models import *
from db.database import db
from flask_login import current_user, login_required, logout_user
admin = Blueprint('admin', __name__,
static_folder='static', template_folder='templates', static_url_path='/static/admin')

#registering the api blueprint
from api.routes import api
admin.register_blueprint(api, url_prefix='/api')
@admin.app_context_processor
def get_current():
    return dict(current = current_user.user, cid=current_user.id)

@admin.route('/')
@login_required
def index():
    return render_template('dashboard.html')
"""
This is used only for silent adding in the database,
manual migration
"""
@admin.route('/silentadd')
def silent_add():
    users_all =  db.session.query(Admin).order_by(Admin.id.desc()).all()
    form = silent_form()
    return render_template('silent_add.html',form=form, data=users_all )


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Succesfully Logout!', 'success')
    return redirect(url_for('login.index'))

    
@admin.route('/users')
@login_required
def users():
    users_all =  db.session.query(Admin).order_by(Admin.id.desc()).limit(10).all()
    print(users_all)
    return render_template('manage_user.html', users=users_all)
#add users 
@admin.route('/users/add')
@login_required
def add_users():
    form = add_user()
    return render_template('add_users.html', form=form)

#editing section endpoints
@admin.route('users/edit/<id>')
@login_required
def edit_users(id):
    name = Admin.query.filter_by(id=id).first()
    form = add_user()
    return render_template('admin_edit.html', form=form, name=name)
@admin.route('products/edit/<id>')
@login_required
def edit_product(id):
    name = Product.query.filter_by(id=id).first()
    form = add_products()
    return render_template('edit/product_edit.html', form=form, name=name)
@admin.route('catalogs/edit/<id>')
@login_required
def edit_catalog(id):
    name = Catalog.query.filter_by(id=id).first()
    form = catalog_forms()
    return render_template('edit/catalog_edit.html', form=form, name=name)
@admin.route('customers/edit/<id>')
@login_required
def edit_customers(id):
    name = Customer.query.filter_by(id=id).first()
    form = customer()
    return render_template('edit/customer_edit.html', form=form, name=name)


# main endpoints for the dashboard
@admin.route('/products', methods=['POST', 'GET'])
@login_required
def manage_product():
  
    form1 = select_catalog()
    form2 = catalog_forms()
    form3 = add_products()
    # for the catalogs fetch
    product_catalog = db.session.query(Catalog).order_by(Catalog.id.desc()).all()
    # for the products, it will get the first data by the first catalog name by itself.
    catalog = Catalog.query.first()
    print(catalog)
    try:
        catalog_child = catalog.products
    except:
        catalog_child = []
    return render_template('manage_products.html', form1=form1, form2=form2, form3=form3,
    catalog=product_catalog, products=catalog_child)

@admin.route('/customers')
@login_required
def manage_customers():
    name = db.session.query(Customer).order_by(Customer.id.desc()).all()
    form = customer()
    return render_template('customer_management.html', form=form, name=name)
@admin.route('/transaction')
@login_required
def manage_transaction():
    form1 = transaction()
    form2 = product_transaction()

    data_transaction = transaction_data.query.all()

    from api.branch.graph import total_count, total_pendingdel, total_notdel
    total_trans = total_count()
    total_pending = total_pendingdel()
    total_not = total_notdel()
    return render_template(
        'transaction_manage.html', 
        form1=form1, form2=form2, transaction=data_transaction,
        total_trans = total_trans, total_pending=total_pending,
        total_not =total_not
        )
