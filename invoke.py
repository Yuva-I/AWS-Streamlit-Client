
import streamlit as st
import boto3
import json
import pefile
from scipy.sparse import hstack, csr_matrix

# Initialize SageMaker runtime client
runtime = boto3.client('sagemaker-runtime',
                      aws_access_key_id='ASIA47CRWCQ4FKEP2WG6',
aws_secret_access_key='I3pq6AqCoRn4/pcheS4kscSoqfut4vkH7OtoglTZ',
aws_session_token='FwoGZXIvYXdzEBwaDCNlJ9/AGhKiNwMNMSLNAb1AIDSHORVw860WZwPSabrPqGtoWYJe3xmLGnH64vpnjnwGoIJ/JfyMbO/eqXVryKEWcECBW7uv4dVbhkiKOevfarqFGSDT5HdLrD2vLV/ER9lZuOC/vL+X5ZHuoO0Vr7qlmGIvgyN1UrSwcUI84J5E6/MTHDL6Rodj4dd842yY5sQLf+d7VgJks6QVKFCGZblup/awCMavHz6FS1g61jjk1chBnkMG419qU2xRt39gQeZJU6DdlA/xzp7+ogSZzrxWIn169Q6U6hb9V4sojdimsAYyLay7mvLL3CC4iKwXKhEIp92gIssSGNhZm0xnLsZ2NO+tY7UY3jnBuoiQEC5znQ==',
                      region_name = 'us-east-1')

# Function to extract features from the .exe file
def extract_features(file_path):
    # Your feature extraction logic here
    # Example: Extract features using pefile, getImports, getSectionNames, etc.
    # Example: Return extracted features as a dictionary
    importsCorpus_pred = []
    numSections_pred = []
    sectionNames_pred = []
    NgramFeaturesList_pred = []

    NGramFeatures_pred = getNGramFeaturesFromSample(file_path, K1_most_common_Ngrams_list)
    pe_pred = pefile.PE(file_path)
    imports_pred = getImports(pe_pred)
    nSections_pred = len(pe_pred.sections)
    secNames_pred = getSectionNames(pe_pred)
    importsCorpus_pred.append(imports_pred)
    numSections_pred.append(nSections_pred)
    sectionNames_pred.append(secNames_pred)
    NgramFeaturesList_pred.append(NGramFeatures_pred)
    importsCorpus_pred_transformed = imports_featurizer.transform(importsCorpus_pred)
    sectionNames_pred_transformed = section_names_featurizer.transform(sectionNames_pred)
    print({
        "NgramFeaturesList_pred": NgramFeaturesList_pred,
        "importsCorpus_pred_transformed": importsCorpus_pred_transformed,
        "sectionNames_pred_transformed": sectionNames_pred_transformed,
        "numSections_pred": csr_matrix(numSections_pred).transpose()
    })
    return {
        "NgramFeaturesList_pred": NgramFeaturesList_pred,
        "importsCorpus_pred_transformed": importsCorpus_pred_transformed,
        "sectionNames_pred_transformed": sectionNames_pred_transformed,
        "numSections_pred": csr_matrix(numSections_pred).transpose()
    }

# Function to send features to SageMaker endpoint for inference
def invoke_endpoint(features):
    # Serialize features to JSON
    payload = json.dumps(features)
    
    # Specify your endpoint name
    endpoint_name = "sklearn-local-ep2024-03-31-08-06-32"
    
    # Send inference request to the endpoint
    response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                       ContentType='application/json',
                                       Body=payload)
    
    # Parse the prediction response
    result = json.loads(response['Body'].read().decode())
    
    return result

# Streamlit app
def main():
    st.title("SageMaker Inference with Streamlit")
    
    # File upload widget
    uploaded_file = st.file_uploader("Upload .exe file", type="exe")
    
    if uploaded_file is not None:
        # Perform feature extraction
        features = extract_features(uploaded_file)
        
        # Perform inference
        prediction = invoke_endpoint(features)
        
        # Display prediction
        st.write("Prediction:", prediction)

if __name__ == "__main__":
    main()
