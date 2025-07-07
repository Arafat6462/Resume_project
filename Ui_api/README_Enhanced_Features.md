# 🎯 Enhanced Resume Skill Gap Analyzer

An intelligent web application that analyzes your resume, identifies skill gaps, and provides **real-time course recommendations** from multiple learning platforms using live web scraping.

## ✨ New Features

### 🔄 Live Course Scraping
- **Real-time course discovery** from FreeCodeCamp, W3Schools, MIT OpenCourseWare, Khan Academy, YouTube, and more
- **Dynamic content updates** - no more static course lists
- **Multi-platform aggregation** - get courses from diverse sources

### 📄 Resume Analysis
- **Upload your resume text** to identify skills you have vs. skills you're missing
- **Skill gap percentage calculation** 
- **Categorized missing skills** by technology areas
- **One-click course search** for any missing skill

### 🔍 Custom Skill Search
- **Search any skill or technology** (not just predefined ones)
- **Live scraping results** for cutting-edge technologies
- **Comprehensive course data** with platform, price, and type information

## 🚀 How to Use

### 1. Start the Application
```bash
cd /path/to/Resume_skill_gap
python skill_gap_api.py
```

### 2. Open Web Interface
Navigate to: **http://localhost:5000**

### 3. Three Ways to Find Courses

#### Option A: Resume Analysis (Recommended)
1. **Paste your resume text** in the "Resume Skill Gap Analysis" section
2. **Click "Analyze My Resume"** - the system will:
   - Extract skills from your resume
   - Identify missing skills from our database
   - Show skill gap percentage
   - Display missing skills by category
3. **Click any missing skill** to get live course recommendations

#### Option B: Quick Skill Selection
1. **Click on predefined skill cards** (Python, JavaScript, React, etc.)
2. **Choose your target level** (Beginner/Intermediate/Advanced)
3. **Click "Find Learning Resources"** to get live courses

#### Option C: Custom Search
1. **Enter any skill** in the custom skill field
2. **Click "Search Any Skill"** for pure course search
3. **Get live results** for any technology, even brand new ones

## 🌐 Live Scraping Sources

The system scrapes courses from:
- **FreeCodeCamp** - Free programming courses and articles
- **W3Schools** - Web development tutorials  
- **MIT OpenCourseWare** - University-level courses
- **Khan Academy** - Interactive programming courses
- **YouTube** - Video tutorials from top channels
- **Codecademy** - Free tier interactive courses

## 📊 What You Get

### Course Information
- **Title and Description**
- **Platform/Source**
- **Price** (Free/Paid)
- **Course Type** (Tutorial/Full Course/Interactive)
- **Direct Links** to access courses

### Resume Analysis Results
- **Skills Found** in your resume
- **Missing Skills** with counts
- **Skill Gap Percentage**
- **Categorized Skills** by technology area
- **Learning Priority** suggestions

## 🔧 API Endpoints

### Resume Analysis
```
POST /api/extract-skills
Body: { "resume_text": "your resume content..." }
```

### Live Course Search
```
POST /api/search-courses  
Body: { "search_term": "skill name" }
```

### Skill Gap Analysis with Live Courses
```
POST /api/analyze
Body: { "skill": "python", "level": "beginner" }
```

## 💡 Pro Tips

1. **For Resume Analysis**: Include your full resume text with job descriptions, skills sections, and project details for best results

2. **For Emerging Technologies**: Use the custom search for new frameworks, tools, or technologies not in predefined lists

3. **Course Quality**: Prioritize courses from FreeCodeCamp and MIT for structured learning, YouTube for quick tutorials

4. **Learning Path**: Start with "Beginner" level even if you have some experience to fill knowledge gaps

## 🎯 Perfect For

- **Job Seekers** identifying skill gaps for target positions
- **Developers** learning new technologies  
- **Students** finding comprehensive learning resources
- **Career Changers** transitioning to tech roles
- **Recruiters** understanding skill requirements and training options

## 🔍 Example Use Cases

### Scenario 1: Resume Gap Analysis
```
1. Paste resume → System finds you know: Python, SQL, Excel
2. System identifies missing: React, AWS, Docker, Kubernetes  
3. Click "React" → Get 15+ live React courses
4. Click "AWS" → Get current AWS training resources
```

### Scenario 2: Learning New Technology
```
1. Enter "Flutter" in custom search
2. Get live Flutter courses from multiple platforms
3. Choose free vs paid options
4. Access courses directly via provided links
```

### Scenario 3: Interview Preparation
```
1. Analyze resume for "Senior Developer" skills
2. Identify 10+ missing skills
3. Get targeted learning resources
4. Create learning plan based on priority
```

## 🚨 Important Notes

- **Live Scraping**: Course results are fetched in real-time, so the first search may take 10-30 seconds
- **Content Freshness**: You get the most current courses and tutorials available
- **Platform Respect**: Scraping includes delays to be respectful to learning platforms
- **Internet Required**: Live scraping requires active internet connection

## 🛠️ Technical Architecture

- **Frontend**: Modern HTML5/CSS3/JavaScript interface
- **Backend**: Flask API with CORS support
- **Scraping**: BeautifulSoup + Requests with respectful delays
- **Analysis**: Custom skill extraction and gap analysis algorithms
- **Data**: Dynamic course aggregation from multiple sources

## 📈 Benefits Over Static Course Lists

✅ **Always Current** - Get the latest courses and tutorials  
✅ **Comprehensive** - Multiple platforms in one search  
✅ **Personalized** - Based on your actual resume content  
✅ **Scalable** - Works for any skill, technology, or framework  
✅ **Actionable** - Direct links to start learning immediately  

---

**Ready to identify your skill gaps and find the perfect learning resources?**

Start the application and begin your personalized learning journey! 🚀
