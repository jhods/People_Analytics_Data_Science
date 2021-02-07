import pandas as pd
import numpy as np
import datetime

#total employee count
emps_2018 = 12500

#new hire rate per year
new_hire_rate = 0.15

min_age = 21
max_age = 65

#employee distributions by department
tech = 0.6
client_mgmt = 0.9
admin = 1

#gender distribution by department
tech_male = 0.65
client_mgmt_male = 0.55
admin_male = 0.45

#individual contributor by department
tech_ic = 0.6
client_mgmt_ic = 0.5
admin_ic = 0.4

#manager by department
tech_mgr = 0.8
client_mgmt_mgr = 0.75
admin_mgr = 0.8

#senior leader by department
tech_sl = 0.9
client_mgmt_sl = 0.85
admin_sl = 0.95

#executive by department
tech_exec = 1
client_mgmt_exec = 1
admin_exec = 1

config = pd.read_excel('generate_dataset_config.xlsx')

def create_new_employees(last_emp_number, emp_count, new_hire_rate, year_of_data):
    employee_numbers = []
    departments = []
    genders = []
    job_level = []
    performance = []
    engagement = []
    salary = []
    tenure = []
    age = []
    promotions = []
    record_start_date = []
    
    for num in range(0, emp_count):
        random_number = np.random.random()
        if random_number <= new_hire_rate:
            #create employee number
            employee_numbers.append(last_emp_number + 1 + num)
        
            #create department
            random_number = np.random.random()
            if random_number <= tech:
                departments.append("Technology")
                department_val = "Technology"
            elif ((random_number > tech) and (random_number <= client_mgmt)):
                departments.append("Account/Client Management")
                department_val = "Account/Client Management"
            else:
                departments.append("Corporate Admin (HR, Finance, etc)")
                department_val = "Corporate Admin (HR, Finance, etc)"
        
            #create gender
            random_number = np.random.random()
            if department_val == "Technology":
                if random_number <= tech_male:
                    genders.append("Male")
                else:
                    genders.append("Female")
            elif department_val == "Account/Client Management":
                if random_number <= client_mgmt_male:
                    genders.append("Male")
                else:
                    genders.append("Female")
            else:
                if random_number <= admin_male:
                    genders.append("Male")
                else:
                    genders.append("Female")
            
            #create job level
            random_number = np.random.random()
            if department_val == "Technology":
                if random_number <= tech_ic:
                    job_level.append("Individual Contributor")
                    job_level_val = "Individual Contributor"
                elif (random_number > tech_ic) and (random_number <= tech_mgr):
                    job_level.append("Manager")
                    job_level_val = "Manager"
                elif (random_number > tech_mgr) and (random_number <= tech_sl):
                    job_level.append("Senior Leader")
                    job_level_val = "Senior Leader"
                else:
                    job_level.append("Executive")
                    job_level_val = "Executive"
            elif department_val == "Account/Client Management":
                if random_number <= client_mgmt_ic:
                    job_level.append("Individual Contributor")
                    job_level_val = "Individual Contributor"
                elif (random_number > client_mgmt_ic) and (random_number <= client_mgmt_mgr):
                    job_level.append("Manager")
                    job_level_val = "Manager"
                elif (random_number > client_mgmt_mgr) and (random_number <= client_mgmt_sl):
                    job_level.append("Senior Leader")
                    job_level_val = "Senior Leader"
                else:
                    job_level.append("Executive")
                    job_level_val = "Executive"
            else:
                if random_number <= admin_ic:
                    job_level.append("Individual Contributor")
                    job_level_val = "Individual Contributor"
                elif (random_number > admin_ic) and (random_number <= admin_mgr):
                    job_level.append("Manager")
                    job_level_val = "Manager"
                elif (random_number > admin_mgr) and (random_number <= admin_sl):
                    job_level.append("Senior Leader")
                    job_level_val = "Senior Leader"
                else:
                    job_level.append("Executive")
                    job_level_val = "Executive"
             
            #create salary
            random_number = np.random.random()
            temp_df = config[(config['metric'] == 'Salary') & 
                             (config['employee_level'] == job_level_val)]
            if temp_df['probability'].max() <= random_number:
                lower_number = temp_df[temp_df['rating'] == 'lower min']['value'].iloc[0] 
                upper_number = temp_df[temp_df['rating'] == 'lower max']['value'].iloc[0]
                random_salary = np.random.randint(lower_number, upper_number)
                salary.append(random_salary)
            else:
                lower_number = temp_df[temp_df['rating'] == 'higher min']['value'].iloc[0]
                upper_number = temp_df[temp_df['rating'] == 'higher max']['value'].iloc[0] 
                random_salary = np.random.randint(lower_number, upper_number)
                salary.append(random_salary)
                
            #create age
            age.append(np.random.randint(21, 65))
            
            #create blanks of unused columns
            performance.append("")
            engagement.append("")
            tenure.append(0)
            promotions.append(0)
            
            #create start date
            start_date = datetime.date(year_of_data, 1, 1)
            end_date = datetime.date(year_of_data, 12, 1)

            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = np.random.randint(1, days_between_dates)
            random_date = start_date + datetime.timedelta(days=random_number_of_days)
            
            record_start_date.append(random_date)

            
    combined_lists = zip(employee_numbers, 
                         departments, 
                         genders, 
                         job_level, 
                         performance, 
                         engagement, 
                         salary, 
                         tenure,
                         age,
                         promotions, 
                         record_start_date)
    global new_emps
    new_emps = pd.DataFrame(combined_lists, columns = ['employee_id', 
                                                       'department', 
                                                       'gender', 
                                                       'job_level', 
                                                       'performance_rating', 
                                                       'engagement', 
                                                       'salary_thousands', 
                                                       'tenure_years', 
                                                       'age_years', 
                                                       'promotion_indicator',
                                                       'record_start_date'])
    new_emps['record_end_date'] =  datetime.date(year_of_data, 12, 31)
    
    return new_emps