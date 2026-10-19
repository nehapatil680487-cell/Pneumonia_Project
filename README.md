# Pneumonia Detection Project

A multimodal machine learning-based system for pneumonia screening using chest X-ray images along with blood parameters and oxygen-related clinical measurements.

## Overview

Pneumonia is a respiratory infection that can affect the lungs and may require early clinical assessment. This project aims to provide a screening-oriented system that analyzes multiple patient data modalities to assist in identifying possible pneumonia cases.

The system combines:

- Chest X-ray image analysis
- Blood parameter analysis
- Oxygen/vital measurements
- Multimodal prediction and result presentation

The application provides a user-friendly interface for entering patient information, uploading medical data, obtaining predictions, viewing diagnosis history, and generating reports.

> **Disclaimer:** This project is intended for academic and screening purposes only. It is not a substitute for professional medical diagnosis or clinical decision-making.

## Features

- Patient registration and login
- Patient information management
- Chest X-ray upload
- X-ray-based pneumonia prediction
- Blood parameter-based prediction
- Oxygen/vital parameter analysis
- Multimodal prediction
- Prediction confidence display
- Diagnosis history
- Patient record management
- Automated report generation
- Model insights and visualization
- Streamlit-based user interface
- FastAPI/Python backend integration

## System Architecture

The project follows a frontend-backend architecture:

```text
                    Patient Data
                         |
          +--------------+--------------+
          |              |              |
       X-ray          Blood Data    Oxygen/Vitals
          |              |              |
      CNN Model       ANN Model      ANN Model
          |              |              |
          +--------------+--------------+
                         |
                  Multimodal Fusion
                         |
                 Final Prediction
                         |
                 Result / Report
