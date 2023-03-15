from pprint import pprint as pprint
import getpass
import sys ,  boto3 , json

select_what = sys.argv[1]
if len(sys.argv) > 2:
    first = sys.argv[2]
else:
    first = 'null'

if len(sys.argv) > 3:
    second = sys.argv[3]
else:
    second = 'null'

if len(sys.argv) > 4:
    third = sys.argv[4]
else:
    third = 'null'

##########################################################
def select_vpc(region):
    session = boto3.session.Session(profile_name = 'default' , region_name = region)
    client = session.client('ec2')
    Vpcs = client.describe_vpcs()['Vpcs']
    for vpc in Vpcs:
        print(vpc['VpcId'])

############################################################
def select_subnet(region , vpc):
    session = boto3.session.Session(profile_name = 'default' , region_name = region)
    client = session.client('ec2')
    all_subnets = ''
    Subnets = client.describe_subnets(Filters = [{'Name' : 'vpc-id' , 'Values' : [vpc]}])['Subnet']
    for subnet in Subnets:
        if all_subnets == '':
            all_subnets = subnet['SubnetId'] + "|" + subnet['AvailabilityZone']
        else:
            all_subnets = all_subnets + ',' + subnet['SubnetId'] + '|' + subnet['AvailabilityZone']
    print(all_subnets)

##############################################################
def select_instance_class(region , rds_engine , rds_engine_version):
    if(rds_engine == 'null'):
        session = boto3.session.Session(profile_name = 'default' , region_name = region)
        client = session.client('ec2')
        paginator = client.get_paginator('describe_instance_types')
        instance_type_selection = []
        for instance_types in paginator.paginate():
            for instance_type in instance_types['InstanceTypes']:
                if('x86_64' in instance_type['ProcessorInfo']['SupportedArchitecture']):
                    instance_type_selection.append(instance_type['InstanceId'])
        instance_type_selection.sort()
        print('\n'.join(instance_type_selection))

    else:
        session = boto3.session.Session(profile_name = 'default' , region_name = region)
        client = session.client('rds')
        instance_types = []
        paginator = client.get_paginator('describe_orderable_db_instance_options')
        for each_item in paginator.paginate(Engine = 'rds_engine' , Engine_version = rds_engine_version):
            for each_value in (each_item["OrderableDbInstanceOptions"]):
                if each_value['SupportsStorageEncryption'] == True:
                    instance_types.append(each_value['DBInstanceClass'])
                    instance_types = list(dict.fromkeys(instance_types))
                    instance_types.sort()
    for each_type in instance_types:
        print(each_type)

######################################################################

def select_az_from_new_sn_group(region , vpcid , subnets):
    session = boto3.session.Session(profile_name = 'default' , region_name = region)
    client = session.client('ec2')
    subnets = subnets.replace('"' , '')
    subnets = list(subnets.split(","))
    azlist = []
    for each_subnet in client.describe_subnets(Filters = [{'Name' : 'vpc-id' , 'Values' : [vpcid]}]):
        azlist.append(each_subnet["AvailabilityZone"])
    azlist = list(dict.fromkeys(azlist))
    azlist.sort()
    for each_az in azlist:
        print(each_az)
    if len(azlist == 1):
        print('one_az')

##############################################################################

def select_az_from_existing_SNgroup(region , vpcid , subnetgroup):
    session = boto3.session.Session(profile_name = 'default' , region_name = region)
    client = session.client('rds')
    azlist = []
    for each_subnet in client.describe_db_subnet_groups(DBSubnetGroupName = subnetgroup)['DBSubnetGroup']:
        for each_az in each_subnet['Subnets']:
            azlist.append(each_az["SubnetAvailabilityZone"]['Name'])
    azlist = list(dict.fromkeys(azlist))
    for each_az in azlist:
        print(each_az)

#############################################################################

def select_engine_version(region , engine):
    session = boto3.session.Session(profile_name = 'default' , region_name = region)
    client = session.client('rds')
    for each_engine_version in client.describe_db_engine_versions(Engine = engine)['DBEngineVersions']:
        print(each_engine_version['EngineVersion'])

##############################################################################

def select_subnet_group(region , vpc):
    session = boto3.session.Session(profile_name = 'default' , region_name = region)
    client = session.client('rds')
    for subnet_group in client.describe_db_subnet_groups()['DBSubnetGroups']:
        if(subnet_group['VpcId'] == vpc):
            print(subnet_group['DBSubnetGroupName'])

#################################################################################

