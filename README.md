# Multi Agent Storage and Delivery Algorithm (MASD)

## Problem Statement
Autonomous robots have the potential to revolutionize the way people work and live, and their use is increasing rapidly in a variety of industries. The use of Multi-Agent Systems (MAS) increases the capabilities that can be performed automatically. In the field of logistics and in particular in warehouses, autonomous MAS can be used to automate the movement of packages, reducing the need for human labor and increasing efficiency. However, coordinating the movement of multiple agents can be a complex task especially in crowded or dynamic environments.

One way to address this challenge is through the use of multi-agent pathfinding algorithms, which allow multiple agents to find the optimal path to a destination with no collisions. These algorithms consider the capabilities and constraints of each robot, as well as the layout of the environment and potential obstacles. In addition to pathfinding, another important aspect of coordinating MAS is task allocation, which involves assigning specific tasks to each agent in a way that maximizes efficiency and minimizes performance time. To date, the integration of these two fields has been studied in a limited manner way the literature as will be presented in Chapter 2, there has not been an examination of the algorithm with the use of heterogeneous agents in 3D environment. The amalgamation of these fields has the potential to significantly enhance the efficiency of the overall process in comparison to previous research.

In this project, several tasks were performed to develop and evaluate an algorithm for managing packages through heterogeneous multi-agent systems in a warehouse environment. First, a literature review was conducted to gain insight into how previous studies have approached task assignment and collision-free path finding. Based on this, relevant algorithms were selected as a foundation and a new algorithm for managing packages in a warehouse was formulated. In addition, a simulation environment was developed to visually test and evaluate the capabilities of the algorithm, and a performance analysis was conducted to evaluate the effectiveness and limitations of the algorithm.



## MASD Implementation
To ensure efficient and timely collection, storage, and delivery of packages, it is necessary to divide the task into several sub-steps. This includes determining the appropriate storage location for each package within the warehouse, assigning agents to transport the packages to their destinations, and determining the optimal routes for the agents to take in the warehouse while ensuring that there are no conflicts between agents. In this chapter, the Multi-Agent Storage and Delivery (MASD) algorithm which has been developed as part of this project will be presented. The MASD algorithm is based on the principles of the Hungarian algorithm and CBS and incorporates their key concepts and methodologies.

To determine the location of packages within the warehouse, the ABC analysis is employed. This analysis considers the duration of package storage in the warehouse to determine its corresponding location, with longer storage times leading to placement in deeper areas of the warehouse.

For task assignment among the agents, the Hungarian algorithm is utilized. To construct the cost matrix for this algorithm, the following scheme is employed:

![54515](https://github.com/StavBiton1/MASD-Algorithm/assets/131392307/2e73983f-aa69-4597-a35d-74488d5baaea)

Once tasks are assigned, an independent route is planned for each agent using the A* algorithm. Subsequently, a check is conducted to detect any potential collisions with other agents. In the event of a conflict, alternative routes are evaluated, or the agent will wait in its current position.

The video below showcases the output of an algorithm in a scenario where there are four agents and four packages within the warehouse.

https://github.com/StavBiton1/MASD-Algorithm/assets/131392307/79e5f753-0576-4f43-8d4a-282408518886


