Hi Taavo,

I hope this message finds you well. Please find below the notes regarding the state and progress of converting MIT to work against Redshift.

### EIA
To enable EIA to function with Redshift, the following steps are required:

#### Transformation Script Modifications
- **Modify the transformation script to work against Redshift.**  
  *In progress (estimated completion: end of day Friday)*
- **Update the SQL that generates the dependency views for the transformation script.**  
  *In progress (estimated completion: end of day Friday)*
- **Ensure the transformation script does not use schemas, as Redshift does not utilize schemas.**  
  *In progress (estimated completion: end of day Friday)*
- **Update the script that creates the EIA metadata table on which EIA relies.**  
  *In progress (estimated completion: end of day Friday)*

#### EIA App Modifications
- **Change the connection from Snowflake to Redshift.**  
  *Done*
- **Update the SQL that generates the grids and lag charts to work against Redshift.**  
  *Done (awaiting testing)*

### Model Manager
To ensure the Model Manager works with Redshift, the following tasks need to be completed:
- **Update the modeling and scoring process to populate metadata tables in Redshift.**
- **Update the Model Manager SQL to work against tables in Redshift.**

### Model Interpreter
- **Update the SQL that creates the charts and grids to work against Redshift.**  
  *Note:* The SQL in this part of the app is still pointing to the SHAP tables, not the P-Allocs tables. Should I change this to work with P-Allocs? The current SQL may not work with Redshift.
- **Perform testing.**

### AvsB
- **Update the SQL that creates the charts and grids to work against Redshift.**  
  *Note:* The SQL in this part of the app is still pointing to the SHAP tables, not the P-Allocs tables. Should I change this to work with P-Allocs? The current SQL may not work with Redshift.

Please let me know if you have any questions or need further details.

Best regards,  
[Your Name]

