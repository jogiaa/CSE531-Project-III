import grpc
import bankingsystem_pb2
import bankingsystem_pb2_grpc
from concurrent import futures
import multiprocessing
from google.protobuf.json_format import MessageToDict
import json
from BankingSystemUtility import log_msg, initializeLogging, parseInputFile, getProcessId, parseLocalArgs, \
    translateEntityToEnum
from time import sleep


class Branch(bankingsystem_pb2_grpc.TransactionServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # list of ids for operations
        self.writeSet = set()

    def MsgDelivery(self, request, context):
        """
        The RPC call to handle the incoming requests.

        :param request: un-marsheled BankRequest received by the RPC call.
        :param context: Server context
        :return: BankResponse
        """
        log_msg('*' * 10 + 'REQUEST' + '*' * 10)
        log_msg(json.dumps(MessageToDict(request)))
        log_msg('*' * 30)

        responseList = list()

        for event in request.events:
            # Checking the write set consistency
            if self.checkConsistency(reqWriteSet=request.writeSet):
                log_msg(f'---Consistency PASSED for {self.id}---')
                # only process the events which has the same destination ID as the current server.
                if event.dest == self.id:
                    # handle the operation and add it the response list
                    responseList.append(self.handleOperations(event))
                else:
                    # if dest id is not same as the current server, forward the event to server with that ID by calling
                    # sendToDestinationBranch and add the response to the list
                    responseList.append(self.sendToDestinationBranch(event))
            else:
                log_msg(f'---Consistency issues for branch {self.id}---')
                # Creating failure response
                responseList.append(
                    bankingsystem_pb2.outputEvent(interface=event.interface, result=bankingsystem_pb2.failure))
                break
        # Creating final response from server
        bankResponse = bankingsystem_pb2.BankResponse(id=request.id, recv=responseList, writeSet=self.writeSet)

        log_msg('Response from Branch#{0}:{1}'.format(self.id, json.dumps(MessageToDict(bankResponse))))

        return bankResponse

    def checkConsistency(self, reqWriteSet):
        """
        Checking consistency of the incoming request by comparing the write sets coming as part of request with
        the write set available at the branch side. Write set coming as part of request is list, converting it into seq
        eases the comparison process.

        :param reqWriteSet:
        :return: Boolean if the write set matches else false
        """
        log_msg(f'Checking consistency for BRANCH++{list(self.writeSet)} and REQ++{reqWriteSet}')
        return self.writeSet == set(reqWriteSet)

    def handleOperations(self, event):
        """
        The core function performing all the operations for the interfaces
        :param event: The 'event' from resuest
        :return:
        """
        res = {}
        # Query interface
        if bankingsystem_pb2.query == event.interface:
            # Mandatory sleep after query interface so the results can be propagated.
            sleep(3)
            res = self.query()

        # deposit interface
        elif bankingsystem_pb2.deposit == event.interface:
            res = self.deposit(event)
            # calling the function to propagate if the response of the deposit was successful.
            self.propagateIfOperationSuccessful(res, event, bankingsystem_pb2.propagate_deposit)

        # withdraw interface
        elif bankingsystem_pb2.withdraw == event.interface:
            res = self.withdraw(event)
            # calling the function to propagate if the response of the withdraw was successful.
            self.propagateIfOperationSuccessful(res, event, bankingsystem_pb2.propagate_withdraw)

        # propagate deposit interface
        elif bankingsystem_pb2.propagate_deposit == event.interface:
            res = self.handlePropagateDeposit(event)

        # propagate withdraw interface
        elif bankingsystem_pb2.propagate_withdraw == event.interface:
            res = self.handlePropagateWithdraw(event)

        # we are tracking the write sets, for monotonic writes and read-writes
        # we will propagating event ids for all the write operations i.e. withdraw /deposit
        # this will also include the propagation events for these write interfaces
        if bankingsystem_pb2.query != event.interface:
            log_msg(f'adding event id {event.id} to write set {self.writeSet} '
                    f'for branch{self.id} on event {event.interface}')
            self.writeSet.add(event.id)
        else:
            log_msg('Ignoring event id for query')

        log_msg(f'Response of event {event.id} of type {event.interface} ==== {str(res)}')
        return res

    def sendToDestinationBranch(self, event):
        """
        Based on 'dest' param of the request , we need to send the request to that appropriate branch. This function
        will perform that functionality. The way this function is called we, don't need the whole
        bankingsystem_pb2_grpc.BankResponse object. We will use the bankingsystem_pb2_grpc.outputEvent
        from this to add it to our final bankingsystem_pb2_grpc.BankResponse if needed.

        :param event: bankingsystem_pb2_grpc.inputEvent
        :return: bankingsystem_pb2_grpc.outputEvent
        """

        log_msg(f'-----Sending to Destination {event.dest} Event {str(event)}-------')
        # Getting process ID based on destination ID
        portId = getProcessId(event.dest)

        with grpc.insecure_channel(f'localhost:{str(portId)}') as channel:
            stub = bankingsystem_pb2_grpc.TransactionStub(channel)
            # bankingsystem_pb2.BankRequest 's events expects a list. The event to this function is one event.
            # converting that to list so it can be made part of bankingsystem_pb2.BankRequest
            eventList = list()
            eventList.append(event)

            response = stub.MsgDelivery(
                bankingsystem_pb2.BankRequest(id=event.dest, type=bankingsystem_pb2.bank, events=eventList,
                                              writeSet=list(self.writeSet)))

            log_msg(f'Received from :::::{json.dumps(MessageToDict(response))}')
            # only returning bankingsystem_pb2_grpc.outputEvent from the full bankingsystem_pb2_grpc.BankResponse
            return response.recv[0]

    def propagateEvent(self, eventType, eventIn):
        """
        This function is called when withdraw or deposit operation is successful. This will propagate that operation
        to other branches. This function will also call and log the subinterface PROPAGATE_RESPONSE when response is
        received from propagation.

        :param eventType: Interface indicating the propagation type
        :param eventIn: The event will contain the details for propagation
        :return: None
        """
        for bid in self.branches:
            event = bankingsystem_pb2.inputEvent(id=eventIn.id, interface=eventType,
                                                 money=eventIn.money, dest=bid)
            log_msg(f'Propagating to branch {bid}  for event {str(event)}')
            response = self.sendToDestinationBranch(event)
            log_msg('Response on propagation {0} from branch {1}'.format(json.dumps(MessageToDict(response)), bid))

    def query(self):
        """
        Implementation of the Query interface.

        :return: bankingsystem_pb2_grpc.outputEvent in dict form
        """
        log_msg('-----QUERY-------')
        return {'interface': bankingsystem_pb2.query, 'result': bankingsystem_pb2.success, 'money': self.balance}

    def deposit(self, event):
        """
        Implementation of the deposit interface.

        :return: bankingsystem_pb2_grpc.outputEvent in dict form
        """
        log_msg('-----DEPOSIT-------')
        # if deposited amount is < ZERO operation will be considered as failure
        if event.money > 0:
            self.balance += event.money
            opResult = bankingsystem_pb2.success
        else:
            log_msg('Deposit amount negative.Operation failed.')
            opResult = bankingsystem_pb2.failure

        return {'interface': bankingsystem_pb2.deposit, 'result': opResult}

    def withdraw(self, event):
        """
        Implementation of the withdraw interface.

        :return: bankingsystem_pb2_grpc.outputEvent in dict form
        """
        log_msg('-----WITHDRAW-------')
        if event.money < 0 or self.balance - event.money < 0:
            log_msg('Insufficient funds for Withdraw.Operation failed.')
            opResult = bankingsystem_pb2.failure
        else:
            self.balance -= event.money
            opResult = bankingsystem_pb2.success
        return {'interface': bankingsystem_pb2.withdraw, 'result': opResult}

    def propagateIfOperationSuccessful(self, operationResponse, event, propagateOperation):
        """
        Propagate  if withdraw / deposit operations were successful.

        :param operationResponse: The response fro original withdraw / deposit operation
        :param event: The event containing the details
        :param propagateOperation: Valid values propropagate_deposit or propagate_withdraw
        :return: None
        """

        if operationResponse['result'] == bankingsystem_pb2.success:
            self.propagateEvent(propagateOperation, event)
        else:
            log_msg('{0} operation failed. No propagation required.'.format(event.interface))

    def handlePropagateDeposit(self, event):
        """
        Implementation of the propropagate_deposit interface.

        :return: bankingsystem_pb2_grpc.outputEvent in dict form
        """

        log_msg('-----Handling Propagated Deposit-------')
        self.balance += event.money
        return {'interface': bankingsystem_pb2.propagate_deposit, 'result': bankingsystem_pb2.success}

    def handlePropagateWithdraw(self, event):
        """
        Implementation of the propagate_withdraw interface.

        :return: bankingsystem_pb2_grpc.outputEvent in dict form
        """

        log_msg('-----Handling Propagated Withdraw-------')
        self.balance -= event.money
        return {'interface': bankingsystem_pb2.propagate_withdraw, 'result': bankingsystem_pb2.success}

    def __str__(self):
        return "BRANCH[id = {0}, balance = {1} , branches = {2} , writeSet={3}".format(self.id,
                                                                                       self.balance,
                                                                                       str(self.branches),
                                                                                       str(self.writeSet)
                                                                                       )


def extractBranchData(parsedData):
    """
    Extracting branch data from the input file
    :param parsedData: parsed command line arguments
    :return: List of branches
    """
    branches = list()
    branchIds = list()
    for data in parsedData:
        log_msg(data)
        entityType = translateEntityToEnum(data['type'])
        if bankingsystem_pb2.branch == entityType or bankingsystem_pb2.bank == entityType:
            log_msg(f'its a branch with id : {data["id"]}')
            branches.append(Branch(id=data['id'], balance=data['balance'], branches=None))
            branchIds.append(data['id'])

    for branch in branches:
        branch.branches = [id for id in branchIds if branch.id != id]
        log_msg(branch)

    return branches


def startBranch(branch):
    """

    :param branch:
    :return:
    """
    portNumber = getProcessId(branch.id)
    log_msg(
        'Starting Branch server for {0} with balance {1} on port {2}'.format(branch.id, branch.balance, portNumber))
    options = (('grpc.so_reuseport', 1),)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
    bankingsystem_pb2_grpc.add_TransactionServicer_to_server(branch, server)
    server.add_insecure_port('[::]:{0}'.format(portNumber))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    initializeLogging()
    inputFile = parseLocalArgs()
    branches = extractBranchData(parseInputFile(inputFile[0]))

    workers = []
    for branch in branches:
        # NOTE: It is imperative that the worker subprocesses be forked before
        # any gRPC servers start up. See
        # https://github.com/grpc/grpc/issues/16001 for more details.
        worker = multiprocessing.Process(target=startBranch,
                                         args=(branch,))
        worker.start()
        workers.append(worker)
    for worker in workers:
        worker.join()
