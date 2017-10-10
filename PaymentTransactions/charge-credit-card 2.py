"""
Charge a credit card
"""

import imp
import os
import sys

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController

CONSTANTS = imp.load_source('modulename', 'constants.py')


def charge_credit_card(amount):
    """
    Charge a credit card
    """

    merchant_auth = add_authentication()
    credit_card = add_card()
    payment = add_payment(credit_card)
    order = add_order()
    customer_address = add_address()
    customer_data = add_customer()
    settings = add_settings()
    line_items = add_line_items()

    # Create a transactionRequestType object and add the other objects to it.
    transaction_request = create_transaction_request(
        amount, payment, order, customer_address, customer_data, settings,
        line_items)

    # Assemble the complete transaction request
    transaction_controller = create_transaction_controller(
        merchant_auth, transaction_request)

    return get_response(transaction_controller)


def get_response(transaction_controller):
    """ parses response from Authorize.Net """
    response = transaction_controller.getresponse()
    if response is not None:
        # Check to see if the API request was successfully received and acted upon
        if response.messages.resultCode == "Ok":
            # Since the API request was successful, look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages') is True:
                print ('Successfully created transaction with Transaction ID: %s' \
                    % response.transactionResponse.transId)
                print ('Transaction Response Code: %s' \
                    % response.transactionResponse.responseCode)
                print ('Message Code: %s' \
                    % response.transactionResponse.messages.message[0].code)
                print ('Description: %s' \
                    % response.transactionResponse.messages.message[0].description)
            else:
                print('Failed Transaction.')
                if hasattr(response.transactionResponse, 'errors') is True:
                    print ('Error Code:  %s' \
                        % str(response.transactionResponse.errors.error[0].errorCode))
                    print ('Error message: %s' \
                        % response.transactionResponse.errors.error[0].errorText)
        # Or, print errors if the API request wasn't successful
        else:
            print('Failed Transaction.')
            if hasattr(response, 'transactionResponse') is True \
                and hasattr(response.transactionResponse, 'errors') is True:
                print ('Error Code: %s' \
                    % str(response.transactionResponse.errors.error[0].errorCode))
                print ('Error message: %s' \
                    % response.transactionResponse.errors.error[0].errorText)
            else:
                print ('Error Code: %s' \
                    % response.messages.message[0]['code'].text)
                print ('Error message: %s' \
                    % response.messages.message[0]['text'].text)
    else:
        print('Null Response.')

    return response


def create_transaction_controller(merchant_auth, transaction_request):
    """ Assemble the complete transaction request """
    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchant_auth
    createtransactionrequest.refId = "MerchantID-0001"
    createtransactionrequest.transactionRequest = transaction_request
    # Create the controller
    createtransactioncontroller = createTransactionController(
        createtransactionrequest)
    createtransactioncontroller.execute()
    return createtransactioncontroller


def create_transaction_request(amount, payment, order, customer_address,
                               customer_data, settings, line_items):
    """ Create a transactionRequestType object and add the other objects to it. """
    transaction_request = apicontractsv1.transactionRequestType()
    transaction_request.transactionType = "authCaptureTransaction"
    transaction_request.amount = amount
    transaction_request.payment = payment
    transaction_request.order = order
    transaction_request.billTo = customer_address
    transaction_request.customer = customer_data
    transaction_request.transactionSettings = settings
    transaction_request.lineItems = line_items
    return transaction_request


def add_line_items():
    """ add an array of line items """
    # setup individual line items
    line_item_1 = apicontractsv1.lineItemType()
    line_item_1.itemId = "12345"
    line_item_1.name = "first"
    line_item_1.description = "Here's the first line item"
    line_item_1.quantity = "2"
    line_item_1.unitPrice = "12.95"
    line_item_2 = apicontractsv1.lineItemType()
    line_item_2.itemId = "67890"
    line_item_2.name = "second"
    line_item_2.description = "Here's the second line item"
    line_item_2.quantity = "3"
    line_item_2.unitPrice = "7.95"

    # build the array of line items
    line_items = apicontractsv1.ArrayOfLineItem()
    line_items.lineItem.append(line_item_1)
    line_items.lineItem.append(line_item_2)
    return line_items


def add_settings():
    """ Add values for transaction settings """
    duplicate_window_setting = apicontractsv1.settingType()
    duplicate_window_setting.settingName = "duplicateWindow"
    duplicate_window_setting.settingValue = "60"
    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(duplicate_window_setting)
    return settings


def add_customer():
    """ Set the customer's identifying information """
    customer_data = apicontractsv1.customerDataType()
    customer_data.type = "individual"
    customer_data.id = "99999456654"
    customer_data.email = "EllenJohnson@example.com"
    return customer_data


def add_order():
    """ Create order information """
    order = apicontractsv1.orderType()
    order.invoiceNumber = "10101"
    order.description = "Golf Shirts"
    return order


def add_payment(credit_card):
    """ Add the payment data to a paymentType object """
    payment = apicontractsv1.paymentType()
    payment.creditCard = credit_card
    return payment


def add_address():
    """Set the customer's Bill To address """
    customer_address = apicontractsv1.customerAddressType()
    customer_address.firstName = "Ellen"
    customer_address.lastName = "Johnson"
    customer_address.company = "Souveniropolis"
    customer_address.address = "14 Main Street"
    customer_address.city = "Pecan Springs"
    customer_address.state = "TX"
    customer_address.zip = "44628"
    customer_address.country = "USA"
    return customer_address


def add_authentication():
    """
    Create a merchantAuthenticationType object with authentication details
    retrieved from the constants file
    """
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = CONSTANTS.apiLoginId
    merchant_auth.transactionKey = CONSTANTS.transactionKey
    return merchant_auth


def add_card():
    """ Create the payment data for a credit card """
    credit_card = apicontractsv1.creditCardType()
    credit_card.cardNumber = "4111111111111111"
    credit_card.expirationDate = "2020-12"
    credit_card.cardCode = "123"
    return credit_card


if (os.path.basename(__file__) == os.path.basename(sys.argv[0])):
    charge_credit_card(CONSTANTS.amount)
