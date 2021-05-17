import grpc
import bankingsystem_pb2
import bankingsystem_pb2_grpc
import json
from google.protobuf.json_format import MessageToDict
from BankingSystemUtility import log_msg, initializeLogging, parseInputFile, getProcessId, parseLocalArgs, \
    translateEntityToEnum, translateInterfaceToEnum
import uuid


class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = self.createStub()
        # client's write set
        self.writeSet = set()

    def createStub(self):
        """
        This will create the stub for the client. There is one to one relationship between
        client and branch.
        :return: TransactionStub created for the current client
        """
        processId = getProcessId(self.id)
        log_msg('Creating branch stub for customer {0} on {1}'.format(self.id, processId))
        return bankingsystem_pb2_grpc.TransactionStub(
            grpc.insecure_channel('[::]:{0}'.format(str(processId))))

    def executeEvents(self):
        """
        The main function which will be calling the service method , i.e sending events to branch.
        For project 3 we want to create a scenario where customer performs deposits/withdraw on one branch and
        then moves on when he/she is trying to check the balance. For that reason we will be making separate service
        calls for each of the events.

        :return: List of bankingsystem_pb2.BankResponse returned from the service call.
        """
        responseList = list()
        for event in self.events:
            log_msg('Sending out events for {0} with event ID {1}'.format(self.id, event['id']))
            # 'events' in bankingsystem_pb2.BankRequest is expected to be list, since we are sending
            # one event a time, so it needs to be wrapped in list
            eventList = list()
            eventList.append(event)
            resp = self.stub.MsgDelivery(
                bankingsystem_pb2.BankRequest(id=self.id,  # customer ID
                                              type=bankingsystem_pb2.customer,
                                              events=eventList,
                                              writeSet=list(self.writeSet)))  # set is converted to list
            # once we get response back for the event, we update customer's write set with write set provided by the
            # server. That way next time when we are sending a request to the server we have the updated write set.
            self.writeSet = self.writeSet.union(set(resp.writeSet))
            responseList.append(resp)

        return responseList

    def __str__(self):
        return 'CUSTOMER[id={0},events={1} , writeSet={2}'.format(self.id, str(self.events), str(self.writeSet))


def extractCustomerData(parsedData):
    """
    Extracting customer data from the input files. The operations performed by this function
        * Reads the customer json entry for input file
        * Create a new Customer object and adds it to the list
        * If a customer object with same ID exists, it will add the events to existing Customer object
    The last step was done because while combining different inputs files it was realised that, whenever
    there are two or more entries for the same customer then it creates two different Customer objects
    and when events are send to the server they both have different write sets, which doesn't match with server's write sets
    causing a failure.

    :param parsedData:  The arguments from command line
    :return: List of Customers
    """
    customersList = list()
    for data in parsedData:
        # sine we are reading a file where branch data is also present,this check is needed so we can
        # only create objects customer
        if bankingsystem_pb2.customer == translateEntityToEnum(data['type']):
            # checking if the customersList already has the customer with ID of data read from file
            existingCustomer = customerAlreadyExists(data['id'], customersList)

            # if we already have that customer, we will use it to populate the events list
            if existingCustomer:
                log_msg('customer already exists!!')
                cust = existingCustomer
            else:  # we will create a new customer
                log_msg('Creating new customer!!')
                cust = Customer(id=data['id'], events=list())
                customersList.append(cust)

            log_msg('its a Customer with id : %s' % data['id'])

            events = data['events']
            for event in events:
                # translating event names into bankingsystem_pb2.operation enums
                event['interface'] = translateInterfaceToEnum(event['interface'])
                # this check is there to make sure that all input events have DEST set.
                # if none is present, the customer's ID will be used as 'dest'
                if 'dest' not in event:
                    event['dest'] = data['id']

                # If event does not have an ID, then we will assign one by using uuid4.
                # uuid4 is completely random and doesn't reveal any privacy as uuid1 does
                if 'id' not in event:
                    event['id'] = str(uuid.uuid4().hex)
            # Adding the events to Customer.events
            cust.events.extend(events)
    log_msg(f'FINAL LIST OF CUSTOMERS::{len(customersList)}')
    return customersList


def customerAlreadyExists(customerId, inCustomersList):
    """
    Utility function to iterate through the list of Customers to see if any of them have an object with same
    ID as supplied cusotmerId

    :param customerId: The customer Id we want to check
    :param inCustomersList: The list of existing customers
    :return: None if not exists else returns the Customer object
    """
    for cust in inCustomersList:
        if cust.id == customerId:
            return cust
    return None


def writeToOutputFile(allResponses, outputFileName):
    """
    Writing the output to the file. The format of the responses send from the server are
    changed to match the desired format.

    :param allResponses: List of bankingsystem_pb2.BankResponse from the server
    :param outputFileName: Name of the output file
    :return: None
    """
    convertedResponses = list()
    log_msg('*' * 20 + 'FINAL RESPONSES' + '*' * 20)
    log_msg(f'FINAL RESPONSES \n{allResponses}')
    log_msg('*' * 60)

    for respo in allResponses:
        # converting the bankingsystem_pb2.BankResponse to python 'dict' using
        # google.protobuf.json_format.MessageToDict. This will convert the enums to their text equivalent
        # names to match the desired output format.
        resToDict = MessageToDict(respo)
        for resp in resToDict['recv']:
            # for project three we are only intrested in writing out the 'query'
            if resp['interface'] == 'query':
                # Since proto3 doesn't write outfields with ZERO. This is to make sure that for 'money'
                # we get a value, even if it is ZERO.
                if 'money' not in resp.keys():
                    resp['money'] = 0
                # creating the desired output format from the information received
                convertedResponses.append({'id': resToDict['id'], 'balance': resp['money']})

    log_msg(f'Formatted output: {convertedResponses}')
    dataToWrite = list()
    # We are trying to read the existing data and append the new data to it
    try:
        with open(outputFileName, "r") as readFile:
            existingData = json.load(readFile)
            print(existingData, type(existingData))
            dataToWrite.extend(existingData)
            dataToWrite.extend(convertedResponses)
    except Exception as err:
        # When coming in for the first time we will not have the file.
        log_msg(err)
        # Adding the new data so that can be written to the file
        dataToWrite.extend(convertedResponses)

    log_msg(f'Data to write {dataToWrite}')
    # writing data to the file
    with open(outputFileName, 'w') as writeFile:
        json.dump(dataToWrite, writeFile)


if __name__ == '__main__':
    initializeLogging()
    fileNames = parseLocalArgs()
    customers = extractCustomerData(parseInputFile(fileNames[0]))
    responses = list()
    for customer in customers:
        log_msg(customer)
        response = customer.executeEvents()
        responses.extend(response)

    writeToOutputFile(responses, fileNames[1])
