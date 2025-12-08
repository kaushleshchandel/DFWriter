# REQUIREMENTS.md

## 1. Project Overview
DFWriter is a distraction-free writing application designed to run on a Raspberry Pi with a wide-screen display. The primary goal is to provide an immersive environment for authors to write books, supported by an intelligent AI writing assistant.

## 2. Hardware & System Requirements
- **Hardware**: Raspberry Pi (Optimized for Lite OS).
- **Display**: Wide-screen monitor support.
  - Custom HDMI configuration for specific resolution (e.g., 1280x400).
- **OS**: Raspberry Pi OS Lite (with Openbox window manager).
- **Startup**: Custom Plymouth splash screen for a polished, appliance-like boot experience.

## 3. Functional Requirements

### 3.1. Writing Interface
- **Distraction-Free Mode**: Clean, minimalist UI to focus solely on text.
- **Navigation**: Easy switching between Books, Chapters, and Pages.
- **Search**: Natural language search across the entire book content.

### 3.2. Project Management & Planning
- **Book Setup Wizard**:
  - AI suggestions for Title, Genre, Target Length, and Complexity based on initial user input.
  - Manual fine-tuning of book settings.
- **Structural Planning**:
  - Organize by Genre and Category.
  - Chapter management.
  - Character builder/profiles.
  - Plot outlining.

### 3.3. AI Writing Assistant
- **Content Generation & Refinement**:
  - **Grammar & Spell Check**: Real-time or on-demand fixes.
  - **Rewrite Suggestions**: Rephrase sentences for better flow or clarity.
  - **Proofreading**: Comprehensive review of content.
  - **Style Matching**: AI analyzes user's writing style to maintain consistency.
  - **Dictation**: Speech-to-text integration for hands-free writing.
- **Creative Support**:
  - **Character Development**: Help build and flesh out characters.
  - **Plot Twists**: Generate ideas for plot progression and twists.
  - **Analysis**: Analyze chapters and provide specific recommendations.
  - **Engagement Enhancer**: Suggestions to make content more engaging.

### 3.4. Research Tools
- **Research Assistance**: AI helps research topics relevant to the book.
- **Note Taking**: Dedicated system for saving and organizing research notes.
- **Fact Checker**: AI verification of facts within the text.
- **Genre Statistics**: AI provides data and trends relevant to the chosen genre.

### 3.5. Progress Tracking & Gamification
- **Goal Setting**: Set daily, session, or book-level writing goals (word count, chapters).
- **Progress Tracking**: Visual indicators of progress towards goals.
- **Motivation**: Features to keep writing fun and maintain momentum (e.g., streaks, achievements).
- **Analytics**: Writing statistics analysis.

### 3.6. Publishing
- **Compilation**: Tools to compile the manuscript.
- **Publishing Support**: Assistance with formatting and preparing for publication.

## 4. User Flow Definitions
- **Initial Setup**: User inputs a rough idea -> AI suggests structure/metadata -> User confirms.
- **Writing Process**: User writes in distraction-free view -> AI provides sidebar/overlay assistance on request.
- **Review**: User requests analysis -> AI provides feedback on style, grammar, and plot.

## 5. Future Considerations
- Cloud sync/backup.
- Export to multiple formats (ePub, PDF, Docx).
