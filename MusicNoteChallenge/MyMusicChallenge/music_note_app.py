import streamlit as st
import streamlit.components.v1 as components
import random
import time

# Page config
st.set_page_config(page_title="Music Note Learning App", page_icon="🎹", layout="wide")

# Initialize session state
def init_session_state():
    defaults = {
        'game_state': 'menu',
        'current_level': 1,
        'question_number': 0,
        'correct_answers': 0,
        'current_note': None,
        'current_clef': None,
        'start_time': None,
        'question_start_time': None,
        'record_mode': False,
        'record_streak': 0,
        'best_streak': 0,
        'visual_position': 0,
        'last_answer': None,
        'previous_correct_answer': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Game configuration
LEVELS = {
    1: {
        'name': 'Beginner',
        'description': 'Natural notes only, 5 minutes total',
        'include_accidentals': False,
        'total_time_limit': 300,  # 5 minutes
        'individual_time_limit': None,
        'questions': 20
    },
    2: {
        'name': 'Intermediate',
        'description': 'Including sharps and flats, 4 minutes total',
        'include_accidentals': True,
        'total_time_limit': 240,  # 4 minutes
        'individual_time_limit': None,
        'questions': 20
    },
    3: {
        'name': 'Advanced',
        'description': 'All notes, 3 minutes total, 15 seconds per question',
        'include_accidentals': True,
        'total_time_limit': 180,  # 3 minutes
        'individual_time_limit': 15,
        'questions': 20
    },
    4: {
        'name': 'Expert',
        'description': 'All notes, 2 minutes total, 10 seconds per question',
        'include_accidentals': True,
        'total_time_limit': 120,  # 2 minutes
        'individual_time_limit': 10,
        'questions': 20
    }
}

# Note definitions with chromatic numbering (C=0, C#/Db=1, D=2, etc.)
CHROMATIC_NOTES = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
NATURAL_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
ACCIDENTAL_NOTES = ['C#/Db', 'D#/Eb', 'F#/Gb', 'G#/Ab', 'A#/Bb']

# Staff positions relative to middle C (C4 = 0)
# Each step is a half-line (line or space)
TREBLE_POSITIONS = {
    # Below staff
    'T-10': ('B3', -5),   # Well below staff
    'T-9': ('C4', -4.5),  # Middle C (ledger line below)
    'T-8': ('D4', -4),    # Below staff
    'T-7': ('E4', -3.5),  # Below staff
    'T-6': ('F4', -3),    # Below staff
    'T-5': ('G4', -2.5),  # Below staff
    'T-4': ('A4', -2),    # Below staff
    'T-3': ('B4', -1.5),  # Below staff
    'T-2': ('C5', -1),    # Below staff
    'T-1': ('D5', -0.5),  # Below staff
    # On staff
    'T0': ('E4', 0),      # Bottom line - E above middle C
    'T1': ('F4', 0.5),    # First space - F
    'T2': ('G4', 1),      # Second line - G
    'T3': ('A4', 1.5),    # Second space - A
    'T4': ('B4', 2),      # Third line - B
    'T5': ('C5', 2.5),    # Third space - C (treble C)
    'T6': ('D5', 3),      # Fourth line - D
    'T7': ('E5', 3.5),    # Fourth space - E
    'T8': ('F5', 4),      # Top line - F
    # Above staff
    'T9': ('G5', 4.5),    # Above staff
    'T10': ('A5', 5),     # Above staff (ledger line)
}

BASS_POSITIONS = {
    # Below staff
    'B-10': ('E2', -5),   # Well below staff
    'B-9': ('F2', -4.5),  # Below staff
    'B-8': ('G2', -4),    # Below staff
    'B-7': ('A2', -3.5),  # Below staff
    'B-6': ('B2', -3),    # Below staff
    'B-5': ('C3', -2.5),  # Below staff
    'B-4': ('D3', -2),    # Below staff
    'B-3': ('E3', -1.5),  # Below staff
    'B-2': ('F3', -1),    # Below staff
    'B-1': ('G3', -0.5),  # Below staff
    # On staff
    'B0': ('G2', 0),      # Bottom line
    'B1': ('A2', 0.5),    # First space
    'B2': ('B2', 1),      # Second line
    'B3': ('C3', 1.5),    # Second space (middle C)
    'B4': ('D3', 2),      # Third line (middle)
    'B5': ('E3', 2.5),    # Third space
    'B6': ('F3', 3),      # Fourth line
    'B7': ('G3', 3.5),    # Fourth space
    'B8': ('A3', 4),      # Top line
    # Above staff
    'B9': ('B3', 4.5),    # Above staff
    'B10': ('C4', 5),     # Above staff (middle C ledger line)
}

CLEFS = ['Treble', 'Bass']

def generate_question(level_config):
    """Generate a random note question based on level configuration"""
    clef = random.choice(CLEFS)
    
    # Choose from common positions on the staff
    if clef == 'Treble':
        positions = ['T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8']  # E4 to F5
    else:  # Bass
        positions = ['B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']  # G2 to A3
    
    position_key = random.choice(positions)
    note_name, visual_position = (TREBLE_POSITIONS if clef == 'Treble' else BASS_POSITIONS)[position_key]
    
    # Add accidentals if enabled
    if level_config['include_accidentals']:
        # Only add accidentals to notes that can have them (not E/F and B/C adjacent pairs)
        base_letter = note_name[0]
        if base_letter in ['C', 'D', 'F', 'G', 'A']:
            if random.choice([True, False, False]):  # 33% chance of accidental
                accidental = random.choice(['#', 'b'])
                note_name = note_name[0] + accidental
    
    return note_name, clef, visual_position

def get_simple_note_name(note_name):
    """Convert note name to simple format for answer matching"""
    if '#' in note_name:
        base_letter = note_name[0]
        if base_letter == 'E':  # E# = F
            return 'F'
        elif base_letter == 'B':  # B# = C
            return 'C'
        else:
            # Find the equivalent flat note
            next_letter = chr(ord(base_letter) + 1) if base_letter < 'G' else 'A'
            return base_letter + '#/' + next_letter + 'b'
    elif 'b' in note_name:
        base_letter = note_name[0]
        if base_letter == 'F':  # Fb = E
            return 'E'
        elif base_letter == 'C':  # Cb = B
            return 'B'
        else:
            # Find the equivalent sharp note
            prev_letter = chr(ord(base_letter) - 1) if base_letter > 'A' else 'G'
            return prev_letter + '#/' + base_letter + 'b'
    else:
        return note_name[0]

def get_note_options(level_config):
    """Get all possible note options for multiple choice"""
    if level_config['include_accidentals']:
        return NATURAL_NOTES + ACCIDENTAL_NOTES
    else:
        return NATURAL_NOTES

def create_staff_html(note_name, clef, visual_position):
    """Create HTML representation of musical staff with note"""
    
    # Clef symbols
    clef_symbol = "𝄞" if clef == 'Treble' else "𝄢"
    
    # Check for accidentals
    accidental = ""
    if '#' in note_name:
        accidental = "♯"
    elif 'b' in note_name:
        accidental = "♭"
    
    # Calculate Y position (staff lines are at y=70, 85, 100, 115, 130)
    # Bottom line (E4) = y=130, top line (F5) = y=70
    # Each position step = 15 units
    note_y = 130 - (visual_position * 15)
    
    # Determine stem direction based on position relative to middle line
    # Middle line is at position 2 (y=100)
    stem_up = visual_position <= 2
    
    if stem_up:
        # Stem goes up on the right side
        stem_x1 = 172  # Right side of note
        stem_x2 = 172
        stem_y1 = note_y
        stem_y2 = note_y - 35
    else:
        # Stem goes down on the left side
        stem_x1 = 148  # Left side of note
        stem_x2 = 148
        stem_y1 = note_y
        stem_y2 = note_y + 35
    
    html_content = f"""
    <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; margin: 10px 0;">
        <h3 style="color: #333; margin-bottom: 15px;">{clef} Clef</h3>
        <div style="position: relative; display: inline-block;">
            <svg width="300" height="200" viewBox="0 0 300 200">
                <!-- Staff lines (y=70, 85, 100, 115, 130) -->
                <line x1="50" y1="70" x2="250" y2="70" stroke="black" stroke-width="2"/>
                <line x1="50" y1="85" x2="250" y2="85" stroke="black" stroke-width="2"/>
                <line x1="50" y1="100" x2="250" y2="100" stroke="black" stroke-width="2"/>
                <line x1="50" y1="115" x2="250" y2="115" stroke="black" stroke-width="2"/>
                <line x1="50" y1="130" x2="250" y2="130" stroke="black" stroke-width="2"/>
                
                <!-- Ledger lines if needed -->
                {f'<line x1="140" y1="{note_y}" x2="180" y2="{note_y}" stroke="black" stroke-width="2"/>' if note_y < 70 or note_y > 130 else ''}
                
                <!-- Clef symbol -->
                <text x="60" y="110" font-family="serif" font-size="48" fill="black">{clef_symbol}</text>
                
                <!-- Accidental -->
                {f'<text x="130" y="{note_y + 5}" font-family="serif" font-size="24" fill="black">{accidental}</text>' if accidental else ''}
                
                <!-- Note head -->
                <ellipse cx="160" cy="{note_y}" rx="12" ry="8" fill="black"/>
                
                <!-- Note stem -->
                <line x1="{stem_x1}" y1="{stem_y1}" x2="{stem_x2}" y2="{stem_y2}" stroke="black" stroke-width="2"/>
            </svg>
        </div>
    </div>
    """
    
    return html_content

def check_time_limits():
    """Check if time limits have been exceeded"""
    if st.session_state.record_mode:
        return None
        
    current_time = time.time()
    level_config = LEVELS[st.session_state.current_level]
    
    # Check total time limit
    if st.session_state.start_time:
        elapsed_total = current_time - st.session_state.start_time
        if elapsed_total > level_config['total_time_limit']:
            return 'total_timeout'
    
    # Check individual question time limit
    if (level_config['individual_time_limit'] and 
        st.session_state.question_start_time):
        elapsed_question = current_time - st.session_state.question_start_time
        if elapsed_question > level_config['individual_time_limit']:
            return 'question_timeout'
    
    return None

def reset_game():
    """Reset game state"""
    st.session_state.question_number = 0
    st.session_state.correct_answers = 0
    st.session_state.current_note = None
    st.session_state.current_clef = None
    st.session_state.start_time = None
    st.session_state.question_start_time = None
    st.session_state.last_answer = None
    st.session_state.previous_correct_answer = None

def start_new_question():
    """Start a new question"""
    level_config = LEVELS[st.session_state.current_level] if not st.session_state.record_mode else {
        'include_accidentals': True
    }
    note, clef, visual_position = generate_question(level_config)
    st.session_state.current_note = note
    st.session_state.current_clef = clef
    st.session_state.visual_position = visual_position
    st.session_state.question_start_time = time.time()
    
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

# Main app layout
st.title("🎹 Music Note Learning App")

# Menu state
if st.session_state.game_state == 'menu':
    st.header("Choose Your Challenge")
    
    # Level selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Level Mode")
        for level_num, config in LEVELS.items():
            if st.button(f"Level {level_num}: {config['name']}", 
                        key=f"level_{level_num}"):
                st.session_state.current_level = level_num
                st.session_state.record_mode = False
                st.session_state.game_state = 'playing'
                reset_game()
                st.rerun()
            
            st.markdown(f"*{config['description']}*")
            st.markdown("---")
    
    with col2:
        st.subheader("🏆 Record Breaker Mode")
        st.markdown("Go for the longest streak of correct answers!")
        st.markdown("*All notes included, no time limits*")
        
        if st.button("Start Record Breaker Mode"):
            st.session_state.record_mode = True
            st.session_state.game_state = 'playing'
            st.session_state.record_streak = 0
            reset_game()
            st.rerun()
        
        if st.session_state.best_streak > 0:
            st.markdown(f"**Best Streak:** {st.session_state.best_streak} 🎯")

# Playing state
elif st.session_state.game_state == 'playing':
    # Check time limits
    timeout = check_time_limits()
    if timeout:
        st.session_state.game_state = 'finished'
        st.rerun()
    
    # Compact header with key info only
    if st.session_state.record_mode:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Streak", st.session_state.record_streak)
        with col2:
            st.metric("Best Streak", st.session_state.best_streak)
        with col3:
            if st.button("Back to Menu", key="back_menu_1"):
                st.session_state.game_state = 'menu'
                st.rerun()
    else:
        level_config = LEVELS[st.session_state.current_level]
        
        # First row - Level info
        st.markdown(f"**Level {st.session_state.current_level}: {level_config['name']}**")
        
        # Second row - Progress metrics in 3 columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Progress", f"{st.session_state.question_number + 1}/{level_config['questions']}")
        with col2:
            st.metric("Correct", st.session_state.correct_answers)
        with col3:
            # Time display
            if st.session_state.start_time:
                elapsed = time.time() - st.session_state.start_time
                remaining = level_config['total_time_limit'] - elapsed
                st.metric("Time", f"{max(0, int(remaining))}s")
    
    # Generate question if needed
    if st.session_state.current_note is None:
        start_new_question()
    
    # Display the staff notation (this is now much higher up)
    staff_html = create_staff_html(st.session_state.current_note, st.session_state.current_clef, st.session_state.visual_position)
    components.html(staff_html, height=280)
    
    # Show last answer result
    if st.session_state.last_answer is not None:
        if st.session_state.last_answer == 'correct':
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. The answer was **{st.session_state.previous_correct_answer}**")
    
    # Answer options with compact layout
    st.markdown("### What note is this?")
    
    if st.session_state.record_mode:
        options = NATURAL_NOTES + ACCIDENTAL_NOTES
    else:
        options = get_note_options(LEVELS[st.session_state.current_level])
    
    # Create compact button layout - 3 columns per row
    options_per_row = 3
    
    for row_start in range(0, len(options), options_per_row):
        cols = st.columns(options_per_row)
        row_options = options[row_start:row_start + options_per_row]
        
        for i, option in enumerate(row_options):
            with cols[i]:
                if st.button(option, key=f"answer_{option}_{st.session_state.question_number}", 
                            use_container_width=True):
                    # Check answer
                    correct_answer = get_simple_note_name(st.session_state.current_note)
                    
                    if option == correct_answer:
                        st.session_state.correct_answers += 1
                        st.session_state.last_answer = 'correct'
                        if st.session_state.record_mode:
                            st.session_state.record_streak += 1
                            if st.session_state.record_streak > st.session_state.best_streak:
                                st.session_state.best_streak = st.session_state.record_streak
                    else:
                        st.session_state.last_answer = 'incorrect'
                        # Store the correct answer for the current question before moving on
                        st.session_state.previous_correct_answer = correct_answer
                        if st.session_state.record_mode:
                            st.session_state.record_streak = 0
                    
                    # Move to next question or finish
                    if st.session_state.record_mode:
                        # In record mode, continue indefinitely
                        st.session_state.current_note = None
                        st.rerun()
                    else:
                        st.session_state.question_number += 1
                        level_config = LEVELS[st.session_state.current_level]
                        
                        if st.session_state.question_number >= level_config['questions']:
                            st.session_state.game_state = 'finished'
                            st.rerun()
                        else:
                            st.session_state.current_note = None
                            st.rerun()
    
    # Back to menu button (only show if not already shown above)
    if not st.session_state.record_mode:
        st.markdown("---")
        if st.button("Back to Menu", key="back_menu_2"):
            st.session_state.game_state = 'menu'
            st.rerun()

# Finished state
elif st.session_state.game_state == 'finished':
    st.header("🎊 Game Complete!")
    
    if st.session_state.record_mode:
        st.markdown(f"## Final Streak: {st.session_state.record_streak}")
        st.markdown(f"## Best Streak: {st.session_state.best_streak}")
    else:
        level_config = LEVELS[st.session_state.current_level]
        score_percentage = (st.session_state.correct_answers / level_config['questions']) * 100
        
        st.markdown(f"## Level {st.session_state.current_level}: {level_config['name']}")
        st.markdown(f"**Score:** {st.session_state.correct_answers}/{level_config['questions']} ({score_percentage:.1f}%)")
        
        # Performance feedback
        if score_percentage >= 90:
            st.success("Excellent! 🌟 You're ready for the next level!")
        elif score_percentage >= 70:
            st.info("Good job! 👍 Keep practicing!")
        else:
            st.warning("Keep practicing! 💪 You'll get there!")
    
    # Options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Play Again"):
            st.session_state.game_state = 'playing'
            reset_game()
            st.rerun()
    
    with col2:
        if st.button("Back to Menu"):
            st.session_state.game_state = 'menu'
            st.rerun()

# Footer
st.markdown("---")
st.markdown("*Happy practicing! 🎵*")