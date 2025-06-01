OVERVIEW :
This is a Career Guidance System that helps students get personalized career recommendation based on their profile 
in the indian education system

Features :  
Student Profile management   
Career recommendation generation  
Basic recommendations based on student profile  
Education Stream information  

Tech Stack Used :  
Framework : spring boot   
Language : Java  
Build Tool : Maven  

**API Endpoints**  
Student Profile Management

POST /api/career/profile - Create a new student profile

GET /api/career/profile/{id} - Get a student profile by ID

GET /api/career/profiles - Get all student profiles

PUT /api/career/profile/{id} - Update a student profile

DELETE /api/career/profile/{id} - Delete a student profile

**Career Recommendations**   
POST /api/career/recommendations/{studentId} - Generate career recommendations (async)

GET /api/career/recommendations/basic/{studentId} - Get basic recommendations

**Education Streams**  
GET /api/career/streams - Get all education streams

GET /api/career/streams/level/{level} - Get streams by education level

GET /api/career/exams/{streamName} - Get common exams for a stream

**How to Run**
1. Clone the repository
   
   git clone <repository-url>
2. Build the project 
3. Run the Application 