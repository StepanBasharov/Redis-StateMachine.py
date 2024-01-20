class StateDoesNotExistException(Exception):
    message = "State Does Not Exist"


class FinalStateTransitionException(Exception):
    message = "State dont have after state"


class InitialStateTransitionException(Exception):
    message = "State dont have before state"
