from tsp import OwnedVid, Store, GenericMessage, MessageType

def main():
    def new_vid():
        return OwnedVid.new_did_peer("tcp://127.0.0.1:1337")

    store = Store()
    alice = new_vid()
    bob = new_vid()

    store.add_private_vid(alice)
    store.add_private_vid(bob)

    message = b"hello world"

    (url, sealed) = store.seal_message(alice.identifier(), bob.identifier(), None, message)

    assert url == "tcp://127.0.0.1:1337"

    received = store.open_message(sealed)

    match received:
        case GenericMessage(sender, _, received_message, message_type):
            assert sender == alice.identifier()
            assert received_message == message
            assert message_type == MessageType.SignedAndEncrypted
            print("success:", received_message)

        case other:
            print(f"unexpected message type {other}")
            assert False

if __name__ == '__main__':
    main()
