from opyoid import Injector, ProviderBinding, ClassBinding, InstanceBinding

from data.state import MasterState, SlaveState
from service.candidate_client import CandidateClient
from service.master_client import MasterClient

if __name__ == "__main__":

    chat = injector.inject(Chat)
    chat.run()