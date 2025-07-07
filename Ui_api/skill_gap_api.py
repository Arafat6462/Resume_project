from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our analyzer and scraper
from resume_skill_gap_analyzer import ResumeSkillGapAnalyzer
from universal_course_scraper import CourseScraper

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the analyzer
analyzer = ResumeSkillGapAnalyzer()

@app.route('/')
def index():
    """Serve the HTML interface"""
    try:
        with open('skill_gap_web_interface.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return jsonify({'error': 'Web interface not found'}), 404

@app.route('/api/analyze', methods=['POST'])
def analyze_skill():
    """API endpoint to analyze a skill gap and fetch real-time courses"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        skill = data.get('skill', '').strip()
        level = data.get('level', 'beginner').strip()
        
        if not skill:
            return jsonify({'error': 'Skill is required'}), 400
        
        if level not in ['beginner', 'intermediate', 'advanced']:
            level = 'beginner'
        
        print(f"🔍 Analyzing skill gap for: {skill} (Level: {level})")
        
        # Get basic learning plan from analyzer
        learning_plan = analyzer.analyze_skill_gap(skill, level)
        
        # Scrape real-time courses for this skill
        print(f"🌐 Scraping courses for: {skill}")
        scraper = CourseScraper(skill)
        courses = scraper.scrape_all_courses()
        
        # Enhance learning plan with real-time courses
        enhanced_plan = {
            'skill': skill,
            'level': level,
            'basic_plan': learning_plan,
            'live_courses': courses,
            'total_courses_found': len(courses),
            'platforms': list(set([course['platform'] for course in courses])),
            'course_summary': {
                platform: len([c for c in courses if c['platform'] == platform])
                for platform in set([course['platform'] for course in courses])
            }
        }
        
        return jsonify({
            'success': True,
            'learning_plan': enhanced_plan
        })
        
    except Exception as e:
        print(f"❌ Error analyzing skill: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/skills', methods=['GET'])
def get_available_skills():
    """Get list of available skills in the database"""
    try:
        skills = []
        for skill, info in analyzer.skill_database.items():
            skills.append({
                'name': skill,
                'category': info.get('category', 'General'),
                'related_skills': info.get('related_skills', [])
            })
        
        return jsonify({
            'success': True,
            'skills': skills
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/extract-skills', methods=['POST'])
def extract_skills_from_resume():
    """Extract skills from resume text and identify skill gaps"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        resume_text = data.get('resume_text', '').strip()
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        
        print(f"📄 Analyzing resume text...")
        
        # Extract skills from resume
        found_skills = analyzer.extract_skills_from_text(resume_text)
        
        # Get all available skills for comparison
        all_skills = list(analyzer.skill_database.keys())
        
        # Find missing skills (skills in database but not in resume)
        missing_skills = [skill for skill in all_skills if skill not in found_skills]
        
        # Categorize missing skills by importance/category
        categorized_missing = {}
        for skill in missing_skills:
            skill_info = analyzer.skill_database.get(skill, {})
            category = skill_info.get('category', 'General')
            if category not in categorized_missing:
                categorized_missing[category] = []
            categorized_missing[category].append({
                'name': skill,
                'category': category,
                'related_skills': skill_info.get('related_skills', []),
                'importance': skill_info.get('importance', 'medium')
            })
        
        return jsonify({
            'success': True,
            'found_skills': found_skills,
            'missing_skills': missing_skills,
            'categorized_missing_skills': categorized_missing,
            'total_skills_in_database': len(all_skills),
            'skill_gap_percentage': round((len(missing_skills) / len(all_skills)) * 100, 1),
            'skills_found_count': len(found_skills),
            'skills_missing_count': len(missing_skills)
        })
        
    except Exception as e:
        print(f"❌ Error extracting skills: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search-courses', methods=['POST'])
def search_courses():
    """Search for courses on any custom skill/topic"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        search_term = data.get('search_term', '').strip()
        
        if not search_term:
            return jsonify({'error': 'Search term is required'}), 400
        
        print(f"🔍 Custom search for courses: {search_term}")
        
        # Use the scraper to find courses
        scraper = CourseScraper(search_term)
        courses = scraper.scrape_all_courses()
        
        # Organize results
        platforms = {}
        for course in courses:
            platform = course['platform']
            if platform not in platforms:
                platforms[platform] = []
            platforms[platform].append(course)
        
        return jsonify({
            'success': True,
            'search_term': search_term,
            'courses': courses,
            'total_courses': len(courses),
            'platforms': list(platforms.keys()),
            'courses_by_platform': platforms,
            'course_summary': {
                platform: len(platform_courses) 
                for platform, platform_courses in platforms.items()
            }
        })
        
    except Exception as e:
        print(f"❌ Error searching courses: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Resume Skill Gap Analyzer'})

if __name__ == '__main__':
    print("🚀 Starting Enhanced Resume Skill Gap Analyzer API...")
    print("📝 Access the web interface at: http://localhost:5000")
    print("🔧 API endpoints:")
    print("   - POST /api/analyze - Analyze skill gap with live courses")
    print("   - GET /api/skills - Get available skills")
    print("   - POST /api/extract-skills - Extract skills from resume text")
    print("   - POST /api/search-courses - Search courses for any skill")
    print("   - GET /health - Health check")
    print("\n🌐 Features:")
    print("   ✅ Real-time course scraping")
    print("   ✅ Resume skill gap analysis")
    print("   ✅ Custom skill search")
    print("   ✅ Multiple learning platforms")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
