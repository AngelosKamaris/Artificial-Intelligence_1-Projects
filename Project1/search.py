# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))

    frontier=util.Stack()                                   #use stack cause DFS needs FILO
    frontier.push((problem.getStartState(),[]))             #push the starting position and the path to it in stack
    expanded=[]                                             #list to keep the positions we have visited
    while not frontier.isEmpty():                           #as long as we haven't reached a goal and we can make legal moves:
        node=frontier.pop()                                     #get the last item out of the stack and check if it is goal
        if problem.isGoalState(node[0]):                        #if it is, return the path, up to this position
            return node[1]
        if node[0] not in expanded:                         #if the path isn't visited, push it in the list
            expanded.append(node[0])
            nodechild=problem.expand(node[0])               #use expand to get its succesors and push them in the stack
            for i in nodechild:
                frontier.push((i[0],node[1]+[i[1]]))
    return []                                               #if we don't find a goal, return an empty path

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier=util.Queue()                                  #the exact same code as DFS but we now use a queue because we need FIFO
    frontier.push((problem.getStartState(),[]))
    expanded=[]
    while not frontier.isEmpty():
        node=frontier.pop()
        if problem.isGoalState(node[0]):
            return node[1]
        if node[0] not in expanded:
            expanded.append(node[0])
            nodechild=problem.expand(node[0])
            for i in nodechild:
                frontier.push((i[0],node[1]+[i[1]]))
    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier=util.PriorityQueue()                                                                  #Similar to the other two, but now the node also holds the total cost to reach this path and the heuristic+cost
    frontier.push((problem.getStartState(),[],0),heuristic(problem.getStartState(),problem))
    expanded=[]
    while not frontier.isEmpty():
        node=frontier.pop()
        if problem.isGoalState(node[0]):
            return node[1]
        if node[0] not in expanded:
            expanded.append(node[0])
            nodechild=problem.expand(node[0])
            for i in nodechild:
                frontier.push((i[0],node[1]+[i[1]],node[2]+i[2]),node[2]+i[2]+heuristic(i[0],problem))
    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
