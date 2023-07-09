import random
from datetime import datetime, timedelta

class Package:
    def __init__(self, ID, Arival_time, Exit_time, Storage_id):
        self.ID = ID
        self.Arival_time = Arival_time
        self.Exit_time = Exit_time
        self.Storage_id = Storage_id
        
    def __str__(self):
        return f'ID: {self.ID}, Arrival Time: {self.Arival_time}, Exit Time: {self.Exit_time}, Storage ID: {self.Storage_id}'
    
    def __repr__(self):
        return f'ID: {self.ID}, Arrival Time: {self.Arival_time}, Exit Time: {self.Exit_time}, Storage ID: {self.Storage_id}'
    

# create 5 packages randomly
now = datetime.now()
packages = [Package(i, now + timedelta(hours=random.randint(1, 24)), now + timedelta(hours=random.randint(1, 24)) + timedelta(hours=random.randint(1, 24)), random.randint(1, 20)) for i in range(5)]

print("Packages: ")
print(packages)

# Create a list of arrival and exit times
arrival_exit_times = []
for package in packages:
    arrival_exit_times.append((package.ID , package.Arival_time))
    arrival_exit_times.append((package.ID , package.Exit_time))

# Sort the list by arrival
sorted_arrival_exit_times = sorted(arrival_exit_times, key=lambda x: x[1])
print("Organized tasks: ")
print(arrival_exit_times)
