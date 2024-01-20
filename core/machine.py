from uuid import uuid4

import redis

from core.exceptions import core_exception
from core.interfaces import IStateMachine, IState


class State(IState):
    def __init__(
            self,
            name: str,
            transition_before: IState | None,
            transition_after: IState | None
    ):
        self.transition_name = name
        self.transition_before = transition_before
        self.transition_after = transition_after


class Machine(IStateMachine):
    def __init__(
            self,
            host: str,
            port: int,
            init_state: State
    ):
        self.redis_machine = redis.Redis(
            host=host,
            port=port
        )
        self.transitions = [init_state]
        self.current_state = init_state

    def __repr__(self):
        return self.current_state.transition_name

    def add_state(self, state: State) -> None:
        if state.transition_before and state not in self.transitions:
            raise core_exception.StateDoesNotExistException
        if state.transition_after and State not in self.transitions:
            raise core_exception.StateDoesNotExistException

        self.transitions.append(state)

    def transition_next(self) -> None:
        if self.current_state.transition_after:
            self.current_state = self.current_state.transition_after
        else:
            raise core_exception.FinalStateTransitionException

    def transition_prev(self) -> None:
        if self.current_state.transition_before:
            self.current_state = self.current_state.transition_before
        else:
            raise core_exception.InitialStateTransitionException
