# AWS Data Pipeline with Python and MySQL
## [If something is not clear, please check my blog post for further explanation of this work on medium.com](https://medium.com/@asimjkw/building-an-automated-data-science-pipeline-web-scraping-mysql-and-amazon-aws-c9aa65f2bfdc)
**This repository aims to guide and help create an automated data pipeline on AWS using Python and MySQL, utilizing services such as RDS, Lambda, and CloudWatch. The pipeline is designed to gather information on the geographic location and population size of pre-specified cities in Germany by web scraping data from Wikipedia. It also retrieves weather information and data on arriving flights for the next day (CET). All the collected data is stored in a relational database consisting of tables for cities, airports, population, weather, and flights.**
Prerequisites
Before running this project, make sure you have the following:

-	An API key for the Weather from [**openweathermap.org**](https://openweathermap.org/forecast5) for 5-day forecast to fetch weather data.
-	An API key from [**AeroDataBox**](https://rapidapi.com/aedbx-aedbx/api/aerodatabox/) to fetch flight data. Free options with monthly limited requests are available.
-	An AWS account to execute the project on the cloud.
	
  ##                   ∗∗IMPORTANT!!!!∗∗           ∗∗IMPORTANT!!!!∗∗        ∗∗IMPORTANT!!!!∗∗
  
**Note: AWS provides free tier options, but please be cautious as costs may occur if you choose the wrong payment plan or exceed the limits. I am not responsible for any costs incurred.**

## AWS Account and RDS Instance Setup

To set up your AWS account and RDS instance, follow these steps:

1.	Create an [AWS_account]( https://aws.amazon.com/free/) if you haven't already.
2.	Sign in to your [AWS_Console](http://console.aws.amazon.com/).
3.	Go to Services > RDS.
4.	Choose "Create a database".
5.	Select "MySQL" as the database type and choose the latest MySQL version (probably 8.0.XX).
6.	Pick the "Free tier" template to avail the free option.
7.	Provide a name for your instance.
8.	Choose a username and password for the "master user".
9.	Disable the pre-selected option "Enable storage autoscaling" to avoid extra charges.
10.	Leave the default settings for VPC.
11.	Allow public access to your instance and create a new VPC security group with a recognizable name.
12.	Leave the default values for Availability Zone and Database port.
13.	In the "Database authentication" settings, leave the default as "Password authentication".
14.	Disable the pre-selected option "Enable automated backups" to avoid extra charges.
15.	Click on "Create database" and wait for the database status to switch from "Creating" to "Active".
    
**Note: Ensure you have set up your AWS credentials properly and have the necessary permissions to create and manage AWS resources. You can find resources on the internet, such as this [example](https://dev.to/chrisgreening/deploying-a-free-tier-relational-database-with-amazon-rds-3jd2#creating-an-instance-of-mysql).**

## Connect to your Amazon RDS MySQL Instance

![](https://learn.wbscodingschool.com/wp-content/uploads/2021/06/Screenshot-2021-07-07-at-10.57.44-e1625739643919-1024x718.png)

### To connect to your Amazon RDS MySQL instance, follow these steps:
1.	Obtain the host address or "endpoint" of your instance. From AWS Console > RDS > Databases, click on your database and copy the endpoint from the "Connectivity & security" tab.
2.	Open MySQL Workbench and create a new connection.
3.	Provide a connection name as an identifier for your AWS instance.
4.	Paste the instance endpoint as the hostname.
5.	Set the port as 3306.
6.	Use "admin" as the username unless you changed it during the database creation.
7.	Store the password in Keychain or Vault and enter the password you set for the AWS instance in RDS (not the password used to connect to your local server).
8.	Leave the other fields with their default values and click OK. Test the connection to ensure it's successful.
You can now create a database and table in MySQL by executing the scraped_database_scrip.sql file to set up the schema and necessary tables.

**Note: You can find resources on the internet for the above-mentioned requirements, such as this [example](https://dev.to/chrisgreening/deploying-a-free-tier-relational-database-with-amazon-rds-3jd2#creating-an-instance-of-mysql).**

## AWS Lambda Setup: Move your scripts to the cloud

**Before creating our first Lambda function, we will create a role that allows the Lambda function to connect to our RDS instance.**

### Create a role:

1.	Sign in to your [AWS_Console](http://console.aws.amazon.com/).
2.	Search for "IAM" in the search bar at the top and click on it.
3.	On the left side menu, click on "Roles".
4.	Click on "Create role".
5.	In step 1, select "AWS service" as the type of trusted entity and "Lambda" as the use case, then click on "Next".
6.	In step 2, tick the box of the policy "AdministratorAccess" and click on "Next".
7.	In step 3, set "LambdaAdminAccess" as the role name.
8.	Click on "Create role".

### Create a Lambda function:

1.	Sign in to your AWS console.
2.	Go to Services > Lambda.
3.	Click on "Create function".
4.	Select "Author from scratch".
5.	Give your function a name you can recognize, for testing purposes.
6.	Select "Python 3.9" as the runtime.
7.	On the "Permissions" section, click on "Change default execution role".
8.	Tick "Use an existing role" and select the "LambdaAdminAccess" role you created.
9.	Click on "Create function".

**If everything went well, you should now be in the function dashboard.**

### Connect your Lambda function to your RDS instance:
![](https://learn.wbscodingschool.com/wp-content/uploads/2021/06/Screenshot-2021-07-26-at-16.02.17.png)
1.	On your Lambda function dashboard, scroll down to the "Code Source" section.
2.	Click on lambda_function.py to open the code editor.
3.	Choose the "Upload from" button in the top-right corner and select the ".zip file" option to upload the lambda-function zip file provided in (folder with data-scraping py codes) in the repository for the intended update function.
4.	Add "AWS Data Wrangler + KLayers" for both Python and SQLAlchemy. Go back to your Lambda function on the AWS console, scroll down to the bottom of the page, and click on "Add a layer" in the "Layers" section.
5.	Select "AWS Layers" and choose "AWSSDKPandas-Python39" followed by the latest (or intended) version. Click on "Add".
6.	To include SQLAlchemy, visit the GitHub repository from Keith about Klayers. Scroll down to the README.md and find the "List of ARNs". Select the appropriate Python version (e.g., Python 3.9), find SQLAlchemy in the list of Python packages, and copy the ARN code.
7.	Go back to your Lambda Function on the AWS Console and add another layer. Instead of selecting a layer from the list, click on "Specify an ARN" and paste the ARN code you copied from the Klayers repository. Click on "Add".
8.	Your Lambda function should now be ready to run all the code.

### Click "Deploy" to save the code, and you can now test if the Lambda function is working.
# Automate the Data Pipeline
To automate the intended update schedule for different data, you need to create a schedule event using AWS EventBridge service (previously known as CloudWatch) and associate the relevant Lambda function as the target. You can find a brief tutorial here[](https://youtu.be/iUIWG0h2D84).
Feel free to customize and explore the project according to your needs.

