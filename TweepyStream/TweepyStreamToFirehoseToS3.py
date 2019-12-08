from tweepy import StreamListener,Stream,OAuthHandler
import boto3
import logging
from Utilities.Config import *


class TweetListener(StreamListener):

    def on_data(self,data):
        firehose_client = boto3.client('firehose',
                                        aws_access_key_id=aws_access_key_id,
                                        aws_secret_access_key=aws_secret_access_key
                                       ,region_name=region_name)
        try:
            print("putting data")
            response = firehose_client.put_record(DeliveryStreamName=DeliveryStreamName,
                                                  Record={
                                                           'Data': data
                                                         }
                                                  )
            logging.info(response)
            return True
        except Exception:
            logging.exception("Problem pushing to firehose")

    def on_error(self, status):
        print(status)


