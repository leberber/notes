


from dash import Dash, html, dcc, callback, Output, Input, State, no_update
import pandas as pd 
from dash_iconify import DashIconify
import numpy as np

from sklearn import svm
from sklearn.model_selection import train_test_split 
from features import feature_list
# print(feature_list)
import dash_mantine_components as dmc
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
df = pd.read_csv("cleaned_data.csv", index_col=0)
X= df.drop(['Target'],axis=1)
y=df['Target']
svc = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo', probability=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 0)

print(X_test.iloc[42])

feature_list = {"Application mode" :  {
      "1st phase - general contingent": 1,
      "Ordinance No. 612/93": 2,
      "1st phase - special contingent (Azores Island)": 5,
      "Holders of other higher courses": 7,
      "Ordinance No. 854-B/99": 10,
      "International student (bachelor)": 15,
      "1st phase - special contingent (Madeira Island)": 16,
      "2nd phase - general contingent": 17,
      "3rd phase - general contingent": 18,
      "Ordinance No. 533-A/99, item b2) (Different Plan)": 26,
      "Ordinance No. 533-A/99, item b3 (Other Institution)": 27,
      "Over 23 years old": 39,
      "Transfer": 42,
      "Change of course": 43,
      "Technological specialization diploma holders": 44,
      "Change of institution/course": 51,
      "Short cycle diploma holders": 53,
      "Change of institution/course (International)": 57
    },
"Application order" :[1,9],
"Course" :  {
      "Biofuel Production Technologies": 33,
      "Animation and Multimedia Design": 171,
      "Social Service (evening attendance)": 8014,
      "Agronomy": 9003,
      "Communication Design": 9070,
      "Veterinary Nursing": 9085,
      "Informatics Engineering": 9119,
      "Equinculture": 9130,
      "Management": 9147,
      "Social Service": 9238,
      "Tourism": 9254,
      "Nursing": 9500,
      "Oral Hygiene": 9556,
      "Advertising and Marketing Management": 9670,
      "Journalism and Communication": 9773,
      "Basic Education": 9853,
      "Management (evening attendance)": 9991
    },

"Previous qualification (grade)" : [0,200],
  
"Mother's qualification" : {
    "Secondary Education - 12th Year of Schooling or Eq.": 1,
    "Higher Education - Bachelor's Degree": 2,
    "Higher Education - Degree": 3,
    "Higher Education - Master's": 4,
    "Higher Education - Doctorate": 5,
    "Frequency of Higher Education": 6,
    "12th Year of Schooling - Not Completed": 9,
    "11th Year of Schooling - Not Completed": 10,
    "7th Year (Old)": 11,
    "Other - 11th Year of Schooling": 12,
    "10th Year of Schooling": 14,
    "General commerce course": 18,
    "Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.": 19,
    "Technical-professional course": 22,
    "7th Year of Schooling": 26,
    "2nd Cycle of the General High School Course": 27,
    "9th Year of Schooling - Not Completed": 29,
    "8th Year of Schooling": 30,
    "Unknown": 34,
    "Can't read or write": 35,
    "Can read without having a 4th Year of Schooling": 36,
    "Basic Education 1st Cycle (4th/5th Year) or Equiv.": 37,
    "Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.": 38,
    "Technological specialization course": 39,
    "Higher Education - Degree (1st cycle)": 40,
    "Specialized Higher Studies Course": 41,
    "Professional Higher Technical Course": 42,
    "Higher Education - Master (2nd cycle)": 43,
    "Higher Education - Doctorate (3rd cycle)": 44
},
"Father's qualification": {
    "Secondary Education - 12th Year of Schooling or Eq.": 1,
    "Higher Education - Bachelor's Degree": 2,
    "Higher Education - Degree": 3,
    "Higher Education - Master's": 4,
    "Higher Education - Doctorate": 5,
    "Frequency of Higher Education": 6,
    "12th Year of Schooling - Not Completed": 9,
    "11th Year of Schooling - Not Completed": 10,
    "7th Year (Old)": 11,
    "Other - 11th Year of Schooling": 12,
    "2nd year complementary high school course": 13,
    "10th Year of Schooling": 14,
    "General commerce course": 18,
    "Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.": 19,
    "Complementary High School Course": 20,
    "Technical-professional course": 22,
    "Complementary High School Course - not concluded": 25,
    "7th year of schooling": 26,
    "2nd cycle of the general high school course": 27,
    "9th Year of Schooling - Not Completed": 29,
    "8th year of schooling": 30,
    "General Course of Administration and Commerce": 31,
    "Supplementary Accounting and Administration": 33,
    "Unknown": 34,
    "Can't read or write": 35,
    "Can read without having a 4th year of schooling": 36,
    "Basic education 1st cycle (4th/5th year) or equiv.": 37,
    "Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.": 38,
    "Technological specialization course": 39,
    "Higher education - degree (1st cycle)": 40,
    "Specialized higher studies course": 41,
    "Professional higher technical course": 42,
    "Higher Education - Master (2nd cycle)": 43,
    "Higher Education - Doctorate (3rd cycle)": 44
},
"Mother's occupation": {
    "Student": 0,
    "Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers": 1,
    "Specialists in Intellectual and Scientific Activities": 2,
    "Intermediate Level Technicians and Professions": 3,
    "Administrative staff": 4,
    "Personal Services, Security and Safety Workers and Sellers": 5,
    "Farmers and Skilled Workers in Agriculture, Fisheries and Forestry": 6,
    "Skilled Workers in Industry, Construction and Craftsmen": 7,
    "Installation and Machine Operators and Assembly Workers": 8,
    "Unskilled Workers": 9,
    "Armed Forces Professions": 10,
    "Other Situation": 90,
    "(blank)": 99,
    "Health professionals": 122,
    "Teachers": 123,
    "Specialists in information and communication technologies (ICT)": 125,
    "Intermediate level science and engineering technicians and professions": 131,
    "Technicians and professionals, of intermediate level of health": 132,
    "Intermediate level technicians from legal, social, sports, cultural and similar services": 134,
    "Office workers, secretaries in general and data processing operators": 141,
    "Data, accounting, statistical, financial services and registry-related operators": 143,
    "Other administrative support staff": 144,
    "Personal service workers": 151,
    "Sellers": 152,
    "Personal care workers and the like": 153,
    "Skilled construction workers and the like, except electricians": 171,
    "Skilled workers in printing, precision instrument manufacturing, jewelers, artisans and the like": 173,
    "Workers in food processing, woodworking, clothing and other industries and crafts": 175,
    "Cleaning workers": 191,
    "Unskilled workers in agriculture, animal production, fisheries and forestry": 192,
    "Unskilled workers in extractive industry, construction, manufacturing and transport": 193,
    "Meal preparation assistants": 194
},
  
"Father's occupation": {
    "Student": 0,
    "Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers": 1,
    "Specialists in Intellectual and Scientific Activities": 2,
    "Intermediate Level Technicians and Professions": 3,
    "Administrative staff": 4,
    "Personal Services, Security and Safety Workers and Sellers": 5,
    "Farmers and Skilled Workers in Agriculture, Fisheries and Forestry": 6,
    "Skilled Workers in Industry, Construction and Craftsmen": 7,
    "Installation and Machine Operators and Assembly Workers": 8,
    "Unskilled Workers": 9,
    "Armed Forces Professions": 10,
    "Other Situation": 90,
    "(blank)": 99,
    "Armed Forces Officers": 101,
    "Armed Forces Sergeants": 102,
    "Other Armed Forces personnel": 103,
    "Directors of administrative and commercial services": 112,
    "Hotel, catering, trade and other services directors": 114,
    "Specialists in the physical sciences, mathematics, engineering and related techniques": 121,
    "Health professionals": 122,
    "Teachers": 123,
    "Specialists in finance, accounting, administrative organization, public and commercial relations": 124,
    "Intermediate level science and engineering technicians and professions": 131,
    "Technicians and professionals, of intermediate level of health": 132,
    "Intermediate level technicians from legal, social, sports, cultural and similar services": 134,
    "Information and communication technology technicians": 135,
    "Office workers, secretaries in general and data processing operators": 141,
    "Data, accounting, statistical, financial services and registry-related operators": 143,
    "Other administrative support staff": 144,
    "Personal service workers": 151,
    "Sellers": 152,
    "Personal care workers and the like": 153,
    "Protection and security services personnel": 154,
    "Market-oriented farmers and skilled agricultural and animal production workers": 161,
    "Farmers, livestock keepers, fishermen, hunters and gatherers, subsistence": 163,
    "Skilled construction workers and the like, except electricians": 171,
    "Skilled workers in metallurgy, metalworking and similar": 172,
    "Skilled workers in electricity and electronics": 174,
    "Workers in food processing, woodworking, clothing and other industries and crafts": 175,
    "Fixed plant and machine operators": 181,
    "Assembly workers": 182,
    "Vehicle drivers and mobile equipment operators": 183,
    "Unskilled workers in agriculture, animal production, fisheries and forestry": 192,
    "Unskilled workers in extractive industry, construction, manufacturing and transport": 193,
    "Meal preparation assistants": 194,
    "Street vendors (except food) and street service providers": 195
},
"Admission grade" : [0.0, 200.0],

"Displaced":{
    "yes": 1,
    "no": 0
},

"Debtor" : {
    "yes": 1,
    "no": 0
},

"Tuition fees" :{
    "yes": 1,
    "no": 0
},

"Gender": {
    "male": 1,
    "female": 0
},

"Scholarship holder":{
    "yes": 1,
    "no": 0
},

"Age at enrollment": [16, 90],

"Curricular units 1st sem (evaluations)" : [0,60],
"Curricular units 1st sem (approved)" : [0, 60],
"Curricular units 1st sem (grade)" :[0.0,60,0],
"Curricular units 2nd sem (evaluations)": [0, 30],
"Curricular units 2nd sem (approved)": [0, 60],
"Curricular units 2nd sem (grade)":[0.0,30.0],
"Unemployment rate":[0.0, 0.25],
"Inflation rate":[-0.05, 0.2],
"GDP":[0.05,20.0]

  
}


