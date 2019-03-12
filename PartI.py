# state is denoted by a dictionary
import copy
class tic_tac_toe:
    def initialize(self):
        # Ask the player to make a choice of 'x' and 'o'. If 'x', ask the player
        # to select the first move.
        while True:
            turn = input("Which player do you want to choose, 'x' or 'o': ")
            turn = turn.strip().lower()
            if not turn in ['x','o']:
                print("Input error! Please input 'x' or 'o': ")
                continue
            break
        # Initialize the state. A state includes: what positions are filled
        # by player, computer and are left blank; the current turn; whether
        # the player are on the offensive.
        if turn == 'x':
            initial_state = {'player':([],'x'),'comp':([],'o'),'left':\
            [1,2,3,4,5,6,7,8,9],'turn':-1}
        else:
            initial_state = {'player':([],'o'),'comp':([],'x'),'left':\
            [1,2,3,4,5,6,7,8,9],'turn':1}
        self.print_state(initial_state)
        return initial_state

    def print_state(self, state):
        res = list(range(1,10))
        for i in state['player'][0]:
            res[i-1] = state['player'][1]
        for j in state['comp'][0]:
            res[j-1] = state['comp'][1]
        for k in range(3):
            print("{}  {}  {}".format(res[3*k],res[3*k+1],res[3*k+2]))
        if state['turn']>0:
            print("\nIt's computer's turn.")
        else:
            print("\nIt's your turn.")

    # To check wheter the player or the computer has winned and return
    # corresponding values.
    def check_state(self, state):
        win_state = [{1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7}]
        player_state = state['player'][0]
        computer_state = state['comp'][0]
        for i in win_state:
            if i.issubset(player_state):
                return -1
            elif i.issubset(computer_state):
                return 1
        if len(state['left']) == 0:
            return 0
        return None

    def change_state(self,state,a):
        s = copy.deepcopy(state)
        s['left'].remove(a)
        if s['turn']>0:
            s['comp'][0].append(a)
        else:
            s['player'][0].append(a)
        s['turn'] *= -1
        return s

    # Ask the computer to search for an action.
    def action_search(self, state):
        assert state['turn'] == 1
        if self.check_state(state)!= None:
            return None
        if len(state['left']) == 9:
            return 5
        val = float('-inf')
        a = None
        for i in state['left']:
            new_state = self.change_state(state,i)
            v = self.Min_Value(new_state,float('-inf'),float('inf'))
            if v == 1:
                return i
            elif v > val:
                val = v
                a = i
        return a

    def Max_Value(self, state, mini, maxi):
        v = self.check_state(state)
        if v != None:
            return v
        v = float('-inf')
        for a in state['left']:
            new_state = self.change_state(state, a)
            val = self.Min_Value(new_state,mini,maxi)
            v  = max(v,val)
            if v >= maxi:
                return v
            mini = max(mini,v)
        return v

    def Min_Value(self, state, mini, maxi):
        v = self.check_state(state)
        if v != None:
            return v
        v = float('inf')
        for a in state['left']:
            new_state = self.change_state(state, a)
            val = self.Max_Value(new_state,mini,maxi)
            v = min(v,val)
            if v <= mini:
                return v
            maxi = min(maxi,v)
        return v

    # Ask the player to select an action.
    def action_ask(self, state):
        assert state['turn'] == -1
        if self.check_state(state)!= None:
            return None
        while True:
            try:
                a = int(input("Please select a move from {}: ".format(state['left'])))
            except:
                print("Input error! Please input a number from {}: ".format(state['left']))
                continue
            if not a in state['left']:
                print("Input error! Please input a number from {}: ".format(state['left']))
                continue
            break
        return a

    def print_result(self, state):
        res = self.check_state(state)
        if res == 1:
            print('Computer wins!')
        elif res == -1:
            print('You win!')
        else:
            print('Tie game!')

    def implement(self):
        state = self.initialize()
        while True:
            if state['turn'] == 1:
                a = self.action_search(state)
            else:
                a = self.action_ask(state)
            if a == None:
                self.print_result(state)
                return
            state = self.change_state(state,a)
            self.print_state(state)


game1 = tic_tac_toe()
game1.implement()
