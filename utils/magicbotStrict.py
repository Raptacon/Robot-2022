from magicbot.state_machine import * # noqa: F403,F401
from magicbot.state_machine import StateMachine
import magicbot.state_machine
import functools

class InvalidStateTransition(Exception):
    pass

def state(f=None, *, first=False, must_finish=False, state_transitions=[]):
    """
        If this decorator is applied to a function in an object that inherits
        from :class:`.StateMachine`, it indicates that the function
        is a state. The state will continue to be executed until the
        ``next_state`` function is executed.
        
        The decorated function can have the following arguments in any order:
        
        - ``tm`` - The number of seconds since the state machine has started
        - ``state_tm`` - The number of seconds since this state has been active
          (note: it may not start at zero!)
        - ``initial_call`` - Set to True when the state is initially called,
          False otherwise. If the state is switched to multiple times, this
          will be set to True at the start of each state execution.
        - ``state_transitions`` - Contains list of valid state transitions from
          this state. If a transition is invalid the change state will fail.
          if this is empty or "any" is used no limitation on transitions is enforced.
        
        :param first: If True, this state will be ran first
        :type  first: bool
        :param must_finish: If True, then this state will continue executing
                            even if ``engage()`` is not called. However,
                            if ``done()`` is called, execution will stop
                            regardless of whether this is set.
        :type  must_finish: bool
    """
    if f is None:
        f = functools.partial(state, first=first, must_finish=must_finish, state_transitions=state_transitions)
        #f.state_transitions = state_transitions
    else:
        f =  _strict_create_wrapper(f, first, must_finish, state_transitions)
    return f

def _strict_create_wrapper(f, first, must_finish, state_transitions):
    wrapper = magicbot.state_machine._create_wrapper(f, first, must_finish)
    wrapper.state_transitions = state_transitions
    return wrapper


class StrictStateMachine(StateMachine):
    """
    Allows creation of state machines with strict state transitions. On a bad transition
    states will throw an exception. Use valid_change for checking mode changes.
    """
    def valid_change(self, state):
        """
        Used to check for valid state transition. Returns true if the transition is allowed
        otherwise returns false.
        """
        #when the current state has not been set, allow state to be set.
        if self.current_state == "":
            return True
        stateFunc = getattr(self, self.current_state)
        stateTransTbl = getattr(stateFunc, "state_transitions")
        if state in stateTransTbl \
            or len(stateTransTbl) == 0 \
            or "any" in stateTransTbl \
            or state == self.current_state:
            return True
        return False

    def next_state(self, name, force = False):
        """
        See StateMachine.
        Addes force variable to allow bypassing checks
        """
        if force or self.valid_change(name):
            return super().next_state(name)
        raise InvalidStateTransition(f"{self.current_state} to {name} is invalid")
    def next_state_now(self, name, force = False):
        """
        See StateMachine.
        Addes force variable to allow bypassing checks
        """
        if force or self.valid_change(name):
            return super().next_state_now(name)
        raise InvalidStateTransition(f"{self.current_state} to {name} is invalid")