X_train = sc.fit_transform(X_train.values)
X_test = sc.transform(X_test.values)
svc.fit(X_train, y_train)




# y = df['Target']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
# model = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo')
# model.fit(X_train, y_train)

    
def label_value (label, value):
    return dmc.Paper(
        style = {'display':'flex'},  p = 3,
        children = [
            dmc.Text(f'Input {label}', color='gray',  w=320),
            value
        ]



    )
drop_downs = []
for key, value in feature_list.items():
    _id = key.replace("'",'')
    _id = _id.replace(" ",'_')
    _id = _id.replace("(",'_')
    _id = _id.replace(")",'_')

    if type(value) == list:
        if type(value[0]) == float:
            numveric = dmc.NumberInput(
                    # label="Number input with decimal steps",
                    id= _id,
                    value=value[0],
                    precision=2,
                    min=value[0],
                    # step=0.05,
                    max=value[1],
                    style={"width": 300},
                    
                )
            
            drop_downs.append(label_value (key, numveric))

        else:
            options = [ {'label': str(i),  'value':i} for i in range(value[0], value[1])]
            drop = dmc.Select(
                data=options,
                searchable=True,
                nothingFound="No options found",
                style={"width": 300},
                id=_id,
                value = options[0]['value']
            )
            drop_downs.append(label_value (key, drop))

    else:
        options = [{'label': key, 'value': value} for key, value in value.items()]

        drop = dmc.Select(
            data=options,
            searchable=True,
            nothingFound="No options found",
            style={"width": 300},
            value = options[0]['value'],
            id=_id
        )
        drop_downs.append(label_value (key, drop))

    # print(f"State('{_id}', 'value' ),")


