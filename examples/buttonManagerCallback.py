"""Example callbacks for buttonManager"""


def exampleCallback(**kwargs):
    """
    kwargs hasgi
    event = event trigger
    hidDevice = trigger device
    buttonId = tigger button ID
    eventTypes = all registered event types
    eventCount = Number of times even occured
    TODO: Add timers
    """
    print(kwargs["action"],":",kwargs["hidDevice"].getName(), ":Sample callback", kwargs)

def exampleCallback1(action, **kwargs):
    """
    kwargs hasgi
    event = event trigger
    hidDevice = trigger device
    buttonId = tigger button ID
    eventTypes = all registered event types
    eventCount = Number of times even occured
    TODO: Add timers
    """
    print(action,":",kwargs["hidDevice"].getName(), ":Sample callback", kwargs)


def simpleCallback():
    """
    Simple callback that ignored kwargs.
    """
    print("Simple")

def crashCallback():
    """
    Call back will crash
    """
    raise Exception("crashCallback crashed. Doh?")


def actionCallback(action):
    """
    Example of only using action
    """
    print(f"Action {action} triggered")
