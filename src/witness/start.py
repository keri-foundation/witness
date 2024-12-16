from hio.base import doing
from hio.help import decking
from keri import help

logger = help.ogler.getLogger()


class WitnessStart(doing.DoDoer):
    """Doer to print witness prefix after initialization"""

    def __init__(self, hab, parser, kvy, tvy, rvy, exc, cues=None, replies=None, responses=None, queries=None, **opts):
        self.hab = hab
        self.parser = parser
        self.kvy = kvy
        self.tvy = tvy
        self.rvy = rvy
        self.exc = exc
        self.queries = queries if queries is not None else decking.Deck()
        self.replies = replies if replies is not None else decking.Deck()
        self.responses = responses if responses is not None else decking.Deck()
        self.cues = cues if cues is not None else decking.Deck()

        doers = [doing.doify(self.start), doing.doify(self.msg_do), doing.doify(self.escrow_do), doing.doify(self.cue_do)]
        super().__init__(doers=doers, **opts)

    def start(self, tymth=None, tock=0.0):
        """Prints witness name and prefix

        Parameters:
            tymth (function): injected function wrapper closure returned by .tymen() of
                Tymist instance. Calling tymth() returns associated Tymist .tyme.
            tock (float): injected initial tock value

        """
        self.wind(tymth)
        self.tock = tock
        _ = yield self.tock

        while not self.hab.inited:
            yield self.tock

        print('Witness', self.hab.name, ':', self.hab.pre)

    def msg_do(self, tymth=None, tock=0.0):
        """
        Returns doifiable Doist compatible generator method (doer dog) to process
            incoming message stream of .kevery

        Parameters:
            tymth (function): injected function wrapper closure returned by .tymen() of
                Tymist instance. Calling tymth() returns associated Tymist .tyme.
            tock (float): injected initial tock value

        Usage:
            add result of doify on this method to doers list
        """
        self.wind(tymth)
        self.tock = tock
        _ = yield self.tock

        if self.parser.ims:
            logger.info('Client %s received:\n%s\n...\n', self.kvy, self.parser.ims[:1024])
        done = yield from self.parser.parsator()  # process messages continuously
        return done  # should nover get here except forced close

    def escrow_do(self, tymth=None, tock=0.0):
        """
         Returns doifiable Doist compatible generator method (doer dog) to process
            .kevery and .tevery escrows.

        Parameters:
            tymth (function): injected function wrapper closure returned by .tymen() of
                Tymist instance. Calling tymth() returns associated Tymist .tyme.
            tock (float): injected initial tock value

        Usage:
            add result of doify on this method to doers list
        """
        self.wind(tymth)
        self.tock = tock
        _ = yield self.tock

        while True:
            self.kvy.processEscrows()
            self.rvy.processEscrowReply()
            if self.tvy is not None:
                self.tvy.processEscrows()
            self.exc.processEscrow()

            yield

    def cue_do(self, tymth=None, tock=0.0):
        """
         Returns doifiable Doist compatible generator method (doer dog) to process
            .kevery.cues deque

        Doist Injected Attributes:
            g.tock = tock  # default tock attributes
            g.done = None  # default done state
            g.opts

        Parameters:
            tymth is injected function wrapper closure returned by .tymen() of
                Tymist instance. Calling tymth() returns associated Tymist .tyme.
            tock is injected initial tock value

        Usage:
            add result of doify on this method to doers list
        """
        self.wind(tymth)
        self.tock = tock
        _ = yield self.tock

        while True:
            while self.cues:
                cue = self.cues.pull()  # self.cues.popleft()
                cue_kin = cue['kin']
                if cue_kin == 'stream':
                    self.queries.append(cue)
                else:
                    self.responses.append(cue)
                yield self.tock
            yield self.tock
