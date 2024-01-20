from abc import ABC, abstractmethod


class IState(ABC):
    ...


class IStateMachine(ABC):

    @abstractmethod
    def add_state(self, state: IState):
        ...

    @abstractmethod
    def transition_next(self):
        ...

    @abstractmethod
    def transition_prev(self):
        ...

