Warning: You have requested next@15.0.4 but the supported version is 15.3.1, 
abandon all hope ye who enter here.
Warning: Database is not initialized, run reflex db init first.
[WARN] Parameter '_user_agent_entry' is deprecated; use 'user_agent_entry' instead. This parameter will be removed in the upcoming releases.
Databricks dialect ignores SQLAlchemy's autoincrement semantics. Use explicit Identity() instead.
Databricks dialect ignores SQLAlchemy's autoincrement semantics. Use explicit Identity() instead.
Databricks dialect ignores SQLAlchemy's autoincrement semantics. Use explicit Identity() instead.

CREATE TABLE experiments (
	id INT NOT NULL, 
	name STRING NOT NULL, 
	date DATE NOT NULL, 
	CONSTRAINT experiments_pk PRIMARY KEY (id)
) USING DELTA
TBLPROPERTIES('delta.feature.allowColumnDefaults' = 'enabled')



CREATE TABLE data_types (
	id INT NOT NULL, 
	type_name STRING NOT NULL, 
	CONSTRAINT data_types_pk PRIMARY KEY (id)
) USING DELTA
TBLPROPERTIES('delta.feature.allowColumnDefaults' = 'enabled')



CREATE TABLE data_points (
	id INT NOT NULL, 
	experiment_id INT NOT NULL, 
	data_type_id INT NOT NULL, 
	step INT NOT NULL, 
	value FLOAT NOT NULL, 
	CONSTRAINT data_points_pk PRIMARY KEY (id), 
	CONSTRAINT data_points_experiments_fk FOREIGN KEY(experiment_id) REFERENCES experiments (id), 
	CONSTRAINT data_points_data_types_fk FOREIGN KEY(data_type_id) REFERENCES data_types (id)
) USING DELTA
TBLPROPERTIES('delta.feature.allowColumnDefaults' = 'enabled')


