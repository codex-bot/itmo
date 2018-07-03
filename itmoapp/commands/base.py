from functools import partial


class CommandBase:

    def __init__(self, sdk, state_controller):
        """
        :param sdk:
        :param Controller state_controller:
        """
        self.sdk = sdk
        self.state = state_controller
