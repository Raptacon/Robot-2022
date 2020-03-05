
class Callback():
    callbacks = {}

    def registerCallback(self, base, state):
        print("registered %s for %s" % (state, base))
        self.callbacks[state] = base

    def runCallbacks(self):
        for key,value in self.callbacks.items():
            print("state=%s value=%s, type=%s" % (key, value, type(value)) )
            print(type(value))
            # Note that we have no clue what/who we're calling here..just some instance with a
            # function called runme()
            value.runme()

class Base():
    def runme(self):
        print("Base")
        pass

class One(Base):
    def runme(self):
        print("One")

class Two(Base):
    def hold(self):
        pass

# base = Base()
# base.runme()
one = One()
#one.runme()
two = Two()
# two.runme()

callback = Callback()
callback.registerCallback(one, "hi")
callback.registerCallback(two, "there")

callback.runCallbacks()
