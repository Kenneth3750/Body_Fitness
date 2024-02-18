from  datetime import datetime, timedelta

def plan_info(plan, user, get_plan_duration):
    month_plans = [1, 2, 3, 4]
    day_plans = [5, 6, 7]
    if plan in month_plans:
        plan_duration= get_plan_duration(plan)
        plan_duration = plan_duration[0][0]
        plan_duration = int(plan_duration)

        end_date = datetime.now() + timedelta(days=30*plan_duration) 
        end_date = end_date.strftime("%Y-%m-%d")
        frequency = None
    elif plan in day_plans:
        plan_duration= get_plan_duration(plan)
        plan_duration = plan_duration[0][0]
        plan_duration = int(plan_duration)
        end_date = datetime.now() + timedelta(days=plan_duration)
        end_date = end_date.strftime("%Y-%m-%d")
        if plan == 5:
            frequency = 10
        elif plan == 6:
            frequency = 12
        else:
            frequency = 15
    else:
        plan_duration = user['duracion']
        plan_duration = int(plan_duration)
        end_date = datetime.now() + timedelta(days = 30*plan_duration)
        end_date = end_date.strftime("%Y-%m-%d")
        frequency = None
    return end_date, frequency






