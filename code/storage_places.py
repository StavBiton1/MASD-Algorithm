"""
create a list of storage locations in the warehouse by the number of shelves and the number of rows.
This code takes into account that in every shelf there are two stages, and it is possible to put two packages
in one stage of the shelves. 
"""
import math as m
import datetime
import random

class storage_location:

    def AllocateOldPackages(packages, FreeA_list, FreeB_list, FreeC_list, allocate_list):
        # Calculate the timedelta once
        delta7 = datetime.timedelta(days=7)
        delta21 = datetime.timedelta(days=21)
        delta30 = datetime.timedelta(days=30)

        for package in packages:
            # Pre-assign a default value for the storage_id
            storage_id = None

            time_diff = package["income_time"].date() - package["outcome_time"].date()

            if time_diff <= delta7 and len(FreeA_list) > 0:
                storage_id = random.choice(FreeA_list)
                state = 'A'
                FreeA_list.remove(storage_id)
            elif time_diff <= delta21 and len(FreeB_list) > 0:
                storage_id = random.choice(FreeB_list)
                state='B'
                FreeB_list.remove(storage_id)
            elif time_diff <= delta30 and len(FreeC_list) > 0:
                storage_id = random.choice(FreeC_list)
                state='C'
                FreeC_list.remove(storage_id)
            else:
                storage_id = random.choice(FreeB_list)
                state= 'B'
                FreeB_list.remove(storage_id)

            # Assign the storage_id to the package
            package["storage_id"] = storage_id
            package["state"] = state
            allocate_list.append(storage_id)

        return packages, FreeA_list, FreeB_list, FreeC_list, allocate_list


#Function that calculates the number of rows in section (A,B,C)
    def RowPerSection(row_num):
        RowNumForSection=m.floor(row_num/3)
        AdditionalRows=row_num%3
        if AdditionalRows ==1:
            a=RowNumForSection 
            b=RowNumForSection+1 
            c=RowNumForSection
        elif AdditionalRows ==2:
            a=RowNumForSection 
            b=RowNumForSection+1 
            c=RowNumForSection+1
        else:
            a=b=c=RowNumForSection
        return a,b,c

#Function that create the all storage location in the warehouse and split them for each section (A,B,C)
    def storage_spaces(shelves_num , row_num):
        Storage_list = [] # Create a list to store the Storage places (True=free False=occupied)
        # Create list of storage locations of each section (A,B,C)
        A_list = []
        B_list = []
        C_list = []
        a,b,c=storage_location.RowPerSection(row_num)
        for row in range(1 , row_num+1):
            row_char = chr(64 + row)  # Convert row number to corresponding uppercase letter 
            # Loop over the numbers 10 to 80, incrementing by 10 each time
            if row <=a:
                for number in range(10, 10*2*shelves_num+1 , 10):
                    # Loop over the digits 0 and 1
                    for digit in range(2):
                        # Create a string with the letter and number
                        A_place = f"{row_char}{number+digit:02}"
                        # Add the string and boolean value to a tuple
                        A_tuple = A_place
                        # Add the tuple to the list
                        A_list.append(A_tuple)
            elif row <=a+b:
                for number in range(10, 10*2*shelves_num+1 , 10):
                    # Loop over the digits 0 and 1
                    for digit in range(2):
                        # Create a string with the letter and number
                        B_place = f"{row_char}{number+digit:02}"
                        # Add the string and boolean value to a tuple
                        B_tuple = B_place
                        # Add the tuple to the list
                        B_list.append(B_tuple)
            else:
                for number in range(10, 10*2*shelves_num+1 , 10):
                    # Loop over the digits 0 and 1
                    for digit in range(2):
                        # Create a string with the letter and number
                        C_place = f"{row_char}{number+digit:02}"
                        # Add the string and boolean value to a tuple
                        C_tuple = C_place
                        # Add the tuple to the list
                        C_list.append(C_tuple)
        return A_list,B_list,C_list

    def AllocateNewPackages(package, FreeA_list, FreeB_list, FreeC_list, allocate_list, agent):
        # Calculate the timedelta once
        delta7 = datetime.timedelta(days=7)
        delta21 = datetime.timedelta(days=21)
        delta30 = datetime.timedelta(days=30)

        storage_id = None


        time_diff = package["income_time"].date() - package["outcome_time"].date()
        if agent["lift_up"]==True:
            if time_diff <= delta7 and len(FreeA_list) > 0:
                storage_id = random.choice(FreeA_list)
                state = 'A'
                FreeA_list.remove(storage_id)
            elif time_diff <= delta21 and len(FreeB_list) > 0:
                storage_id = random.choice(FreeB_list)
                state='B'
                FreeB_list.remove(storage_id)
            elif time_diff <= delta30 and len(FreeC_list) > 0:
                storage_id = random.choice(FreeC_list)
                state='C'
                FreeC_list.remove(storage_id)
            else:
                storage_id = random.choice(FreeB_list)
                state= 'B'
                FreeB_list.remove(storage_id)
        
        if agent["lift_up"]==False:
            filtered_list_A = [storage_id for storage_id in FreeA_list if storage_id[-1] == '0']
            filtered_list_B = [storage_id for storage_id in FreeB_list if storage_id[-1] == '0']
            filtered_list_C = [storage_id for storage_id in FreeC_list if storage_id[-1] == '0']
            
            if time_diff <= delta7 and len(filtered_list_A) > 0:
                storage_id = random.choice(filtered_list_A)
                state = 'A'
                FreeA_list.remove(storage_id)
            elif time_diff <= delta21 and len(filtered_list_B) > 0:
                storage_id = random.choice(filtered_list_B)
                state = 'B'
                FreeB_list.remove(storage_id)
            elif time_diff <= delta30 and len(filtered_list_C) > 0:
                storage_id = random.choice(filtered_list_C)
                state = 'C'
                FreeC_list.remove(storage_id)
            else:
                storage_id = random.choice(FreeB_list)
                state = 'B'
                FreeB_list.remove(storage_id)

        # Assign the storage_id to the package
        package["storage_id"] = storage_id
        package["state"] = state
        allocate_list.append(storage_id)

        return package, FreeA_list, FreeB_list, FreeC_list, allocate_list