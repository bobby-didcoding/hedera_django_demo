import os
from hedera import AccountId, PrivateKey, Client

if "OPERATOR_ID" not in os.environ or "OPERATOR_KEY" not in os.environ:
    exit("Must set OPERATOR_ID OPERATOR_KEY environment variables")

OPERATOR_ID = AccountId.fromString(os.environ["OPERATOR_ID"])
OPERATOR_KEY = PrivateKey.fromString(os.environ["OPERATOR_KEY"])
HEDERA_NETWORK = os.environ.get("HEDERA_NETWORK", "testnet")
CONFIG_FILE = os.environ.get("CONFIG_FILE", "")


def network():

    if HEDERA_NETWORK == "previewnet":
        client = Client.forPreviewnet()
    elif HEDERA_NETWORK == "testnet":
        client = Client.forTestnet()
    else:
        client = Client.fromConfigFile(CONFIG_FILE)

    return client


client = network().setOperator(OPERATOR_ID, OPERATOR_KEY)



def config_user_client(user):

    OPERATOR_ID = AccountId.fromString(user.userprofile.acc)
    OPERATOR_KEY = PrivateKey.fromString(user.userprofile.privatekey)
    return network().setOperator(OPERATOR_ID, OPERATOR_KEY)