app = Dash(__name__)


app.layout = html.Div(
children = [   
    dmc.Center(
        
        children =[
            html.Div(
                children = [
                    dmc.Text('Title here', size=22, fw=500),
                    html.Div(
                        style = {'display':'flex'},
                        children = [
                            dmc.Paper(drop_downs[:12], shadow='md', m = 10, p = 12),
                            dmc.Paper(drop_downs[12:], shadow='md', m = 10, p = 12),  
                        ]
                    ),
                    dmc.Button(
                        "Predict",   
                        id = 'predict',
                        mt = 10,
                        # mr = '20%',
                        style = {'float':'right'},
                        leftIcon=DashIconify(icon="carbon:machine-learning-model"),
                        variant="gradient",
                        gradient={"from": "teal", "to": "lime", "deg": 105},
                    ),
                    dmc.Text("Please enter the candidate's values and click 'Predict' to see whether the student is likely to graduate or drop out", color='gray'),
                    html.Div(id = 'prediction')
                ]
            )
          
        ]
    ),

    
])

@callback(
    Output("prediction", "children"), 
    
    State('Application_mode', 'value' ),
    State('Application_order', 'value' ),
    State('Course', 'value' ),
    State('Previous_qualification__grade_', 'value' ),
    State('Mothers_qualification', 'value' ),

    State('Fathers_qualification', 'value' ),
    State('Mothers_occupation', 'value' ),
    State('Fathers_occupation', 'value' ),
    State('Admission_grade', 'value' ),
    State('Displaced', 'value' ),
    State('Debtor', 'value' ),

    State('Tuition_fees', 'value' ),
    State('Gender', 'value' ),
    State('Scholarship_holder', 'value' ),
    State('Age_at_enrollment', 'value' ),
    State('Curricular_units_1st_sem__evaluations_', 'value' ),

    State('Curricular_units_1st_sem__approved_', 'value' ),
    State('Curricular_units_1st_sem__grade_', 'value' ),
    State('Curricular_units_2nd_sem__evaluations_', 'value' ),
    State('Curricular_units_2nd_sem__approved_', 'value' ),
    State('Curricular_units_2nd_sem__grade_', 'value' ),

    State('Unemployment_rate', 'value' ),
    State('Inflation_rate', 'value' ),
    State('GDP', 'value' ),

    Input("predict", "n_clicks")
)
def checkbox(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, predict):
    d = {1:'Drop Out', 0:'Graduate'}
    if not predict:
        return no_update
    ob = [[v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24]]
    ob = np.array(ob) 
    # print(ob)
    # for ix, i in enumerate(range(100)):
    #     print(ix, svc.predict([X_test[i]]))
    print(svc.predict(X_test))
    ob = sc.transform(ob)
    pr = int(svc.predict(ob)[0])
    # print('HHHHH')
    # print(type(pr))
    # print(svc.predict_proba([ob]) [:,1])
    # print(d[pr])
    return dmc.Text(d[pr], color='gray')
                


if __name__ == '__main__':
     app.run(debug=True, port = 8730)
