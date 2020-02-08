# Menge File Generator
This program is used to generate the files used to run a scenario in [Menge](https://github.com/MengeCrowdSim/Menge). A compiled version of [Menge](https://github.com/MengeCrowdSim/Menge) has been included inside of this repository. 

## Table of Contents
1. [Creating the Scenario Wall PNG File](#1-creating-the-scenario-wall-png-file)
1. [Creating the Scenario Behavior PNG File](#2-creating-the-scenario-behavior-png-file)
1. [Creating the Scenario XML File](#3-creating-the-scenario-xml-file)
   1. [Defining the Root Node](#defining-the-root-node)
   1. [Defining Group Nodes](#defining-group-nodes)
   1. [Defining the Group Spawn Node](#defining-the-group-spawn-node)
   1. [Defining Group Goal Set Nodes](#defining-group-goal-set-nodes)
   1. [Defining a Color](#defining-a-color)
   1. [Defining a Transition](#defining-a-transition)
1. [Running the File Generator](#4-running-the-file-generator)
   1. [Installing Dependencies](#installing-dependencies)
   1. [Command Arguments and Flags](#command-arguments-and-flags)
   1. [Program Output](#program-output)
1. [Bottle Neck Example](#5-bottle-neck-example)
   1. [Scenario Wall PNG File](#scenario-wall-png-file)
   1. [Scenario Behavior PNG File](#scenario-behavior-png-file)
   1. [Scenario XML File](#scenario-xml-file)
   1. [Running the Generator](#running-the-generator)

## 1. Creating the Scenario Wall PNG File
* It is recommended you use image editing software similar to MS Paint to create this file as pixels must be a defined color with no antialiasing.
* The dimensions of this image reflect the dimensions of the simulation and should match the dimensions of the Scenario Behavior PNG file.
* This image must contain only black and white pixels
  * Black pixels are pixels with an RGB value of (0, 0, 0)
  * White pixels are pixels with an RGB value of (255, 255, 255)

## 2. Creating the Scenario Behavior PNG File
* It is recommended you use image editing software similar to MS Paint to create this file as pixels must be a defined color with no antialiasing.
* The dimensions of this image reflect the dimensions of the simulation and should match the dimensions of the Scenario Wall PNG file.
* Spawn locations and goal locations are set in this file.
* Each pixel represents a single spawn or goal point.
* Spawn points and goal points are grouped together by color.
  * See [_Defining the Group Spawn Node_](#defining-the-group-spawn-node) and [_Defining Group Goal Set Nodes_](#defining-group-goal-set-nodes) for details on how to link a pixel color to a group spawn or goal set.
* Agents will pick a random location in a group of spawn points / group of points to go to.
* Spawn points and goal points should be non-black (RGB of (0, 0, 0)) and non-white (RGB of (255, 255, 255)).

## 3. Creating the Scenario XML File
### Defining the Root Node
The XML File must have a root XML node titled **Data** as shown below:
```xml
<Data>
  ...
</Data>
```

### Defining Group Nodes
* The **Group** XML defines a set of agents with unique goals and behavior. Groups are defined inside of the root data XML node.
* The **speed** attribute sets the distance agents in this group will go after one step in the simulation. 
  * This defaults to 1.
* The **amount** attribute sets the total number of agents in the group.
  * This defaults to 1.
* You must define at least one group.
* In the example below two groups are created. The first group has a speed of 1 and has a total of 1 agent. The second group has a speed of 2 and a total of 4 agents.
```xml
<Data>
	<Group speed=”1” amount=”1”>
          ...
	</Group>
	<Group speed=”2” amount=”4”>
          ...
	</Group>
  ...
</Data>
```

### Defining the Group Spawn Node
The **Spawn** XML node defines the points at which agents will enter the simulation. Spawns are defined inside of the group XML node.
* The **min** attribute defines the minimum amount of time (steps in the simulation) an agent will wait before entering the simulation. This defaults to 0.
* The **max** attribute defines the maximum amount of time (steps in the simulation) an agent will wait before entering the simulation. This defaults to 0.
* The wait time for agents in the group will be uniformly distributed between the minimum and maximum values.
* The **Spawn** XML node must have one color XML node. See [_Defining a Color_](#defining-a-color) for details on defining this type of XML node.
  * Spawn location(s) will be chosen from the provided spawn points. If there are multiple possible spawn points, agents will uniformly distribute themselves between all eligible spawn points. See [_Creating the Scenario Behavior PNG File_](#2-creating-the-scenario-behavior-png-file) for details on creating this file.
* The **Spawn** XML node must have at least one transition XML node. See [_Defining a Transition_](#defining-a-transition) for details on defining this type of XML node.
* In the example below agents in this group will wait 100 steps before spawning at a random location specified by color. Afterwards, the agent will transition to the next goal set.
```xml
<Group speed=”1” amount=”1”>
	<Spawn min=”100” max=”100”>
		<Color r=”255” g=”0” b=”0 />
		<Transition to=”0” chance=”1” />
	</Spawn>
  ...
</Group>
...
```

### Defining Group Goal Set Nodes
The **GoalSet** XML node defines properties of a goal and the next goal set agents will move to.
* The **capacity** attribute defines the maximum number of agents that can be at a goal inside of this goal set. This defaults to 1.
* The **min** attribute defines the minimum amount of time (steps in the simulation) an agent will wait before transitioning to another goal. This defaults to 0.
* The **max** attribute defines the maximum amount of time (steps in the simulation) an agent will wait before transitioning to another goal. This defaults to 0.
The wait time for agents in the group will be uniformly distributed between the minimum and maximum values.
* The **GoalSet** XML node must have one color XML node. See [_Defining a Color_](#defining-a-color) for details on defining this type of XML node.
  * Goal location(s) will be chosen from the provided goal points. If there are multiple possible spawn points, agents will uniformly distribute themselves between all eligible goal points. See [_Creating the Scenario Behavior PNG File_](#2-creating-the-scenario-behavior-png-file) for details on creating this file.
* The **GoalSet** XML node must have at least one transition XML node. See [_Defining a Transition_](#defining-a-transition) for details on defining this type of XML node.
  * If the goal set specified in a transition is the same as the current goal set, the agent will wait at its current goal.
* All **GoalSet** XML nodes have an implicit ID associated with them. This ID is based off the order in which a goal set is defined. This ID is on a per group basis.
* In the example below the goal set with the color green (0, 255, 0) has an implicit ID of 0 and the goal set with the color blue (0, 0, 255) has an implicit ID of 1.
* The agent in the example below will exhibit the following behavior:
  1. Agent immediately spawns at a random location with an RGB value of (255, 0, 0).
  1. Agent picks a random goal inside of goal set 0. Upon arrival the agent waits 10 steps.
  1. Agent picks a random goal inside of goal set 1. Upon arrival the agent waits 10 seconds.
  1. The agent will wait at its current goal until the end of the simulation.
```xml
<Group speed=”1” amount=”1”>
	<Spawn min=”0” max=”0”>
		<Color r=”255” g=”0” b=”0” />
		<Transition to=”0” chance=”1” />
	</Spawn>
	<GoalSet capacity=”1” min=”10” max=”10”>
		<Color r=”0” g=”255” b=”0” />
		<Transition to=”1” chance=”1” />
	</GoalSet>
	<GoalSet capacity=”1” min=”10” max=”10”>
		<Color r=”0” g=”0” b=”255” />
		<Transition to=”1” chance=”1” />
	</GoalSet>
    ...
</Group>
```

### Defining a Color
The **Color** XML node defines the RGB value associated with a spawn or goal set. 
* The **r** attribute defines the red value of the color. This must be an integer between 0 and 255 (inclusive).
* The **g** attribute defines the green attribute of the color. This must be an integer between 0 and 255 (inclusive).
* The **b** attribute defines the blue attribute of the color. This must be an integer between 0 and 255 (inclusive).
* In the example below the color green is defined with an RGB value of (0, 255, 0).
```
<Color r=”0” g=”255” b=”0 />
```

### Defining a Transition
* The **Transition** XML node defines the next goal set an agent will go to after arriving and waiting at its goal. 
* The **to** attribute defines the ID of the next goal set an agent can go to. This must be an integer pointing to a valid goal set. This defaults to 0 if the transition is defined in spawn and the current goal set ID when defined in a goal set.
* The **chance** attribute defines how likely an agent will decide to go to the goal set defined by the **to** attribute. This must be an integer or a decimal. This defaults to 1.
  * The chance is a weighted average between all other transition XML nodes within the same parent XML node.
* In the example below two transitions are defined. There is a 50% chance an agent will go to the goal set with an ID of 0 and a 50% chance an agent will go to the goal set with an ID of 1.
```xml
<Transition to=”0” chance=”0.5” />
<Transition to=”1” chance=”0.5” />
```

## 4. Running the File Generator
### Installing Dependencies
You will need to download the following:
* Python3

You will need to use Python’s package manager pip to install the following python packages:
* pillow (version 6.00)
* imageio (version 2.5.0)
* numpy (version 1.16.4)
* scipy (version 1.1.0)
This can be done with the command `sudo pip3 install pillow imageio numpy scipy`

### Command Arguments and Flags
* path: path to the Scenario XML File
* -b: path to the Scenario Behavior PNG File
  * Will use the same base file name as the XML with '.png' extension.
* -w: path to the Scenario Wall PNG File
  * Will use the base file name of the XML file with 'Walls.png' extension.

### Program Output
* If successful all generated files will be outputted into a folder named after the Scenario XML File.
* A command to run the scenario using Menge will be printed to the console.

## 5. Bottle Neck Example
### Scenario Wall PNG File
* This file is saved as [BottleNeckWalls.png]((https://github.com/Ntsee/MengeFileGenerator/blob/master/example/BottleNeckWalls.png)) in the example folder. 
* The image below has a size of 100x100 pixels. There is a wall in the middle of the simulation with a tight choke in the middle through which agents can pass.

![Image of Bottle Neck Scenario Behavior PNG File](https://github.com/Ntsee/MengeFileGenerator/blob/master/example/BottleNeckWalls.png)

### Scenario Behavior PNG File
* This file is saved as [BottleNeck.png](https://github.com/Ntsee/MengeFileGenerator/blob/master/example/BottleNeck.png) in the example folder.
* The image below has a size of 100x100 pixels. It is a copy of the Scenario Wall PNG File. 
* A line of red pixels with an RGB value of (237, 28, 36) has been added to the left side. 
* A line of blue pixels with an RGB value of (63, 72, 204) has been added to the right side.

![Image of Bottle Neck Scenario Wall PNG File](https://github.com/Ntsee/MengeFileGenerator/blob/master/example/BottleNeck.png)

### Scenario XML File
* This file is saved as [BottleNeck.xml](https://github.com/Ntsee/MengeFileGenerator/blob/master/example/BottleNeck.xml) in the example folder.
* The first group (denoted as ‘Left Group’) has a speed of 1 and size of 90. Agents in this group will spawn at a random red pixel. This group will head towards a random blue pixel (their goal). Upon arrival, agents will wait at their goal for the remainder of the simulation.
* The second group (denoted as ‘Right Group’) has a speed of 1 and size of 90. Agents in this group will spawn at a random blue pixel. This group will head towards a random red pixel (their goal). Upon arrival, agents will wait at their goal for the remainder of the simulation.
* `<!-- ... -->` tags are comments are only included to help explain the example.
```xml
<Data>
	<!-- Left Group -->
	<Group speed=”1” amount=”90”>
		<Spawn min=”0” max=”0”>
			<Color r=”237” g=”28” b=”36” />
			<Transition to=”0” chance=”1” />
		</Spawn>
		
		<GoalSet capacity=”1” min=”1000” max=”1000”>
			<Color r=”63” b=”72” g=”204” />
			<Transition to=”0” chance=”1” />
		</GoalSet>
	</Group>

	<!-- Right Group -->
	<Group speed=”1” amount=”90”>
		<Spawn min=”0” max=”0”>
			<Color r=”63” b=”72” g=”204” />
			<Transition to=”0” chance=”1” />
		</Spawn>
		
		<GoalSet capacity=”1” min=”1000” max=”1000”>
			<Color r=”237” g=”28” b=”36” />
			<Transition to=”0” chance=”1” />
		</GoalSet>
	</Group>
</Data>
```

### Running the Generator
1. Open the terminal and change your directory to the folder containing menge_generator.py.
1. Use the command `python3 menge_generator.py ./example/BottleNeck.xml`
1. When the command is done running you should see a completion message and how to run the example in menge.
   1. You should now see a new folder called `./BottleNeck/` that will contain the generated files.