# def s3_bucket_create_or_exist(account_number , rdsRegion , tagInfoString):
#     session = boto3.session.Session(profile_name = 'default' , region_name = region)
#     client = session.client('s3')
#     tfStateRegion = 'us-west-2'
#     tagInfo = list(tagInfoString.split(','))
#     rdsInstanceName = tagInfo[0]
#     Budget = tagInfo[1]
#     gearid = tagInfo[2]
#     tags = ('TagSet' : [
#         {'Key' : 'BU:Budget' , 'Value' : Budget},
#         {'Key' : 'BU:Gearid' , 'Value' : gearid} 
#     ])
#     destination_folder = "RDS/" + rdsRegion + "/" + rdsInstanceName + "/"
#     tfstate = destination_folder + 'terraform.tfstate'
#     all_buckets = []
#     output = []
#     checkBucket = 'test-terraform-tfstate-' + account_number
#     bucket_policy = """{ "Versions" : "2012-10-17",
#         "Statement" : [
#         {
#             "Sid" : "RevokeAccessForOthers",
#             "Effect" : "Deny",
#             "Principal" : "*",
#             "Action" : "s3 : *",
#             "Resource" : [
#                 "arn:aws:s3:::""" + checkBucket + """",
#                 "arn:aws:s3:::""" + checkBucket + """/*"
#             ],
#             "Condition" : {
#                 "StringNotEquals" : {
#                     "aws:PrincipalArn" : [
#                         "arn:aws:iam::""" + account_number + """:role/JenkinsMemberRole",
#                         "arn:aws:iam::""" + account_number + """:role/aws-reserved/sso.amazonaws.com/AWSReservedSSo_CloudCoreOps_gggjjdjsvio"
#                     ]
#                 }
#             }
#         }
#         ]
#     """
#     for each_bucket in client.list_buckets()['Buckets']:
#         all_buckets.append(each_bucket['Name'])
#     if(checkBucket in all_buckets):
#         client.put_object(Bucket = checkBucket , Key = tfstate)
#         client.delete_object(Bucket = checkBucket , Key = tfstate)
#         existingBucketRegion = client.get_bucket_location(Bucket = checkBucket)['LocationConstraint']
#         output = checkBucket + ' ' + existingBucketRegion + ' ' + tfstate
#         print(output)
#     else:
#         client.create_bucket(Bucket = checkBucket , CreateBucketConfiguration = {"LocationConstraint" : tfStateRegion})
#         client.put_bucket_tagging(Bucket = checkBucket , Tagging = tags)
#         client.put_bucket_encryption(Bucket = checkBucket , ServerSideEncryptionConfiguration = {'Rules' : [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm' : 'aws:kms'} , 'bucket')
#         client.put_bucket_tagging(Bucket = checkBucket , Tagging = tags)
#         client.put_bucket_tagging(Bucket = checkBucket , Tagging = tags)

def check_rds_instance(region ,  rds_instance_name):
    session = boto3.session.Session(profile_name = 'default' , region_name = region)
    client = session.client('rds')
    rds_instances_list = []
    for each_db_instance in client.describe_db_instance()['DBInstances']:
        rds_instances_list.append(each_db_instance['DBInstanceIdentifier'])
    if rds_instance_name in rds_instances_list:
        print('True')
    else:
        print('False')
###############################################################################
# def select_kms_key(region):
#     session = boto3.session.Session(profile_name = 'default' , region_name = region)
#     client = session.client('kms')
#     keys_list = []
#     for keys in client.list_keys()['Keys']:
#         keys_list.append(keys['KeyArn'])
#     for each_key_arn in keys_list:
#         key_manager = client.describe+key(KeyId = each_key_arn)['KeyMetaData']['KeyManager']
#         if key_manager == 'CUSTOMER':

###################################################################################
def select_security_group(region , vpc):
    session = boto3.session.Session(profile_name = 'default' , region_name = region)
    client = session.client('ec2')
    security_groups_selection = ''
    response = client.describe_security_groups()
    for securityGroup in response['SecurityGroups']:
        if securityGroup['VpcId'] == vpc:
            security_groups_selection = security_groups_selection + securityGroup['GroupId'] + '|' + securityGroup['GroupName'] + '\n'
    print(security_groups_selection)

###############################################################################
def get_all_accts():
    session = boto3.session.Session(profile_name = 'default')
    client = session.client('organizations')
    paginator = client.get_paginator('list_accounts')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for acct in page['Accounts']:
            if acct['Status'] == 'ACTIVE':
                print(acct['Id'] + '|' + acct['Name'])
    
################################################################################

if select_what == 'vpc':
    select_vpc(first)

elif select_what == 'subnet':
    select_subnet(first , second)

elif select_what == 'instanceclass':
    select_instance_class(first , second , third)

elif select_what == 'az_new_subnet_group':
    select_az_from_new_sn_group(first , second , third)

elif select_what == 'az_existing_subnet_group':
    select_az_from_existing_SNgroup(first , second , third)

elif select_what == 'engineversion':
    select_engine_version(first , second)

elif select_what == 'subnetgroup':
    select_subnet_group(first , second)

# elif select_what == 's3bucket':
#     s3_bucket_create_or_exist(first , second , third)

elif select_what == 'check_rds_instance':
    check_rds_instance(first , second)

# elif select_what == 'kms':
#     select_kms_key(first)

# elif select_what == 'auroraengineversion':
#     select_aurora_engine_version(first , second , third)

elif select_what == 'security_group':
    select_security_group(first , second)

elif select_what == 'list_accounts':
    select_subnet(first)