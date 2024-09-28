from opyoid import Injector, ProviderBinding, ClassBinding, InstanceBinding

if __name__ == "__main__":
    injector = Injector()
    chat = injector.inject(Chat)
    chat.run()