import falcon
from hio.core import http, tcp
from hio.core.tcp import serving
from hio.help import decking
from keri import help
from keri.app import httping, oobiing, directing
from keri.core import routing, eventing, parsing
from keri.db import basing
from keri.end import ending
from keri.vdr import viring, verifying
from keri.vdr.eventing import Tevery

from .receipt_end import ReceiptEnd
from .start import WitnessStart

logger = help.ogler.getLogger()


def setup_witness(
    hby, alias='witness', mbx=None, aids=None, tcp_port=5631, http_port=5632, keypath=None, cert_path=None, ca_filepath=None
):
    """
    Setup witness controller and doers

    """
    cues = decking.Deck()
    doers = []

    # make hab
    hab = hby.habByName(name=alias)
    if hab is None:
        hab = hby.makeHab(name=alias, transferable=False)

    reger = viring.Reger(name=hab.name, db=hab.db, temp=False)
    verfer = verifying.Verifier(hby=hby, reger=reger)

    # mbx = mbx if mbx is not None else storing.Mailboxer(name=alias, temp=hby.temp)
    # forwarder = forwarding.ForwardHandler(hby=hby, mbx=mbx)
    # exchanger = exchanging.Exchanger(hby=hby, handlers=[forwarder])
    clienter = httping.Clienter()
    oobiery = oobiing.Oobiery(hby=hby, clienter=clienter)

    app = falcon.App(cors_enable=True)
    ending.loadEnds(app=app, hby=hby, default=hab.pre)
    oobiing.loadEnds(app=app, hby=hby, prefix='/ext')
    # rep = storing.Respondant(hby=hby, mbx=mbx, aids=aids)

    rvy = routing.Revery(db=hby.db, cues=cues)
    kvy = eventing.Kevery(db=hby.db, lax=True, local=False, rvy=rvy, cues=cues)
    kvy.registerReplyRoutes(router=rvy.rtr)

    tvy = Tevery(reger=verfer.reger, db=hby.db, local=False, cues=cues)

    tvy.registerReplyRoutes(router=rvy.rtr)
    # parser = parsing.Parser(framed=True, kvy=kvy, tvy=tvy, exc=exchanger, rvy=rvy)
    parser = parsing.Parser(framed=True, kvy=kvy, tvy=tvy, rvy=rvy)

    # http_end = HttpEnd(rxbs=parser.ims, mbx=mbx)
    # app.add_route('/', http_end)
    receipt_end = ReceiptEnd(hab=hab, inbound=cues, aids=aids)
    app.add_route('/receipts', receipt_end)

    server = create_http_server(http_port, app, keypath, cert_path, ca_filepath)
    if not server.reopen():
        raise RuntimeError(f'cannot create http server on port {http_port}')
    http_server_doer = http.ServerDoer(server=server)

    # setup doers
    reg_doer = basing.BaserDoer(baser=verfer.reger)

    if tcp_port is not None:
        server = serving.Server(host='', port=tcp_port)
        if not server.reopen():
            raise RuntimeError(f'cannot create tcp server on port {tcp_port}')
        server_doer = serving.ServerDoer(server=server)

        directant = directing.Directant(hab=hab, server=server, verifier=verfer)
        doers.extend([directant, server_doer])

    wit_start = WitnessStart(
        hab=hab,
        parser=parser,
        cues=receipt_end.outbound,
        kvy=kvy,
        tvy=tvy,
        rvy=rvy,
        # exc=exchanger,
        # replies=rep.reps,
        # responses=rep.cues,
        # queries=http_end.qrycues,
    )

    # doers.extend([reg_doer, http_server_doer, rep, wit_start, receipt_end, *oobiery.doers])
    doers.extend([reg_doer, http_server_doer, wit_start, receipt_end, *oobiery.doers])
    return doers


def create_http_server(port, app, keypath=None, cert_path=None, ca_filepath=None):
    """
    Create an HTTP or HTTPS server depending on whether TLS key material is present
    Parameters:
        port (int)         : port to listen on for all HTTP(s) server instances
        app (falcon.App)   : application instance to pass to the http.Server instance
        keypath (string)   : the file path to the TLS private key
        cert_path (string)  : the file path to the TLS signed certificate (public key)
        ca_filepath (string): the file path to the TLS CA certificate chain file
    Returns:
        hio.core.http.Server
    """
    if keypath is not None and cert_path is not None and ca_filepath is not None:
        servant = tcp.ServerTls(certify=False, keypath=keypath, certpath=cert_path, cafilepath=ca_filepath, port=port)
        server = http.Server(port=port, app=app, servant=servant)
    else:
        server = http.Server(port=port, app=app)
    return server
