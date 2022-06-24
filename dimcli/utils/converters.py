from .misc_utils import printDebug
from .dim_utils import dimensions_url
from collections import OrderedDict


# ===========
# TESTING - UNSUPPORTED FEATURE
# ===========
#

class DslDataConverter():
	"""
	Helper class containing methods for transforming JSON complex snippets to other formats.
	Useful eg for creating a nice looking CSV from raw API data.

	Status: ALPHA - UNSUPPORTED FEATURE

	Converters subclasses available only for
	* Pubs
	* Grants
	* Clinical Trials
	* Datasets 
	Missing: Patents, Organizations, Policy Documents


	Example
	========
	>>> from dimcli.utils.converters import *
	>>> df_temp = dsl.query_iterative("search publications return publications").as_dataframe()
	>>> c1 = DslDatasetsConverter(df_temp)
	>>> df_final = c1.run()

	ALGORITHM
	==========
	# iterate through all keys/columns in dataframe
	#
	# if column name == key in fields_mappings:
	#   apply all functions => generate new columns
	#   remove old column 
	# else if column value is list 
	#   break down list into semicolon delimited string
	#   replace old column
	#
	#  PS dimensions_url special case, we just add a new column without removing 'ID'
	#   also, it applies only to sources

	"""

	def __init__(self, df, object_type="", verbose=False):

		self.df_original = df
		self.df_modified = None

		self.object_type = object_type
		# self.df_converted = df.copy()
		self.verbose = verbose

		self.columns_original = self.df_original.columns.to_list()
		if self.verbose: printDebug("Original columns are:", self.columns_original)

		# PS decided to not deal with DEPRECATED FIELDS!
		# self.column_transformations_old = {
		#     # ('new_col_name', 'fun_name')
		# }

		self.column_transformations = OrderedDict()


	def run(self):
		"""@TODO define a suitable abstraction for automatic transformation
		eg simplify all fields to strings
		"""
		self.apply_transformations()
		self.sort_and_prune()
		return self.df_modified




	#
	#
	# Helpers METHODS
	#
	#

	def apply_transformations(self):
		"""

		"""
		if self.verbose: printDebug("Applying transformations..")
		
		df = self.df_original.copy()
		
		if self.column_transformations:
			for new_col, details in self.column_transformations.items():
				source, action, arg = details[0], details[1], None
				if len(details)>2:
					arg = details[2]
				if source in self.columns_original:
					if self.verbose: printDebug(f"...converting '{source}' to '{new_col}'")
					if action:
						function = getattr(self, action)
						if arg:
							df[new_col] = df[source].fillna("").apply(lambda cell: function(cell, arg))
						else:
							df[new_col] = df[source].fillna("").apply(lambda cell: function(cell))
					else:
						df[new_col] = df[source]

		df.fillna('', inplace=True)
		self.df_modified = df
		return self.df_modified


	def sort_and_prune(self, new_cols_ordered_list=None, keep_extra_cols=True):
		"""generate a default order if not provided, keeping only those cols
		
		keep_extra_cols:
			bool, False
			Columns not included in the transformation rules are dropped by default.
		
		"""

		if self.verbose: printDebug("Sorting / dropping columns...")

		if new_cols_ordered_list and type(new_cols_ordered_list) == list:
			self.df_modified = self.df_modified[new_cols_ordered_list]
		else:
			# infer from all declared columns
			new_cols_ordered_list = []
			new_cols_ordered_list_prev_names = []
			existing_cols = self.df_modified.columns.to_list()

			for new_col in self.column_transformations:
				# PS ensure declared cols actually exist!!
				if new_col in existing_cols:
					new_cols_ordered_list.append(new_col)
					prev_name = self.column_transformations[new_col][0]
					new_cols_ordered_list_prev_names.append(prev_name)

		if keep_extra_cols:
			# add to the right any column not touched by transformations
			for col in self.df_modified:
				if col not in new_cols_ordered_list:
					if col not in new_cols_ordered_list_prev_names:
						new_cols_ordered_list.append(col)

		if new_cols_ordered_list:
			self.df_modified = self.df_modified[new_cols_ordered_list]
		
		return self.df_modified



	def truncate_for_gsheets(self, cols_subset=None):
		"""
		helper to avoid gsheets error
		'Your input contains more than the maximum of 50000 characters in a single cell.'

		cols_subset: eg ['Abstract', 'Authors', 'Authors Affiliations']

		"""

		if self.verbose: printDebug("Truncating strings longer than 50k chars...")

		def helper(s):
			# printDebug(len(str(s)))
			# n = str(s)[:49500]
			# printDebug(len(str(n)))
			if len(str(s)) > 49500:
				n = str(s)[:49500]
				return n + "..."
			return s

		if cols_subset:
			for col in cols_subset:
				self.df_modified[col] = self.df_modified[col].apply(lambda x: helper(x))



	#
	#
	# CONVERSION METHODS
	#
	#


	def convert_id_to_url(self, idd, ttype=None):
		"""
		"""
		if ttype:
			return dimensions_url(idd, ttype)
		else:
			return dimensions_url(idd)


	def convert_authors_to_names(self, authorslist):
		"""
		"""
		authors = []
		for x in authorslist:
			name = x.get('last_name', "") + ", "+ x.get('first_name', "") 
			authors.append(name)
		return "; ".join(authors)


	def convert_authors_corresponding(self, authorslist):
		authors = []
		for x in authorslist:
			if x.get("corresponding", ""):
				name = x.get('last_name', "") + ", "+ x.get('first_name', "")
				authors.append(name)
		return "; ".join(authors)        

	def convert_authors_affiliations(self, authorslist):
		"""
		"""
		author_affiliations = []
		for x in authorslist:
			name = x.get('last_name', "") + ", "+ x.get('first_name', "")
			affiliations = "; ".join([a.get('name', "") for a in x['affiliations']])
			author_affiliations.append(f"{name} ({affiliations})")
		return "; ".join(author_affiliations)

	def convert_investigators_cltrials(self, investigatorslist):
		"""
		From: 
		[['Chaoqian Li', '', 'Study leader', '6 Shuangyong Road, Nanning, Guangxi Zhuang Autonomous Region, China', '', ''], ['Jianlin Huang', '', 'Applicant', "Beihai People's Hospital", "Beihai People's Hospital", 'grid.452719.c']]
		To
		"Chaoqian Li; Jianlin Huang"
		"""
		return "; ".join([x[0] for x in investigatorslist]) 

	def convert_list(self, data):
		return "; ".join([str(x) for x in data])

	def convert_dict_name(self, data):
		return "; ".join([y['name'] for y in data])

	def convert_dict_ids(self, data):
		return "; ".join([y['id'] for y in data])

	def convert_city_name(self, data):
		return "; ".join([y['city_name'] for y in data])

	def convert_state_name(self, data):
		return "; ".join([y['city_name'] for y in data])

	def convert_country_name(self, data):
		return "; ".join([y['country_name'] for y in data])

	def convert_interventions_dict(self, data):
		"""
		Return 'name' and 'type' for clinical trials / interventions 

		From: "[{'arm_group_labels': 'Hydroxychloroquine and conventional treatments', 'type': 'Drug', 'description': 'Subjects take hydroxychloroquine 400 mg per day for 5 days, also take conventional treatments', 'other_names': '', 'name': 'Hydroxychloroquine'}]"
		
		To: "Hydroxychloroquine (Drug)"
		"""
		return "; ".join([f"{x.get('name', '')} ({x.get('type', '')})" for x in data])

	def convert_float_to_integer(self, data):
		try:
			return int(data)
		except:
			return data


	def convert_abstract_to_preview(self, abstract):
		"""
		"""
		if abstract:
			return ""
			# May 22, 2020
			# return " ".join(abstract.split()[:20]) + "..."
		else:
			return ""




