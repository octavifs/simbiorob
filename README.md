# simbiorob for humans

The objective of this repo is to provide some tips as to how to implement the necessary code to move the MeArm and the inverse kinematics algorithm.


## Installation
The code uses *Python 2* (2.7 should be fine). I would suggest using [Anaconda](http://anaconda.org/) if you don't have a Python setup ready. Make sure to download the python 2 version.

I've created the list of packages you would need to install so you can run this. It's called `requirements.txt`. If you use Anaconda, it's possible that everything will just work. If something fails, you can run, go to this folder on the command line and run (Windows people, this may not work for you, but just lookup a way to execute pip or conda on your machines on Google. Shouldn't be too bad):

    pip install -r requirements.txt

## The code

### TLDR
Just modify `MearmControl.ipynb`, you can ignore the rest.

*MearmControl* is a Jupyter notebook. You can execute it by running in the command line (same directory as this repository):

    jupyter notebook

Or, again, for the Windows people, just find jupyter notebook on your Start menu (you should have it once Anaconda finishes installing) and navigate to this folder.


### Director's cut:
- `frames.py`,`links.py` and `trans.py` are the files that setup the mathematical model (linear transformations and creating the links between each arm)
- `pythonSB.py`, `servos.py` is the code that deals with the interactions between the Raspberry and the actual servos.
- `transformations.ipynb` and `sb_example.py` are just demos for how to use the link system and the servos (respectively)


## How to move the robot
To be honest, I haven't tried it nor I will over the weekend, so don't ask. I'd happily add your comments though.

What I can tell you is that the code in charge of the movement should be implemented in the MeArm class (inside `MearmControl.ipynb`). The methods are:

- base
- shoulder
- elbow
- gripper
- openGripper
- closeGripper

Also, if you work on it, this will have to be executed on the Raspberry to properly test it. The Python code actually relies on a program called [Servoblaster](https://github.com/richardghirst/PiBits/tree/master/ServoBlaster) which should have been installed already. In case it's not, now you have the link.

## How to do the Inverse Kinematics
You'll need to finish the implementation of the methods `calculate_movement_delta` and `gotoPoint`. I've drafted `goToPoint` with a very barebones version of the loop.
As a suggestion, I'd say it would be interesting if you plot the arm at every step, or at least record the position at every step, so you can plot the trajectory that the arm takes towards the final position. This is going to help when debugging the algorithm.


## Problems I haven't addressed
Too many to mention! Still, I'm not too sure at the moment how the 3rd dimension is dealt with. Right now there is a nice 2D representation of the arm, but that essentially ignores that the robot can rotate (we would also need to add a top view to fully capture the DoF of the system).
