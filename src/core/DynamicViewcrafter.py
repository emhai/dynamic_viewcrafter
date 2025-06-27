from src.wrappers.viewcrafter_wrapper import ViewCrafterWrapper
from src.wrappers.easi3r_wrapper import Easi3rWrapper

class DynamicViewcrafter:
    def __init__(self, config):

        self.easi3r = Easi3rWrapper(config.easi3r)
        self.viewcrafter = ViewCrafterWrapper(config.viewcrafter)

