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


if __name__ == "__main__":
    init = State(
        name="Init",
        transition_before=None,
        transition_after=None
    )
    go_to_the_gym = State(
        name="working in gym",
        transition_after=None,
        transition_before=init
    )

    init.transition_after = go_to_the_gym

    machine = Machine(
        host="127.0.0.1",
        port=6379,
        init_state=init
    )
    print(machine)

    machine.transition_next()

    print(machine)

    machine.transition_prev()

    print(machine)