class DslPubsConverter(DslDataConverter):
	"""
	"""

	def __init__(self, df, verbose=False):

		super().__init__(df, "publications", verbose)

		## OVERRRIDE VALUES

		self.column_transformations = OrderedDict({
			# ('new_col_name', 'fun_name')
			'Date added' : ('date_inserted', ''), 
			'Publication ID' : ('id', ''), 
			'DOI' : ('doi', ''), 
			'PMID' : ('pmid', ''), 
			'PMCID' : ('pmcid', ''), 
			'Title' : ('title', ''), 
			'Abstract' : ('abstract', ''), 
			'Source title' : ('journal.title', ''), 
			'Source ID' : ('journal.id', ''), 
			'Publisher' : ('publisher', ''), 
			'MeSH terms' : ('mesh_terms', 'convert_list'), 
			'Publication Date' : ('date', ''), 
			'PubYear' : ('year', ''), 
			'Volume' : ('volume', ''), 
			'Issue' : ('issue', ''), 
			'Pagination' : ('pages', ''), 
			'Open Access' : ('open_access_categories', 'convert_dict_name'), 
			'Publication Type' : ('type', ''), 
			'Authors' : ('authors', 'convert_authors_to_names'), 
			'Corresponding Authors' : ('authors', 'convert_authors_corresponding'), 
			'Authors Affiliations' : ('authors', 'convert_authors_affiliations'), 
			'Research Organizations - standardized' : ('research_orgs', 'convert_dict_name'), 
			'GRID IDs' : ('research_orgs', 'convert_dict_ids'), 
			'City of Research organization' : ('research_orgs', 'convert_city_name'), 
			# 'State of Research organization' : ('research_orgs', 'convert_state_name'), 
			'Country of Research organization' : ('research_orgs', 'convert_country_name'), 
			'Funder' : ('funders', 'convert_dict_name'), 
			'UIDs of supporting grants' : ('supporting_grant_ids', 'convert_list'), 
			# TODO Supporting Grants (proj number?)
			'Times cited' : ('times_cited', 'convert_float_to_integer'), 
			'Altmetric' : ('altmetric', 'convert_float_to_integer'), 
			'Source Linkout' : ('linkout', ''), 
			'Dimensions URL' : ('id', 'convert_id_to_url'), 
			# NOT USED
			'FOR (ANZSRC) Categories' : ('category_for', 'convert_dict_name'), 
			'RCDC Categories' : ('category_rcdc', 'convert_dict_name'), 
			'HRCS HC Categories' : ('category_hrcs_hc', 'convert_dict_name'), 
			'HRCS RAC Categories' : ('category_hrcs_rac', 'convert_dict_name'), 
			'ICRP Cancer Types' : ('category_icrp_ct', 'convert_dict_name'), 
			'ICRP CSO Categories' : ('category_icrp_cso', 'convert_dict_name'), 
		})


	def run(self):
		"""
		"""
		self.apply_transformations()
		self.sort_and_prune()
		if False:
			self.truncate_for_gsheets(['Abstract', 'Authors', 'Authors Affiliations'])
		return self.df_modified








