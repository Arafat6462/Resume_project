import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin, urlparse
import random
import sys

class CourseScraper:
    def __init__(self, topic="python"):
        self.topic = topic.lower()
        self.topic_display = topic.title()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.all_courses = []
        
        # Topic-specific keywords for better filtering
        self.topic_keywords = self._get_topic_keywords()
    
    def _get_topic_keywords(self):
        """Generate topic-specific keywords for better filtering"""
        common_keywords = [self.topic, self.topic_display]
        
        # Add specific keywords based on topic
        topic_lower = self.topic.lower()
        if topic_lower in ['python', 'py']:
            return common_keywords + ['programming', 'coding', 'development', 'script']
        elif topic_lower in ['javascript', 'js']:
            return common_keywords + ['web development', 'frontend', 'backend', 'node']
        elif topic_lower in ['java']:
            return common_keywords + ['programming', 'object-oriented', 'development']
        elif topic_lower in ['data science', 'data']:
            return common_keywords + ['analytics', 'machine learning', 'statistics']
        elif topic_lower in ['web development', 'web']:
            return common_keywords + ['html', 'css', 'frontend', 'backend']
        elif topic_lower in ['machine learning', 'ml', 'ai']:
            return common_keywords + ['artificial intelligence', 'deep learning', 'neural networks']
        else:
            return common_keywords + ['course', 'tutorial', 'learning']
    
    def add_delay(self):
        """Add random delay to be respectful to servers"""
        time.sleep(random.uniform(1, 3))
    
    def scrape_freecodecamp(self):
        """Scrape FreeCodeCamp articles and tutorials for the specified topic"""
        print(f"🔍 Scraping FreeCodeCamp {self.topic_display} content...")
        courses = []
        
        try:
            # Topic tag page
            url = f"https://www.freecodecamp.org/news/tag/{self.topic}/"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.find_all('article', class_='post-card')
                
                for article in articles[:15]:  # Get more articles
                    title_elem = article.find('h2', class_='post-card-title')
                    link_elem = article.find('a', class_='post-card-image-link')
                    excerpt_elem = article.find('p', class_='post-card-excerpt')
                    
                    if title_elem:
                        # Get the URL and make it absolute
                        relative_url = link_elem['href'] if link_elem else ''
                        absolute_url = urljoin("https://www.freecodecamp.org", relative_url) if relative_url else ''
                        
                        courses.append({
                            'platform': 'FreeCodeCamp',
                            'title': title_elem.get_text(strip=True),
                            'url': absolute_url,
                            'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                            'type': 'Article/Tutorial',
                            'price': 'Free'
                        })
            
            # Also check for main course based on topic
            if self.topic == 'python':
                main_course_url = "https://www.freecodecamp.org/learn/scientific-computing-with-python/"
                courses.append({
                    'platform': 'FreeCodeCamp',
                    'title': 'Scientific Computing with Python',
                    'url': main_course_url,
                    'description': 'Complete Python certification course with projects',
                    'type': 'Full Course',
                    'price': 'Free'
                })
            elif self.topic in ['javascript', 'js']:
                main_course_url = "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/"
                courses.append({
                    'platform': 'FreeCodeCamp',
                    'title': 'JavaScript Algorithms and Data Structures',
                    'url': main_course_url,
                    'description': 'Complete JavaScript certification course',
                    'type': 'Full Course',
                    'price': 'Free'
                })
            elif 'web' in self.topic:
                main_course_url = "https://www.freecodecamp.org/learn/responsive-web-design/"
                courses.append({
                    'platform': 'FreeCodeCamp',
                    'title': 'Responsive Web Design',
                    'url': main_course_url,
                    'description': 'Complete web design certification course',
                    'type': 'Full Course',
                    'price': 'Free'
                })
            
            print(f"✅ Found {len(courses)} FreeCodeCamp {self.topic_display} resources")
            
        except Exception as e:
            print(f"❌ Error scraping FreeCodeCamp: {e}")
        
        self.add_delay()
        return courses
    
    def scrape_w3schools(self):
        """Scrape W3Schools tutorials for the specified topic"""
        print(f"🔍 Scraping W3Schools {self.topic_display} tutorials...")
        courses = []
        
        try:
            # Map topics to W3Schools URLs
            topic_urls = {
                'python': 'https://www.w3schools.com/python/',
                'javascript': 'https://www.w3schools.com/js/',
                'js': 'https://www.w3schools.com/js/',
                'java': 'https://www.w3schools.com/java/',
                'html': 'https://www.w3schools.com/html/',
                'css': 'https://www.w3schools.com/css/',
                'sql': 'https://www.w3schools.com/sql/',
                'php': 'https://www.w3schools.com/php/',
                'react': 'https://www.w3schools.com/react/',
                'node': 'https://www.w3schools.com/nodejs/',
                'web': 'https://www.w3schools.com/html/',
            }
            
            url = topic_urls.get(self.topic, f'https://www.w3schools.com/{self.topic}/')
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Get tutorial sections from sidebar
                sidebar = soup.find('div', id='leftmenuinnerinner')
                if sidebar:
                    links = sidebar.find_all('a', href=True)
                    
                    for link in links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        if f'/{self.topic}/' in href and text and len(text) > 2:
                            full_url = urljoin("https://www.w3schools.com", href)
                            courses.append({
                                'platform': 'W3Schools',
                                'title': f"{self.topic_display} {text}",
                                'url': full_url,
                                'description': f"Learn {text} in {self.topic_display}",
                                'type': 'Tutorial',
                                'price': 'Free'
                            })
                
                # Add main course
                courses.insert(0, {
                    'platform': 'W3Schools',
                    'title': f'{self.topic_display} Tutorial - Complete Course',
                    'url': url,
                    'description': f'Complete {self.topic_display} tutorial from basics to advanced',
                    'type': 'Full Tutorial Series',
                    'price': 'Free'
                })
            
            print(f"✅ Found {len(courses)} W3Schools {self.topic_display} tutorials")
            
        except Exception as e:
            print(f"❌ Error scraping W3Schools: {e}")
        
        self.add_delay()
        return courses
    
    def scrape_mit_courses(self):
        """Scrape MIT OpenCourseWare courses related to the specified topic"""
        print(f"🔍 Scraping MIT OpenCourseWare {self.topic_display} courses...")
        courses = []
        
        try:
            # Search for topic-related courses
            search_terms = [self.topic] + self.topic_keywords[:3]  # Use topic and some keywords
            
            for term in search_terms:
                url = f"https://ocw.mit.edu/search/?q={term}"
                response = requests.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for course cards
                    course_cards = soup.find_all('div', class_='course-card')
                    
                    for card in course_cards:
                        title_elem = card.find('h3')
                        link_elem = card.find('a')
                        desc_elem = card.find('p')
                        
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            # Only include if it's topic-related
                            if any(keyword.lower() in title.lower() for keyword in self.topic_keywords):
                                courses.append({
                                    'platform': 'MIT OpenCourseWare',
                                    'title': title,
                                    'url': urljoin("https://ocw.mit.edu", link_elem['href']) if link_elem else '',
                                    'description': desc_elem.get_text(strip=True) if desc_elem else '',
                                    'type': 'University Course',
                                    'price': 'Free'
                                })
                
                self.add_delay()
            
            print(f"✅ Found {len(courses)} MIT {self.topic_display} courses")
            
        except Exception as e:
            print(f"❌ Error scraping MIT: {e}")
        
        return courses
    
    def scrape_khan_academy(self):
        """Scrape Khan Academy courses for the specified topic"""
        print(f"🔍 Scraping Khan Academy {self.topic_display} courses...")
        courses = []
        
        try:
            # Khan Academy course sections
            base_urls = [
                "https://www.khanacademy.org/computing/computer-programming",
                "https://www.khanacademy.org/computing/computer-science"
            ]
            
            # Add topic-specific URLs
            if self.topic in ['python', 'programming']:
                base_urls.append("https://www.khanacademy.org/computing/intro-to-programming")
            elif self.topic in ['javascript', 'js']:
                base_urls.append("https://www.khanacademy.org/computing/computer-programming/programming")
            elif 'math' in self.topic or 'calculus' in self.topic:
                base_urls = ["https://www.khanacademy.org/math"]
            
            for url in base_urls:
                response = requests.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for course links
                    course_links = soup.find_all('a', href=True)
                    
                    for link in course_links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        if any(keyword.lower() in text.lower() for keyword in self.topic_keywords) and len(text) > 10:
                            courses.append({
                                'platform': 'Khan Academy',
                                'title': text,
                                'url': urljoin("https://www.khanacademy.org", href),
                                'description': 'Interactive programming course',
                                'type': 'Interactive Course',
                                'price': 'Free'
                            })
                
                self.add_delay()
            
            # Add known Khan Academy courses based on topic
            if self.topic in ['python', 'programming']:
                courses.extend([
                    {
                        'platform': 'Khan Academy',
                        'title': 'Intro to Programming: Drawing & Animation',
                        'url': 'https://www.khanacademy.org/computing/computer-programming/programming',
                        'description': 'Learn programming fundamentals with JavaScript',
                        'type': 'Interactive Course',
                        'price': 'Free'
                    },
                    {
                        'platform': 'Khan Academy',
                        'title': 'Computer Science Principles',
                        'url': 'https://www.khanacademy.org/computing/computer-science-principles',
                        'description': 'Foundational computer science concepts',
                        'type': 'Full Course',
                        'price': 'Free'
                    }
                ])
            elif self.topic in ['javascript', 'js', 'web']:
                courses.extend([
                    {
                        'platform': 'Khan Academy',
                        'title': 'Intro to Programming: Drawing & Animation',
                        'url': 'https://www.khanacademy.org/computing/computer-programming/programming',
                        'description': 'Learn programming fundamentals with JavaScript',
                        'type': 'Interactive Course',
                        'price': 'Free'
                    }
                ])
            
            print(f"✅ Found {len(courses)} Khan Academy {self.topic_display} courses")
            
        except Exception as e:
            print(f"❌ Error scraping Khan Academy: {e}")
        
        return courses
    
    def scrape_codecademy_free(self):
        """Add known Codecademy free content for the specified topic"""
        print(f"🔍 Checking Codecademy free {self.topic_display} content...")
        courses = []
        
        # Add known free Codecademy courses based on topic
        if self.topic in ['python']:
            courses.extend([
                {
                    'platform': 'Codecademy',
                    'title': 'Learn Python 3 (Free Tier)',
                    'url': 'https://www.codecademy.com/learn/learn-python-3',
                    'description': 'Interactive Python course with exercises',
                    'type': 'Interactive Course',
                    'price': 'Free (Limited)'
                },
                {
                    'platform': 'Codecademy',
                    'title': 'Python Fundamentals',
                    'url': 'https://www.codecademy.com/courses/learn-python-3',
                    'description': 'Basic Python syntax and concepts',
                    'type': 'Course Module',
                    'price': 'Free (Limited)'
                }
            ])
        elif self.topic in ['javascript', 'js']:
            courses.extend([
                {
                    'platform': 'Codecademy',
                    'title': 'Learn JavaScript (Free Tier)',
                    'url': 'https://www.codecademy.com/learn/introduction-to-javascript',
                    'description': 'Interactive JavaScript course with exercises',
                    'type': 'Interactive Course',
                    'price': 'Free (Limited)'
                }
            ])
        elif self.topic in ['html', 'web']:
            courses.extend([
                {
                    'platform': 'Codecademy',
                    'title': 'Learn HTML (Free)',
                    'url': 'https://www.codecademy.com/learn/learn-html',
                    'description': 'Basic HTML course',
                    'type': 'Interactive Course',
                    'price': 'Free (Limited)'
                }
            ])
        
        print(f"✅ Added {len(courses)} Codecademy free {self.topic_display} courses")
        return courses
    
    def get_youtube_channels(self):
        """List popular YouTube channels for the specified topic (manual curation)"""
        print(f"📺 Adding popular YouTube {self.topic_display} channels...")
        
        youtube_channels = []
        
        if self.topic in ['python']:
            youtube_channels = [
                {
                    'platform': 'YouTube',
                    'title': 'Python for Everybody - Dr. Chuck',
                    'url': 'https://www.youtube.com/user/csev',
                    'description': 'Complete Python course by University of Michigan',
                    'type': 'Video Course',
                    'price': 'Free'
                },
                {
                    'platform': 'YouTube',
                    'title': 'Corey Schafer - Python Tutorials',
                    'url': 'https://www.youtube.com/user/schafer5',
                    'description': 'Excellent Python tutorials and projects',
                    'type': 'Video Tutorials',
                    'price': 'Free'
                },
                {
                    'platform': 'YouTube',
                    'title': 'Programming with Mosh - Python',
                    'url': 'https://www.youtube.com/c/programmingwithmosh',
                    'description': 'Python tutorials for beginners',
                    'type': 'Video Course',
                    'price': 'Free'
                },
                {
                    'platform': 'YouTube',
                    'title': 'Real Python',
                    'url': 'https://www.youtube.com/c/realpython',
                    'description': 'Advanced Python concepts and best practices',
                    'type': 'Video Tutorials',
                    'price': 'Free'
                },
                {
                    'platform': 'YouTube',
                    'title': 'Sentdex - Python Programming',
                    'url': 'https://www.youtube.com/user/sentdex',
                    'description': 'Python for data science and machine learning',
                    'type': 'Video Tutorials',
                    'price': 'Free'
                }
            ]
        elif self.topic in ['javascript', 'js']:
            youtube_channels = [
                {
                    'platform': 'YouTube',
                    'title': 'JavaScript Mastery',
                    'url': 'https://www.youtube.com/c/JavaScriptMastery',
                    'description': 'Complete JavaScript and React tutorials',
                    'type': 'Video Course',
                    'price': 'Free'
                },
                {
                    'platform': 'YouTube',
                    'title': 'The Net Ninja - JavaScript',
                    'url': 'https://www.youtube.com/c/TheNetNinja',
                    'description': 'JavaScript tutorials and modern frameworks',
                    'type': 'Video Tutorials',
                    'price': 'Free'
                }
            ]
        elif self.topic in ['web', 'html', 'css']:
            youtube_channels = [
                {
                    'platform': 'YouTube',
                    'title': 'freeCodeCamp.org',
                    'url': 'https://www.youtube.com/c/Freecodecamp',
                    'description': 'Complete web development courses',
                    'type': 'Video Course',
                    'price': 'Free'
                },
                {
                    'platform': 'YouTube',
                    'title': 'Traversy Media',
                    'url': 'https://www.youtube.com/c/TraversyMedia',
                    'description': 'Web development tutorials and crash courses',
                    'type': 'Video Tutorials',
                    'price': 'Free'
                }
            ]
        else:
            # Generic programming/tech channels
            youtube_channels = [
                {
                    'platform': 'YouTube',
                    'title': 'freeCodeCamp.org',
                    'url': 'https://www.youtube.com/c/Freecodecamp',
                    'description': f'Complete {self.topic_display} courses and tutorials',
                    'type': 'Video Course',
                    'price': 'Free'
                }
            ]
        
        print(f"✅ Added {len(youtube_channels)} YouTube {self.topic_display} channels")
        return youtube_channels
    
    def scrape_all_courses(self):
        """Scrape courses for the specified topic from all available sources"""
        print(f"🎯 Starting comprehensive {self.topic_display} course collection...\n")
        
        # Collect from all sources
        all_sources = [
            self.scrape_freecodecamp(),
            self.scrape_w3schools(),
            self.scrape_mit_courses(),
            self.scrape_khan_academy(),
            self.scrape_codecademy_free(),
            self.get_youtube_channels()
        ]
        
        # Flatten the list
        for source_courses in all_sources:
            self.all_courses.extend(source_courses)
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_courses = []
        for course in self.all_courses:
            if course['title'] not in seen_titles:
                seen_titles.add(course['title'])
                unique_courses.append(course)
        
        self.all_courses = unique_courses
        
        print(f"\n🎉 TOTAL {self.topic_display.upper()} COURSES FOUND: {len(self.all_courses)}")
        return self.all_courses
    
    def display_courses_by_platform(self):
        """Display courses organized by platform"""
        platforms = {}
        
        for course in self.all_courses:
            platform = course['platform']
            if platform not in platforms:
                platforms[platform] = []
            platforms[platform].append(course)
        
        print("\n" + "="*80)
        print(f"🎯 COMPLETE {self.topic_display.upper()} LEARNING RESOURCES")
        print("="*80)
        
        for platform, courses in platforms.items():
            print(f"\n📚 {platform.upper()} ({len(courses)} courses)")
            print("-" * 50)
            
            for i, course in enumerate(courses, 1):
                print(f"{i:2d}. {course['title']}")
                print(f"     🔗 {course['url']}")
                print(f"     📝 {course['description']}")
                print(f"     💰 {course['price']} | 📖 {course['type']}")
                print()
    
    def save_to_json(self, filename=None):
        """Save courses to JSON file"""
        if filename is None:
            filename = f"{self.topic}_courses.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_courses, f, indent=2, ensure_ascii=False)
        print(f"💾 Courses saved to {filename}")

def main():
    # Get topic from command line arguments or use default
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = input("Enter the topic to search for (e.g., python, javascript, web development): ").strip()
        if not topic:
            topic = "python"  # Default fallback
    
    print(f"🔍 Searching for '{topic}' courses...\n")
    scraper = CourseScraper(topic)
    
    # Scrape all courses
    courses = scraper.scrape_all_courses()
    
    # Display results
    scraper.display_courses_by_platform()
    
    # Save to file
    scraper.save_to_json()
    
    print(f"\n✅ Found {len(courses)} total {topic.title()} learning resources!")
    print(f"📁 Results saved to '{topic}_courses.json'")
    
    # Summary by platform
    platforms = {}
    for course in courses:
        platform = course['platform']
        platforms[platform] = platforms.get(platform, 0) + 1
    
    print("\n📊 SUMMARY BY PLATFORM:")
    for platform, count in platforms.items():
        print(f"   {platform}: {count} courses")

if __name__ == "__main__":
    main()
