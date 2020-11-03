# Assignment 1
## RSEG176 Cloud Computing

These are the files used in the lambda functions for our first assignment.
Each file represents a single function. 

They are executed in the following sequence:

1. detectS3andLoad 
1. cleanSalesData
1. generateBranchSalesReport
1. generatePaymentTypeSalesReport
1. generateProductBranchSalesReport
1. generateProductPaymentSalesReport
1. generateProductSalesReport

With the Exception of detectS3andLoad each function is triggered 
by the success of the previous function. They pass the company name and original event
through each execution in order to make sure they can be used for any company or csv.

detectS3andLoad is triggered by detecting a csv loaded in the sales_record_in
folder in the companies directory.

This project is built on Python3.7 and requires the following libraries
1. Boto3 for S3 Management - https://aws.amazon.com/sdk-for-python/
1. psycopg2 for Redshift - https://www.psycopg.org/docs/
