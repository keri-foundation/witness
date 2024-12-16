import argparse
import logging

from keri import help
from keri.app import directing, habbing, keeping, configing
from keri.app.cli.common import existing

from ..setup import setup_witness

d = 'Run Witness'
parser = argparse.ArgumentParser(description=d)
parser.set_defaults(handler=lambda args: launch(args))
parser.add_argument('-V', '--version', action='version', version=__version__, help='Prints out version of script runner.')
parser.add_argument(
    '-H', '--http', action='store', default=5631, help='Local port number the HTTP server listens on. Default is 5631.'
)
parser.add_argument(
    '-T', '--tcp', action='store', default=5632, help='Local port number the TCP server listens on. Default is 5632.'
)
parser.add_argument('-n', '--name', action='store', default='witness', help='Name of controller. Default is witness.')
parser.add_argument(
    '--base', '-b', help='additional optional prefix to file location of KERI keystore', required=False, default=''
)
parser.add_argument('--alias', '-a', help='human readable alias for the new identifier prefix', required=True)
parser.add_argument(
    '--passcode', '-p', help='21 character encryption passcode for keystore (is not saved)', dest='bran', default=None
)  # passcode => bran
parser.add_argument('--config-dir', '-c', help='directory override for configuration data')
parser.add_argument('--config-file', action='store', default=None, help='configuration filename override')
parser.add_argument('--keypath', action='store', required=False, default=None)
parser.add_argument('--certpath', dest='cert_path', action='store', required=False, default=None)
parser.add_argument('--cafilepath', dest='ca_filepath', action='store', required=False, default=None)
parser.add_argument(
    '--loglevel',
    action='store',
    required=False,
    default='CRITICAL',
    help='Set log level to DEBUG | INFO | WARNING | ERROR | CRITICAL. Default is CRITICAL',
)
parser.add_argument(
    '--logfile',
    action='store',
    required=False,
    default=None,
    help='path of the log file. If not defined, logs will not be written to the file.',
)


def launch(args):
    help.ogler.level = logging.getLevelName(args.loglevel)
    if args.logfile is not None:
        help.ogler.headDirPath = args.logfile
        help.ogler.reopen(name=args.name, temp=False, clear=True)
    logger = help.ogler.getLogger()

    logger.info('\nStarting Witness for %s listening: http/%s, tcp/%s ' '.\n\n', args.name, args.http, args.tcp)

    run_witness(
        name=args.name,
        base=args.base,
        alias=args.alias,
        bran=args.bran,
        tcp=int(args.tcp),
        http=int(args.http),
        config_dir=args.config_dir,
        config_file=args.config_file,
        keypath=args.keypath,
        cert_path=args.cert_path,
        ca_filepath=args.ca_filepath,
    )

    logger.info('\nEnded Witness for %s listening: http/%s, tcp/%s' '.\n\n', args.name, args.http, args.tcp)


def run_witness(
    name='witness',
    base='',
    alias='witness',
    bran='',
    tcp=5631,
    http=5632,
    expire=0.0,
    config_dir='',
    config_file='',
    keypath=None,
    cert_path=None,
    ca_filepath=None,
):
    """
    Setup and run one witness
    """

    ks = keeping.Keeper(name=name, base=base, temp=False, reopen=True)

    aeid = ks.gbls.get('aeid')

    cf = None
    if config_file is not None:
        cf = configing.Configer(name=config_file, headDirPath=config_dir, temp=False, reopen=True, clear=False)

    if aeid is None:
        hby = habbing.Habery(name=name, base=base, bran=bran, cf=cf)
    else:
        hby = existing.setupHby(name=name, base=base, bran=bran, cf=cf)

    hby_doer = habbing.HaberyDoer(habery=hby)  # setup doer
    doers = [hby_doer]

    doers.extend(
        setup_witness(
            alias=alias, hby=hby, tcp_port=tcp, http_port=http, keypath=keypath, cert_path=cert_path, ca_filepath=ca_filepath
        )
    )

    directing.runController(doers=doers, expire=expire)
