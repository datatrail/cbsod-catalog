from flask import Flask, request, session, redirect, url_for, render_template, flash
from py2cbs import CatalogTree, Table

app = Flask(__name__)

tree = CatalogTree(language = 'en')
tree.set_feeds()

@app.route('/')
def index():
	#return redirect('/theme')
	return render_template('index.html')

@app.route('/theme/None',  methods=['GET'])
@app.route('/theme',  methods=['GET'])
def theme_root():
	theme_id = None
	breadcrumbs = []
	children = tree.get_children(theme_id)
	context = {'theme_id':theme_id,'tree':tree, 'children':children, 'breadcrumbs':breadcrumbs}
	return render_template('theme.html', **context)

@app.route('/theme/<theme_id>',  methods=['GET'])
def theme_child(theme_id):
	theme_id = int(theme_id)
	breadcrumbs = tree.get_parents(theme_id) 
	children = tree.get_children(theme_id)
	context = {'theme_id':theme_id,'tree':tree, 'children':children, 'breadcrumbs':breadcrumbs}
	return render_template('theme.html', **context)

@app.route('/table/<tables_themes_id>',  methods=['GET'])
def table(tables_themes_id):
	tables_themes_id = int(tables_themes_id)
	theme_id = tree.get_property('Tables_Themes', tables_themes_id, 'ID', 'ThemeID')
	table_id = tree.get_property('Tables_Themes', tables_themes_id, 'ID', 'TableID')
	identifier = tree.get_property('Tables', table_id, 'ID', 'Identifier')
 	breadcrumbs = tree.get_parents(theme_id)
	children = tree.get_children(theme_id)

	table = Table(identifier)
	context = {'theme_id':theme_id, 'tree':tree, 'children':children, 'breadcrumbs':breadcrumbs, 'tables_themes_id':tables_themes_id, 'table_id':table_id, 'table':table}
	return render_template('table_select.html', **context)

@app.route('/table/<tables_themes_id>/<active_tab>',  methods=['GET', 'POST'])
def table_collection(tables_themes_id, active_tab):
	tables_themes_id = int(tables_themes_id)
	theme_id = tree.get_property('Tables_Themes', tables_themes_id, 'ID', 'ThemeID')
	table_id = tree.get_property('Tables_Themes', tables_themes_id, 'ID', 'TableID')
	identifier = tree.get_property('Tables', table_id, 'ID', 'Identifier')
 	breadcrumbs = tree.get_parents(theme_id)
	children = tree.get_children(theme_id)

	if request.method == 'POST':
		session['collections'] = request.form.getlist('collections')

	query_options = {'UntypedDataSet':'$top=100', 'TypedDataSet':'$top=100'}
	if active_tab == 'Description':
		table = Table(identifier)
	else:
		table = Table(identifier, collections = [active_tab], query_options = query_options)
		table.set_feeds()

	context = {'theme_id':theme_id, 'tree':tree, 'children':children, 'breadcrumbs':breadcrumbs, 'tables_themes_id':tables_themes_id, \
			'table_id':table_id, 'table':table, 'collections':session['collections'], 'active_tab':active_tab}
	return render_template('table_show.html', **context)