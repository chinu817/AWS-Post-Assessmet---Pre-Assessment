import boto3
import time

region = 'us-east-1'
instance_id = input("Enter Instance Id: ")
ec2 = boto3.client('ec2', region_name=region)
ec21=boto3.resource('ec2', region_name=region)

#Start an Instance
ec2.start_instances(InstanceIds=[instance_id])
print('started your instances: ' + instance_id)

time.sleep(200)

#Stop our instance
ec2.stop_instances(InstanceIds=[instance_id])
print('stopped your instances: ' + instance_id)

time.sleep(200)

#Snapshot our instance
instance=ec21.Instance(instance_id)
volumes=instance.volumes.all()

volumes_dict = {'pratik-snapshot' : 'v_id',}
       
for i in volumes:
 if i not in volumes_dict.keys():
   volumes_dict['pratik-snapshot']=i.id
 print(i.id)

successful_snapshots = dict()
for snapshot in volumes_dict:
  try:
      response = ec2.create_snapshot(
          Description= snapshot,
          VolumeId= volumes_dict[snapshot],
          DryRun= False
      )
      status_code = response['ResponseMetadata']['HTTPStatusCode']
      snapshot_id = response['SnapshotId']
     
      if status_code == 200:
          successful_snapshots[snapshot] = snapshot_id
  except Exception as e:
      exception_message = "There was error in creating snapshot " + snapshot + " with volume id "+volumes_dict[snapshot]+" and error is: \n"\
                          + str(e)

print(successful_snapshots)

time.sleep(200)

#Terinating an instance
ec2.terminate_instances(InstanceIds=[instance_id])