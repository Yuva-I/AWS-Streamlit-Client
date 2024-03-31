
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
    K1_most_common_Ngrams_list = [(0, 0),
 (255, 255),
 (204, 204),
 (2, 100),
 (1, 0),
 (0, 139),
 (131, 196),
 (2, 0),
 (68, 36),
 (139, 69),
 (0, 131),
 (255, 117),
 (133, 192),
 (255, 139),
 (254, 255),
 (46, 46),
 (139, 77),
 (141, 77),
 (255, 21),
 (7, 0),
 (69, 252),
 (8, 139),
 (76, 36),
 (0, 1),
 (4, 0),
 (4, 139),
 (137, 69),
 (141, 69),
 (0, 137),
 (0, 255),
 (255, 131),
 (51, 192),
 (80, 232),
 (255, 141),
 (85, 139),
 (8, 0),
 (3, 100),
 (0, 232),
 (15, 182),
 (0, 116),
 (139, 236),
 (64, 0),
 (80, 141),
 (15, 132),
 (12, 139),
 (100, 0),
 (253, 255),
 (255, 0),
 (84, 36),
 (73, 78),
 (65, 68),
 (0, 204),
 (80, 65),
 (68, 68),
 (78, 71),
 (68, 73),
 (16, 0),
 (198, 69),
 (192, 116),
 (199, 69),
 (80, 255),
 (204, 139),
 (2, 101),
 (4, 137),
 (139, 68),
 (116, 36),
 (3, 0),
 (0, 8),
 (139, 76),
 (106, 0),
 (101, 0),
 (196, 12),
 (100, 139),
 (139, 70),
 (64, 2),
 (36, 8),
 (0, 89),
 (69, 8),
 (117, 8),
 (196, 4),
 (86, 139),
 (95, 94),
 (139, 255),
 (32, 0),
 (0, 16),
 (131, 192),
 (0, 80),
 (0, 141),
 (195, 204),
 (36, 20),
 (36, 16),
 (0, 117),
 (139, 240),
 (9, 0),
 (100, 232),
 (0, 128),
 (6, 0),
 (8, 137),
 (1, 100),
 (131, 248)]
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
