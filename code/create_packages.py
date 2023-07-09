import datetime
import random

class create_packages:
    today = datetime.date.today()

    def random_time(start, end):
        """
        Generate a random time between start and end.
        """
        return start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
# income time - the time which package arrived to the warehouse
# outcome time - the time which package leaving the warehouse
# storae id - The ID of the storage location where the package will be while it is stored in the warehouse
# package id - The ID of the package 
# allocate - Is there an agent assigned to take the package to its destination
#  
    def split_packages(x):
        packages = []
    # Create 0.3*X packages with random income times within the last month
        for i in range(round(x)):
            income_time = create_packages.random_time(datetime.datetime(create_packages.today.year, 
                                                                        create_packages.today.month, create_packages.today.day, 0, 0), 
                                                                        datetime.datetime(create_packages.today.year, create_packages.today.month, 
                                                                                          create_packages.today.day, 0, 10))
            outcome_time = create_packages.random_time(income_time + datetime.timedelta(days=1), income_time + datetime.timedelta(days=30))
            storage_id = None 
            package_id = i
            allocate = False
            state = None
            packages.append({"package_id": package_id, "income_time": income_time, "outcome_time": outcome_time, "storage_id": storage_id,
                              "allocate": allocate, "state": state})

        # Create 0.3*X packages with random outcome times within the next month
        for i in range(round(0*x), round(0*x)):
            outcome_time = create_packages.random_time(datetime.datetime(create_packages.today.year, create_packages.today.month, 
                                                                         create_packages.today.day, 0, 0), 
                                                                         datetime.datetime(create_packages.today.year, create_packages.today.month, 
                                                                                           create_packages.today.day, 1, 0))
            income_time =  create_packages.random_time(outcome_time - datetime.timedelta(days=30), outcome_time - datetime.timedelta(days=1))
            storage_id = None
            package_id = i
            allocate = False
            state = None
            packages.append({"package_id": package_id, "income_time": income_time, "outcome_time": outcome_time, "storage_id": storage_id,
                              "allocate": allocate,"state": state})

        # Create 0.4*X packages with random income and outcome times within the last and next month, with the income time before today
        for i in range(round(0*x), 0*x):
            income_time = create_packages.random_time(datetime.datetime(create_packages.today.year, create_packages.today.month, 
                                                                        create_packages.today.day, 0, 0)- datetime.timedelta(days=14) , 
                                                                        datetime.datetime(create_packages.today.year, create_packages.today.month, 
                                                                                          create_packages.today.day, 23, 59)- datetime.timedelta(days=1))
            outcome_time = create_packages.random_time(datetime.datetime(create_packages.today.year, create_packages.today.month, 
                                                                         create_packages.today.day, 0, 0)+ datetime.timedelta(days=1) , 
                                                                         datetime.datetime(create_packages.today.year, create_packages.today.month, 
                                                                                           create_packages.today.day, 23, 59)+ 
                                                                                           datetime.timedelta(days=14))
            storage_id = None
            package_id = i
            allocate = False
            state = None
            packages.append({"package_id": package_id, "income_time": income_time, "outcome_time": outcome_time, "storage_id": storage_id,
                              "allocate": allocate, "state": state})


        #print packages
        for package in packages:
            print(package)
            print()  # Add an empty line between packages
        return packages
    
   
