import sagemaker
import boto3
from Preprocessing.PreprocessingFunctions import *
from PostProcessing.PostProcessingFunctions import *
from Utilities.Config import *
from TweepyStream.TweepyStreamToFirehoseToS3 import *
import os

###########Get Data
#Run the Twitter API to Firehose to S3 process

auth=OAuthHandler(twitterkey1,twitterkey2)
auth.set_access_token(twitterkey3, twitterkey4)

twitter_stream = Stream(auth, TweetListener())
#Extract tweets by key word
twitter_stream.filter(track=["stock"])

######Extraction and Preprocessing

#Get text file from s3 database after streaming from twitter api and kinesis firehose.
s3 = boto3.resource('s3',aws_access_key_id=aws_access_key_id,
         aws_secret_access_key=aws_secret_access_key)

obj = s3.Object(bucket, bucket_data)

#Split text and save as list.
text = clean_text(obj)

#Generate plain text file for blazingtext input.
generate_text_file(text)

#Get sagemaker blazing text container.

container = sagemaker.amazon.amazon_estimator.get_image_uri(region_name, "blazingtext", "latest")
sess = sagemaker.Session()

#Upload text file to
sess.upload_data("tweet_text.txt")

######Training
#Tune and train model
bt_model = sagemaker.estimator.Estimator(container,
                                         role=role,
                                         train_instance_count=2,
                                         train_instance_type='ml.m5.large',
                                         train_volume_size = 5,
                                         train_max_run = 36000,
                                         input_mode= 'File',
                                         output_path=output_path,
                                         sagemaker_session=sess)

# set the hyperparameters of the BlazingText model
bt_model.set_hyperparameters(mode="batch_skipgram",
                             epochs=15,
                             min_count=5,
                             sampling_threshold=0.0001,
                             learning_rate=0.05,
                             window_size=5,
                             vector_dim=300,
                             negative_samples=5,
                             batch_size=11,
                             evaluation=True,
                             subwords=False)

train_data = sagemaker.session.s3_input(train_data, distribution='FullyReplicated',
                        content_type='text/plain', s3_data_type='S3Prefix')

data_channels = {'train': train_data}

bt_model.fit(inputs=data_channels, logs=True)

########Postprocessing

#Get vector
unzip_text_vectors(s3,bt_model,bucket)

vectors = prepare_vectors_for_analysis(text_file)

cosine_similarity_vector_comparison(vectors, "president","arealdonaldtrump")

#Word Embedding method with a cosine distance assesses that our two sentences are similar to 99.07 %