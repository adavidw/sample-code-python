"""http://developer.authorize.net/api/reference/#recurring-billing-get-a-list-of-subscriptions"""
import os
import sys
import imp
import time

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import ARBGetSubscriptionListController
constants = imp.load_source('modulename', 'constants.py')

def get_list_of_subscriptions():
    """get list of subscriptions"""
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = constants.apiLoginId
    merchant_auth.transactionKey = constants.transactionKey

    # Set the transaction's refId
    ref_id = "ref{}".format(int(time.time())*1000)

    # Set the sorting
    sorting = apicontractsv1.ARBGetSubscriptionListSorting()
    sorting.orderBy = apicontractsv1.ARBGetSubscriptionListOrderFieldEnum.id
    sorting.orderDescending = "false"

    # Set the paging
    paging = apicontractsv1.Paging()
    paging.limit = 100
    paging.offset = 1

    request = apicontractsv1.ARBGetSubscriptionListRequest()
    request.merchantAuthentication = merchant_auth
    request.refId = ref_id
    request.searchType = apicontractsv1.ARBGetSubscriptionListSearchTypeEnum.subscriptionInactive
    request.sorting = sorting
    request.paging = paging

    controller = ARBGetSubscriptionListController(request)
    controller.execute()

    response = controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            print ("SUCCESS")
            print ("Message Code : %s" % response.messages.message[0]['code'].text)
            print ("Message text : %s" % response.messages.message[0]['text'].text)
            print ("Total Number In Results : %s" % response.totalNumInResultSet)
        else:
            print ("ERROR")
            if response.messages is not None:
                print ("Result code: %s" % response.messages.resultCode)
                print ("Message code: %s" % response.messages.message[0]['code'].text)
                print ("Message text: %s" % response.messages.message[0]['text'].text)
    return response

if os.path.basename(__file__) == os.path.basename(sys.argv[0]):
    get_list_of_subscriptions()
