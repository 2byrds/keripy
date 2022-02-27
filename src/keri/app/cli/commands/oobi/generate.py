# -*- encoding: utf-8 -*-
"""
keri.kli.commands.oobi module

"""
import argparse
from urllib.parse import urlparse

import sys
from hio import help

from keri import kering
from keri.app.cli.common import existing

logger = help.ogler.getLogger()

parser = argparse.ArgumentParser(description='Initialize a prefix')
parser.set_defaults(handler=lambda args: generate(args),
                    transferable=True)

# Parameters for basic structure of database
parser.add_argument('--name', '-n', help='keystore name and file location of KERI keystore', required=True)
parser.add_argument('--base', '-b', help='additional optional prefix to file location of KERI keystore',
                    required=False, default="")
parser.add_argument('--alias', '-a', help='human readable alias for the new identifier prefix', required=True)
parser.add_argument("--role", "-r", help="role of oobis to generate", required=True)

# Parameters for Manager access
# passcode => bran
parser.add_argument('--passcode', '-p', help='22 character encryption passcode for keystore (is not saved)',
                    dest="bran", default=None)


def generate(args):
    """ command line method for generating oobies

    Parameters:
        args(Namespace): parse args namespace object

    """
    name = args.name
    alias = args.alias
    base = args.base
    bran = args.bran
    role = args.role

    with existing.existingHab(name=name, alias=alias, base=base, bran=bran) as (_, hab):
        if role in (kering.Roles.witness,):
            if not hab.kever.wits:
                print(f"{alias} identfier {hab.pre} does not have any witnesses.")
                sys.exit(-1)

            for wit in hab.kever.wits:
                urls = hab.fetchUrls(eid=wit, scheme=kering.Schemes.http)
                if not urls:
                    raise kering.ConfigurationError(f"unable to query witness {wit}, no http endpoint")
            
                up = urlparse(urls[kering.Schemes.http])
                print(f"http://{up.hostname}:{up.port}/oobi/{hab.pre}/witness/{wit}")
