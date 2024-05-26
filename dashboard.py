"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

import json
import pandas as pd


df = pd.read_json('data.json')
df_gp2_volumes = pd.DataFrame(df["costs"]["gp2_volumes"])
df_volumes_on_stopped_instances = pd.DataFrame(df["costs"]["volumes_on_stopped_instances"])
df_detached_volumes = pd.DataFrame(df["costs"]["detached_volumes"])
df_detached_ips = pd.DataFrame(df["costs"]["detached_ips"])
df_old_snapshots = pd.DataFrame(df["costs"]["old_snapshots"])
df_insecure_security_groups = pd.DataFrame(df["security"]["insecure_security_groups"])
df_rds_instances_publicly_accessible = pd.DataFrame(df["security"]["rds_instances_publicly_accessible"])
df_s3_bucket_no_public_access_block = pd.DataFrame(df["security"]["s3_bucket_no_public_access_block"])


st.set_page_config(
    page_title="Revise.cli",
    page_icon="🧊",
    initial_sidebar_state="collapsed",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)


st.header('📄 Revise.cli', divider='rainbow')
st.text('These were the improvement opportunities we found for the AWS account xxxx..')


# st.json(json.load(open('data.json')))

add_selectbox = st.sidebar.selectbox(
    "Would you like to view the data from which check?",
    ("Latest", "uid-xxxxxx", "uid-zzzzzz")
)

tab1, tab2 = st.tabs(["Costs", "Security"])

with tab1:
    tab1.subheader("🤑 Costs improvements")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("GP2 Volumes", df_gp2_volumes.shape[0])
    col2.metric("Volumes on stopped instances", df_volumes_on_stopped_instances.shape[0])
    col3.metric("Detached Volumes", df_detached_volumes.shape[0])
    col4.metric("Detached IPs", df_detached_ips.shape[0])    
    col5.metric("Old snapshots", df_old_snapshots.shape[0])
    style_metric_cards(background_color="#e0e1dd", border_color="#778da9", border_left_color="#778da9")

    
    if df_gp2_volumes.shape[0] > 0:
        with st.expander("GP2 Volumes"):
            st.write('''
                gp3 provides a better cost-benefit when considering the ability to adjust the IOPS rate and throughput independently, which can result in significant savings, especially for workloads that demand higher performance..
            ''')

            st.dataframe(df_gp2_volumes,use_container_width=True)

    if df_volumes_on_stopped_instances.shape[0] > 0:
        with st.expander("Volumes on stopped instances"):
            st.write('''
                One way to reduce the storage costs of stopped instances in cloud services is simply to delete them when they're not in use.
            ''')

            st.dataframe(df_volumes_on_stopped_instances,use_container_width=True)
    
    if df_detached_volumes.shape[0] > 0:
        with st.expander("Detached Volumes"):
            st.write('''
                If you find unattached volumes that are no longer needed, safely delete them. This will immediately stop incurring storage costs for those volumes.
            ''')

            st.dataframe(df_detached_volumes,use_container_width=True)        

    if df_detached_ips.shape[0] > 0:
        with st.expander("Detached IPs"):
            st.write('''
                Free up unused IPs: After disassociating the IPs from running instances, you can release them entirely. This removes them from your AWS account and stops the costs associated with their reservation.
                
                Automate the cleanup: Implement scripts or automation tools to regularly check and disassociate or release unused IPs. This helps ensure you're not paying for unnecessary resources.
            ''')

            st.dataframe(df_detached_ips,use_container_width=True)        

    if df_old_snapshots.shape[0] > 0:
        with st.expander("Old Snapshots"):
            st.write('''
                Once you've identified obsolete snapshots, safely delete them using AWS management tools or CLI commands. Make sure to double-check before deletion to avoid accidental data loss.
                
                AWS offers lifecycle policies for Amazon EBS snapshots, allowing you to automate the process of managing snapshot retention. You can define rules to automatically delete snapshots after a certain period or based on specific criteria, such as age or number of generations.

            ''')

            st.dataframe(df_old_snapshots,use_container_width=True)   

with tab2:
    tab2.subheader("👮‍♂️ Security improvements")    
    col6, col7, col8, col9, col10 = st.columns(5)

    col6.metric("Insecure Security Groups", df_insecure_security_groups.shape[0])
    col7.metric("RDS instances publicly accessible", df_rds_instances_publicly_accessible.shape[0])
    col8.metric("S3 bucket no public access block", df_s3_bucket_no_public_access_block.shape[0])

    if df_insecure_security_groups.shape[0] > 0:
        with st.expander("Insecure Security Groups"):
            st.write('''
                If possible, restrict access only to specific IPs or IP ranges that really need to access your cloud resources. This can be done by changing security rules to allow traffic only from trusted sources.
            ''')

            st.dataframe(df_insecure_security_groups,use_container_width=True)
        
    if df_rds_instances_publicly_accessible.shape[0] > 0:
        with st.expander("RDS instances publicly accessible"):
            st.write('''
                If a public endpoint is not properly configured with the appropriate access controls, firewall, and other security measures, it can represent a significant vulnerability.

    Ensure that security restrictions are properly enforced.
            ''')

            st.dataframe(df_rds_instances_publicly_accessible,use_container_width=True)

    if df_s3_bucket_no_public_access_block.shape[0] > 0:
        with st.expander("S3 bucket no public access block"):
            st.write('''
                When all options for public access blocking are disabled on an S3 bucket (Amazon Simple Storage Service), it means that the bucket and the objects within it are configured to allow public access. This can have several implications:

    Ensure that the ACL policies are configured correctly.
            ''')
            st.dataframe(df_s3_bucket_no_public_access_block, use_container_width=True)