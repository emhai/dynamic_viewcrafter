import sys

class DynamicViewcrafter:
    def __init__(self, config):

        sys.path.append('../external/eas1er')
        sys.path.append('../external/viewcrafter')
        sys.path.append('../external/dust3r')

        from dust3r.model import DUSt3R  # adjust import path
        self.model = DUSt3R(config)
        self.config = config

def main():




if __name__ == '__main__':
    main()