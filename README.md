# 🤖 AI Smart Hiring Platform

### AI-Driven Candidate Matching & Hiring Platform

An intelligent recruitment platform that helps automate the hiring process through **resume parsing, ATS analysis, candidate-job matching, skill-gap analysis, interview assistance, AI interview simulation, recruitment analytics, and voice-based screening**.

---

## 📌 Project Overview

The **AI Smart Hiring Platform** is a web-based recruitment application developed using Python and Streamlit.

The platform allows recruiters to upload candidate resumes, extract important candidate information, analyze resumes using ATS concepts, compare candidates with job descriptions, identify skill gaps, generate role-specific interview questions, conduct AI-based interview simulations, and perform voice-based candidate screening.

The project is developed across **four milestones**, with each milestone extending the functionality of the previous milestone.

---

# 🚀 Project Milestones

## 🔹 Milestone 1 – Resume Analysis & Candidate Management

The first milestone focuses on automated resume processing and candidate profile creation.

### Features

- 📄 PDF resume parsing
- 📝 DOCX resume parsing
- 📃 TXT resume parsing
- 👤 Candidate name extraction
- 📧 Email extraction
- 📱 Phone number extraction
- 🎓 Education extraction
- 💻 Skills extraction
- 🏆 Certification extraction
- 📂 Project extraction
- 💼 Experience extraction
- 👥 Candidate profile creation
- 🔐 User login and registration

---

## 🔹 Milestone 2 – Candidate Matching & Hiring Analysis

Milestone 2 introduces candidate-job matching and hiring analysis.

### Features

- 💼 Job description input
- 🔍 Candidate-job matching
- 🎯 Hiring / compatibility score
- 🧠 Skill matching
- ❌ Missing skill identification
- 📊 Skill-gap analysis
- 📈 Candidate analytics
- 📋 Candidate comparison
- 📌 Job application tracking
- 📊 Matching visualizations

The matching engine compares the candidate's extracted skills and profile information with the requirements provided in the job description.

---

## 🔹 Milestone 3 – ATS & Interview Assistance

Milestone 3 introduces ATS functionality and interview automation.

### ATS Integration

ATS analysis is integrated into the **Resume Analyzer**.

The system analyzes relevant candidate information such as:

- Candidate details
- Skills
- Education
- Experience
- Projects
- Certifications
- Job-related information

The system generates an ATS score that can be used along with the candidate's matching and hiring information.

### Interview Question Generator

The Interview Assistant generates questions according to the selected job role.

Question types include:

- 📝 Descriptive questions
- 🔘 Multiple-choice questions
- 🔄 Mixed questions

### AI Interview Simulation

The AI Interview Simulation allows a candidate to participate in an interactive interview.

The workflow includes:

1. Candidate selection
2. Job role selection
3. Interview question generation
4. Candidate response
5. Response evaluation
6. Progression through interview questions
7. Interview result

---

# 🔹 Milestone 4 – Recruitment Dashboard & Voice Screening

Milestone 4 extends the platform with recruitment analytics, voice screening, and deployment support.

## 📊 Recruitment Dashboard

The dashboard provides an overview of the recruitment process.

### Dashboard Metrics

- 👥 Total Candidates
- 🎤 Interviews
- 📈 Hiring Success Rate
- ⏱️ Average Time to Hire
- 🎯 Average Match Score
- 📄 Average ATS Score
- ✅ Selected Candidates

### Recruitment Analytics

The dashboard provides visual information about:

- Candidate distribution
- Hiring status
- Matching performance
- ATS performance
- Recruitment activity

---

# 🎙️ Voice-Based Candidate Screening

The Voice Screening module provides an additional method for preliminary candidate screening.

### Features

- 🎤 Voice recording
- 🔊 Audio input
- 🗣️ Speech-to-text conversion
- 🤖 AI interviewer interaction
- 📋 Preliminary candidate assessment
- 📊 Screening result

### Technologies

- SpeechRecognition
- pyttsx3

### Voice Screening Workflow

```text
Candidate Selection
        ↓
Job Role Selection
        ↓
Voice Question
        ↓
Candidate Response
        ↓
Speech Recognition
        ↓
Response Analysis
        ↓
Preliminary Screening Result
