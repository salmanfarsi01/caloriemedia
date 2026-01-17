# 🥑 CalorieMedia - AI-Powered Social Nutrition Platform

**CalorieMedia** is a social media application built with **Django** designed to help users track their nutrition journey. Users can post pictures of their meals, receive instant feedback from an **AI Nutritionist**, and interact with a community of fitness enthusiasts.

> 🎓 **Educational Purpose:** This project was developed to master **Basic Backend Logic** using the Django Framework, focusing on CRUD operations, User Authentication, Database Relationships, and API Integration.

---

## Key Features

### User Authentication & Profile
*   **Secure Auth:** Register, Login, and Logout using Django's built-in authentication system.
*   **Profile Management:** Users can update their unique username, physical stats (Age, Weight, Height), and set a fitness goal (Lose Weight/Gain Muscle).
*   **Profile Pictures:** Support for uploading and updating profile avatars.

###Social Feed (CRUD Operations)
*   **Create:** Users can post text updates and upload food images.
*   **Read:** A dynamic home feed displaying posts from all users ordered by date.
*   **Update:** Edit existing posts via a dropdown menu.
*   **Delete:** Remove posts permanently.
*   **Interact:** Like posts (AJAX-based, no page reload) and Repost content to your own feed.

### AI Integration (Groq API)
*   **Auto-Commenter:** When a user posts a meal, the AI analyzes the food based on the user's specific goal (Diet vs. Gain) and posts a helpful, human-like comment automatically.
*   **Fitness Chatbot:** A floating chat widget allowing users to ask fitness questions to a "Gym Buddy" AI in real-time.

---

## Tech Stack

*   **Backend:** Python, Django 5.x
*   **Frontend:** HTML5, CSS3, Bootstrap 5 (Responsive Design)
*   **Database:** SQLite (Default Django DB)
*   **AI Service:** Groq API (Model: Llama-3.3-70b-versatile)
*   **Scripting:** JavaScript (For AJAX Likes & Chatbot)

---

## What I Learned (Backend Logic)

This project was built step-by-step to understand the core concepts of Django:

1.  **MTV Architecture:** Learned how Models, Templates, and Views interact to serve a web page.
2.  **Database Modeling:** Created relationships like `OneToOne` (User ↔ Profile) and `ForeignKey` (Post ↔ User).
3.  **Media Handling:** Configured `MEDIA_ROOT` and `enctype="multipart/form-data"` to handle image uploads securely.
4.  **Signals:** Used Django Signals (`post_save`) to automatically create a Profile whenever a new User registers.
5.  **Decorators:** Implemented `@login_required` to protect routes.
6.  **Asynchronous Requests:** Used JavaScript `fetch()` API to make the **Like** button update instantly without refreshing the page.
7.  **Environment Variables:** Learned to secure API keys using `.env` files.

---

## Installation Guide

Follow these steps to run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/caloriemedia.git
cd caloriemedia
