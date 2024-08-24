# Diagnosis-of-Schizophrenia-based-on-EEG-signals-using-Spiking-Neural-Networks

Abstract

Schizophrenia, a chronic psychotic disorder, is a very challenging disease for doctors for prediction as it involves a series of tests and activity analysis. Having Electroencephalogram (EEG) signal data of the patient is one of the most important reports for analysis of the brain activity during such tasks. Since it involves huge amounts of data that corresponds to defining relationships between different parts of the brain, there is a need for computer interference for data visualization and understanding. This leads to bringing in the power of machine learning models that helps in resolving the complexities using mathematical models for better understanding of the correlations in the data features. 

Our work aims to build a system that can reliably classify a patient as Schizophrenic or normal based on their EEG signal data, obtained from the various experiments, using a cognitive model, built by applying Spiking Neural Networks. 

Proposed Sysyem

Patients’ EEG data is acquired in a laboratory monitored by an EEG technologist. These signals are preprocessed and 3 csv files are created from this data: EEG time series data, Demographics data and EEG components data. Our system has two AI models which does the prediction on this data:
-Multimodel Classification architucture using CNN+SNN: accepts EEG time series data and patient demographics data providing an accuracy of 86%
-Evaluation model using ANN: accepts EEG components data to enhance the MCA reliability by 15%

Results

The outcome of our work is an end-to-end system which can be used by labs or hospitals where Schizophrenia is a use case or attended disorder. Our system can assist them to predict the chances of a patient having Schizophrenia using the EEG time series data and Demographics data, with the help of a model built with Spiking neural network architecture. Also built an evaluation model using Random Forest algorithm to validate the MCA, enhancing model reliability by 15%.
We also provide another option to visualize the EEG time series data as a graph for the better understanding of the stakeholders.
