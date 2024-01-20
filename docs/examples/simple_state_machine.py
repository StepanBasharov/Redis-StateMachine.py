from core.machine import State, Machine

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

current_state = machine.get_current_state()

print(f"StateID: {current_state}")
