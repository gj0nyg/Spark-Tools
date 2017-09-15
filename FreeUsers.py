#!/usr/local/bin/python3
# Code borrows heavily from Cisco Devnet lessons
from ciscosparkapi import CiscoSparkAPI, SparkApiError
import os
import sys

if __name__ == '__main__':

        # Command line arguments parsing    
        from argparse import ArgumentParser  
        parser = ArgumentParser("ConvertUsers.py")  
        parser.add_argument("-t", "--token", help="[optional] your admin access token. Alternatively, you can use the SPARK_ACCESS_TOKEN env variable", required=False)
        args = parser.parse_args() 
        access_token = args.token
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
            FreeUser=[]
            api = CiscoSparkAPI(access_token=token)
            users=api.people.list()
            for user in users:  
                userDetails=api.people.get(personId=user.id)
                if userDetails.licenses == []:
                    FreeUser.append(userDetails.emails[0])
                    print (userDetails.emails[0])            
#            print(FreeUser)
        except SparkApiError as e:
            print("failed with statusCode: %d" % e.response_code)
            if e.response_code == 404:
                print ("user is invalid")
            elif e.response_code == 400:
                print ("the request was invalid")
            elif e.response_code == 401:
                print ("please check the Cisco Spark token is correct...")
