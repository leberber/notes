Hi Taavo,

Please find the notes below regarding the state and progress of converting MIT to work against Redshift.

1. **EIA**
   To make EIA work against Redshift, the following steps need to be completed:

   - **Transformation Script Modifications:**
     - Modify the transformation script to work against Redshift.
       *In progress (estimated completion: end of day Friday)*
     - Update the SQL that generates the dependency views for the transformation script. *In progress (estimated completion: end of day Friday)*
     - Ensure the transformation script does not use schemas, as Redshift does not utilize schemas. *In progress (estimated completion: end of day Friday)*
     - Update the script that creates the EIA metadata table on which EIA relies. *In progress (estimated completion: end of day Friday)*

   - **EIA App Modifications:**
     - Change the connection from Snowflake to Redshift. *Done*
     - Update the SQL that generates the grids and lag charts to work against Redshift. *Done, awaits testing*

2. **Model Manager**
   To make the Model Manager work against Redshift, the following tasks need to be completed:

   - Update the modeling and scoring process to populate metadata tables in Redshift.
   - Update the Model Manager SQL to work against tables in Redshift.

3. **Model Interpreter**
   - Update the SQL that creates the charts and grids to work against Redshift.
     - *Note:* The SQL in this part of the app is still pointing to the SHAP tables, not the P-Allocs tables. Should I change this to work against P-Allocs? The current SQL may not work against Redshift.
   - Perform testing.

4. **AvsB**
   - Update the SQL that creates the charts and grids to work against Redshift.
     - *Note:* The SQL in this part of the app is still pointing to the SHAP tables, not the P-Allocs tables. Should I change this to work against P-Allocs? The current SQL may not work against Redshift.

Please let me know if you have any questions or need further details.