class DslDatasetsConverter(DslDataConverter):
	"""
	"""

	def __init__(self, df, verbose=False):

		super().__init__(df, "datasets", verbose)

		## OVERRRIDE VALUES

		self.column_transformations = OrderedDict({
			'Date added' : ('date_inserted', ''), 
			'Dataset ID' : ('id', ''), 
			'DOI' : ('doi', ''), 
			'Title' : ('title', ''), 
			'Description' : ('description', ''), 
			'Repository' : ('repository_id', ''), 
			'Publication year' : ('year', ''), 
			'Dataset author' : ('authors', 'convert_dict_name'), 
			'Associated publication' : ('associated_publication_id', ''), 
			'Source Linkout' : ('figshare_url', ''), 
			'Dimensions URL' : ('id', 'convert_id_to_url', 'datasets'), 
		})


	def run(self):
		"""
		"""
		self.apply_transformations()
		self.sort_and_prune()        
		if False:
			# TODO clarify when to use
			self.truncate_for_gsheets(['Description'])
			self.sort_and_prune()
		return self.df_modified





class DslClinicaltrialsConverter(DslDataConverter):
	"""
	"""

	def __init__(self, df, verbose=False):

		super().__init__(df, "clinical_trials", verbose)

		self.column_transformations = OrderedDict({
			'Date added' : ('date_inserted', ''), 
			'Trial ID' : ('id', ''), 
			'Title' : ('title', ''), 
			'Brief title' : ('brief_title', ''), 
			'Acronym' : ('acronym', ''), 
			'Abstract' : ('abstract', ''), 
			'Publication date' : ('date', ''), 
			'Active years' : ('active_years', 'convert_list'), 
			'Phase' : ('phase', ''), 
			'Conditions' : ('conditions', 'convert_list'), 
			'Intervention' : ('interventions', 'convert_interventions_dict'), 
			'Gender' : ('gender', ''), 
			'Registry' : ('registry', ''), 
			'Investigators/Contacts' : ('investigators', 'convert_investigators_cltrials'), 
			'Sponsors/Collaborators' : ('research_orgs', 'convert_dict_name'), 
			'GRID IDs' : ('research_orgs', 'convert_dict_ids'), 
			# 'City of Sponsor/Collaborator' : ('research_orgs', ''), 
			# 'State of Sponsor/Collaborator' : ('research_orgs', ''), 
			'Country of Sponsor/Collaborator' : ('research_orgs', 'convert_country_name'), 
			'Collaborating Funders' : ('funders', 'convert_dict_name'), 
			'Funder Country' : ('funders', 'convert_country_name'), 
			'Source Linkout' : ('linkout', ''), 
			'Dimensions URL' : ('id', 'convert_id_to_url', 'clinical_trials'), 
		})


	def run(self):
		"""
		"""
		
		self.apply_transformations()
		self.sort_and_prune()
		if False:
			# TODO clarify when to use
			self.truncate_for_gsheets(['Abstract'])
		return self.df_modified






class DslGrantsConverter(DslDataConverter):
	"""
	"""

	def __init__(self, df, verbose=False):

		super().__init__(df, "grants", verbose)

		self.column_transformations = OrderedDict({
			'Date added' : ('date_inserted', ''), 
			'Grant ID' : ('id', ''), 
			'Title' : ('title', ''), 
			'Abstract' : ('abstract', ''), 
			'Start date' : ('start_date', ''), 
			'End date' : ('end_date', ''), 
			'Funders' : ('funders', 'convert_dict_name'), 
			'Funders GRID IDs' : ('funders', 'convert_dict_ids'), 
			'Funders country' : ('funders', 'convert_country_name'), 
			'Research organizations' : ('research_orgs', 'convert_dict_name'), 
			'Research organizations GRID IDs' : ('research_orgs', 'convert_dict_ids'), 
			'Research organizations country' : ('research_orgs', 'convert_country_name'), 
			'Source linkout' : ('linkout', ''), 
			'Dimensions URL' : ('id', 'convert_id_to_url', 'grants'), 
		})


	def run(self):
		"""
		"""
		self.apply_transformations()
		self.sort_and_prune()
		if False:
			# TODO clarify when to use
			self.truncate_for_gsheets(['Abstract'])
		return self.df_modified
