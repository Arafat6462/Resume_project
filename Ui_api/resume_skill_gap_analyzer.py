import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin, urlparse
import random
import sys
import re
from typing import List, Dict, Optional

class ResumeSkillGapAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # Comprehensive skill database with levels and related skills
        self.skill_database = {
            # Programming Languages
            'python': {
                'category': 'Programming Languages',
                'related_skills': ['django', 'flask', 'pandas', 'numpy', 'machine learning'],
                'beginner_keywords': ['basics', 'fundamentals', 'introduction', 'getting started'],
                'intermediate_keywords': ['advanced', 'projects', 'web development', 'data science'],
                'advanced_keywords': ['expert', 'mastery', 'professional', 'architecture']
            },
            'javascript': {
                'category': 'Programming Languages',
                'related_skills': ['react', 'node.js', 'angular', 'vue.js', 'typescript'],
                'beginner_keywords': ['basics', 'fundamentals', 'introduction', 'getting started'],
                'intermediate_keywords': ['frameworks', 'async', 'promises', 'es6'],
                'advanced_keywords': ['performance', 'architecture', 'advanced patterns']
            },
            'java': {
                'category': 'Programming Languages',
                'related_skills': ['spring', 'hibernate', 'maven', 'gradle', 'android'],
                'beginner_keywords': ['basics', 'fundamentals', 'introduction', 'oop'],
                'intermediate_keywords': ['spring boot', 'web development', 'microservices'],
                'advanced_keywords': ['enterprise', 'architecture', 'performance']
            },
            
            # Web Technologies
            'react': {
                'category': 'Frontend Frameworks',
                'related_skills': ['javascript', 'redux', 'next.js', 'hooks', 'jsx'],
                'beginner_keywords': ['basics', 'fundamentals', 'introduction', 'components'],
                'intermediate_keywords': ['hooks', 'state management', 'routing'],
                'advanced_keywords': ['performance', 'testing', 'advanced patterns']
            },
            'node.js': {
                'category': 'Backend Technologies',
                'related_skills': ['express', 'mongodb', 'npm', 'api development'],
                'beginner_keywords': ['basics', 'fundamentals', 'introduction', 'getting started'],
                'intermediate_keywords': ['express', 'databases', 'apis', 'middleware'],
                'advanced_keywords': ['microservices', 'scalability', 'performance']
            },
            
            # Data & AI
            'machine learning': {
                'category': 'Data Science & AI',
                'related_skills': ['python', 'tensorflow', 'scikit-learn', 'pandas', 'statistics'],
                'beginner_keywords': ['basics', 'fundamentals', 'introduction', 'concepts'],
                'intermediate_keywords': ['algorithms', 'supervised learning', 'projects'],
                'advanced_keywords': ['deep learning', 'neural networks', 'production']
            },
            'data science': {
                'category': 'Data Science & AI',
                'related_skills': ['python', 'pandas', 'numpy', 'matplotlib', 'sql'],
                'beginner_keywords': ['basics', 'fundamentals', 'introduction', 'analysis'],
                'intermediate_keywords': ['visualization', 'statistics', 'projects'],
                'advanced_keywords': ['advanced analytics', 'big data', 'production']
            },
            
            # Cloud & DevOps
            'aws': {
                'category': 'Cloud & DevOps',
                'related_skills': ['docker', 'kubernetes', 'terraform', 'lambda'],
                'beginner_keywords': ['basics', 'fundamentals', 'introduction', 'cloud'],
                'intermediate_keywords': ['ec2', 's3', 'deployment', 'services'],
                'advanced_keywords': ['architecture', 'enterprise', 'certification']
            },
            'docker': {
                'category': 'DevOps',
                'related_skills': ['kubernetes', 'containerization', 'deployment'],
                'beginner_keywords': ['basics', 'fundamentals', 'introduction', 'containers'],
                'intermediate_keywords': ['compose', 'deployment', 'orchestration'],
                'advanced_keywords': ['production', 'optimization', 'security']
            }
        }
    
    def add_delay(self):
        """Add random delay to be respectful to servers"""
        time.sleep(random.uniform(1, 3))
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract potential skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skill_database.keys():
            if skill in text_lower:
                found_skills.append(skill)
        
        # Also check for variations and related terms
        skill_variations = {
            'js': 'javascript',
            'py': 'python',
            'ml': 'machine learning',
            'ai': 'machine learning',
            'react.js': 'react',
            'nodejs': 'node.js',
            'node':'node.js'
        }
        
        for variation, standard_skill in skill_variations.items():
            if variation in text_lower and standard_skill not in found_skills:
                found_skills.append(standard_skill)
        
        return found_skills
    
    def get_skill_level_courses(self, skill: str, target_level: str = 'beginner') -> List[Dict]:
        """Get courses for a specific skill and level"""
        skill_lower = skill.lower()
        
        # Get topic keywords based on skill level
        if skill_lower in self.skill_database:
            skill_info = self.skill_database[skill_lower]
            level_keywords = skill_info.get(f'{target_level}_keywords', [])
        else:
            level_keywords = ['basics', 'fundamentals'] if target_level == 'beginner' else ['advanced']
        
        courses = []
        
        # Scrape courses for the skill
        courses.extend(self._scrape_freecodecamp_for_skill(skill, level_keywords))
        courses.extend(self._scrape_w3schools_for_skill(skill))
        courses.extend(self._scrape_youtube_for_skill(skill, target_level))
        courses.extend(self._get_recommended_courses_for_skill(skill, target_level))
        
        # Sort courses by relevance to level
        courses = self._rank_courses_by_level(courses, target_level, level_keywords)
        
        return courses[:10]  # Return top 10 most relevant courses
    
    def _scrape_freecodecamp_for_skill(self, skill: str, level_keywords: List[str]) -> List[Dict]:
        """Scrape FreeCodeCamp for skill-specific content"""
        courses = []
        
        try:
            url = f"https://www.freecodecamp.org/news/tag/{skill.replace(' ', '-')}/"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.find_all('article', class_='post-card')
                
                for article in articles[:8]:
                    title_elem = article.find('h2', class_='post-card-title')
                    link_elem = article.find('a', class_='post-card-image-link')
                    excerpt_elem = article.find('p', class_='post-card-excerpt')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        relative_url = link_elem['href'] if link_elem else ''
                        absolute_url = urljoin("https://www.freecodecamp.org", relative_url)
                        
                        # Calculate relevance score
                        relevance_score = self._calculate_relevance_score(title, level_keywords)
                        
                        courses.append({
                            'platform': 'FreeCodeCamp',
                            'title': title,
                            'url': absolute_url,
                            'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                            'type': 'Article/Tutorial',
                            'price': 'Free',
                            'skill': skill,
                            'relevance_score': relevance_score,
                            'estimated_time': self._estimate_reading_time(title)
                        })
            
            self.add_delay()
            
        except Exception as e:
            print(f"❌ Error scraping FreeCodeCamp for {skill}: {e}")
        
        return courses
    
    def _scrape_w3schools_for_skill(self, skill: str) -> List[Dict]:
        """Scrape W3Schools for skill tutorials"""
        courses = []
        
        try:
            skill_urls = {
                'python': 'https://www.w3schools.com/python/',
                'javascript': 'https://www.w3schools.com/js/',
                'html': 'https://www.w3schools.com/html/',
                'css': 'https://www.w3schools.com/css/',
                'sql': 'https://www.w3schools.com/sql/',
                'react': 'https://www.w3schools.com/react/',
            }
            
            url = skill_urls.get(skill.lower())
            if not url:
                return courses
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                courses.append({
                    'platform': 'W3Schools',
                    'title': f'{skill.title()} Tutorial - Complete Course',
                    'url': url,
                    'description': f'Complete {skill.title()} tutorial from basics to advanced',
                    'type': 'Full Tutorial Series',
                    'price': 'Free',
                    'skill': skill,
                    'relevance_score': 95,  # W3Schools is highly relevant for web skills
                    'estimated_time': '15-20 hours'
                })
            
            self.add_delay()
            
        except Exception as e:
            print(f"❌ Error scraping W3Schools for {skill}: {e}")
        
        return courses
    
    def _scrape_youtube_for_skill(self, skill: str, level: str) -> List[Dict]:
        """Get curated YouTube channels for specific skills"""
        youtube_courses = []
        
        skill_channels = {
            'python': [
                {
                    'title': f'Python for Everybody - Dr. Chuck ({level})',
                    'url': 'https://www.youtube.com/user/csev',
                    'description': 'Complete Python course by University of Michigan',
                    'estimated_time': '40+ hours'
                },
                {
                    'title': f'Corey Schafer - Python Tutorials ({level})',
                    'url': 'https://www.youtube.com/user/schafer5',
                    'description': 'Excellent Python tutorials and projects',
                    'estimated_time': '20+ hours'
                }
            ],
            'javascript': [
                {
                    'title': f'JavaScript Mastery ({level})',
                    'url': 'https://www.youtube.com/c/JavaScriptMastery',
                    'description': 'Complete JavaScript and React tutorials',
                    'estimated_time': '30+ hours'
                }
            ],
            'react': [
                {
                    'title': f'React - The Complete Guide ({level})',
                    'url': 'https://www.youtube.com/c/academind',
                    'description': 'Complete React course with projects',
                    'estimated_time': '25+ hours'
                }
            ],
            'machine learning': [
                {
                    'title': f'Machine Learning Course - Andrew Ng ({level})',
                    'url': 'https://www.youtube.com/watch?v=PPLop4L2eGk',
                    'description': 'Stanford CS229 Machine Learning Course',
                    'estimated_time': '60+ hours'
                }
            ]
        }
        
        channels = skill_channels.get(skill.lower(), [])
        
        for channel in channels:
            youtube_courses.append({
                'platform': 'YouTube',
                'title': channel['title'],
                'url': channel['url'],
                'description': channel['description'],
                'type': 'Video Course',
                'price': 'Free',
                'skill': skill,
                'relevance_score': 90,
                'estimated_time': channel['estimated_time']
            })
        
        return youtube_courses
    
    def _get_recommended_courses_for_skill(self, skill: str, level: str) -> List[Dict]:
        """Get hand-curated recommended courses for specific skills"""
        recommended_courses = {
            'python': [
                {
                    'platform': 'edX',
                    'title': 'Introduction to Computer Science and Programming Using Python (MIT)',
                    'url': 'https://www.edx.org/course/introduction-to-computer-science-and-programming-7',
                    'description': 'MIT\'s introduction to computer science using Python',
                    'type': 'University Course',
                    'price': 'Free (Certificate: $99)',
                    'estimated_time': '9 weeks, 14-16 hours/week'
                }
            ],
            'machine learning': [
                {
                    'platform': 'Coursera',
                    'title': 'Machine Learning Course by Andrew Ng',
                    'url': 'https://www.coursera.org/learn/machine-learning',
                    'description': 'The most popular machine learning course online',
                    'type': 'University Course',
                    'price': 'Free (Certificate: $49/month)',
                    'estimated_time': '11 weeks, 5-7 hours/week'
                }
            ],
            'react': [
                {
                    'platform': 'React Official',
                    'title': 'React Official Tutorial',
                    'url': 'https://reactjs.org/tutorial/tutorial.html',
                    'description': 'Official React tutorial from the React team',
                    'type': 'Official Documentation',
                    'price': 'Free',
                    'estimated_time': '2-4 hours'
                }
            ]
        }
        
        courses = recommended_courses.get(skill.lower(), [])
        
        for course in courses:
            course.update({
                'skill': skill,
                'relevance_score': 100  # Recommended courses get highest score
            })
        
        return courses
    
    def _calculate_relevance_score(self, title: str, level_keywords: List[str]) -> int:
        """Calculate relevance score based on title and level keywords"""
        title_lower = title.lower()
        score = 50  # Base score
        
        # Boost score for level-specific keywords
        for keyword in level_keywords:
            if keyword in title_lower:
                score += 15
        
        # Boost for comprehensive content indicators
        comprehensive_indicators = ['complete', 'full', 'comprehensive', 'course', 'tutorial', 'guide']
        for indicator in comprehensive_indicators:
            if indicator in title_lower:
                score += 10
        
        # Boost for project-based learning
        project_indicators = ['project', 'build', 'create', 'develop']
        for indicator in project_indicators:
            if indicator in title_lower:
                score += 10
        
        return min(score, 100)  # Cap at 100
    
    def _estimate_reading_time(self, title: str) -> str:
        """Estimate time based on content type"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['complete', 'comprehensive', 'full course']):
            return '10-20 hours'
        elif any(word in title_lower for word in ['tutorial', 'guide']):
            return '2-5 hours'
        elif any(word in title_lower for word in ['introduction', 'basics']):
            return '1-3 hours'
        else:
            return '30 minutes - 2 hours'
    
    def _rank_courses_by_level(self, courses: List[Dict], level: str, level_keywords: List[str]) -> List[Dict]:
        """Rank courses by relevance to the target level"""
        return sorted(courses, key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    def analyze_skill_gap(self, missing_skill: str, target_level: str = 'beginner') -> Dict:
        """Analyze a specific skill gap and provide learning recommendations"""
        print(f"\n🎯 Analyzing skill gap: {missing_skill.upper()} ({target_level} level)")
        print("="*60)
        
        # Get courses for the skill
        courses = self.get_skill_level_courses(missing_skill, target_level)
        
        # Get skill information
        skill_info = self.skill_database.get(missing_skill.lower(), {})
        related_skills = skill_info.get('related_skills', [])
        category = skill_info.get('category', 'General')
        
        # Create learning plan
        learning_plan = {
            'skill': missing_skill,
            'level': target_level,
            'category': category,
            'total_courses': len(courses),
            'estimated_total_time': self._calculate_total_time(courses),
            'related_skills': related_skills,
            'recommended_courses': courses,
            'learning_path': self._create_learning_path(courses, target_level)
        }
        
        return learning_plan
    
    def _calculate_total_time(self, courses: List[Dict]) -> str:
        """Calculate estimated total learning time"""
        # Simple estimation - this could be made more sophisticated
        return f"{len(courses) * 3}-{len(courses) * 8} hours"
    
    def _create_learning_path(self, courses: List[Dict], level: str) -> List[str]:
        """Create a suggested learning path"""
        if level == 'beginner':
            return [
                "1. Start with fundamentals and basic concepts",
                "2. Follow official tutorials or documentation",
                "3. Complete hands-on projects",
                "4. Practice with coding exercises",
                "5. Build a portfolio project"
            ]
        elif level == 'intermediate':
            return [
                "1. Review advanced concepts and best practices",
                "2. Study framework-specific patterns",
                "3. Build complex projects",
                "4. Learn testing and deployment",
                "5. Contribute to open source projects"
            ]
        else:  # advanced
            return [
                "1. Master architecture and design patterns",
                "2. Study performance optimization",
                "3. Learn advanced tooling and workflows",
                "4. Mentor others and teach",
                "5. Lead technical projects"
            ]
    
    def display_learning_plan(self, learning_plan: Dict):
        """Display the learning plan in a formatted way"""
        print(f"\n📚 LEARNING PLAN FOR {learning_plan['skill'].upper()}")
        print("="*60)
        print(f"🎯 Target Level: {learning_plan['level'].title()}")
        print(f"📂 Category: {learning_plan['category']}")
        print(f"⏱️  Estimated Time: {learning_plan['estimated_total_time']}")
        print(f"📖 Total Courses Found: {learning_plan['total_courses']}")
        
        if learning_plan['related_skills']:
            print(f"🔗 Related Skills: {', '.join(learning_plan['related_skills'])}")
        
        print(f"\n📋 RECOMMENDED LEARNING PATH:")
        for step in learning_plan['learning_path']:
            print(f"   {step}")
        
        print(f"\n🏆 TOP RECOMMENDED COURSES:")
        print("-" * 60)
        
        for i, course in enumerate(learning_plan['recommended_courses'][:5], 1):
            print(f"{i:2d}. {course['title']}")
            print(f"     🏢 Platform: {course['platform']}")
            print(f"     🔗 URL: {course['url']}")
            print(f"     📝 {course['description']}")
            print(f"     💰 Price: {course['price']}")
            print(f"     ⏱️  Time: {course.get('estimated_time', 'Not specified')}")
            print(f"     ⭐ Relevance: {course.get('relevance_score', 'N/A')}/100")
            print()
    
    def save_learning_plan(self, learning_plan: Dict, filename: str = None):
        """Save learning plan to JSON file"""
        if filename is None:
            skill_name = learning_plan['skill'].replace(' ', '_')
            filename = f"{skill_name}_learning_plan.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(learning_plan, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Learning plan saved to {filename}")

def main():
    analyzer = ResumeSkillGapAnalyzer()
    
    print("🎯 RESUME SKILL GAP ANALYZER")
    print("="*40)
    print("This tool helps you find learning resources for skills missing from your resume.")
    print()
    
    # Get skill and level from user
    if len(sys.argv) >= 2:
        missing_skill = sys.argv[1]
        target_level = sys.argv[2] if len(sys.argv) >= 3 else 'beginner'
    else:
        missing_skill = input("Enter the skill you want to learn: ").strip()
        target_level = input("Enter target level (beginner/intermediate/advanced) [beginner]: ").strip() or 'beginner'
    
    if not missing_skill:
        print("❌ No skill specified. Exiting...")
        return
    
    # Validate level
    if target_level not in ['beginner', 'intermediate', 'advanced']:
        print(f"❌ Invalid level '{target_level}'. Using 'beginner' instead.")
        target_level = 'beginner'
    
    # Analyze the skill gap
    learning_plan = analyzer.analyze_skill_gap(missing_skill, target_level)
    
    # Display the results
    analyzer.display_learning_plan(learning_plan)
    
    # Save the plan
    analyzer.save_learning_plan(learning_plan)
    
    print(f"\n✅ Analysis complete! Learning plan created for {missing_skill}")

if __name__ == "__main__":
    main()
