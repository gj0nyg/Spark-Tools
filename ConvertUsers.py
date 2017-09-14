#!/usr/local/bin/python3
from ciscosparkapi import CiscoSparkAPI, SparkApiError
import os
import sys
# Licence UUIDs can be obtained from https://developer.ciscospark.com/endpoint-licenses-get.html
A25UserMeeting="Replace with UUID for meeting"
WebExMeeting="Replace with WebEx UUID"
Messaging="Replace with Messaging licence UUID"
WebExCMR="Replace with CMR UUID"
licences=[A25UserMeeting,WebExMeeting,WebExCMR,Messaging]

if __name__ == '__main__':

        # Command line arguments parsing    
        from argparse import ArgumentParser  
        parser = ArgumentParser("ConvertUsers.py")  
        parser.add_argument("-e", "--email", help="the email address of the user that you wish to convert", required=True)
        parser.add_argument("-t", "--token", help="[optional] your admin access token. Alternatively, you can use the SPARK_ACCESS_TOKEN env variable", required=False)
        args = parser.parse_args() 
        access_token = args.token
        email = args.email

        # Check access token
        spark_access_token = os.environ.get("SPARK_ACCESS_TOKEN")
        token = access_token if access_token else spark_access_token
        if not token:
            error_message = "You must provide a Cisco Spark API access token to " \
                            "interact with the Cisco Spark APIs, either via " \
                            "a SPARK_ACCESS_TOKEN environment variable " \
                            "or via the -t command line argument."
            print(error_message)
            sys.exit(2)
        try:
            api = CiscoSparkAPI(access_token=token)
            users=api.people.list(email=email)
            for user in users:  
                userDetails=api.people.get(personId=user.id)
                api.people.update(
                    personId=user.id,emails=userDetails.emails,
                    displayName=userDetails.displayName,firstName=userDetails.firstName,
                    lastName=userDetails.lastName,avatar=userDetails.avatar,
                    orgId=userDetails.orgId,roles=userDetails.roles,licenses=licences
                    )
            
            print("User %s was updated" %userDetails.displayName)
        except SparkApiError as e:
            print("failed with statusCode: %d" % e.response_code)
            if e.response_code == 404:
                print ("user is invalid")
            elif e.response_code == 400:
                print ("the request was invalid")
            elif e.response_code == 401:
                print ("please check the Cisco Spark token is correct...")
