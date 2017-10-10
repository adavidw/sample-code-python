import os, sys
import imp
import time

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
constants = imp.load_source('modulename', 'constants.py')
from decimal import *

def create_an_accept_transaction(amount):

    # Create a merchantAuthenticationType object with authentication details
    # retrieved from the constants file
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = constants.apiLoginId
    merchant_auth.transactionKey = constants.transactionKey

    # Set the transaction's refId
    ref_id = "ref{}".format(int(time.time())*1000)

    # Create the payment object for a payment nonce
    opaqueData = apicontractsv1.opaqueDataType()
    opaqueData.dataDescriptor = "COMMON.ACCEPT.INAPP.PAYMENT"
    opaqueData.dataValue = "119eyJjb2RlIjoiNTBfMl8wNjAwMDUyN0JEODE4RjQxOUEyRjhGQkIxMkY0MzdGQjAxQUIwRTY2NjhFNEFCN0VENzE4NTUwMjlGRUU0M0JFMENERUIwQzM2M0ExOUEwMDAzNzlGRDNFMjBCODJEMDFCQjkyNEJDIiwidG9rZW4iOiI5NDkwMjMyMTAyOTQwOTk5NDA0NjAzIiwidiI6IjEuMSJ9"

    # Add the payment data to a paymentType object
    paymentOne = apicontractsv1.paymentType()
    paymentOne.opaqueData = opaqueData
    
    # Create order information
    order = apicontractsv1.orderType()
    order.invoiceNumber = "10101"
    order.description = "Golf Shirts"
    
    # Set the customer's Bill To address
    customer_address = apicontractsv1.customerAddressType()
    customer_address.firstName = "Ellen"
    customer_address.lastName = "Johnson"
    customer_address.company = "Souveniropolis"
    customer_address.address = "14 Main Street"
    customer_address.city = "Pecan Springs"
    customer_address.state = "TX"
    customer_address.zip = "44628"
    customer_address.country = "USA"
    
    # Set the customer's identifying information
    customer_data = apicontractsv1.customerDataType()
    customer_data.type = "individual"
    customer_data.id = "99999456654"
    customer_data.email = "EllenJohnson@example.com"
    
    # Add values for transaction settings
    duplicateWindowSetting = apicontractsv1.settingType()
    duplicateWindowSetting.settingName = "duplicateWindow"
    duplicateWindowSetting.settingValue = "600"
    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(duplicateWindowSetting)

    # Create a transactionRequestType object and add the previous objects to it
    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount
    transactionrequest.order = order
    transactionrequest.payment = paymentOne
    transactionrequest.billTo = customer_address
    transactionrequest.customer = customer_data
    transactionrequest.transactionSettings = settings

    # Assemble the complete transaction request
    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchant_auth
    createtransactionrequest.refId = ref_id
    createtransactionrequest.transactionRequest = transactionrequest
    
    # Create the controller and get response
    createtransactioncontroller = createTransactionController(createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    if response is not None:
        # Check to see if the API request was successfully received and acted upon
        if response.messages.resultCode == "Ok":
            # Since the API request was successful, look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages') is True:
                print ('Successfully created transaction with Transaction ID: %s' % response.transactionResponse.transId)
                print ('Transaction Response Code: %s' % response.transactionResponse.responseCode)
                print ('Message Code: %s' % response.transactionResponse.messages.message[0].code)
                print ('Auth Code: %s' % response.transactionResponse.authCode)
                print ('Description: %s' % response.transactionResponse.messages.message[0].description)
            else:
                print ('Failed Transaction.')
                if hasattr(response.transactionResponse, 'errors') is True:
                    print ('Error Code:  %s' % str(response.transactionResponse.errors.error[0].errorCode))
                    print ('Error Message: %s' % response.transactionResponse.errors.error[0].errorText)
        # Or, print errors if the API request wasn't successful
        else:
            print ('Failed Transaction.')
            if hasattr(response, 'transactionResponse') is True and hasattr(response.transactionResponse, 'errors') is True:
                print ('Error Code: %s' % str(response.transactionResponse.errors.error[0].errorCode))
                print ('Error Message: %s' % response.transactionResponse.errors.error[0].errorText)
            else:
                print ('Error Code: %s' % response.messages.message[0]['code'].text)
                print ('Error Message: %s' % response.messages.message[0]['text'].text)
    else:
        print ('Null Response.')

    return response

if(os.path.basename(__file__) == os.path.basename(sys.argv[0])):
    create_an_accept_transaction(constants.amount)
