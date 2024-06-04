# RegiErg

## Overview
The RegiErg App aims to provide a comprehensive solution for capturing, processing, and analysing erg screen data from Concept2 rowing machines.The app will use advanced OCR capabilities to extract performance data and store it for tracking and analysis.

## Objectives
1. **Capture Erg Screen Data**: Enable users to upload photos of erg screens or capture them directly via a mobile app.
2. **OCR Processing**: Use Azure Vision API to recognize and extract text data from the erg screen images.
3. **Data Storage**: Save the extracted data and images to cloud storage (e.g., Azure Blob Storage) and metadata in a database (e.g., MongoDB).
4. **Incremental Learning**: Train a custom model using Azure Custom Vision with confirmed data to improve accuracy over time.
5. **User Interface**: Develop a web and mobile interface for users to upload images, view processed data, and track performance over time.

## Features
- **Image Upload**: Users can upload erg screen images via the web or mobile app.
- **Real-time OCR**: Process uploaded images in real-time to extract performance metrics.
- Data Visualisation
- Custom Model Training
- Cloud Storage Integration

# Technologies
- **Web Frontend**: React (regimate-frontend)
- **Backend**: Python
- **Database**: MongoDB for storing metadata
- **Cloud Storage**: Azure Blob Storage for storing images
- **OCR**: Azure Vision API for initial OCR and Custom Vision for model training
- **Mobile App**: Planned future integration for direct photo capture and processing