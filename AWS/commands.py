# Import necessary libraries

from common import config
from AWS.recommendations import AWSSecurityChecker, AWSCostChecker
from AWS.commom import Account
import json


#Load config file
config = config.load_configs()

def check_costs(regions, output):
    account = Account()
    account_id = account.get_account_id()
    
    snapshot_retention = config["finders"]["aws"]["costs"]["oldSnapshots"]["daysOfRetention"]
    aws_cost_checker = AWSCostChecker(regions, account_id, output=output)
    
    costs_recommendations = {}
    
    
    if config["finders"]["aws"]["costs"]["gp2Volumes"] == True:
        costs_recommendations["gp2_volumes"] = aws_cost_checker.get_gp2_volumes()
        
    if config["finders"]["aws"]["costs"]["volumesOnStoppedInstances"] == True:    
        costs_recommendations["volumes_on_stopped_instances"] = aws_cost_checker.get_volumes_on_stopped_instances()
    
    if config["finders"]["aws"]["costs"]["detachedVolumes"] == True:
        costs_recommendations["detached_volumes"] = aws_cost_checker.get_detached_volumes()

    if config["finders"]["aws"]["costs"]["detachedIps"] == True:
        costs_recommendations["detached_ips"] = aws_cost_checker.get_detached_ips()    
    
    if config["finders"]["aws"]["costs"]["oldSnapshots"]["enabled"] == True:
        costs_recommendations["old_snapshots"] = aws_cost_checker.get_old_snapshots(snapshot_retention)

    # print(json.dumps(costs_recommendations, indent=4))
    return costs_recommendations
    
def check_security(regions, output):
    account = Account()
    account_id = account.get_account_id()    
    aws_security_checker = AWSSecurityChecker(regions, account_id, output=output)
    
    security_recommendations = {}
    
    if config["finders"]["aws"]["security"]["insecureSecurityGroups"] == True:    
        security_recommendations["insecure_security_groups"] = aws_security_checker.get_security_groups_public_egress()

    if config["finders"]["aws"]["security"]["rdsInstancePubliclyAccessible"] == True:        
        security_recommendations["rds_instances_publicly_accessible"] = aws_security_checker.get_rds_instance_publicly_accessible()
        
    if config["finders"]["aws"]["security"]["s3BucketNoPublicAccessBlock"] == True:          
        security_recommendations["s3_bucket_no_public_access_block"] = aws_security_checker.get_buckets_not_public_acess_block()
    
    return security_recommendations
def check_all(regions, output):
    recommendations = {}
    recommendations["costs"] = check_costs(regions, output)
    recommendations["security"] = check_security(regions, output)
    
    # print(json.dumps(recommendations, indent=4))
    
    with open("data.json", "w") as file:
        json.dump(recommendations, file, indent=4)
    return recommendations