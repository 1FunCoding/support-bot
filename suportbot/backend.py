from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import markdown2  

client = OpenAI(api_key="", base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

app = Flask(__name__, static_folder='.', static_url_path='')

# Store conversation history by session_id
conversation_store = {}

# Personalized content for each major
major_content = {
    "Computer Science": {
        "concerns": [
            "Feeling overwhelmed by rapid tech changes.",
            "Fear of being replaced by AI.",
            "Frustration with mastering new frameworks or languages."
        ],
        "quotes": [
            "Technology, like art, is a soaring exercise of your imagination. Trust in your ability to create.",
            "Every bug you encounter is sharpening your skills for something bigger.",
            "Your code is a reflection of your creativity and resilience."
        ],
        "affirmations": [
            "Your value isn't defined by the frameworks you know today but by your relentless ability to adapt and grow.",
            "You're becoming more adaptable and resourceful with every coding challenge you face.",
            "Your willingness to learn is your greatest strength, carrying you through any technology shift."
        ],
        "wellness": [
            "Coding Breaks: After tackling challenging code, step away for 5 minutes to reset your brain.",
            "Debugging Self-Talk: When stuck, remind yourself: 'I'm capable of solving this—it just takes time.'",
            "Healthy Setup Ritual: Start each coding session by checking your posture and environment—small adjustments prevent burnout."
        ]
    },
    "Psychology": {
        "concerns": [
            "Exam stress, anxiety about research participation, and managing heavy reading loads."
        ],
        "quotes": [
            "Your curiosity is the first step toward wisdom—embrace the journey.",
            "Growth begins when you accept yourself exactly as you are.",
            "The answers you seek are often found within—trust yourself."
        ],
        "affirmations": [
            "Your insights into human nature make you uniquely equipped to navigate and support your own mental well-being.",
            "Every challenge you face deepens your empathy and understanding, helping you support others and yourself.",
            "Remember, you're cultivating skills not just academically, but personally, which will serve you throughout life."
        ],
        "wellness": [
            "Mindful Journaling: Spend 5 minutes each day reflecting on your emotional reactions to class materials, easing anxiety and enhancing understanding.",
            "Peer Connection: Regularly share your insights and questions with classmates to reinforce concepts and build a supportive network.",
            "Self-Reflection Breaks: Pause between readings to connect concepts to your own experiences, deepening comprehension and self-awareness."
        ]
    },
    "Communications": {
        "concerns": [
            "Anxiety during presentations, navigating conflicts in group projects, and finding a clear media focus."
        ],
        "quotes": [
            "Your voice has the power to lead, inspire, and transform.",
            "Speaking thoughtfully creates connections; silence wisely chosen also speaks volumes.",
            "True communication is hearing beyond words—trust your intuition."
        ],
        "affirmations": [
            "Your ability to clearly communicate ideas is improving every day, building your confidence in any setting.",
            "Team dynamics become easier as you gain experience—trust your capacity to manage challenges effectively.",
            "Every presentation you deliver or media project you undertake is a valuable opportunity to refine your unique voice."
        ],
        "wellness": [
            "Speech Practice: Record your presentations privately to build confidence and comfort with your communication style.",
            "Calming Rituals: Develop a short routine—such as deep breathing—before presentations to manage anxiety.",
            "Conflict Resolution Prep: Write down a few empathetic phrases to help navigate team conflicts smoothly."
        ]
    },
    "Finance": {
        "concerns": [
            "Stress from market volatility, challenging quantitative coursework, and competitive internships."
        ],
        "quotes": [
            "Your knowledge is the safest and most rewarding investment you'll ever make.",
            "Focus your energy on creating your future rather than worrying about uncertainties.",
            "Every market challenge you face strengthens your ability to succeed in future opportunities."
        ],
        "affirmations": [
            "Your analytical skills are invaluable, especially in uncertain financial times.",
            "Each complex financial concept mastered today contributes directly to your professional growth tomorrow.",
            "You are building resilience and discipline that extend beyond coursework and into your personal life."
        ],
        "wellness": [
            "Market Boundaries: Check financial news only during set daily intervals to minimize stress and maximize focus.",
            "Mindful Study Sessions: Break complex quantitative problems into manageable segments, allowing regular mental rest periods.",
            "Career Check-ins: Regularly remind yourself why you chose finance—focusing on your passion and future goals helps keep burnout at bay."
        ]
    },
    "Economics": {
        "concerns": [
            "Abstract model complexity, heavy theory readings, competitive job and internship markets."
        ],
        "quotes": [
            "Seeing the bigger picture helps you navigate complexities clearly and confidently.",
            "Every economic concept you master today sharpens your vision of tomorrow.",
            "Real-world applications will bridge the gap between theory and practice—trust your process."
        ],
        "affirmations": [
            "Your skill at connecting abstract theories to real-world issues grows daily—value this strength.",
            "Every challenging concept you grasp today becomes a tool for solving tomorrow's problems.",
            "Competition refines your strengths; trust your growing expertise and analytical mindset."
        ],
        "wellness": [
            "Theory to Life: Regularly link economic models to current events or personal experiences for better retention and motivation.",
            "Structured Reading: Tackle dense materials by summarizing key ideas every 20 minutes, making readings more manageable and less overwhelming.",
            "Community Learning: Engage in discussions with classmates about real-world economic scenarios to ground your learning practically."
        ]
    },
    "Business": {
        "concerns": [
            "Competitive job markets, developing leadership skills, balancing theory with real-world applications."
        ],
        "quotes": [
            "Your business acumen is built daily through practical insights and experiences.",
            "The best investment you can make is in your own skill set.",
            "Every challenge in business is an opportunity to innovate and lead."
        ],
        "affirmations": [
            "Your ability to adapt and learn is key to thriving in the dynamic world of business.",
            "Each step you take in your business journey is a foundation for future success.",
            "You have the resourcefulness to turn obstacles into opportunities."
        ],
        "wellness": [
            "Professional Networking: Regularly reach out to peers and mentors to gain fresh perspectives and reduce stress.",
            "Mini Case Studies: Break down real-world business scenarios to apply classroom knowledge and keep learning engaging.",
            "Vision Board: Keep a personal vision board of your long-term goals to stay motivated and resilient."
        ]
    },
    "Mechanical Engineering": {
        "concerns": [
            "Pressure from rigorous coursework, complex projects, and balancing theory with practical applications."
        ],
        "quotes": [
            "Engineering challenges are opportunities in disguise—each one builds your problem-solving prowess.",
            "Your persistence in the face of complexity lays the groundwork for future innovations.",
            "Every design and prototype you develop is a step toward mastering your craft."
        ],
        "affirmations": [
            "Your ability to tackle tough problems is a testament to your ingenuity and dedication.",
            "Every project you complete builds your skills and opens new avenues for success.",
            "You are engineering a future full of possibility with every challenge you overcome."
        ],
        "wellness": [
            "Project Breaks: Take regular breaks during long work sessions to keep your mind fresh.",
            "Peer Collaboration: Engage with classmates to exchange ideas and support each other's progress.",
            "Mindful Planning: Organize your tasks into manageable steps to prevent overwhelm."
        ]
    },
    "Electrical Engineering": {
        "concerns": [
            "Pressure from rigorous coursework, complex projects, and balancing theory with practical applications."
        ],
        "quotes": [
            "Engineering challenges are opportunities in disguise—each one builds your problem-solving prowess.",
            "Your persistence in the face of complexity lays the groundwork for future innovations.",
            "Every design and prototype you develop is a step toward mastering your craft."
        ],
        "affirmations": [
            "Your ability to tackle tough problems is a testament to your ingenuity and dedication.",
            "Every project you complete builds your skills and opens new avenues for success.",
            "You are engineering a future full of possibility with every challenge you overcome."
        ],
        "wellness": [
            "Project Breaks: Take regular breaks during long work sessions to keep your mind fresh.",
            "Peer Collaboration: Engage with classmates to exchange ideas and support each other's progress.",
            "Mindful Planning: Organize your tasks into manageable steps to prevent overwhelm."
        ]
    },
    "Biology": {
        "concerns": [
            "Lab work pressure, extensive terminology memorization, balancing lectures and experiments."
        ],
        "quotes": [
            "Every new term you learn is a step closer to understanding the wonders of life.",
            "Your lab experiences now can lead to discoveries that benefit the world tomorrow.",
            "Trust the journey: each experiment deepens your connection with the living world."
        ],
        "affirmations": [
            "You’re building the foundational knowledge to make impactful discoveries in health and environmental science.",
            "Your dedication to detailed learning today is laying the foundation for future success.",
            "Balancing your studies and experiments is teaching you valuable organizational and prioritization skills."
        ],
        "wellness": [
            "Memorization Games: Turn terminology review into fun, quick quizzes to reduce overwhelm.",
            "Reflection Moments: Briefly reflect on how daily learning relates to your broader interests in biology, keeping you motivated.",
            "Community Lab Work: Collaborate regularly with peers to share tips and reduce the stress of challenging lab tasks."
        ]
    },
    "Chemistry": {
        "concerns": [
            "Complex reactions, lab safety, theory versus practical work."
        ],
        "quotes": [
            "Every reaction you master deepens your understanding of the building blocks of our universe.",
            "Mistakes in the lab today lead to breakthroughs tomorrow—embrace the learning process.",
            "Chemistry is a puzzle; every reaction you understand connects another piece."
        ],
        "affirmations": [
            "Your persistence through challenging reactions is building your resilience and analytical strength.",
            "Safety and care in the lab reflect your respect for your craft and yourself—be proud of this responsibility.",
            "Balancing theory and practical applications demonstrates your versatility and adaptability—key professional strengths."
        ],
        "wellness": [
            "Safety Check-ins: Pause before each lab session to mentally review safety protocols—reinforcing confidence and reducing anxiety.",
            "Equation Breaks: After each complex problem set, take a short break to refresh your mind.",
            "Peer Collaboration: Regularly discuss challenging topics with classmates, deepening understanding and fostering camaraderie."
        ]
    },
    "Environmental Science": {
        "concerns": [
            "Balancing fieldwork with academic studies, heavy reading on environmental policies, concern about climate change and ecological crises."
        ],
        "quotes": [
            "The environment is where we all meet; it's the one thing we all share.",
            "A small change can make a significant impact—every effort counts.",
            "By studying our planet, you become part of the solution."
        ],
        "affirmations": [
            "Your commitment to understanding and preserving the environment is both noble and urgent.",
            "Each piece of research or fieldwork you undertake is a step toward a healthier planet.",
            "You have the power to inspire others through your passion for sustainable solutions."
        ],
        "wellness": [
            "Nature Breaks: Spend a few minutes outdoors daily, reconnecting with the environment you strive to protect.",
            "Policy Discussions: Engage with peers or online forums to broaden your perspective on environmental legislation and global efforts.",
            "Eco-Journaling: Keep track of your daily habits and reflect on how you can reduce your carbon footprint—small steps matter."
        ]
    },
    "Fine Arts & Humanities": {
        "concerns": [
            "Creative block, lack of recognition or funding, balancing creativity with theory."
        ],
        "quotes": [
            "Your creativity brings meaning and color into everyday life—never underestimate your impact.",
            "Every creative block is temporary. Trust the ebb and flow of inspiration.",
            "Your work resonates because it reflects genuine thought and emotion."
        ],
        "affirmations": [
            "Your unique perspective enriches the world; recognition follows authenticity.",
            "Balancing creativity and critical thinking makes your work deeper and more influential.",
            "Every moment of uncertainty is part of the artistic process—trust your journey."
        ],
        "wellness": [
            "Creative Freewriting: Set aside 10 minutes daily to write freely, overcoming blocks and tapping into your inner creativity.",
            "Community Connection: Regularly share your work with trusted peers for constructive feedback and motivation.",
            "Inspiration Breaks: Take short, intentional breaks to absorb inspiration from nature, art, or daily life."
        ]
    }
}

# Year context dictionary
year_context = {
    "freshman": {
        "context": "As you begin your college journey",
        "challenges": "adjusting to college life, finding your academic rhythm, and building new social connections",
        "opportunities": "exploring different courses, joining student organizations, and establishing good study habits"
    },
    "sophomore": {
        "context": "Now that you're settling into college life",
        "challenges": "choosing or confirming your major, balancing increased coursework difficulty, and maintaining motivation",
        "opportunities": "deepening your academic interests, taking on leadership roles, and exploring internship possibilities"
    },
    "junior": {
        "context": "At this critical point in your academic journey",
        "challenges": "handling advanced coursework, preparing for internships or research, and planning for your senior year",
        "opportunities": "specializing in your field, building professional connections, and developing career-relevant skills"
    },
    "senior": {
        "context": "As you approach graduation",
        "challenges": "managing job search anxiety, completing capstone projects, and preparing for the transition to professional life",
        "opportunities": "leveraging your college experience, finalizing your professional portfolio, and networking with alumni"
    }
}

# Default content if a major is not found
defaultContent = {
    "quotes": [
        {"text": "Success is not final, failure is not fatal: It is the courage to continue that counts.", "author": "Winston Churchill"},
        {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
        {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"}
    ],
    "affirmations": [
        "Your persistence through challenges is building your resilience and character.",
        "Your unique perspective and abilities contribute value to your field of study.",
        "You are capable of adapting to new challenges and finding solutions."
    ],
    "wellness": [
        {"title": "Stress Management", "content": "Practice deep breathing exercises for 5 minutes when feeling overwhelmed. Inhale for 4 counts, hold for 2, exhale for 6."},
        {"title": "Time Management", "content": "Use the Eisenhower Matrix to categorize tasks by urgency and importance, focusing first on important but not urgent work."},
        {"title": "Self-Compassion", "content": "Speak to yourself as you would to a friend when facing setbacks. Acknowledge difficulties without harsh self-judgment."}
    ]
}

@app.route('/')
def serve_index():
    # Serve index.html from the current directory.
    return send_from_directory('.', 'index.html')

@app.route('/api/get_support', methods=['POST'])
def get_support():
    data = request.get_json()
    major = data.get("major", "")
    year = data.get("year", "")
    prompt = data.get("prompt", "")
    session_id = data.get("session_id", "default")
    
    # Initialize or retrieve conversation history
    if session_id not in conversation_store:
        conversation_store[session_id] = []
    conversation = conversation_store[session_id]
    
    # Compose the base system message
    system_message = (
        "You are a helpful assistant specializing in academic burnout and stress management. "
        "Format your responses with Markdown."
        "Provide short answers that include great advice tailored to the user's major and academic year. "
        "If user input is overly detailed or off-topic, answer briefly while still relating it back to academic burnout and stress management."
    )
    
    # For new conversation, include personalized content from the selected major and year context
    if not conversation:
        content = major_content.get(major, defaultContent)
        year_info = year_context.get(year, {"context": "", "challenges": "", "opportunities": ""})
        
        personalized_info = ""
        if "concerns" in content:
            personalized_info += "Concerns: " + ", ".join(content["concerns"]) + ". "
        if "quotes" in content:
            quotes_text = ", ".join([quote["text"] for quote in content["quotes"]])
            personalized_info += "Quotes: " + quotes_text + ". "
        if "affirmations" in content:
            personalized_info += "Affirmations: " + ", ".join(content["affirmations"]) + ". "
        if "wellness" in content:
            wellness_titles = ", ".join([tip["title"] for tip in content["wellness"]])
            personalized_info += "Wellness Tips: " + wellness_titles + ". "
        
        year_message = f"Year Context: {year_info.get('context', '')}. Challenges: {year_info.get('challenges', '')}. Opportunities: {year_info.get('opportunities', '')}."
        
        user_message = f"Major: {major}, Year: {year}. {personalized_info} {year_message} " + (prompt if prompt else "Provide general advice on managing academic burnout.")
        
        conversation.append({"role": "system", "content": system_message})
        conversation.append({"role": "user", "content": user_message})
    else:
        # Continuation of conversation
        conversation.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model="gemini-2.0-flash-thinking-exp-01-21",
            messages=conversation,
            stream=False
        )
        answer = response.choices[0].message.content
        
        # Store the assistant's response in conversation history
        conversation.append({"role": "assistant", "content": answer})
        
        # Convert Markdown to HTML
        html_answer = markdown2.markdown(answer)
        
    except Exception as e:
        html_answer = f"Error: {str(e)}"
    
    return jsonify({"response": html_answer, "session_id": session_id})

if __name__ == '__main__':
    app.run(debug=True)
